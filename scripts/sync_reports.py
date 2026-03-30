#!/usr/bin/env python3
"""
Syncs new research reports from the UXD Research Engagements spreadsheet
to Archie's Google Drive context folder.

Reads column F (Report links/hyperlinks) starting from a configurable row,
identifies documents not yet in the context folder, copies them there,
and strips any "Copy of" prefix from the copy name.

Authentication: expects a GOOGLE_SERVICE_ACCOUNT_KEY env var containing
the JSON key for a Google Cloud service account with Sheets (readonly)
and Drive (read/write) scopes.
"""

import json
import os
import re
import sys

from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID = "1gdiYnzLB6knn_JS6RFbAgdwJa5r6NL0tH9IhJwcMqPQ"
SHEET_GID = 603259644
CONTEXT_FOLDER_ID = "1yW2GbqKThAskAAKA1UodTWqMzWZbVBo1"
START_ROW = 7

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive",
]


def get_credentials():
    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_KEY", "")
    if not raw:
        print(
            "ERROR: GOOGLE_SERVICE_ACCOUNT_KEY environment variable is not set.",
            file=sys.stderr,
        )
        sys.exit(1)
    return service_account.Credentials.from_service_account_info(
        json.loads(raw), scopes=SCOPES
    )


def extract_file_id(url: str) -> str | None:
    """Pull a Drive / Docs / Slides file ID out of a URL."""
    if not url:
        return None
    for pattern in (r"/d/([a-zA-Z0-9_-]+)", r"[?&]id=([a-zA-Z0-9_-]+)"):
        m = re.search(pattern, url)
        if m:
            return m.group(1)
    return None


def resolve_sheet_name(sheets_svc, spreadsheet_id: str, gid: int) -> str | None:
    meta = sheets_svc.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    for sheet in meta["sheets"]:
        if sheet["properties"]["sheetId"] == gid:
            return sheet["properties"]["title"]
    return None


def read_report_links(sheets_svc, spreadsheet_id: str, sheet_name: str, start_row: int):
    """
    Return a list of dicts with keys: row, title, url, file_id.

    Reads columns C–F starting at *start_row*.  Column C is the study
    title (index 0) and column F is the report link (index 3).  The
    Sheets API grid-data response gives us both the display text
    (formattedValue) and any embedded hyperlink.
    """
    range_str = f"'{sheet_name}'!C{start_row}:F"
    resp = (
        sheets_svc.spreadsheets()
        .get(
            spreadsheetId=spreadsheet_id,
            ranges=[range_str],
            fields="sheets.data.rowData.values(formattedValue,hyperlink)",
        )
        .execute()
    )

    rows = (
        resp.get("sheets", [{}])[0]
        .get("data", [{}])[0]
        .get("rowData", [])
    )

    reports = []
    for i, row in enumerate(rows):
        vals = row.get("values", [])
        title = vals[0].get("formattedValue", "") if vals else ""

        report_cell = vals[3] if len(vals) > 3 else {}
        display = report_cell.get("formattedValue", "")
        hyperlink = report_cell.get("hyperlink", "")

        url = hyperlink or (display if display.startswith("http") else "")
        if not url:
            continue

        file_id = extract_file_id(url)
        if file_id:
            reports.append(
                {"row": start_row + i, "title": title, "url": url, "file_id": file_id}
            )

    return reports


def list_context_folder(drive_svc, folder_id: str):
    """Return (name_set, source_id_set) for every file in the folder."""
    names: set[str] = set()
    source_ids: set[str] = set()
    page_token = None

    while True:
        resp = (
            drive_svc.files()
            .list(
                q=f"'{folder_id}' in parents and trashed = false",
                fields="nextPageToken, files(id, name, appProperties)",
                pageToken=page_token,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
                pageSize=500,
            )
            .execute()
        )
        for f in resp.get("files", []):
            names.add(f["name"])
            sid = (f.get("appProperties") or {}).get("source_file_id")
            if sid:
                source_ids.add(sid)
        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    return names, source_ids


def copy_to_context_folder(drive_svc, file_id: str, folder_id: str):
    """Copy *file_id* into *folder_id*, return (new_file_meta, original_name)."""
    original = (
        drive_svc.files()
        .get(fileId=file_id, fields="name", supportsAllDrives=True)
        .execute()
    )
    original_name = original["name"]
    clean_name = re.sub(r"^Copy of ", "", original_name)

    copied = (
        drive_svc.files()
        .copy(
            fileId=file_id,
            body={
                "name": clean_name,
                "parents": [folder_id],
                "appProperties": {"source_file_id": file_id},
            },
            supportsAllDrives=True,
            fields="id,name",
        )
        .execute()
    )

    # Safeguard: the API *shouldn't* prepend "Copy of" when we supply a name,
    # but strip it again if it does.
    if copied["name"].startswith("Copy of "):
        fixed = copied["name"][len("Copy of "):]
        drive_svc.files().update(
            fileId=copied["id"],
            body={"name": fixed},
            supportsAllDrives=True,
        ).execute()
        copied["name"] = fixed

    return copied, original_name


def main():
    dry_run = "--dry-run" in sys.argv

    creds = get_credentials()
    sheets_svc = build("sheets", "v4", credentials=creds)
    drive_svc = build("drive", "v3", credentials=creds)

    sheet_name = resolve_sheet_name(sheets_svc, SPREADSHEET_ID, SHEET_GID)
    if not sheet_name:
        print(f"ERROR: No sheet with GID {SHEET_GID}", file=sys.stderr)
        sys.exit(1)
    print(f"Sheet: '{sheet_name}'")

    reports = read_report_links(sheets_svc, SPREADSHEET_ID, sheet_name, START_ROW)
    print(f"Found {len(reports)} report link(s) in column F (row {START_ROW}+)\n")
    if not reports:
        print("Nothing to sync.")
        return

    existing_names, existing_source_ids = list_context_folder(drive_svc, CONTEXT_FOLDER_ID)
    print(f"Context folder has {len(existing_names)} file(s)\n")

    errors: list[str] = []
    copied = 0
    skipped = 0

    for rpt in reports:
        row, title, file_id = rpt["row"], rpt["title"], rpt["file_id"]

        if file_id in existing_source_ids:
            skipped += 1
            continue

        try:
            orig_meta = (
                drive_svc.files()
                .get(fileId=file_id, fields="name", supportsAllDrives=True)
                .execute()
            )
            clean_name = re.sub(r"^Copy of ", "", orig_meta["name"])

            if clean_name in existing_names:
                skipped += 1
                continue

            if dry_run:
                print(f"  [DRY RUN] Row {row} [{title}]: Would copy '{orig_meta['name']}' → '{clean_name}'")
                copied += 1
                continue

            new_file, original_name = copy_to_context_folder(
                drive_svc, file_id, CONTEXT_FOLDER_ID
            )
            print(f"  Row {row} [{title}]: Copied '{original_name}' → '{new_file['name']}'")
            existing_names.add(new_file["name"])
            existing_source_ids.add(file_id)
            copied += 1

        except Exception as exc:
            msg = f"Row {row} [{title}]: Failed to process {file_id} — {exc}"
            print(f"  ERROR: {msg}", file=sys.stderr)
            errors.append(msg)

    prefix = "[DRY RUN] " if dry_run else ""
    print(f"\n{prefix}Done — Copied: {copied}, Skipped: {skipped}, Errors: {len(errors)}")

    if errors:
        print("\nErrors:", file=sys.stderr)
        for e in errors:
            print(f"  • {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
