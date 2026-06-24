# Archie — UX Research Insights Assistant

**Archie** is a Cursor skill that lets you "talk to the data" in our research repository. Ask questions like *"What do we know about AI engineers from our UX research reports?"* and Archie uses the **Google Workspace CLI (`gws`)** to read the [User Research and User Engagements spreadsheet](https://docs.google.com/spreadsheets/d/1gdiYnzLB6knn_JS6RFbAgdwJa5r6NL0tH9IhJwcMqPQ/edit?gid=603259644#gid=603259644) as the catalog of eligible reports, fetch linked artifacts (Slides, Docs, PDFs), and answer from that content. Archie retrieves and relays data directly from UX research reports — it does not synthesize, interpret, or editorialize.

> **Upgrading from v1?** If you previously used Archie with the Google Workspace MCP and Drive Context Folder, see [UPGRADE.md](UPGRADE.md).

## What you need

- **Cursor** with this project open (or the skill available in your workspace).
- **Google Workspace CLI (`gws`)** installed and authenticated on your machine (IT-approved OAuth; **Sheets API enabled**). See [`.cursor/README.md`](.cursor/README.md).
- **Spreadsheet access** to the [User Research and User Engagements spreadsheet](https://docs.google.com/spreadsheets/d/1gdiYnzLB6knn_JS6RFbAgdwJa5r6NL0tH9IhJwcMqPQ/edit?gid=603259644#gid=603259644). (This is currently set to full edit access by anyone at Red Hat).
- **Dataverse MCP (optional):** For live UX research team roster data (reporting lines, emails, titles). Without it, Archie falls back to a static markdown roster that may be less current. See [`.cursor/skills/archie/DATAVERSE_UXR.md`](.cursor/skills/archie/DATAVERSE_UXR.md).
- **Recommended model:** the **latest Claude Sonnet** available in Cursor, in **Agent** mode (see [Recommended model](#recommended-model) below).

## Recommended model

**Use the latest Claude Sonnet** in Cursor's model picker when running Archie (e.g. Sonnet 4 / 4.5 / 4.6 — whichever is current in your build). Run queries in **Agent** mode so the agent can execute `gws` shell commands.

Archie is a retrieval workflow, not open-ended synthesis. Sonnet is the recommended default because it balances:

- **Reliable multi-step shell use** — Archie reads the spreadsheet catalog, resolves file IDs, fetches content on 2–4 reports, and checks Google Docs for extra tabs via `includeTabsContent`. Sonnet handles multi-step agent work well without the latency and cost of the largest models on every question.
- **Instruction following** — The skill requires strict behavior: no synthesis across reports, source citation schema (product-area header + authors per study), recency-aware retrieval (prefer 12–18 month studies; legacy warnings for ≥24 month sources), a clickable link on every citation, study metadata (n, method, date), uniform formatting (tables or bullets, not mixed), a tracing log with reasoning, and a limitations disclaimer on every reply. Sonnet adheres to long, rigid prompts more consistently than smaller/faster models.
- **Practical throughput** — Most Archie questions (personas, targeted findings, validation, quotes) are run often; Sonnet is fast enough for day-to-day use while still strong on agent tasks.

**When to use Claude Opus (latest):** broad discovery across many reports, or when Sonnet missed tabs, skipped `gws` calls, or produced weak citations. Opus is optional for highest-stakes retrieval, not required for every query.

## Quick start

1. **Clone this repo** (or pull the latest).

   ```bash
   git clone https://github.com/ymanor2404/archie
   cd archie
   ```

2. **Set up `gws`** — see [`.cursor/README.md`](.cursor/README.md). **VPN required.** Full steps: [Google Workspace CLI setup (AI Skills Workshop)](https://redhat-ai-analysis.pages.redhat.com/ai-skills-workshop/06-gws/#using-gws). For Archie, enable Drive, Docs, Sheets, and Slides APIs and run `gws auth login -s drive,docs,slides,sheets`.

3. **Optional: Dataverse MCP** — copy `.cursor/dataverse-mcp.json` to `.cursor/mcp.json` if you want live UXR team roster data. Restart Cursor.

4. **Use Archie** in Cursor chat (Agent mode, latest Sonnet): ask a question about our UX research. Archie will read the spreadsheet catalog via `gws`, fetch relevant reports, and answer with citations and a tracing log.

## What's in this repo

| Path | Purpose |
|------|--------|
| `.cursor/skills/archie/` | Archie skill: `SKILL.md` (when/how to use, `gws` commands), `INSTRUCTIONS.md` (behavior, tone, tracing, references), `SPREADSHEET.md` (catalog config), `VERSION` (current skill version), `DATAVERSE_UXR.md` (live team roster via Dataverse), `UXR_TEAM.md` (fallback static roster). |
| `.cursor/dataverse-mcp.json` | Optional **Dataverse** MCP config for live UXR team roster only — not used for research retrieval. |
| `.cursor/README.md` | **First-time setup guide** — `gws` install, auth, and enabling the skill. |
| `UPGRADE.md` | **Migration guide** from v1 (Google Workspace MCP + Context Folder) to v2 (`gws` + spreadsheet). |

The file `.cursor/mcp.json` is gitignored if you add a local MCP config (e.g. Dataverse for team roster). **Archie does not use Google Workspace MCP** — research queries run via `gws` only.

## Research catalog

Archie's **source of truth** is the **Completed (Formal) Research** tab of the [User Research and User Engagements spreadsheet](https://docs.google.com/spreadsheets/d/1gdiYnzLB6knn_JS6RFbAgdwJa5r6NL0tH9IhJwcMqPQ/edit?gid=603259644#gid=603259644).

**Adding studies to Archie's context:** If you have a research study that you recently completed that you would like to add to Archie's context, add it to the spreadsheet linked above. Create a new row and fill out the relevant information at the top of the document. Make sure that you provide a link to your report in Column F and a Month and Year that the study was completed, as Archie will only process rows that have these values filled.

**Eligibility:** A row is included into Archie's context only when both **Report (Slides or document)** (column F) and **Month Study was completed (research readout complete and ready to share)** (column O) have values.

See [`.cursor/skills/archie/SPREADSHEET.md`](.cursor/skills/archie/SPREADSHEET.md) for column map, `gws` commands, and ranking rules.

For day-to-day Archie queries in Cursor, `gws` applies the recency rules in [INSTRUCTIONS.md](.cursor/skills/archie/INSTRUCTIONS.md).

## Feedback and guidelines

- **Feedback on Archie:** [Share your feedback](https://forms.gle/zoHWJ1YcMNtkG1fX9)
- **Archie guidelines / best practices:** [Guidelines doc](https://docs.google.com/document/d/1wPq_kw4BWvWxqLTKVTbip9evvUo5cwCqBl_Bh-TRywQ/edit?usp=drive_web&ouid=104626679691194729068)

## License

See [LICENSE](LICENSE) if present; otherwise use according to your organization's policy.
