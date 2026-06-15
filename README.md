# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

This system answers questions about off-campus housing and dorm-life advice from student discussions, especially Reddit threads in r/college. That knowledge is useful because official housing pages explain policies, prices, and eligibility, but they do not capture the practical student perspective on waitlists, roommate matching, rental approval barriers, or whether dorm life is actually worth the cost.

---

## Document Sources

The corpus uses 10 local markdown files derived from r/college threads:

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | My school has no where for me to live on campus | Reddit thread | documents/01_housing_shortage.md |
| 2 | Is dorm life worth it? | Reddit thread | documents/02_dorm_life_worth_it.md |
| 3 | College student apartments | Reddit thread | documents/03_college_student_apartments.md |
| 4 | Is student housing a scam? | Reddit thread | documents/04_student_housing_scam.md |
| 5 | What is it Like Living in a College Dorm? | Reddit thread | documents/05_living_in_dorm.md |
| 6 | Best and worst floor to live on in a dorm | Reddit thread | documents/06_floor_choice_dorm.md |
| 7 | Sharing a dorm: I'm nervous and have some questions | Reddit thread | documents/07_sharing_a_dorm_questions.md |
| 8 | Dorm vs apartment | Reddit thread | documents/08_dorm_vs_apartment.md |
| 9 | Should I stay off campus as a freshman? | Reddit thread | documents/09_off_campus_as_freshman.md |
| 10 | Is it a bad idea to live off campus in an apartment as a freshman? | Reddit thread | documents/10_bad_idea_off_campus_freshman.md |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 1000 characters

**Overlap:** 150 characters

**Why these choices fit your documents:** The documents are short, opinion-heavy Reddit summaries. A 1000-character chunk keeps each anecdote or advice point intact while still leaving enough room for surrounding context. The 150-character overlap reduces the chance that a useful recommendation gets cut off at a boundary.

**Preprocessing:** Local markdown files are loaded from `documents/` and cleaned to remove HTML noise, excess whitespace, and blank-line clutter before chunking.

**Final chunk count:** 10 chunks across 10 documents

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:** If cost were not a constraint, I would compare larger embedding models with better semantic nuance and longer context handling against the local MiniLM baseline. For this corpus, the main goal is matching student phrasing to the right anecdote, so I would trade some latency and model size for stronger retrieval on housing-specific language, roommate terms, and credit or income barriers. I would also consider multilingual support if the corpus were expanded beyond English.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** The model is told: "You are answering questions about student-generated knowledge using only the provided context. Do not use outside knowledge. If the context does not contain enough information, say so explicitly. Keep the answer concise and cite the most relevant source names in the response."

**How source attribution is surfaced in the response:** The retrieved chunks are formatted with source title, file path, distance, and text before being sent to Groq. The final answer appends a `Sources:` line listing the distinct source names that were retrieved for that question.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say to do if on-campus housing is full? | Look for off-campus housing, ask about emergency housing or temporary placements, and use leftover financial aid or loans for rent if allowed. | Suggested off-campus housing, leftover financial aid for rent, asking for a landlord letter, and checking for emergency housing or temporary placements. | Relevant | Accurate |
| 2 | Is dorm life always cheaper than living off campus? | No. Students say it depends on the school; off-campus can be cheaper, but utilities, transportation, and furnishings can change the total cost. | Said dorm life is not always cheaper and explained that off-campus housing can be cheaper depending on meals, commute time, and the school. | Relevant | Accurate |
| 3 | What problems do students run into when trying to rent an apartment off campus? | Lack of credit history, rental history, and income can make approval difficult. | Mentioned roommate splitting costs, affordability, and credit or income requirements for approval. | Partially relevant | Partially accurate |
| 4 | What makes freshmen consider living off campus anyway? | Lower cost, more comfort, roommate matching, and the ability to choose a better housing setup. | Explained that freshmen consider off-campus living for lower cost, more comfort, roommate matching, and independence. | Relevant | Accurate |
| 5 | What advice do students give about choosing a dorm room or floor? | Pick based on noise, privacy, and convenience rather than assuming there is one universally best floor. | Recommended choosing based on privacy, noise, convenience, and roommate boundaries. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** What problems do students run into when trying to rent an apartment off campus?

**What the system returned:** The answer mixed the expected credit-history and income barriers with roommate-splitting and general affordability advice.

**Root cause (tied to a specific pipeline stage):** Retrieval pulled a few nearby off-campus tradeoff chunks because they were semantically close to the question, so the generator blended related but less specific advice instead of staying tightly focused on apartment approval barriers.

**What you would change to fix it:** Add a reranker or a more targeted document set for approval-specific questions, and consider a tighter retrieval filter so that credit and income barrier chunks outrank general housing-cost chunks.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The planning document kept the pipeline disciplined: it fixed the domain, chunk size, overlap, retrieval top-k, and evaluation questions before implementation started. That made it easier to validate the system against specific, testable housing questions instead of drifting into a generic chatbot.

**One way your implementation diverged from the spec, and why:** I used local markdown summaries derived from the Reddit threads instead of scraping live thread content at runtime. That made the project reproducible, kept the corpus self-contained, and avoided depending on fragile network or HTML parsing during evaluation.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* The Domain, Chunking Strategy, and Retrieval Approach sections from planning.md plus the assignment requirements.
- *What it produced:* A modular RAG pipeline layout with document ingestion, chunking, embedding, ChromaDB persistence, retrieval, and grounded generation.
- *What I changed or overrode:* I tuned the implementation to use 1000-character chunks, 150-character overlap, and a local all-MiniLM-L6-v2 embedding model to match the short Reddit-style corpus.

**Instance 2**

- *What I gave the AI:* The five evaluation questions from planning.md and the desired reporting format for the README.
- *What it produced:* An evaluation harness that ran the five questions through the pipeline and collected answers, sources, and retrieved chunks.
- *What I changed or overrode:* I added a JSON output file for traceability, then used the real run results to populate the evaluation table and failure analysis instead of writing a generic summary.
