# Cursor setup for Archie

Archie uses the **Google Workspace MCP** to read our UX research from Drive, Docs, and Slides. Each user must configure the MCP with **their own** Google OAuth credentials and email. Credentials are **not** shared in this repo.

## First-time setup (required for each user)

### 1. Copy the MCP config template

Create your local MCP config from the example (do not commit it with real credentials):

```bash
cp .cursor/mcp.json.example .cursor/mcp.json
```

The file `.cursor/mcp.json` is in `.gitignore`, so your credentials will never be committed.

### 2. Add your Google OAuth credentials

Edit `.cursor/mcp.json` and replace the placeholders with **your** values:

| Placeholder | Replace with |
|-------------|--------------|
| `YOUR_GOOGLE_OAUTH_CLIENT_ID` | Your Google OAuth 2.0 client ID |
| `YOUR_GOOGLE_OAUTH_CLIENT_SECRET` | Your Google OAuth 2.0 client secret |
| `your.email@example.com` | Your Google account email |

**How to get OAuth credentials:**

1. Go to [Google Cloud Console](https://console.cloud.google.com/) and create or select a project.
2. **APIs & Services → Credentials → Create Credentials → OAuth client ID**.
3. Choose **Desktop application** as the application type.
4. Copy the Client ID and Client Secret into `.cursor/mcp.json`.
5. In **APIs & Services → Library**, enable: **Google Drive API**, **Google Docs API**, **Google Slides API**.

### 3. Enable the MCP in Cursor

- Open **Cursor Settings** (e.g. **Cmd + Shift + J** / **Ctrl + Shift + J**) → **Tools & MCP**.
- Ensure the **Google Workspace** MCP for this project is enabled (Cursor loads it from `.cursor/mcp.json`).
- If you just created `mcp.json`, **fully quit and restart Cursor** so it picks up the new config.

### 4. First run

The first time you use Archie (e.g. ask a question about our UX research), the MCP may open a browser so you can sign in with the Google account you set as `USER_GOOGLE_EMAIL` and grant access. Do that once per machine.

---

## Amplitude analytics (optional — via Cursor plugin)

Archie can pull live product analytics from Amplitude using the **Amplitude plugin MCP server** — no API keys or Python scripts needed in this repo.

1. Go to **Cursor Settings → Plugins** and enable the **Amplitude** plugin.
2. The plugin provides its own MCP server with tools like `query_chart`, `get_charts`, `get_dashboard`, `search`, and more.
3. Ask Archie about product metrics or analytics and it will use the Amplitude MCP tools automatically.

---

## Optional: use environment variables instead

If you prefer not to put credentials in `mcp.json`, you can leave the `"env"` block out and set these in your shell profile (e.g. `~/.zshrc`):

```bash
export GOOGLE_OAUTH_CLIENT_ID="your-client-id"
export GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret"
export USER_GOOGLE_EMAIL="your.email@example.com"
```

Then restart Cursor. The MCP will read the variables from the environment.
