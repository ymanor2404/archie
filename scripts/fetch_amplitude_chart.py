#!/usr/bin/env python3
"""
Fetch data from an Amplitude dashboard chart via the Dashboard REST API.
Uses chart ID from the chart URL (e.g. .../chart/abc123).

Requires: AMPLITUDE_API_KEY and AMPLITUDE_SECRET_KEY in environment or .env.
Usage: python scripts/fetch_amplitude_chart.py CHART_ID [--eu]
"""

import argparse
import base64
import os
import sys

try:
    import requests
except ImportError:
    print("Install requests: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # optional

DEFAULT_BASE = "https://amplitude.com"
EU_BASE = "https://analytics.eu.amplitude.com"


def main():
    parser = argparse.ArgumentParser(description="Fetch Amplitude chart data by chart ID")
    parser.add_argument("chart_id", help="Chart ID from the chart URL (e.g. abc123)")
    parser.add_argument("--eu", action="store_true", help="Use EU residency server")
    parser.add_argument("--format", choices=["csv", "raw"], default="csv", help="Output format (default: csv)")
    args = parser.parse_args()

    api_key = os.environ.get("AMPLITUDE_API_KEY")
    secret_key = os.environ.get("AMPLITUDE_SECRET_KEY")

    if not api_key or not secret_key:
        print(
            "Set AMPLITUDE_API_KEY and AMPLITUDE_SECRET_KEY in the environment or .env file.",
            file=sys.stderr,
        )
        sys.exit(1)

    base = EU_BASE if args.eu else DEFAULT_BASE
    url = f"{base}/api/3/chart/{args.chart_id}/csv"

    credentials = f"{api_key}:{secret_key}"
    encoded = base64.b64encode(credentials.encode()).decode()
    headers = {"Authorization": f"Basic {encoded}"}

    try:
        resp = requests.get(url, headers=headers, timeout=60)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}", file=sys.stderr)
        if resp.status_code == 401:
            print("Check your API key and secret key.", file=sys.stderr)
        elif resp.status_code == 404:
            print("Chart ID not found or no access. Check the chart URL.", file=sys.stderr)
        elif resp.status_code == 429:
            print("Rate limited. Wait and retry.", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)

    body = resp.text
    if args.format == "raw":
        print("Content-Type:", resp.headers.get("Content-Type", ""), file=sys.stderr)
    print(body)


if __name__ == "__main__":
    main()
