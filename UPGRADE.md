# Upgrading Archie to v2

Archie **v2** replaces the Google Workspace MCP + Drive Context Folder with the **Google Workspace CLI (`gws`)** and reads research reports directly from the [User Research and User Engagements spreadsheet](https://docs.google.com/spreadsheets/d/1gdiYnzLB6knn_JS6RFbAgdwJa5r6NL0tH9IhJwcMqPQ/edit?gid=603259644#gid=603259644).

If you are still on **v1** (Google Workspace MCP, Context Folder sync), you may be missing newly completed studies that were never copied into the folder.

## Why upgrade?

| v1 (deprecated) | v2 (current) |
|-----------------|--------------|
| Google Workspace MCP with OAuth credentials in `.cursor/mcp.json` | IT-vetted **`gws` CLI** — credentials in `~/.config/gws/` |
| Reports copied into a Drive Context Folder (manual sync step) | Reads the **engagements spreadsheet** directly — no copy step |
| Catalog limited to synced folder contents | Catalog = all eligible rows in the spreadsheet |

## Quick upgrade

From your existing archie clone:

```bash
cd archie
git pull origin main
```

Confirm you have v2:

```bash
cat .cursor/skills/archie/VERSION
# Should print: 2.0.0
```

## Set up `gws` (required for v2)

Follow [`.cursor/README.md`](.cursor/README.md). **VPN required.** Workshop guide: [Google Workspace CLI setup](https://redhat-ai-analysis.pages.redhat.com/ai-skills-workshop/06-gws/#using-gws).

```bash
gws auth login -s drive,docs,slides,sheets
gws auth status   # expect token_valid: true
```

## Optional: Dataverse MCP (team roster only)

Research retrieval uses `gws` only. Dataverse MCP is still optional for live UXR team roster queries:

```bash
cp .cursor/dataverse-mcp.json .cursor/mcp.json
```

Restart Cursor after changing MCP config.

## Remove deprecated v1 setup

After `gws` works, you can remove the Google Workspace MCP from `.cursor/mcp.json` (or delete the file if you do not use Dataverse). You no longer need:

- `GOOGLE_OAUTH_CLIENT_ID` / `GOOGLE_OAUTH_CLIENT_SECRET` in project MCP config
- The `scripts/sync_reports.py` Context Folder sync pipeline
- A local clone of [archie2](https://github.com/ymanor2404/archie2) — v2 lives in the main [archie](https://github.com/ymanor2404/archie) repo

## Fresh clone

```bash
git clone https://github.com/ymanor2404/archie
cd archie
```

Then complete the `gws` setup in [`.cursor/README.md`](.cursor/README.md).

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Archie warns "deprecated version" after `git pull` | Restart Cursor so it reloads the skill. Confirm `VERSION` and `SPREADSHEET.md` exist under `.cursor/skills/archie/`. |
| `gws: command not found` | Install via the [workshop guide](https://redhat-ai-analysis.pages.redhat.com/ai-skills-workshop/06-gws/#using-gws). |
| Still using MCP for research | Open Agent mode with latest Claude Sonnet. Archie v2 uses shell `gws` commands, not MCP Drive tools. |
