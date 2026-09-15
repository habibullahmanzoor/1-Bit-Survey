# Writing style guide for the 1-Bit LLM survey

Distilled from reading the three genre-exact competitor surveys we have archived
(Gong et al., *A Survey of Low-bit LLMs*, Neural Networks 2025; Liu et al., *Binary
Neural Networks for LLM: A Survey*, arXiv 2025; Hao et al., *Low-Precision Training of
LLMs*, IEEE TPAMI 2025) plus general CS-survey guidance
(https://www.cs.kent.edu/~javed/class-IAD06S/course-area/IAD06S-surveyinfo.pdf,
https://arxiv.org/pdf/2509.25828) and the canonical *A Survey of Large Language Models*
(Zhao et al., arXiv 2303.18223).

## Structure (what these papers actually do)

1. **No table of contents.** None of the three journal-style surveys prints one. Remove `\tableofcontents`.
2. Order: Abstract -> (Index Terms / Keywords) -> 1 Introduction -> 2 Background/Basics ->
   3 Taxonomy -> 4..N thematic sections (one per taxonomy category) -> Evaluation/Comparison ->
   Future Directions -> Conclusion -> References. Methodology is folded into the Introduction
   or a short early subsection, not a peer section (only *systematic* reviews make it a full section;
   keep ours short and titled "Scope and Methodology").
3. **Arabic section numbers** (`1`, `2`, `2.1`, `2.1.1`). Deep numbering (`3.2.1`) is normal.
4. The Introduction **must** end with two things:
   - a **contributions** list (`In summary, this survey makes the following contributions:` + bullets/enumerate);
   - an **organization paragraph** (`The remainder of this survey is organized as follows. Section 2 ...`).
5. A **related-surveys paragraph** in the Introduction: name each prior survey and state precisely how ours differs.
6. Reference an early **overview figure** ("As shown in Figure 1, ...") that depicts the survey's own taxonomy/organization.
7. Each thematic section: short framing paragraph -> per-approach prose -> a **comparison table**;
   close with a 1-2 sentence "what remains unclear" note (we already do this).

## Citations

- **Numbered, IEEE-style**: `[1]`, `[17]`, ranges `[1]-[4]`, groups `[12, 13, 14]`.
- **Ascending order of first appearance** in the text -> use `\bibliographystyle{unsrtnat}`
  (or `IEEEtran`), NOT `plainnat` (which numbers alphabetically). `natbib` option `sort&compress`
  renders multi-cites as sorted compressed ranges.
- In prose, name authors as `Wang et al. [17]`, `Gong et al. [x]`; first mention of a method gives
  its name in the sentence and the cite after it.
- Do not stack two `\cite` commands (`\cite{a}\cite{b}`) -> always `\cite{a,b}`.

## Language and tone

- Formal, objective, third person for the field; **"we" is standard** for the authors' own moves
  ("we categorize", "we organize the field along five axes", "In this survey we ...").
- **Present tense** for what prior work does/claims ("BitNet introduces BitLinear ...",
  "The authors adjust the mean before binarization ...").
- **No em dashes.** Rework every `--`/`---` into a comma, a colon, a semicolon, parentheses, or two sentences.
  En dashes in numeric/date ranges (`2023--2026`, `pp. 10--14`) are fine and expected.
- No contractions ("do not", not "don't"). No rhetorical questions as headings.
- Quotation marks: LaTeX `` `` `` / `` '' ``, not straight `"`.
- No drafting scaffolding in the prose: strip `> Draft ...`, `[report value]`, `[cite OSF DOI]`,
  `(placeholder)`, `Fill after the run`, `TODO`. Turn `[cite ReTern in candidates]` into a real cite or delete.
- Open-problems section: phrase each as a declarative gap statement (`A convergence theory for
  straight-through training of 1-bit Transformers does not yet exist.`), optionally with a short
  `Open problem.` lead-in, not `Question.` / `Claim to test.`
- Keep hedging calibrated: "matches full precision on standard benchmarks to about 7B parameters"
  is good; avoid both overclaiming and vague "some works".
- Numbers: spell out at sentence start ("Twenty-seven works ..."), digits elsewhere ("27 works").
- Define every acronym on first use: "quantization-aware training (QAT)".

## Applied to our draft: change list (done 2026-09-04)

- [x] deleted `\tableofcontents` (+ `\clearpage`); added an `Index Terms:` line instead
- [x] `\bibliographystyle{plainnat}` -> `\bibliographystyle{unsrtnat}` (numbers now ascending by first citation)
- [x] removed all em dashes from `draft/*.md` (paired -> parentheses, lone -> comma); 0 remain
- [x] stripped `[report value]`, `[cite OSF DOI]`, `[cite ReTern in candidates]`, `[summary ... fill after the run]`,
      `[HASH]`, placeholder table cells; §9 placeholder tables now use `n/a`
- [x] Introduction keeps "This survey makes five contributions." + a single clean `enumerate`; organization paragraph kept
- [x] renamed stale cite keys in drafts (Anon2025-UltraQuantisation -> Connor2025-UltraQuantisation, Anon2025-BitROM -> Zhang2025-BitROM, + 10 more)
- [x] fixed the broken bold in `draft/04-taxonomy.md` "Secondary cut"
- [x] `scripts/build_paper.py`: joins wrapped list-item continuation lines; merges adjacent `\cite`;
      `~` -> `$\sim$` in prose / "about" in headings; `<=`/`>=` -> `$\le$`/`$\ge$`; pulls line-leading punctuation back
- [x] §10 leads normalised to `**Open problem.**`
- [x] **Full prose pass done (2026-09-04):** all 12 section drafts rewritten for the genre. Comma-splice
      appositives from the em-dash removal reworked with "such as" / colons / parentheses / restructuring;
      British -ise/-isation/-our -> American throughout (converter now runs a `spell()` safety net);
      straight `"..."` -> LaTeX `` `` '' `` (converter); math written as real `$...$` (converter protects it);
      section cross-references renumbered to the final 1..12 (Methodology is now Section 3, so Benchmarking is 8,
      Applications 9, Reproduction 10, Open Problems 11, Conclusion 12); multi-citations `[a], [b]` grouped to
      `\cite{a,b}` so `unsrtnat` renders `[1, 2]` / `[1]--[3]` in ascending order; drafting notes and placeholder
      table cells removed; open-problems phrased as declarative statements. Body is ~12,300 words.
- [ ] STILL TODO (genuine content work): expand `references.bib` author lists beyond "first-author and others";
      fill the Section 10 reproduction tables after the run; render `figures/*.mmd`; a human read-through for tone.
