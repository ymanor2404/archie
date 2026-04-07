# Archie — UX Research Insights Assistant

**Archie** is a Cursor skill that lets you "talk to the data" in our research repository. Ask questions like *"What do we know about AI engineers from our UX research reports?"* and Archie uses the **Google Workspace MCP** to search and read reports from Google Drive (Slides, Docs, PDFs) in Archie's Context Folder and answer from that content. Archie retrieves and relays data directly from UX research reports — it does not synthesize, interpret, or editorialize.

## What you need

- **Cursor** with this project open (or the skill available in your workspace).
- **Google Workspace MCP** configured in this project with **your own** Google OAuth credentials and email (credentials are per user, not stored in the repo).

## Quick start

1. **Clone this repo** (or pull the latest).
2. **Set up the Google Workspace MCP** — credentials are scoped to you:
   - See [**.cursor/README.md**](.cursor/README.md) for step-by-step setup.
   - Copy `.cursor/mcp.json.example` to `.cursor/mcp.json` and add your Client ID, Client Secret, and Google email.
   - Restart Cursor so it loads the MCP.
3. **Use Archie** in Cursor chat: ask a question about our UX research (personas, themes, studies, etc.). Archie will search the Context Folder, read relevant reports, and answer with citations and a tracing log.

## What's in this repo

| Path | Purpose |
|------|--------|
| `.cursor/skills/archie/` | Archie skill: `SKILL.md` (when/how to use, tools), `INSTRUCTIONS.md` (behavior, tone, tracing, references). |
| `.cursor/mcp.json.example` | Example MCP config; copy to `mcp.json` and add your credentials. |
| `.cursor/README.md` | **First-time setup guide** — MCP config, OAuth, and enabling the skill. |
| `eval/` | **Eval:** 14 prompts and rubric to assess answer quality and retrieval. |
| `scripts/` | `sync_reports.py` — weekly report-sync script (see Automated report sync below). |
| `.github/workflows/` | GitHub Actions workflow for the automated report sync. |

The file `.cursor/mcp.json` is gitignored so your credentials are never committed.

## Automated report sync (GitHub Actions) [WORK IN PROGRESS]

A weekly GitHub Actions pipeline scans the [UXD Research Engagements spreadsheet](https://docs.google.com/spreadsheets/d/1gdiYnzLB6knn_JS6RFbAgdwJa5r6NL0tH9IhJwcMqPQ/edit?gid=603259644#gid=603259644) for new report links in column F (starting at row 7) and copies each new document into Archie's Google Drive context folder.

### How it works

- Runs **every Monday at 9:00 AM UTC** (also triggerable manually from the Actions tab).
- Reads column F for Google Docs/Slides/Drive links; skips text-only cells.
- Compares against existing files in the context folder (by name and tracked source ID) so already-copied reports are never duplicated.
- Strips any "Copy of" prefix from the copy's name.
- Exits with a non-zero code on any copy failure, which triggers a GitHub Actions email notification.

### Setup — one-time steps

1. **Create a Google Cloud service account** in a project with the **Google Sheets API** and **Google Drive API** enabled.
2. **Share** the engagements spreadsheet with the service account email (Viewer role).
3. **Share** Archie's context folder (`1yW2GbqKThAskAAKA1UodTWqMzWZbVBo1`) with the service account email (Editor role).
4. **Share** any source report files (or their parent folder/shared drive) with the service account email (Viewer role) so the pipeline can read and copy them.
5. In the GitHub repo, go to **Settings → Secrets and variables → Actions** and create a repository secret named **`GOOGLE_SERVICE_ACCOUNT_KEY`** containing the full JSON key file for the service account.
6. In your GitHub **notification settings**, ensure "Actions" email notifications are enabled so you receive an email if the pipeline fails.

### Local testing

```bash
export GOOGLE_SERVICE_ACCOUNT_KEY='<paste JSON key contents>'
pip install -r scripts/requirements.txt
python scripts/sync_reports.py            # real run
python scripts/sync_reports.py --dry-run  # preview without copying
```

## Feedback and guidelines

- **Feedback on Archie:** [Share your feedback](https://forms.gle/renMTKS3KQnmN94a7)
- **Archie guidelines / best practices:** [Guidelines doc](https://docs.google.com/document/d/1wPq_kw4BWvWxqLTKVTbip9evvUo5cwCqBl_Bh-TRywQ/edit?tab=t.kjgor4yq1ct7)

## License

See [LICENSE](LICENSE) if present; otherwise use according to your organization's policy.
