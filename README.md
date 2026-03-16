# Archie — UX Research Insights Assistant

**Archie** is a Cursor skill that lets you “talk to the data” in our research repository. Ask questions like *“What do we know about AI engineers from our UX research reports?”* and Archie uses the **Google Workspace MCP** to search and read reports from Google Drive (Slides, Docs, PDFs) and answer from that content.

## What you need

- **Cursor** with this project open (or the skill available in your workspace).
- **Google Workspace MCP** configured in this project with **your own** Google OAuth credentials and email (credentials are per user, not stored in the repo).

## Quick start

1. **Clone this repo** (or pull the latest).
2. **Set up the Google Workspace MCP** — credentials are scoped to you:
   - See [**.cursor/README.md**](.cursor/README.md) for step-by-step setup.
   - Copy `.cursor/mcp.json.example` to `.cursor/mcp.json` and add your Client ID, Client Secret, and Google email.
   - Restart Cursor so it loads the MCP.
3. **Use Archie** in Cursor chat: ask a question about our UX research (personas, themes, studies, etc.). Archie will search the context folder, read relevant reports, and answer with citations and a tracing log.

## What’s in this repo

| Path | Purpose |
|------|--------|
| `.cursor/skills/archie/` | Archie skill: `SKILL.md` (when/how to use, tools), `INSTRUCTIONS.md` (behavior, tone, tracing, references). |
| `.cursor/mcp.json.example` | Example MCP config; copy to `mcp.json` and add your credentials. |
| `.cursor/README.md` | **First-time setup guide** — MCP config, OAuth, and enabling the skill. |
| `eval/` | **Eval:** 15 prompts, rubric (including recall), and scoresheet to assess answer quality and retrieval. |

The file `.cursor/mcp.json` is gitignored so your credentials are never committed.

## Feedback and guidelines

- **Feedback on Archie:** [Share your feedback](https://forms.gle/renMTKS3KQnmN94a7)
- **Archie guidelines / best practices:** [Guidelines doc](https://docs.google.com/document/d/1lr5gX9UPxwYz03sXitWWGOMI6LVgk4qd-whFdEzjNYQ/edit?tab=t.0)

## License

See [LICENSE](LICENSE) if present; otherwise use according to your organization’s policy.
