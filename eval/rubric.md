# Archie eval rubric

Score each response on the criteria below. Use the scale **1–5** unless otherwise noted (1 = poor, 5 = excellent). Record both the numeric score and brief notes.

---

## 1. Recall (retrieval) — required

**Definition:** Of the documents in Archie’s Context Folder that contain *relevant* information for this query, what proportion did Archie actually retrieve and use in the response?

- **Relevant** = a source that could validly be used to answer the query.
- **Retrieved and used** = the source was fetched and its content is reflected in the answer (cited or paraphrased).

**How to score:**  
Establish the set of **relevant sources** for this query (documents in the context folder that contain information that could validly answer it—by auditing the folder or from pre-defined ground truth). Then:

**Recall** = (number of those relevant sources that Archie retrieved and used) ÷ (total number of relevant sources).

Record as a **percentage (0–100%)**. You can also map to 1–5 for averaging with other criteria (e.g. 0–20% → 1, 21–40% → 2, 41–60% → 3, 61–80% → 4, 81–100% → 5).

**Score:** _____ %  
**Notes:** _________________________________________________

---

## 2. Relevance / answer quality

Does the response directly address the question? Is the content on-topic and useful?

- **1** – Off-topic or does not answer the question.  
- **2** – Tangentially related; major gaps.  
- **3** – Partially answers; some irrelevant or missing pieces.  
- **4** – Largely on-topic and useful; minor gaps.  
- **5** – Fully addresses the question; clear and useful.

**Score:** _____  
**Notes:** _________________________________________________

---

## 3. Citation quality

Are sources named clearly? Can a reader trace claims back to specific reports (and ideally slides/sections)?

- **1** – No or almost no citations; cannot verify.  
- **2** – Few citations; vague or incomplete.  
- **3** – Some citations; partially traceable.  
- **4** – Most claims cited with report names; mostly traceable.  
- **5** – Every substantive claim tied to a named source (and section/slide when helpful).

**Score:** _____  
**Notes:** _________________________________________________

---

## 4. Synthesis and structure

Is the answer organized by theme or insight (not just a list of docs)? Are connections between sources clear?

- **1** – Disorganized or document-by-document list only.  
- **2** – Weak structure; little synthesis.  
- **3** – Some themes; some redundancy or fragmentation.  
- **4** – Good thematic structure; clear narrative.  
- **5** – Coherent narrative by theme; findings woven together with clear connectors.

**Score:** _____  
**Notes:** _________________________________________________

---

## 5. Required elements

- **Tracing section:** Present and describes query terms, documents searched, and findings used? (Y/N)  
- **Reference links footer:** Feedback form + guidelines doc links at end? (Y/N)

**Tracing:** _____ **Footer:** _____  
**Notes:** _________________________________________________

---

## 6. Grounding (no hallucination)

Does the response use *only* information from retrieved sources? No invented studies, numbers, or quotes?

- **1** – Clear hallucination or speculation presented as fact.  
- **2** – Likely or possible hallucination.  
- **3** – Unclear; hard to verify.  
- **4** – Largely grounded; minor ambiguity.  
- **5** – Fully grounded in retrieved content; no apparent invention.

**Score:** _____  
**Notes:** _________________________________________________

---

## 7. Appropriate hedging (when applicable)

For validation or “do we have evidence” questions: does Archie say “evidence is limited” or “no research to validate” when that’s true? For weak evidence, is the limitation stated?

- **1** – Overstates or understates evidence; no hedging when needed.  
- **2** – Hedging missing or incorrect in important places.  
- **3** – Some appropriate hedging; some gaps.  
- **4** – Generally appropriate; minor gaps.  
- **5** – Appropriately hedged; limitations and confidence clearly stated.

**Score:** _____ (or N/A if not applicable)  
**Notes:** _________________________________________________

---

## Summary (per response)

| Criterion              | Score | Notes (brief) |
|------------------------|-------|----------------|
| 1. Recall (retrieval)  |       |                |
| 2. Relevance           |       |                |
| 3. Citation quality    |       |                |
| 4. Synthesis           |       |                |
| 5. Required elements   | Y/N   |                |
| 6. Grounding           |       |                |
| 7. Hedging             |       |                |

**Overall (optional):** Average of 1–4 and 6–7, or a single 1–5 “overall quality” score.  
**Recall** should be tracked separately (and at least one criterion in every eval run).
