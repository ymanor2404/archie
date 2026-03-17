#!/usr/bin/env python3
"""
Fetch data for multiple Amplitude charts and save each to a CSV file.
Uses chart IDs from CHARTS_FILE (default: chart_ids.txt) or from arguments.
Respects rate limits with a delay between requests.

Requires: AMPLITUDE_API_KEY and AMPLITUDE_SECRET_KEY in environment or .env.
Usage:
  python scripts/fetch_all_charts.py
  python scripts/fetch_all_charts.py pg2jebgb l3iy6kj6 gw3zp5d0
  python scripts/fetch_all_charts.py --from-file chart_ids.txt --out-dir data
"""

import argparse
import base64
import os
import sys
import time

try:
    import requests
except ImportError:
    print("Install requests: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DEFAULT_BASE = "https://amplitude.com"
EU_BASE = "https://analytics.eu.amplitude.com"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CHARTS_FILE = os.path.join(SCRIPT_DIR, "chart_ids.txt")
DEFAULT_OUT_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "data")
DELAY_SECONDS = 2  # between requests to avoid rate limits


def load_chart_ids(path):
    """Load chart IDs from a file (one per line, skip empty and # comments)."""
    ids = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # in case line is "chart_id  # comment" or "chart_id,label"
            ids.append(line.split()[0].split(",")[0])
    return ids


def fetch_chart(base_url, chart_id, headers):
    """Fetch one chart CSV; return (success, content or error message)."""
    url = f"{base_url}/api/3/chart/{chart_id}/csv"
    try:
        resp = requests.get(url, headers=headers, timeout=90)
        resp.raise_for_status()
        return True, resp.text
    except requests.exceptions.HTTPError as e:
        return False, f"HTTP {resp.status_code}: {e}"
    except requests.exceptions.RequestException as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description="Fetch multiple Amplitude charts to CSV files")
    parser.add_argument(
        "chart_ids",
        nargs="*",
        help="Chart IDs to fetch (if omitted, use --from-file)",
    )
    parser.add_argument(
        "--from-file",
        default=DEFAULT_CHARTS_FILE,
        help=f"File with chart IDs, one per line (default: {DEFAULT_CHARTS_FILE})",
    )
    parser.add_argument(
        "--out-dir",
        default=DEFAULT_OUT_DIR,
        help=f"Directory to write CSV files (default: {DEFAULT_OUT_DIR})",
    )
    parser.add_argument("--eu", action="store_true", help="Use EU residency server")
    parser.add_argument("--delay", type=float, default=DELAY_SECONDS, help="Seconds between requests")
    args = parser.parse_args()

    if args.chart_ids:
        chart_ids = args.chart_ids
    else:
        if not os.path.isfile(args.from_file):
            print(f"Chart IDs file not found: {args.from_file}", file=sys.stderr)
            print("Create it with one chart ID per line, or pass chart IDs as arguments.", file=sys.stderr)
            sys.exit(1)
        chart_ids = load_chart_ids(args.from_file)

    api_key = os.environ.get("AMPLITUDE_API_KEY")
    secret_key = os.environ.get("AMPLITUDE_SECRET_KEY")
    if not api_key or not secret_key:
        print("Set AMPLITUDE_API_KEY and AMPLITUDE_SECRET_KEY (env or .env).", file=sys.stderr)
        sys.exit(1)

    base = EU_BASE if args.eu else DEFAULT_BASE
    credentials = f"{api_key}:{secret_key}"
    encoded = base64.b64encode(credentials.encode()).decode()
    headers = {"Authorization": f"Basic {encoded}"}

    os.makedirs(args.out_dir, exist_ok=True)
    ok = 0
    failed = []

    for i, chart_id in enumerate(chart_ids):
        if i > 0:
            time.sleep(args.delay)
        success, content = fetch_chart(base, chart_id, headers)
        out_path = os.path.join(args.out_dir, f"chart_{chart_id}.csv")
        if success:
            with open(out_path, "w") as f:
                f.write(content)
            ok += 1
            print(f"OK   {chart_id} -> {out_path}")
        else:
            failed.append((chart_id, content))
            print(f"FAIL {chart_id}: {content}", file=sys.stderr)

    print(f"\nDone: {ok} saved, {len(failed)} failed.")
    if failed:
        for cid, msg in failed:
            print(f"  - {cid}: {msg}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
