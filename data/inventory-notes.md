# inventory.csv — notes

**Status:** round-1 coding complete (2026-09-04). 100 rows = the 100 archived PDFs in `papers/`.

## What round 1 is
Each paper coded from **title + abstract + first page** on the `../survey-protocol.md` §7 scheme
(15 of the ~45 fields — the ones extractable without deep reading). Numeric benchmark/efficiency
columns (ppl, zero-shot avg, mem_GB, latency_ms, energy_J) are **not** in this file yet — they
come in round 2 (full-text reading), filled per section as the draft is written.

## Round-2 TODO (before the tables/figures are final)
1. **Normalise controlled vocabularies.** Round-1 values drifted (e.g. `QAT` vs `QAT-finetune`,
   `PTQ+distill`, `native+distill`). Collapse to the protocol's fixed sets:
   - `paradigm` -> {native-scratch, continual-QAT, QAT-finetune, PTQ, analysis, systems, survey, background}
   - `weight_repr` -> {binary, ternary, mixed-partial, n/a}
   - `components` -> {W, W+A, W+A+KV, W+A+sparsify, n/a}
2. Fill numeric result columns from full text for the ~35 papers that report standard benchmarks.
3. Assign final `evidence_score` after checking artifacts (code runs / weights load) — round-1 scores
   are provisional from venue + abstract only.
4. Fix `first_author` where round-1 used `NR`/`Anon` (~20 rows) and the `2024_Kimura_*` filename
   (actual first author: Kaiyan Zhao).
5. Confirm venue for conference papers marked `arXiv` that were later accepted.

## Round-1 tally snapshot (feeds §3 taxonomy + PRISMA figure)

Paradigm (collapsed): native-scratch ~24 · PTQ ~21 · QAT/QAT-finetune ~26 · continual-QAT 3 ·
systems ~14 · scaling/theory analysis ~8 · surveys 3 · background 4.

Weight representation (collapsed): ternary ~46 · binary ~34 · mixed-partial ~4 · n/a (systems/analysis/survey) ~16.

Modality: text-decoder 54 · systems/hardware 14 · theory 8 · embedding 3 · text-encoder 3 · surveys 3 ·
VLM/VLA/MoE 4 · TTS 1 · ASR 1 · SSM 1 · vision/small-LM 3.

Prior surveys in corpus (competitors): Gong 2024 (Neural Networks 2025) · Liu 2025 (arXiv) ·
Hao 2025 (IEEE TPAMI) — all three are broader than native-1-bit and none is systematic.
