# Cursor setup for Archie

Archie uses the **Google Workspace MCP** to read UX research from Drive, Docs, and Slides. Each user must have the MCP configured with **their own** Google OAuth credentials and email. Credentials are **not** shared in this repo.

---

## Already have Google Workspace MCP configured?

If you already have **Google Workspace MCP** set up in Cursor (for example in your user-level MCP settings at `~/.cursor/mcp.json` or another project), you may not need to create a project-level config. Just verify:

1. **Drive, Docs, and Slides tools are enabled** — the MCP must be started with `--tools drive docs slides` (or a tool tier that includes all three).
2. **Your Google email is available** — Archie passes `user_google_email` on every MCP call. The email should be set via the `USER_GOOGLE_EMAIL` environment variable in your MCP config or shell profile.
3. **The MCP appears in Cursor** — open **Cursor Settings → Tools & MCP** and confirm the Google Workspace server is listed and enabled for this project.

If all three are true, you're ready — skip to [First run](#4-first-run) below.

---

## First-time setup (no Google Workspace MCP yet)

Follow these steps if you do **not** have the Google Workspace MCP configured in Cursor.

### 1. Create your Google OAuth credentials

You need OAuth 2.0 credentials so the MCP can access Google Drive on your behalf.

1. Go to [Google Cloud Console](https://console.cloud.google.com/) and create or select a project.
2. Navigate to **APIs & Services → Credentials → Create Credentials → OAuth client ID**.
3. Choose **Desktop application** as the application type.
4. Copy the **Client ID** and **Client Secret** — you'll need them in the next step.
5. In **APIs & Services → Library**, enable these three APIs:
   - **Google Drive API**
   - **Google Docs API**
   - **Google Slides API**

> **Note:** If your organization's Google Cloud requires admin consent for new OAuth apps, you may need to request approval before the OAuth flow will work.

### 2. Copy the MCP config template

```bash
cp .cursor/mcp.json.example .cursor/mcp.json
```

The file `.cursor/mcp.json` is in `.gitignore`, so your credentials will never be committed.

### 3. Add your credentials

Edit `.cursor/mcp.json` and replace the placeholders with **your** values:

| Placeholder | Replace with |
|-------------|--------------|
| `YOUR_GOOGLE_OAUTH_CLIENT_ID` | Your Google OAuth 2.0 Client ID (from step 1) |
| `YOUR_GOOGLE_OAUTH_CLIENT_SECRET` | Your Google OAuth 2.0 Client Secret (from step 1) |
| `your.email@example.com` | Your Google account email (the account you use to access Google Drive) |

Your `.cursor/mcp.json` should look like this when done:

```json
{
  "mcpServers": {
    "google_workspace": {
      "command": "uvx",
      "args": [
        "workspace-mcp",
        "--tools",
        "drive",
        "docs",
        "slides"
      ],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "123456789-abc.apps.googleusercontent.com",
        "GOOGLE_OAUTH_CLIENT_SECRET": "GOCSPX-your-secret-here",
        "USER_GOOGLE_EMAIL": "you@example.com"
      }
    }
  }
}
```

### 4. Enable the MCP in Cursor

- Open **Cursor Settings** (e.g. **Cmd + Shift + J** / **Ctrl + Shift + J**) → **Tools & MCP**.
- Ensure the **Google Workspace** MCP for this project is listed and enabled (Cursor loads it from `.cursor/mcp.json`).
- If you just created `mcp.json`, **fully quit and restart Cursor** so it picks up the new config.

### 5. First run

The first time you use Archie (e.g. ask a question about UX research), the MCP will open a browser window so you can sign in with the Google account you set as `USER_GOOGLE_EMAIL` and grant access. This OAuth consent happens once per machine.

---

## Alternative: use environment variables

If you prefer not to put credentials directly in `mcp.json`, you can set them in your shell profile (e.g. `~/.zshrc` or `~/.bashrc`):

```bash
export GOOGLE_OAUTH_CLIENT_ID="your-client-id"
export GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret"
export USER_GOOGLE_EMAIL="your.email@example.com"
```

Then remove the `"env"` block from `.cursor/mcp.json` (or `.cursor/mcp.json.example`) and restart Cursor. The MCP will read the variables from the environment.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| MCP not showing in Cursor | Fully quit and restart Cursor after creating/editing `.cursor/mcp.json`. |
| OAuth consent screen errors | Make sure Google Drive, Docs, and Slides APIs are enabled in your Google Cloud project. |
| "Permission denied" on Drive files | Your Google account must have access to Archie's Context Folder. Ask the team to share it with your email. |
| `uvx: command not found` | Install `uv` first: `curl -LsSf https://astral.sh/uv/install.sh \| sh`, then restart your terminal. |
| MCP tools not appearing | Verify your `mcp.json` includes `"--tools", "drive", "docs", "slides"` in the `args` array. |
