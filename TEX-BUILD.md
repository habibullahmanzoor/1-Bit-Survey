# Building the paper PDF

To compile you need `1bit-llm-survey.tex`, `references.bib`, and the `figures/` directory
(specifically its `*.pdf` files — the `.tex`/`.mmd`/`.drawio` sources in there are not
needed to compile). The main `.tex` is **self-contained** otherwise (the two `longtable`s
are inlined, no `\input`), so it drops straight into Overleaf or a `-output-directory`
build alongside `figures/`. As of 2026-09-14 every native chart (Figures 3, 4, 6, 7, 9,
10, 11, 12) is a pre-rendered PDF under `\includegraphics`, not embedded TikZ/pgfplots
code, precisely so Overleaf's compile servers don't have to redo that computation on
every build — **if `figures/*.pdf` isn't uploaded/committed alongside the `.tex`, the
build fails outright** rather than falling back to a placeholder. See
`figures/README.md` for how to regenerate them.

## Files
- `1bit-llm-survey.tex` — the full paper, **auto-generated** from `draft/*.md`. Do not hand-edit; edit the markdown.
- `references.bib` — 129 entries, **auto-generated** from `data/inventory.csv` + `scripts/pdf-metadata.tsv`.
- `tables/table1.tex`, `tables/table5.tex` — the same two `longtable`s written out separately for optional reuse.
  The main `.tex` inlines them, so these are **not required** to compile.
- `scripts/build_paper.py` — the assembler (markdown→LaTeX, bib, tables).
- `scripts/pdf-metadata.tsv` — arXiv id + title per archived PDF (extracted once with `pdftotext`).
- `Makefile` — `make regen` then `make pdf`.

## Regenerate the .tex/.bib after editing drafts or CSVs
```
python scripts/build_paper.py      # or: make regen
```

## Compile (needs TeX Live / MiKTeX — not installed in this environment)
```
make pdf
# = pdflatex → bibtex → pdflatex → pdflatex
```

## Status / known gaps (v0.1)
- **Author lists in `references.bib` are `<first-author> and others`** — expand for camera-ready.
  15 titles were hand-corrected in `scripts/build_paper.py:TITLE_FIX`; the rest are auto-extracted.
- All 106 in-text `\cite` keys resolve; 23 archived works are not yet cited.
- 3 literal `[...]` TODO markers remain in the prose (`[report value]`, `[cite OSF DOI]`,
  `[cite ReTern in candidates]`) — intentional, fill during revision.
- Section §7 embeds Table 1 (classification) and Table 5 (reported results); the full
  normalised comparison lives in `data/table72-normalised-comparison.md` (online appendix).
- Figures 1–4 are Mermaid/spec sources in `figures/`; render and `\includegraphics` them.
- §9 result tables are placeholders until `repro/` is run.
- Target venue is ACM Computing Surveys → swap `\documentclass{article}` for `acmart`
  (`\documentclass[acmsmall]{acmart}`) and adjust the abstract to ≤100 words at that point.
