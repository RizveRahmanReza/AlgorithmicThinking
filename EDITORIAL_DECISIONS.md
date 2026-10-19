# EDITORIAL DECISIONS & ARCHITECTURAL LOG (ADR)

This file documents all major conventions, pedagogical trade-offs, language standards, and editorial policies adopted for *The Art of Algorithmic Thinking*.

---

## ADR-0001: Mandatory Dual-Language Mandate (C++20 & Python 3.12+)
- **Context**: Computer science pedagogy often suffers from a false dichotomy: high-level pseudo-code that ignores physical hardware realities, or low-level C code that bogs students down in manual memory management before grasping algorithmic concepts.
- **Decision**: Every cataloged problem must feature both:
  1. **Standard C++20**: Demonstrating explicit types, memory layout, cache locality, references, move semantics, explicit bit-width integers (`int64_t`, `uint32_t`), and STL zero-cost abstractions without non-standard headers (`<bits/stdc++.h>`).
  2. **Python 3.12+**: Demonstrating concise, idiomatic, fully type-annotated code, explicit standard library usage (`collections`, `heapq`, `bisect`), with explicit callouts to interpreter overhead, dynamic hashing, and memory footprints.
- **Consequence**: Readers learn to separate the mathematical essence of an algorithm from language-specific implementation idioms.

---

## ADR-0002: Rigorous 20-Step Problem Pedagogy
- **Context**: Code dumps fail to teach problem-solving. Readers memorize the final code rather than the discovery path.
- **Decision**: Every major problem in the manuscript must follow the 20-step sequence defined in `PROJECT_CHARTER.md`, beginning with real-world motivation, extracting invariants, analyzing brute-force failure, conducting candidate comparisons, and proving correctness before providing code listings.

---

## ADR-0003: Asymptotic and Complexity Notation Conventions
- **Definitions**:
  - Big-$O$ ($\mathcal{O}$): Asymptotic upper bound ($f(n) \le c \cdot g(n)$ for $n \ge n_0$).
  - Big-$\Omega$ ($\Omega$): Asymptotic lower bound ($f(n) \ge c \cdot g(n)$ for $n \ge n_0$).
  - Big-$\Theta$ ($\Theta$): Asymptotically tight bound ($c_1 g(n) \le f(n) \le c_2 g(n)$).
  - Small-$o$ ($o$) and Small-$\omega$ ($\omega$): Strict upper/lower asymptotic bounds.
- **Policy**: Avoid the sloppy colloquialism of calling every bound "Big-O" when describing tight worst-case or average-case bounds; use $\Theta$ when bounds are tight and $O$ when providing upper bounds.

---

## ADR-0004: Toolchain Verification Policy
- **Context**: AI models frequently hallucinate that unit tests passed without executing compilers or interpreters.
- **Decision**: If a compiler or interpreter is not installed on the execution host, mark test statuses as `UNVERIFIED_ENVIRONMENT` and record the missing executable in `BOOK_PROGRESS.md` and `docs/SESSION_LOG.md`. Never fabricate test logs or performance timings.

---

## ADR-0005: Stable Problem Identifier Schema
- Problem IDs follow the format: `<FAMILY>-<4-DIGIT-NUMBER>`
- Examples:
  - `SOLV-0001` (General Problem Solving & Methodology)
  - `ARR-0001` (Arrays, Vectors, In-place manipulations)
  - `STR-0001` (Strings, Buffers, Parsing)
  - `HASH-0001` (Hash Tables, Sets, Hashing)
  - `TREE-0001` (Binary Trees, BSTs, Heaps)
  - `GRAPH-0001` (Graphs, Networks, Paths)
  - `DP-0001` (Dynamic Programming)
  - `SYS-0001` (Systems, Caching, Databases)
