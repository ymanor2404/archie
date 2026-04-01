**Guidelines for Interacting with Archie the Research Insights Assistant**

**1 About Archie**  
Welcome to Archie, your dedicated Research Insights Assistant. Archie is a **Cursor skill** that runs inside the Cursor IDE, giving you direct access to the wealth of knowledge contained within our "[All UXR Reports](https://drive.google.com/drive/folders/1yW2GbqKThAskAAKA1UodTWqMzWZbVBo1)" repository.  
Its purpose is to help you search, synthesize, and validate user research findings without needing to manually comb through dozens of PDFs and documents. Think of Archie as an expert in Red Hat's UX Research who values precision, honesty, and transparency above all else.

Archie is not *limited* to just the research repository folder. It connects to multiple data sources through MCP (Model Context Protocol) integrations:

- **Google Workspace MCP** — Searches and reads research reports (Google Slides, Docs, PDFs) from the primary research repository, supplementary live documents (marketing portfolio intelligence, support case insights, competitive news), and your broader Google Drive.
- **Amplitude Plugin MCP** — Pulls live product analytics, event tracking data, and usage metrics directly from Amplitude.
- **Atlassian MCP** — Queries the UXDR Jira project for research ticket status, team assignments, and actionable recommendations.
- **Web Search** — Accesses the Internet for industry context, market trends, and competitive analysis when internal sources are insufficient.

Archie's purpose is to leverage the research repository as the central source of truth while referencing these other sources (analytics, Jira, supplementary docs, and external data) to help answer your questions.

To get started with Archie, clone the [archie2 repo](https://github.com/RedHatInsights/archie2) and follow the setup instructions in the repo's [README](README.md) and [.cursor/README.md](.cursor/README.md). You will need Cursor with the Google Workspace MCP configured using your own Google OAuth credentials. Amplitude and Jira integrations are optional and can be enabled as described in the repo setup guide. If you have questions about setup, please contact Yahav Manor on Slack or via email ([ymanor@redhat.com](mailto:ymanor@redhat.com)).

**2 What Archie Knows (In-Scope Topics)**  
Users are encouraged to ask any question related to UX research at Red Hat, regardless of whether they know if specific documentation exists in the research repository folder. Archie is designed to help determine the best source of truth, prioritizing the UX research team's research readouts/reports as the primary source and extending to supplementary documents, live product analytics, the UXDR Jira board, and external Internet sources to fill gaps or provide broader context.

**Examples of In-Scope Inquiries:**

- **Broad Discovery:** "What do we know about the installation experience for RHEL?" (Archie will scan the research repository for specific studies).
- **Methodology & Best Practices:** "What is the standard template for a usability test plan?" or "How do I calculate a SUS score?" (Archie can leverage Drive templates or general knowledge).
- **Industry Context:** "What are the current UX trends for developer portals?" (Archie will use web search for external sources).
- **Synthesized Queries:** "Based on our personas and recent competitor news, how should we approach the new dashboard design?" (Archie combines internal persona docs with the Competitive Newstracker and external data).
- **"Blind" Questions:** Asking about a legacy product or feature without knowing if a study was ever conducted. Archie will check the repo and, if nothing is found, pivot to supplementary docs or external knowledge regarding that feature.
- **Product Analytics:** "How many AI Playground setups were there this month?" or "Show me usage trends from the dashboard." (Archie pulls live data from the Amplitude plugin).
- **Research Project Status:** "What UXDR tickets are currently open?" or "What is the team working on right now?" (Archie queries the UXDR Jira board via the Atlassian MCP).
- **Supplementary Context:** "What support issues are customers running into with OpenShift?" (Archie fetches the GSS Case Insights document) or "What are competitors doing in the AI platform space?" (Archie fetches the Competitive Newstracker).

**3 What Archie Does Not Know (Out-of-Scope Topics)**

While Archie has broad access to information, there are specific guardrails regarding the nature of the data and actions outside of information retrieval.

**Examples of Out-of-Scope Inquiries:**

- **Sensitive/HR Information:** Questions regarding employee salaries, performance reviews, or interpersonal conflicts.
- **Non-UX Business Logic:** Deeply technical engineering queries or financial forecasting unrelated to user experience.
- **Write Actions in External Systems:** Archie is read-only across its integrations. It can *query* Jira tickets and Amplitude charts, but it cannot create or modify Jira tickets, send emails, schedule calendar events, or write data to any external system.
- **Engineering Project Status:** Questions about code deployments, CI/CD pipelines, or engineering sprint status outside the UXDR Jira project are not accessible to Archie.
- **Data Outside Connected Sources:** Archie can only access Google Drive (via Google Workspace MCP), Amplitude (via the Amplitude plugin), and the UXDR Jira project (via Atlassian MCP). It does not have access to Slack messages, internal wikis outside Google Drive, or other tools not connected via MCP.

**4 How to Ask Great Questions: Examples**  
The best way to interact with Archie is to ask specific questions about research findings, broad questions about user themes, or targeted questions about analytics and research project status.  
**Note:** If your question is ambiguous, Archie is trained to ask you up to 3 clarifying questions to ensure it searches for the right thing.


| Good Prompt (In-Scope)                                                                             | Why it works                                                  |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| "What were the key takeaways from the 'Project Alpha Interviews.docx' regarding login issues?"     | Asks for specific info from a specific file.                  |
| "Synthesize the findings on user sentiment regarding the dashboard layout from Q3 and Q4 reports." | Asks Archie to combine insights from multiple sources.        |
| "Do we have any research that validates the need for a dark mode?"                                 | Asks for evidence-based confirmation.                         |
| "What are the conflicting points between our 2023 and 2024 onboarding studies?"                    | Asks Archie to identify overlap and contrast.                 |
| "How many AI Playground setups were there this month?"                                             | Asks Archie to pull live product metrics from Amplitude.      |
| "What UXDR tickets are currently in progress and who is working on them?"                          | Asks Archie to query the UXDR Jira board for team status.     |
| "What support issues are customers running into with OpenShift?"                                   | Asks Archie to check the GSS Case Insights supplementary doc. |



| Bad Prompt (Out-of-Scope)                                            | Why it fails                                                                       |
| -------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| "Just tell me the users like the new feature so I can move forward." | Archie is instructed to provide the truth, not rubber-stamp decisions.             |
| "Log a bug in Jira for the login issue we found."                    | Archie is read-only — it can query Jira tickets but cannot create or modify them.  |
| "What is the status of the 'Project Alpha' code deployment?"         | This is engineering project status outside the UXDR Jira project and Google Drive. |


**5 The Tracing Log**  
Unlike other AI tools, Archie is required to "show its work."  
Every time Archie provides an answer, it will include a Tracing Log at the bottom of the response. This log will list:

1. The key terms identified in your query.
2. The specific documents searched and keywords used.
3. The relevant sections and sources data was pulled from (including which data source type: UX research, supplementary doc, Amplitude, or Jira).

Review this log to ensure that the insights are coming from the correct documents and sources. If, for any reason, this log is not provided, you may instruct Archie to provide it by simply stating "Please provide the tracing log for your previous output."

**6 Archie's Data Sources and Integrations**  
Archie connects to its data sources through MCP (Model Context Protocol) servers configured in the Cursor IDE. Each integration serves a specific purpose:

- **Google Workspace MCP (required):** This is Archie's primary integration. It enables searching and reading files from the [UXR research repository](https://drive.google.com/drive/folders/1yW2GbqKThAskAAKA1UodTWqMzWZbVBo1) on Google Drive, including Google Slides decks, Docs, and PDFs. It also provides access to three supplementary live documents (Portfolio Marketing MI Research Index, GSS Case Insights, and Competitive Newstracker) that Archie fetches directly when a query touches their domain. Setup requires your own Google OAuth credentials — see the [repo setup guide](.cursor/README.md) for details.
- **Amplitude Plugin (optional):** Gives Archie access to live product analytics — event tracking, usage metrics, and interactive charts. Enable it in **Cursor Settings → Plugins** (no API keys needed in the repo). If not enabled, Archie will fall back to archived analytics markdown files in the research repository when available.
- **Atlassian MCP (optional):** Allows Archie to query the UXDR Jira project for research ticket status, team assignments, and linked actionable recommendations. Configured in `.cursor/mcp.json`; prompts for Atlassian OAuth on first use.

If an optional integration is not configured, Archie will note this and provide whatever answer it can from the sources that are available.

**7 Responsible AI Usage: The "Human-in-the-Loop"**  
While Archie is a powerful accelerator for finding and synthesizing UX knowledge, it is an assistive tool, not a replacement for critical thinking. Users must adhere to the following principles to ensure data integrity and safe decision-making.

- **Do Not Trust at Face Value:** AI models can hallucinate or misinterpret nuances in data. Treat Archie's responses as a starting point, not the final word. **Never** copy and paste an answer directly into a report or presentation without reviewing it for accuracy first.
- **Citation Review:** Archie is engineered to provide citations to source files whenever it retrieves internal data — including report/deck names, slide or section references, Amplitude chart IDs, and Jira ticket keys. It is the user's responsibility to verify these citations against the original sources.
- **Distinguish Source Types:** Archie draws from multiple source types (UX research reports, supplementary live docs, Amplitude analytics, Jira, and web sources). Pay attention to how Archie labels each source — data from a supplementary marketing document or Jira board is not the same as a validated UX research finding.
- **Context vs. Strategy:** Archie has been tested and optimized for its ability to provide relevant context and information retrieval. It has not been validated for strategic actionability. Archie can tell you what users said in a past study (context) or show you current usage metrics (data). It cannot reliably tell you what specific business move Red Hat should make next based on that information (strategy). Strategic application of the data remains a human responsibility.
- **Data Grounding:** Archie is instructed to ground its answers in the data it retrieves and to explicitly state when evidence is limited or absent. If Archie says "There does not exist enough research to validate this query," take that at face value — do not push for a speculative answer.
- **Validation for High-Stakes Decisions:** If you are using research findings to justify major business decisions (e.g., roadmap pivots, resource allocation, feature deprecation), you must validate the findings against the original data or speak directly with the researcher who conducted the study. Do not make high-stakes decisions based solely on Archie.

