# Cursor setup for Archie

Archie uses the **Google Workspace CLI (`gws`)** to read the UX research catalog from Google Sheets and fetch linked reports from Drive, Docs, and Slides. Each user installs and authenticates `gws` on their own machine. Credentials are stored locally in `~/.config/gws/` — not in this repo.

**No Google Workspace MCP server is required or supported** for Archie in this repo. Do not configure a `google_workspace` / `workspace-mcp` server for research retrieval — use `gws` shell commands instead (see the Archie skill). If you previously used the MCP-based setup, see [UPGRADE.md](../UPGRADE.md).

---

## Set up `gws`

**You must be on VPN** to open the setup guide.

Follow the full walkthrough here: **[Google Workspace CLI setup (AI Skills Workshop)](https://redhat-ai-analysis.pages.redhat.com/ai-skills-workshop/06-gws/#using-gws)**

Summary of the steps in that guide:

1. **Install** — Mac: `brew install googleworkspace-cli`. Windows (or Mac/Linux alternative): `npm install -g @googleworkspace/cli`.
2. **Verify** — Run `gws --version`.
3. **Create a GCP project** — In [Google Cloud Console](https://console.cloud.google.com/) with your `@redhat.com` account, create a project (e.g. `gws-cli-your-user-id`).
4. **Configure OAuth** — Set up an Internal OAuth consent screen and create a **Desktop app** OAuth client. Download the client JSON.
5. **Save credentials** — Put the JSON at `~/.config/gws/client_secret.json` (the guide includes a `mkdir` / `cp` example).
6. **Authenticate** — Run `gws auth login`, open the URL in your browser, and complete sign-in.
7. **Enable APIs** — Run a test command (e.g. `gws drive files list --params '{"pageSize": 5}'`). If you get an `accessNotConfigured` error, open the enable URL from the error and click **Enable**. Repeat for each API you need.

For Archie, enable at least **Drive**, **Docs**, **Sheets**, and **Slides** in your GCP project. After setup, log in with Archie's scopes:

```bash
gws auth login -s drive,docs,slides,sheets
```

### Verify auth

```bash
gws auth status
```

Expect `token_valid: true` and your Red Hat email under `user`. Test spreadsheet access:

```bash
gws sheets spreadsheets get --params '{
  "spreadsheetId": "1gdiYnzLB6knn_JS6RFbAgdwJa5r6NL0tH9IhJwcMqPQ",
  "fields": "sheets.properties"
}' 2>/dev/null
```

You also need view access to the [User Research and User Engagements spreadsheet](https://docs.google.com/spreadsheets/d/1gdiYnzLB6knn_JS6RFbAgdwJa5r6NL0tH9IhJwcMqPQ/edit?gid=603259644#gid=603259644).

---

## Optional: Dataverse MCP (live UX research team roster only)

This is **optional** and **separate from research retrieval** (which uses `gws` only). Archie can answer "who is on the UX research team?" from **live org data** via Red Hat's Dataverse MCP (RoverPeople). Without it, Archie uses a static roster in `UXR_TEAM.md` and warns that it may be less current.

1. Copy the example config:

```bash
cp .cursor/dataverse-mcp.json .cursor/mcp.json
```

2. Open **Cursor Settings → Tools & MCP** and ensure the Dataverse server is enabled.
3. Restart Cursor. The first team query may prompt Snowflake OAuth sign-in.

See [DATAVERSE_UXR.md](skills/archie/DATAVERSE_UXR.md) for how Archie scopes the team (Leslie Hinson + full reporting chain).

---

## Recommended model

In Cursor chat, select the **latest Claude Sonnet** model and use **Agent** mode (not Ask-only) so Archie can run `gws` commands.

| Choice | Guidance |
|--------|----------|
| **Default** | Latest **Claude Sonnet** — best balance of shell reliability, instruction following (citations, tracing, no synthesis), and speed for routine UXR queries. |
| **Optional upgrade** | Latest **Claude Opus** — use for broad multi-report questions or if Sonnet skipped `gws` calls, missed Doc tabs, or produced weak citations. |
| **Avoid** | **Claude Haiku** — more likely to skip retrieval steps or hallucinate quotes; **Ask-only chat** — will not read the spreadsheet catalog. |

More detail is in the repo [README — Recommended model](../README.md#recommended-model).

---

## First-time setup checklist

1. Clone this repo:

```bash
git clone https://github.com/ymanor2404/archie
cd archie
```

2. Install and authenticate `gws` (see [Set up `gws`](#set-up-gws) above).
3. Open the project in **Cursor**.
4. Set model to **latest Claude Sonnet** and **Agent** mode.
5. Ask an Archie question (e.g. "What do we know about AI engineers from our UX research reports?").

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `gws: command not found` | Re-run the install step from the [workshop guide](https://redhat-ai-analysis.pages.redhat.com/ai-skills-workshop/06-gws/#using-gws). Restart your terminal. |
| Auth error / `token_valid: false` | Run `gws auth login -s drive,docs,slides,sheets` again. Check `gws auth status`. |
| "Access blocked" during OAuth | Add your email as a **test user** on the OAuth consent screen in GCP Console. |
| API not enabled (`accessNotConfigured`) | Enable Drive, Docs, Slides, and **Sheets** APIs in your GCP project (see the workshop guide). |
| Sheets 403 "API has not been used" | Enable the [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com) for your OAuth project; wait 1–2 minutes and retry. |
| "Permission denied" on spreadsheet | Your Google account must have view access to the User Research and User Engagements spreadsheet. |
| Agent doesn't run `gws` | Use **Agent** mode, not Ask-only. Confirm `gws auth status` works in your terminal. Do not substitute a Google Workspace MCP server — this repo uses `gws` only. |
| Workshop page won't load | Connect to **VPN** and retry. |

---

## Per-machine portability

Each teammate repeats the same setup on their computer:

1. Clone `archie`
2. Install and authenticate `gws` (workshop guide)
3. Open in Cursor, Agent mode

No project-level Google OAuth config is required. Auth lives in `~/.config/gws/` on each machine.
