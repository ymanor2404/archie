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

## Amplitude analytics setup (optional — for product metrics queries)

Archie can pull live product analytics from Amplitude. If you want to use this capability:

### 1. Get Amplitude credentials

Get the shared `AMPLITUDE_API_KEY` and `AMPLITUDE_SECRET_KEY` from your team maintainer or your organization's secret store (e.g. 1Password, internal wiki).

### 2. Create a `.env` file

In the project root (not inside `.cursor/`), create a `.env` file (it's in `.gitignore`):

```bash
AMPLITUDE_API_KEY=<value from maintainer>
AMPLITUDE_SECRET_KEY=<value from maintainer>
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Chart IDs

The file [AMPLITUDE_CHARTS.md](../AMPLITUDE_CHARTS.md) and `scripts/chart_ids.txt` list the chart IDs from the Red Hat dashboard. When you ask Archie about metrics or analytics, it uses these to fetch the right chart data.

---

## Optional: use environment variables instead

If you prefer not to put credentials in `mcp.json`, you can leave the `"env"` block out and set these in your shell profile (e.g. `~/.zshrc`):

```bash
export GOOGLE_OAUTH_CLIENT_ID="your-client-id"
export GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret"
export USER_GOOGLE_EMAIL="your.email@example.com"
```

For Amplitude, you can also export in the same place:

```bash
export AMPLITUDE_API_KEY="your-amplitude-api-key"
export AMPLITUDE_SECRET_KEY="your-amplitude-secret-key"
```

Then restart Cursor. The MCP and scripts will read the variables from the environment.
