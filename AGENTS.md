# AGENTS.md — Persistent Guidance for Codex Sessions

## Project Identity and Mission

You are collaborating on **THE ART OF ALGORITHMIC THINKING: From First Principles to Mastering Data Structures, Algorithms, and Real-World Problem Solving**.
This is a world-class, multi-volume computer science textbook and verified problem-solving encyclopedia.

- **Ambition**: Comparable to CLRS, Kleinberg & Tardos, and Skiena, with practical engineering rigor, mathematical proofs, low-level systems insights, and competitive problem-solving patterns.
- **Languages**: Mandatory dual-language implementations in **Standard C++20** and **Python 3 (target 3.12+)** for every single cataloged problem.
- **Scope**: 18 comprehensive Parts, target catalog of 1,200+ distinct verified problems across 5 difficulty levels.

---

## Continuation Protocol

When instructed with:
`"Continue writing The Art of Algorithmic Thinking."` or any variation, follow this exact workflow:

1. **Read Core State Files**:
   - `AGENTS.md` (this file)
   - `BOOK_PROGRESS.md` (current chapter progress, verified counts, next action)
   - `PROJECT_CHARTER.md` (core standards, vision, principles)
   - `MASTER_OUTLINE.md` (curriculum architecture across all 18 Parts)
   - `EDITORIAL_DECISIONS.md` (recorded conventions, notation, ADRs)
   - `docs/SESSION_LOG.md` (history of work across sessions)
2. **Identify Current Focus**:
   - Locate the exact next chapter or subchapter specified in `BOOK_PROGRESS.md`.
   - Never skip forward leaving previous chapters incomplete or unverified.
   - Never regenerate existing complete chapters or restart from scratch.
3. **Execute the Step-by-Step Writing & Engineering Workflow**:
   - Review prerequisites and learning outcomes.
   - Write foundational theory and mental models with first-principles reasoning.
   - For every featured problem, adhere strictly to the **20-Step Mandatory Problem Framework** (from real-world motivation to dry runs, proofs, edge cases, C++20, Python 3, complexity, and challenges).
   - Write and save solutions to `solutions/cpp/<PROBLEM_ID>.*` and `solutions/python/<PROBLEM_ID>.*`.
   - Provide comprehensive test suites under `tests/`.
   - Record and execute verification tests. If compilers/interpreters are not installed in the environment, mark as `UNVERIFIED_ENVIRONMENT` with exact failure details (never claim tests passed without execution).
   - Append new problems to `problems/catalog.jsonl` and update `problems/PROBLEM_INDEX.md`.
4. **Update State Files**:
   - Update `BOOK_PROGRESS.md` with newly written chapters, problem counts, and next exact action.
   - Record session actions in `docs/SESSION_LOG.md`.
   - Output the required **End-of-Session Factual Report**.

---

## Non-Negotiable Editorial & Technical Standards

1. **No Superficial AI Filler**: No vague summaries, no hand-waving proofs ("left as an exercise"), no boilerplate placeholders. Write deep, rigorous, engaging textbook prose.
2. **Dual-Language Parity**: Both C++20 and Python 3 solutions must be written, idiomatic, fully typed/commented, and tested against identical problem constraints and test fixtures.
3. **Algorithmic Decision Framework (ADF)**: Anchor every problem and technique in the 20-question ADF decision tree. Teach *why* alternatives fail (bottleneck analysis, counterexamples, cache/memory behavior).
4. **Zero Fabrication**: Do not cite non-existent papers, fake benchmark numbers, or false verification claims. If unexecuted, state unexecuted.
5. **Preservation**: Do not overwrite or modify completed sections unless fixing an explicit errata documented in `EDITORIAL_DECISIONS.md`.
