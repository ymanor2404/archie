# UX Research Engagements Spreadsheet — Archie's Source of Truth

Archie's **only catalog** of eligible UX research reports is the [User Research and User Engagements spreadsheet](https://docs.google.com/spreadsheets/d/1gdiYnzLB6knn_JS6RFbAgdwJa5r6NL0tH9IhJwcMqPQ/edit?gid=603259644#gid=603259644). Archie uses the **Google Workspace CLI (`gws`)** to read this spreadsheet, then fetches linked report artifacts (Slides, Docs, PDFs) by file ID.

**Do not** use Archie's old Context Folder on Drive as a catalog. Reports outside this spreadsheet (or rows that fail the eligibility filter below) are out of scope.

---

## Spreadsheet identifiers

| Field | Value |
|-------|-------|
| **Spreadsheet ID** | `1gdiYnzLB6knn_JS6RFbAgdwJa5r6NL0tH9IhJwcMqPQ` |
| **Sheet name** | `Completed (Formal) Research` |
| **Sheet GID** | `603259644` |
| **Header row** | Row **2** (column titles) |
| **First data row** | Row **3** |

---

## Column map (sheet tab `Completed (Formal) Research`)

| Column | Header | Use in Archie |
|--------|--------|---------------|
| **B** | Product area | Citation product-area tag; keyword search |
| **C** | Study Title | Primary title for citations and keyword search |
| **D** | Owners & Contributors | `Author(s):` line when not in the report body |
| **E** | Goal | Keyword search |
| **F** | Report (Slides or document) | **Required for eligibility.** Report link or title; fetch content from resolved file ID |
| **G** | Method (structured) | Study context (method) |
| **H** | UXR Offering (research type, multi-select) | Study context |
| **I** | # External participants … | Study context (n) |
| **J** | # Internal participants … | Study context (n) |
| **O** | Month Study was completed (research readout complete and ready to share) | **Required for eligibility.** Recency ranking |
| **P** | Year | Recency ranking; citation year |

---

## Eligibility filter (mandatory)

Include a row **only if both** are true:

1. **Report (Slides or document)** (column F) has a non-empty value.
2. **Month Study was completed (research readout complete and ready to share)** (column O) has a non-empty value.

Skip all other rows — even if they have a report link but no completion month, or a completion month but no report.

---

## `gws` commands

**Auth:** `gws auth login -s drive,docs,slides,sheets` (Sheets API must be enabled in your GCP project).

### 1. Verify spreadsheet access

```bash
gws sheets spreadsheets get --params '{
  "spreadsheetId": "1gdiYnzLB6knn_JS6RFbAgdwJa5r6NL0tH9IhJwcMqPQ",
  "fields": "sheets.properties"
}' 2>/dev/null
```

### 2. Read the catalog (report chips/links + completion dates)

Use grid data so column F report links are available. Many rows use a **Smart Chip** (linked file preview), not a plain cell hyperlink — request `chipRuns` in the field mask:

```bash
gws sheets spreadsheets get --params '{
  "spreadsheetId": "1gdiYnzLB6knn_JS6RFbAgdwJa5r6NL0tH9IhJwcMqPQ",
  "ranges": ["'\''Completed (Formal) Research'\''!B3:P1327"],
  "includeGridData": true,
  "fields": "sheets.data.rowData.values(formattedValue,hyperlink,chipRuns)"
}' 2>/dev/null
```

Parse each `rowData` entry (row index + 3 = spreadsheet row number):

| Index in range `B:P` | Column |
|----------------------|--------|
| 0 | B — Product area |
| 1 | C — Study Title |
| 2 | D — Owners & Contributors |
| 3 | E — Goal |
| 4 | F — Report (Slides or document) |
| 5 | G — Method |
| 6 | H — UXR Offering |
| 7 | I — External n |
| 8 | J — Internal n |
| 12 | O — Month completed |
| 13 | P — Year |

### 3. Resolve report file IDs

For each eligible row, resolve the Drive file ID from column F (in order):

1. **`chipRuns[].chip.richLinkProperties.uri`** — preferred. Column F often embeds the report as a Smart Chip (linked Slides/Docs preview); the URL lives here, not in `hyperlink`.
2. **`hyperlink`** on the cell — legacy plain hyperlinks.
3. **`formattedValue`** if it is a full URL (`http…`).
4. **Fallback:** `gws drive files list` with `name contains '<report title fragment>' and trashed=false`, `pageSize`: 5, `supportsAllDrives`: true, `includeItemsFromAllDrives`: true — pick the best title match for **that spreadsheet row only**. Do not browse Drive outside resolving a catalog entry.

Extract file ID from URLs: `/d/{id}/`, `/file/d/{id}/`, or `?id={id}`.

Cells may contain **multiple report lines** (newline-separated). Resolve each line; fetch the **2–4 most relevant** reports total for the query.

### 4. Fetch report content (same as before)

| File type | Command |
|-----------|---------|
| Native Google Slides | `gws slides presentations get --params '{"presentationId": "FILE_ID"}'` |
| Google Docs | `gws docs documents get --params '{"documentId": "FILE_ID", "includeTabsContent": true}'` |
| PDF / Office uploads | `gws drive files export` or `download` |

---

## Search and ranking workflow

1. Load eligible catalog rows via step 2 above.
2. Score rows against the user's query using **Study Title**, **Product area**, **Goal**, **Report** text, and **Owners**.
3. **Recency:** Rank by **Year (P) + Month (O)** — treat as study completion date. For current-product questions, prefer studies completed in the **last 12–18 months** (same tiers as INSTRUCTIONS.md: priority ≤18 mo, aging 18–24, legacy ≥24).
4. Select **2–4** best-matching eligible reports; resolve file IDs; fetch content.
5. Present findings **without synthesis** — same rules as INSTRUCTIONS.md.
