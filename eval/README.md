# Archie eval: prompts and rubric

This folder supports **evaluation of Archie’s answers**: run a fixed set of prompts, capture responses, and score them on a rubric. At least one criterion is **recall** (what proportion of relevant datapoints/sources were successfully retrieved).

## How to run the eval

1. **Run each prompt** in [prompts.md](prompts.md) (in Cursor with Archie enabled). Paste or save each response (e.g. in a doc or the scoresheet).
2. **Define ground truth for recall** (per prompt or per run):
   - Either list the **documents in the context folder** that contain relevant information for that query (you can do this by searching the folder yourself or from prior knowledge).
   - Or after the run, **audit the context folder** for that query and list all relevant docs; then compare to what Archie retrieved.
3. **Score each response** using [rubric.md](rubric.md). Record scores in [scoresheet.md](scoresheet.md) (or a copy).
4. **Aggregate** (e.g. average recall across prompts, average score per criterion) to track quality over time.

## Files

| File | Purpose |
|------|--------|
| [prompts.md](prompts.md) | 15 eval prompts (persona, targeted, general, validation, etc.). |
| [rubric.md](rubric.md) | Scoring criteria, including **recall (retrieval)**. |
| [scoresheet.md](scoresheet.md) | Template to record prompt, response summary, and scores. |

## Recall (retrieval) in practice

**Recall** = (number of relevant sources Archie retrieved and used) / (total number of relevant sources in the context folder for that query).

- **Relevant source**: A document in Archie’s Context Folder that contains information that could validly be used to answer the query.
- **Retrieved and used**: The document was fetched (e.g. via `get_drive_file_content`) and its content is reflected in the answer (e.g. cited or paraphrased).

To score recall:

1. For each eval prompt, establish the set of **relevant sources** (by searching the folder or from a pre-made list).
2. From Archie’s response (and tracing section), list the **sources Archie retrieved and used**.
3. Recall = |retrieved ∩ relevant| / |relevant| (as a proportion or 0–100%).

If you don’t have a full ground truth, you can still rate recall on a 1–5 scale (see rubric) based on whether Archie missed obvious key documents or included most of what you expect.
