# Archie eval: prompts and rubric

This folder supports **evaluation of Archie’s answers**: run a fixed set of prompts, capture responses, and score them on a rubric. 

## How I ran these evaluations

1. **Run each prompt** in [prompts.md](prompts.md) (in Cursor with Archie enabled). Then, I had Archie generate a Google Doc and paste its response into that doc. I repeated this process two more times, having 3 responses for each prompt I provided. I added all of these responses to this spreadsheet: https://docs.google.com/spreadsheets/d/17t-9CECkxosQbfH-6QhuMd7H4BACQ3jKmcmXGyf0sdc/edit?gid=0#gid=0. 
2. **Score each response** using [rubric.md](rubric.md), I recorded a score for each response. I then also had Cursor use the same rubric to give a score on its own responses. Those responses are side by side in the spreadsheet 
4. **Aggregate** (e.g. average across prompts, average score per criterion) to track quality over time.

## Files

| File | Purpose |
|------|--------|
| [prompts.md](prompts.md) | 14 eval prompts |
| [rubric.md](rubric.md) | Scoring criteria |
