**Guidelines for Interacting with Archie the Research Data Retrieval Assistant**

**1 About Archie**  
Welcome to Archie, your dedicated Research Data Retrieval Assistant. Archie is a **Cursor skill** that runs inside the Cursor IDE, giving you direct access to the wealth of knowledge contained within our "[All UXR Reports](https://drive.google.com/drive/folders/1yW2GbqKThAskAAKA1UodTWqMzWZbVBo1)" repository.  
Its purpose is to help you search and retrieve data directly from past user research reports without needing to manually comb through dozens of PDFs and documents. Think of Archie as a retrieval tool for Red Hat's UX Research that values precision, honesty, and transparency above all else.

Archie connects to a single data source through its MCP (Model Context Protocol) integration:

- **Google Workspace MCP** — Searches and reads research reports (Google Slides, Docs, PDFs) from the UX research repository (Archie's Context Folder) on Google Drive.

**Archie does not synthesize, interpret, or editorialize.** It retrieves data from UX research reports and presents it exactly as it appears in the source material. It does not draw cross-document conclusions, create narrative threads, identify themes across reports, or offer its own analysis. It does not have access to product analytics, Jira, competitive analysis tools, supplementary marketing or support documents, or the web.

To get started with Archie, clone the [archie2 repo](https://github.com/RedHatInsights/archie2) and follow the setup instructions in the repo's [README](README.md) and [.cursor/README.md](.cursor/README.md). You will need Cursor with the Google Workspace MCP configured using your own Google OAuth credentials. If you have questions about setup, please contact Yahav Manor on Slack or via email ([ymanor@redhat.com](mailto:ymanor@redhat.com)).

**2 What Archie Knows (In-Scope Topics)**  
Users are encouraged to ask any question related to UX research at Red Hat, regardless of whether they know if specific documentation exists in the research repository folder. Archie searches the UX research team's research readouts/reports as its sole source of truth. If no relevant reports are found, Archie will say so honestly rather than speculate or pull from other sources.

**Examples of In-Scope Inquiries:**

- **Broad Discovery:** "What do we know about the installation experience for RHEL?" (Archie will scan the research repository for specific studies and present what it finds).
- **Targeted Findings:** "What were the key takeaways from the 'Project Alpha Interviews.docx' regarding login issues?" (Asks for specific data from a specific file).
- **Verbatim Quotes:** "Give me 3 direct, verbatim user quotes about RHEL Lightspeed frustrations." (Archie retrieves exact quotes from reports).
- **Validation Questions:** "Do we have any research that validates the need for a dark mode?" (Asks Archie to check if evidence exists in the repository).
- **Persona/Segment Queries:** "What do we know about AI engineers from our UX research reports?" (Archie searches for all relevant persona data across reports).
- **Study Methodology:** "Was the data regarding Product360 gathered via a survey or interviews?" (Archie pulls study details directly from the report).
- **"Blind" Questions:** Asking about a legacy product or feature without knowing if a study was ever conducted. Archie will check the repo and, if nothing is found, say so honestly.

**3 What Archie Does Not Know (Out-of-Scope Topics)**

Archie only retrieves data from UX research reports in the Context Folder. It does not synthesize, interpret, or combine findings across documents. The following are out of scope:

**Examples of Out-of-Scope Inquiries:**

- **Synthesis or Interpretation Requests:** "Synthesize findings across all our onboarding studies" or "What themes emerge across our 2023 and 2024 research?" — Archie presents data from individual reports as-is; drawing cross-document conclusions is a human responsibility.
- **Product Analytics:** Questions about usage metrics, event tracking, or Amplitude data — Archie does not have access to analytics tools.
- **Competitive Analysis / Market Trends:** Questions about competitors, industry benchmarks, or market positioning — Archie does not search the web or access competitive intelligence documents.
- **Jira / Project Status:** Questions about research ticket status, team assignments, or sprint progress — Archie does not have access to Jira.
- **Sensitive/HR Information:** Questions regarding employee salaries, performance reviews, or interpersonal conflicts.
- **Non-UX Business Logic:** Deeply technical engineering queries or financial forecasting unrelated to user experience.
- **Write Actions in External Systems:** Archie is read-only. It cannot create or modify documents, send emails, schedule calendar events, or write data to any external system.
- **Data Outside the Context Folder:** Archie only accesses UX research reports in its Context Folder on Google Drive. It does not access other Drive locations, Slack messages, internal wikis, or other tools.

If you ask about an out-of-scope topic, Archie will let you know it cannot help with that and suggest you consult the appropriate team or tool.

**4 How to Ask Great Questions: Examples**  
The best way to interact with Archie is to ask specific questions about research findings or ask it to retrieve data on a particular topic from the research repository.  
**Note:** If your question is ambiguous, Archie is trained to ask you up to 3 clarifying questions to ensure it searches for the right thing.


| Good Prompt (In-Scope)                                                                             | Why it works                                                        |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| "What were the key takeaways from the 'Project Alpha Interviews.docx' regarding login issues?"     | Asks for specific data from a specific file.                        |
| "What data do we have on user sentiment regarding the dashboard layout from Q3 and Q4 reports?"    | Asks Archie to retrieve relevant data from reports on the topic.    |
| "Do we have any research that validates the need for a dark mode?"                                 | Asks for evidence-based confirmation from the repository.           |
| "What did users say about onboarding friction in our 2024 studies?"                                | Asks Archie to retrieve findings on a topic from a specific period. |
| "Give me 3 direct, verbatim user quotes about RHEL Lightspeed frustrations."                       | Asks for exact quotes directly from research reports.               |


| Bad Prompt (Out-of-Scope)                                                        | Why it fails                                                                             |
| -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| "Just tell me the users like the new feature so I can move forward."             | Archie is instructed to provide the truth, not rubber-stamp decisions.                   |
| "Synthesize the themes across all our onboarding research into a narrative."     | Archie retrieves data as-is from individual reports; it does not synthesize across them.  |
| "How many AI Playground setups were there this month?"                           | Archie does not have access to product analytics or Amplitude.                           |
| "What are competitors doing in the AI platform space?"                           | Archie does not search the web or access competitive intelligence.                       |
| "What UXDR tickets are currently open?"                                          | Archie does not have access to Jira.                                                     |


**5 The Tracing Log and End-of-Response Elements**  
Unlike other AI tools, Archie is required to "show its work."  
Every time Archie provides an answer, it will include a Tracing Log at the bottom of the response. This log will list:

1. The key terms identified in your query.
2. The specific documents searched and keywords used.
3. The relevant sections and sources data was pulled from.
4. **Why Archie made those choices** — why particular reports were selected, why certain search terms were used, and why specific data was surfaced over other material. This gives you a transparent view of Archie's retrieval decisions, not just a list of what was used.

Review this log to ensure that the data is coming from the correct documents and that Archie's reasoning makes sense for your question. If, for any reason, this log is not provided, you may instruct Archie to provide it by simply stating "Please provide the tracing log for your previous output."

After the tracing log, every response also includes:

- **Feedback and guidelines links** — links to the Archie feedback form and these best-practice guidelines.
- **Limitations disclaimer** — a brief closing statement reminding you that Archie has not synthesized any research data, that it is an AI tool that may hallucinate, that you should verify cited sources, and that the number of documents consulted may not represent the full repository. See Section 7 for more on responsible usage.

**6 Archie's Data Source**  
Archie connects to its data source through the Google Workspace MCP server configured in the Cursor IDE:

- **Google Workspace MCP (required):** This is Archie's sole integration. It enables searching and reading files from the [UXR research repository](https://drive.google.com/drive/folders/1yW2GbqKThAskAAKA1UodTWqMzWZbVBo1) (Archie's Context Folder) on Google Drive, including Google Slides decks, Docs, and PDFs. Setup requires your own Google OAuth credentials — see the [repo setup guide](.cursor/README.md) for details.

Archie does not have access to product analytics (Amplitude), project management (Jira), competitive intelligence documents, supplementary marketing or support documents, or the web. If you need data from those sources, please consult the appropriate team or tool directly.

**7 Responsible AI Usage: The "Human-in-the-Loop"**  
While Archie is a powerful accelerator for finding UX research data, it is an assistive retrieval tool, not a replacement for critical thinking. Users must adhere to the following principles to ensure data integrity and safe decision-making.

- **End-of-response disclaimer:** Every Archie answer ends with a brief **limitations disclaimer** (after the feedback and guidelines links). It reminds you that Archie has not synthesized any research data and is solely pulling data directly from past UX research reports, that it is an AI system that may hallucinate or misstate details, that you should **check the original sources** Archie referenced, and that the number of reports consulted is not an exhaustive picture of the repository—search can miss documents, and other relevant studies may exist. **Read it every time**; it is there so risk and coverage limits are explicit, not buried.

- **No Synthesis:** Archie presents data from individual reports exactly as it appears in those reports. It does not draw conclusions, identify themes, or create narrative connections across documents. If you need cross-report synthesis or strategic interpretation, that is a human responsibility — Archie gives you the raw data to work from.
- **Do Not Trust at Face Value:** AI models can hallucinate or misinterpret nuances in data. Treat Archie's responses as a starting point, not the final word. **Never** copy and paste an answer directly into a report or presentation without reviewing it for accuracy first.
- **Citation Review:** Archie is engineered to provide **direct, clickable links** for every source it references — **Google Drive (or Docs/Slides) links** for reports and documents. Report/deck names, slide or section references alone are not sufficient; use the links Archie provides to **open the original artifact and verify** the citation.
- **Context vs. Strategy:** Archie has been tested and optimized for its ability to retrieve relevant data from research reports. It has not been validated for strategic actionability. Archie can tell you what users said in a past study (data retrieval). It cannot reliably tell you what specific business move Red Hat should make next based on that information (strategy). Strategic application of the data remains a human responsibility.
- **Data Grounding:** Archie is instructed to ground its answers in the data it retrieves and to explicitly state when evidence is limited or absent. If Archie says "There does not exist enough research to validate this query," take that at face value — do not push for a speculative answer.
- **Validation for High-Stakes Decisions:** If you are using research findings to justify major business decisions (e.g., roadmap pivots, resource allocation, feature deprecation), you must validate the findings against the original data or speak directly with the researcher who conducted the study. Do not make high-stakes decisions based solely on Archie.
