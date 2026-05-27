#!/usr/bin/env python3
"""
Build a recency-weighted index of UX research reports in Archie's Context Folder.

Lists Drive files, scores them with an age-weighting algorithm (prioritizing work
from the last 12–18 months), and ranks candidates for retrieval. Intended for
local/CI use alongside Archie; the agent also applies the same ranking rules when
using search_drive_files via MCP.

Authentication: GOOGLE_SERVICE_ACCOUNT_KEY (same as sync_reports.py).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone

from pathlib import Path

from googleapiclient.discovery import build

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from sync_reports import CONTEXT_FOLDER_ID, get_credentials  # noqa: E402

# Recency tiers (months since created/modified)
PRIORITY_MAX_MONTHS = 18  # highest age-weight band
LEGACY_MIN_MONTHS = 24  # legacy tier; Archie must warn when citing


def _parse_rfc3339(value: str) -> datetime:
    """Parse Drive API timestamp (RFC 3339)."""
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value).astimezone(timezone.utc)


def months_since(dt: datetime, now: datetime | None = None) -> float:
    now = now or datetime.now(timezone.utc)
    delta = now - dt
    return max(0.0, delta.days / 30.437)


def age_weight(months: float) -> float:
    """
    Age-weighting for retrieval ranking.

    - 0–18 months: priority band (1.0 → ~0.88), aligned with 12–18 month focus
    - 18–24 months: deprioritized but usable
    - >24 months: legacy (low weight; cite only when necessary)
    """
    if months <= PRIORITY_MAX_MONTHS:
        return 1.0 - (months / PRIORITY_MAX_MONTHS) * 0.12
    if months < LEGACY_MIN_MONTHS:
        return 0.65
    return 0.25


def is_legacy(months: float) -> bool:
    return months >= LEGACY_MIN_MONTHS


def title_relevance(title: str, keywords: list[str]) -> float:
    if not keywords:
        return 1.0
    title_l = title.lower()
    hits = sum(1 for k in keywords if k.lower() in title_l)
    if hits == 0:
        return 0.15
    return min(1.0, hits / len(keywords))


def combined_score(rel: float, age_w: float) -> float:
    return rel * 0.55 + age_w * 0.45


def list_folder_files(drive_svc, folder_id: str) -> list[dict]:
    files: list[dict] = []
    page_token = None
    fields = (
        "nextPageToken, files(id, name, mimeType, createdTime, modifiedTime, "
        "webViewLink)"
    )

    while True:
        resp = (
            drive_svc.files()
            .list(
                q=f"'{folder_id}' in parents and trashed = false",
                fields=fields,
                pageToken=page_token,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
                pageSize=500,
                orderBy="modifiedTime desc",
            )
            .execute()
        )
        files.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return files


def build_index_entry(file_meta: dict, keywords: list[str], now: datetime) -> dict:
    name = file_meta.get("name", "")
    created = file_meta.get("createdTime") or file_meta.get("modifiedTime")
    modified = file_meta.get("modifiedTime") or created
    created_dt = _parse_rfc3339(created) if created else now
    modified_dt = _parse_rfc3339(modified) if modified else created_dt

    # Prefer createdTime for study age; fall back to modifiedTime
    age_dt = created_dt
    age_mo = months_since(age_dt, now)
    age_w = age_weight(age_mo)
    rel = title_relevance(name, keywords)
    score = combined_score(rel, age_w)

    tier = "priority"
    if is_legacy(age_mo):
        tier = "legacy"
    elif age_mo > PRIORITY_MAX_MONTHS:
        tier = "aging"

    return {
        "file_id": file_meta["id"],
        "name": name,
        "mimeType": file_meta.get("mimeType"),
        "webViewLink": file_meta.get("webViewLink"),
        "createdTime": created,
        "modifiedTime": modified,
        "age_months": round(age_mo, 1),
        "age_weight": round(age_w, 3),
        "title_relevance": round(rel, 3),
        "score": round(score, 3),
        "tier": tier,
        "legacy": is_legacy(age_mo),
    }


def rank_files(
    files: list[dict],
    keywords: list[str],
    limit: int,
    include_legacy: bool,
) -> list[dict]:
    now = datetime.now(timezone.utc)
    entries = [build_index_entry(f, keywords, now) for f in files]
    if not include_legacy:
        entries = [e for e in entries if not e["legacy"]]
    entries.sort(key=lambda e: (-e["score"], -e["age_weight"], e["name"]))
    return entries[:limit]


def drive_recency_query_clause(months: int = PRIORITY_MAX_MONTHS) -> str:
    """Drive search fragment: files modified in the last *months*."""
    from datetime import timedelta

    cutoff = datetime.now(timezone.utc) - timedelta(days=int(months * 30.437))
    return f"modifiedTime >= '{cutoff.strftime('%Y-%m-%d')}'"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Recency-weighted index of Archie Context Folder reports."
    )
    parser.add_argument(
        "keywords",
        nargs="*",
        help="Optional keywords to boost title matches (e.g. openshift onboarding)",
    )
    parser.add_argument("--limit", type=int, default=25, help="Max results (default 25)")
    parser.add_argument(
        "--include-legacy",
        action="store_true",
        help="Include files older than 24 months (default: exclude from ranked list)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON (default: human-readable table)",
    )
    parser.add_argument(
        "--query-hint",
        action="store_true",
        help="Print a suggested search_drive_files recency clause and exit",
    )
    args = parser.parse_args()

    if args.query_hint:
        clause = drive_recency_query_clause()
        print(
            "Suggested MCP search_drive_files query fragment (append to folder scope):\n"
            f"  and {clause}"
        )
        return

    creds = get_credentials()
    drive_svc = build("drive", "v3", credentials=creds)
    files = list_folder_files(drive_svc, CONTEXT_FOLDER_ID)
    ranked = rank_files(files, args.keywords, args.limit, args.include_legacy)

    payload = {
        "folder_id": CONTEXT_FOLDER_ID,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "keywords": args.keywords,
        "priority_max_months": PRIORITY_MAX_MONTHS,
        "legacy_min_months": LEGACY_MIN_MONTHS,
        "count": len(ranked),
        "files": ranked,
    }

    if args.json:
        print(json.dumps(payload, indent=2))
        return

    print(
        f"Ranked {len(ranked)} file(s) in Context Folder "
        f"(priority ≤{PRIORITY_MAX_MONTHS}mo, legacy ≥{LEGACY_MIN_MONTHS}mo)\n"
    )
    for i, e in enumerate(ranked, 1):
        flag = " [LEGACY]" if e["legacy"] else ""
        print(
            f"{i:2}. score={e['score']:.2f} age={e['age_months']:.0f}mo "
            f"tier={e['tier']}{flag}\n    {e['name']}\n    {e['webViewLink'] or e['file_id']}"
        )


if __name__ == "__main__":
    main()
