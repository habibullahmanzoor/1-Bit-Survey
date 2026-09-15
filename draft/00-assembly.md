# Draft assembly, 1-Bit LLM Survey

**The assembled LaTeX paper is `../1bit-llm-survey.tex`** (auto-generated from these .md files by
`../scripts/build_paper.py`; `../references.bib` = 143 entries, grouped by year; see `../TEX-BUILD.md`).
Edit the markdown here (or the native-TikZ figure/table code in `build_paper.py` itself for anything
not sourced from a `.md` file), then `python ../scripts/build_paper.py` to regenerate, then run
`pdflatex` / `bibtex` / `pdflatex` / `pdflatex` to rebuild `1bit-llm-survey.pdf`.

Title: **"Native 1-Bit and 1.58-Bit Large Language Models: A Survey and an Independent
Re-Evaluation."** Authors: Habib Ullah Manzoor (University of the West of Scotland) et al.
(the full author list is kept in the local build only pre-publication; see
`scripts/build_paper.py`'s `AUTHOR_BLOCK` note). Current build: 58 pages, 0 compile errors,
0 undefined references.

Section files in reading order. Compiled section numbers run 1 (Introduction) to 12 (Conclusion) in
this same order; the leading number in each filename is only a sort key, not the section number.

| file | paper section | status |
|---|---|---|
| `01-introduction.md` | 1. Introduction | complete |
| `02-background.md` | 2. Background and Preliminaries | complete |
| `03-methodology.md` | 3. Scope and Corpus | complete |
| `04-taxonomy.md` | 4. A Taxonomy of Binary and Ternary LLMs | complete |
| `05-architecture.md` | 5. Architectural Design | complete |
| `06-training.md` | 6. Training Methodology and Theory | complete |
| `07-systems.md` | 7. Inference Systems and Hardware | complete |
| `07b-benchmarking.md` | 8. Performance and Benchmarking | complete |
| `08-applications.md` | 9. Applications and Extensions | complete |
| `09-reproduction.md` | 10. Independent Re-Evaluation | complete; results in place (Section 10.2-10.7) |
| `10-open-problems.md` | 11. Challenges and Open Problems | complete |
| `11-conclusion.md` | 12. Conclusion | complete, single paragraph |

Supporting data:
- `../data/inventory.csv` — the corpus sheet (140 rows: 135 in-window + 5 foundational), drives
  Table 1, the taxonomy figures, and `references.bib`'s citation data (title/venue/year/authors).
  Every row now has a real first-author name; no `Anon` placeholders remain.
- `../data/results.csv` — 57 headline-result rows, drives Table 2.
- `../repro/` — the reproduction-study scripts and logs behind Section 10.
- `../data/taxonomy.md`, `../data/table1-classification.md`, `../data/table5-systems.md`,
  `../data/table72-normalised-comparison.md`: early planning drafts, superseded by the CSV-driven
  tables above. Kept for reference only; not read by `build_paper.py`.

See `../figures/README.md` for the figure inventory and which ones are native TikZ (built directly
in `build_paper.py`, no manual step) versus hand-maintained `.drawio` files needing a manual PDF
export after editing.

## What's left, and who it's for

Everything below needs information only the authors can supply — there is nothing further to
draft or generate from the corpus data:

1. **ORCID iDs** for both authors.
2. **Target journal** — once picked, check the 58-page length and abstract length against that
   venue's limits; re-tighten if needed.
3. **OSF/Zenodo deposit** of the artifact repository referenced in Section 10.7 (evaluation
   harness commit, patch files, checkpoint hashes, run scripts, raw benchmark logs), for the DOI
   the paper promises on acceptance.
4. **Cover letter** for submission.
