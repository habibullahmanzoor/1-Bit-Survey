# Reference cross-check (RULE 1 audit)

Last run: 2026-09-09. Script: `scripts/check_refs.py` (re-runnable).

## Verdict: PASS

Every one of the 143 citations resolves to a locally archived source. Nothing is
cited without a downloaded copy.

| check | result |
|---|---|
| distinct `\cite{}`/`\citet{}` keys in `1bit-llm-survey.tex` | 143 |
| entries in `references.bib` | 143 |
| cited keys with no bib entry (MISSING-BIB) | 0 |
| bib entries never cited (ORPHAN-BIB) | 0 |
| non-web bib entries with no `data/inventory.csv` row | 0 |
| inventory rows with `local_file` not present in `papers/` | 0 |
| `papers/*.pdf` not referenced by any inventory row (ORPHAN-PDF) | 0 |
| `papers/*.pdf` on disk | 140 |
| `web-*` keys -> snapshot in `papers/_web/` | 3 / 3 |
| PDFs unreadable by `pdftotext` | 0 |

140 papers + 3 web artifacts (`web-microsoftBitNet` -> `2026-09-03_microsoft-BitNet_readme.md`,
`web-falconEdge` -> `2026-09-03_falcon-edge_hf-blog.md`, `web-bitnet2b4tCard` ->
`2026-09-03_bitnet-b1.58-2B-4T_hf-card.md`) = 143.

## Title correspondence

Each PDF's first-page title was token-matched against its `references.bib` title.
~127 of 140 scored >= 67% token overlap (strong automatic match). The 13 lowest were
eyeballed against the PDF's first lines; all 13 are the paper the bib entry names.
The low automatic scores are an artifact of `pdftotext` rendering ICLR/arXiv
title-case with letter spacing ("B I BERT", "BEE XFORMER"), not a wrong file:

| key | bib title | PDF first line | ok |
|---|---|---|---|
| Ansar2024-BEExformer | BEExformer: A Fast Inferencing Binarized Transformer... | BEEXFORMER: A FAST INFERENCING BINARIZED TRANSFORMER... | yes |
| Li2024-ARBLLM | ARB-LLM: Alternating Refined Binarizations... | ARB-LLM: ALTERNATING REFINED BINARIZATIONS... (ICLR 2025) | yes |
| Qin2022-BiBERT | BiBERT: Accurate Fully Binarized BERT | BIBERT: ACCURATE FULLY BINARIZED BERT (Qin, ICLR 2022) | yes |
| Dong2024-STBLLM | STBLLM: Breaking the 1-Bit Barrier... | STBLLM: BREAKING THE 1-BIT BARRIER WITH STRUCTURED BINARY LLMS | yes |
| Anon2025-MultiBoolean | Highly Efficient and Effective LLMs with Multi-Boolean Architectures | same | yes |
| Huang2025-Tequila | Tequila: Trapping-free Ternary Quantization... | TEQUILA: TRAPPING-FREE TERNARY QUANTIZATION... | yes |
| Anon2025-CPUvsGPU | Challenging GPU Dominance: When CPUs Outperform... | same (Haolin Zhang, Jeff Huang) | yes |
| Chong2026-NanoQuant | NanoQuant: Efficient Sub-1-Bit Quantization... | same (Hyochan Chong) | yes |
| Zhang2026-EdgeRazor | EdgeRazor: A Lightweight Framework for LLMs... | same | yes |
| Wang2026-HESTIA | HESTIA: A Hessian-Guided ... QAT Framework for Extremely Low-Bit LLMs | same (Guoan Wang) | yes |
| + 3 more in the 67-89% band, all confirmed | | | yes |

## Notes (not RULE 1 issues)

- 15 citation *keys* begin `Anon...` (e.g. `Anon2025-CPUvsGPU`, real first author Zhang).
  The keys are cosmetic; the bib author field and the archived PDF are correct.
  Renaming the keys is a user-reserved task.
- `references.bib` author fields are still "Lastname and others" pending the manual
  full-author pass (also user-reserved).
