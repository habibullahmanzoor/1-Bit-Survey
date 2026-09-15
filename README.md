# Native 1-Bit and 1.58-Bit Large Language Models: A Survey and an Independent Re-Evaluation

Habib Ullah Manzoor (University of the West of Scotland) and Basim Alhumaily (Qassim University)

A curated, open-access survey of 135 works (2023–2026) on native binary/ternary LLMs,
post-training and quantization-aware routes toward one bit, inference kernels, and
hardware, organized on a five-axis taxonomy (140 works total including foundational
background). Alongside the survey, Section 10 reports an independent re-evaluation:
a controlled accuracy comparison from open matched checkpoints, and a from-source
efficiency re-run of the reference `bitnet.cpp` runtime against half-precision, 8-bit,
and three 4-bit baselines on one x86 machine — including a real defect found and fixed
in that runtime along the way.

The compiled paper is [`1bit-llm-survey.pdf`](1bit-llm-survey.pdf).

## Layout

| Path | Contents |
|---|---|
| `draft/*.md` | Manuscript source, one file per section |
| `scripts/build_paper.py` | Assembles `1bit-llm-survey.tex` from `draft/*.md` + `data/*.csv`; also generates `references.bib` and `tables/` |
| `1bit-llm-survey.tex` / `.pdf` | The assembled, compiled paper (generated — do not hand-edit the `.tex`) |
| `data/inventory.csv` | The 140-work classification behind Table 1 and the taxonomy figures |
| `data/results.csv` | The headline-results data behind Table 2 |
| `figures/` | Every figure's source (standalone TikZ/pgfplots `.tex`, draw.io `.drawio`) and compiled `.pdf`; see `figures/README.md` for the regeneration workflow |
| `tables/` | Standalone exports of Tables 1 and 2 |
| `protocol/`, `survey-protocol.md` | The pre-specified corpus-assembly protocol and search log |
| `repro/` | The independent reproduction pipeline — see `repro/README.md` |
| `papers/` | `INDEX.md` indexes the 140 cited works (title, source URL, local filename); PDFs are not stored here, see below |

## Building the paper

Requires a TeX distribution (MiKTeX or TeX Live) with `pdflatex` and `bibtex`.

```
python scripts/build_paper.py      # regenerate .tex / references.bib / tables/ from draft/*.md + data/*.csv
pdflatex 1bit-llm-survey.tex
bibtex 1bit-llm-survey
pdflatex 1bit-llm-survey.tex
pdflatex 1bit-llm-survey.tex
```

or `make regen && make pdf`. Figure PDFs are pre-rendered and checked in; see
`figures/README.md` if you need to regenerate one after a data or wording change.

## Independent reproduction

`repro/README.md` documents the full pipeline: environment setup, the exact commits
and checkpoint revisions pinned in `repro/env/`, the one-line runtime patch, and the
run scripts. `repro/logs/` holds the raw per-run harness output (JSON/JSONL) behind
every number reported in Section 10 of the paper.

## Cited papers are indexed, not redistributed

The 140 works classified in Table 1 are open-access (freely readable), which is the
survey's inclusion criterion — but open-access does not mean the survey has the right
to redistribute copies. `papers/INDEX.md` and `data/inventory.csv` give the title,
source URL, and expected local filename for every one; retrieve each from its own
listed source.

## License

Not yet decided. Until a license is added, standard copyright applies (all rights
reserved) — treat the manuscript text, figures, and code accordingly.

## Citing this work

The paper is not yet published at a venue. If you reference this work in the meantime,
please cite the repository and the corresponding author directly.
