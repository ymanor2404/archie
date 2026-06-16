# Archie — UX Research Insights Assistant

**Archie** is a Cursor skill that lets you "talk to the data" in our research repository. Ask questions like *"What do we know about AI engineers from our UX research reports?"* and Archie uses the **Google Workspace MCP** to search and read reports from Google Drive (Slides, Docs, PDFs) in Archie's Context Folder and answer from that content. Archie retrieves and relays data directly from UX research reports — it does not synthesize, interpret, or editorialize.

## What you need

- **Cursor** with this project open (or the skill available in your workspace).
- **Google Workspace MCP** configured in this project with **your own** Google OAuth credentials and email (credentials are per user, not stored in the repo).
- **Dataverse MCP (optional):** For live UX research team roster data (reporting lines, emails, titles). Without it, Archie falls back to a static markdown roster that may be less current. See [`.cursor/skills/archie/DATAVERSE_UXR.md`](.cursor/skills/archie/DATAVERSE_UXR.md).
- **Python** (uv / uvx) — the MCP server is installed via `uvx`. If you don't have `uv`, install it: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Recommended model:** the **latest Claude Sonnet** available in Cursor, in **Agent** mode (see [Recommended model](#recommended-model) below).

## Recommended model

**Use the latest Claude Sonnet** in Cursor’s model picker when running Archie (e.g. Sonnet 4 / 4.5 / 4.6 — whichever is current in your build). Run queries in **Agent** mode so Google Workspace MCP tools can run.

Archie is a retrieval workflow, not open-ended synthesis. Sonnet is the recommended default because it balances:

- **Reliable MCP tool use** — Archie chains Drive search, `get_drive_file_content` on 2–4 files, and `inspect_doc_structure` for multi-tab Google Docs. Sonnet handles multi-step agent work well without the latency and cost of the largest models on every question.
- **Instruction following** — The skill requires strict behavior: no synthesis across reports, source citation schema (product-area header + authors per study), recency-aware retrieval (prefer 12–18 month studies; legacy warnings for ≥24 month sources), a clickable link on every citation, study metadata (n, method, date), uniform formatting (tables or bullets, not mixed), a tracing log with reasoning, and a limitations disclaimer on every reply. Sonnet adheres to long, rigid prompts more consistently than smaller/faster models.
- **Faithful quoting** — Answers should pull verbatim quotes and say when the Context Folder has no evidence. Sonnet is a better fit than Haiku-class models, which are more prone to skipping tool steps or inventing citations.
- **Practical throughput** — Most Archie questions (personas, targeted findings, validation, quotes) are run often; Sonnet is fast enough for day-to-day use while still strong on agent tasks.

**When to use Claude Opus (latest):** broad discovery across many reports, or when Sonnet missed tabs, skipped MCP calls, or produced weak citations. Opus is optional for highest-stakes retrieval, not required for every query.

**Avoid for Archie:** Claude Haiku and non-agent chat modes without MCP — higher risk of hallucinated quotes and answers that do not search the repository.

## Quick start

1. **Clone this repo** (or pull the latest).

2. **Set up the Google Workspace MCP** — see [**.cursor/README.md**](.cursor/README.md) for full details.

   **If you already have Google Workspace MCP configured in Cursor** (e.g. in your user-level MCP settings), you can skip creating `.cursor/mcp.json` — just make sure Drive, Docs, and Slides tools are enabled and your Google email is set. See the [setup guide](.cursor/README.md#already-have-google-workspace-mcp-configured) for what to verify.

   **If you do not have Google Workspace MCP configured yet**, you will need Google OAuth credentials:
   - Copy `.cursor/mcp.json.example` to `.cursor/mcp.json` and fill in your Client ID, Client Secret, and Google email.
   - See the [setup guide](.cursor/README.md) for how to obtain OAuth credentials from the Google Cloud Console.
   - Restart Cursor so it loads the MCP.

3. **Use Archie** in Cursor chat: ask a question about our UX research (personas, themes, studies, etc.). Archie will search the Context Folder, read relevant reports, and answer with citations and a tracing log.

## What's in this repo

| Path | Purpose |
|------|--------|
| `.cursor/skills/archie/` | Archie skill: `SKILL.md` (when/how to use, tools), `INSTRUCTIONS.md` (behavior, tone, tracing, references), `DATAVERSE_UXR.md` (live team roster via Dataverse), `UXR_TEAM.md` (fallback static roster). |
| `.cursor/mcp.json.example` | Example MCP config; copy to `mcp.json` and add your credentials. |
| `.cursor/README.md` | **First-time setup guide** — MCP config, OAuth, and enabling the skill. |
| `eval/` | **Eval:** 14 prompts and rubric to assess answer quality and retrieval. |
| `scripts/` | `sync_reports.py` (weekly report sync), `index_retriever.py` (recency-weighted Drive index for ranking). |
| `.github/workflows/` | GitHub Actions workflow for the automated report sync. |

The file `.cursor/mcp.json` is gitignored so your credentials are never committed.

## Automated report sync (GitHub Actions) {Work in Progress}

A weekly GitHub Actions pipeline scans the [UXD Research Engagements spreadsheet](https://docs.google.com/spreadsheets/d/1gdiYnzLB6knn_JS6RFbAgdwJa5r6NL0tH9IhJwcMqPQ/edit?gid=603259644#gid=603259644) for new report links in column F (starting at row 7) and copies each new document into Archie's Google Drive context folder.

### How it works

- Runs **every Monday at 9:00 AM UTC** (also triggerable manually from the Actions tab).
- Reads column F for Google Docs/Slides/Drive links; skips text-only cells.
- Compares against existing files in the context folder (by name and tracked source ID) so already-copied reports are never duplicated.
- Strips any "Copy of" prefix from the copy's name.
- Exits with a non-zero code on any copy failure, which triggers a GitHub Actions email notification.

### Related scripts

| Script | Purpose |
|--------|---------|
| `sync_reports.py` | Copy new reports from the engagements spreadsheet into the Context Folder. |
| `index_retriever.py` | List and rank Context Folder files by **age-weighting** (priority: last 18 months; legacy: ≥24 months). Use `python scripts/index_retriever.py [keywords] --json` with `GOOGLE_SERVICE_ACCOUNT_KEY` set. Add `--query-hint` for a suggested `modifiedTime` Drive search clause. |

For day-to-day Archie queries in Cursor, MCP search applies the same recency rules in [INSTRUCTIONS.md](.cursor/skills/archie/INSTRUCTIONS.md); the index script is optional for local ranking or CI.

**Drive query syntax:** Folder-scoped search uses `'FOLDER_ID' in parents and fullText contains "keyword"` — use **double quotes** for the search term so apostrophes (e.g. `we're`, `user's`) do not break the query.


## Feedback and guidelines

- **Feedback on Archie:** [Share your feedback](https://forms.gle/zoHWJ1YcMNtkG1fX9)
- **Archie guidelines / best practices:** [Guidelines doc](https://docs.google.com/document/d/1lr5gX9UPxwYz03sXitWWGOMI6LVgk4qd-whFdEzjNYQ/edit?tab=t.0)

## License

See [LICENSE](LICENSE) if present; otherwise use according to your organization's policy.
