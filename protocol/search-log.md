# Search log — 1-Bit LLM systematic review

Protocol: `../survey-protocol.md` §5 (frozen 2026-09-03).
**Status (2026-09-07):** the paper is a structured, arXiv-primary survey with an independent
re-evaluation, not a systematic review; it does not claim an exhaustive multi-database
PRISMA harvest (see `survey-protocol.md` and manuscript Section 3.2). The runs below are
the identification record for the 135 in-window primary studies now in `data/inventory.csv`.

**Search run 1:** 2026-09-03 — scoping / seed-expansion pass (this file).
**Search runs 2--4:** 2026-09-03 to 2026-09-05 — arXiv API over cs.CL/cs.LG/cs.AI/cs.AR with the
Boolean bit-width/technique query plus fifteen exact-name queries, two rounds of backward and
forward citation chasing on eight seed papers via Semantic Scholar, targeted web searches for
named methods, and monitoring of Hugging Face Papers and official release logs. One
automated citation list contained confabulated entries and was discarded; every archived
record was confirmed against its primary source.

---

## Sources queried (run 1)

| Source | Method | Notes |
|---|---|---|
| arXiv | Atom API (`export.arxiv.org/api/query`, `abs:` fields, sort by submittedDate) | 2 queries, 120 + 100 max results |
| Google/web | interactive search | 6 targeted queries for named methods |
| Semantic Scholar | Graph API | **rate-limited (HTTP 429)** on run 1 — deferred to run 2 |

## Queries executed (run 1)

**Q1 (arXiv Atom):**
`abs:"BitNet" OR abs:"1.58-bit" OR abs:"ternary language model" OR abs:"binarized LLM"`
→ ~40 entries returned (submittedDate desc); ~28 on-topic after title screen, ~12 off-topic (information-geometry, memristor physics, robot dynamics, crypto-binary-analysis).

**Q2 (arXiv Atom):**
`abs:"matmul-free" OR abs:"1-bit LLM" OR abs:"binary large language model" OR (abs:"ternary weight" AND abs:"language model")`
→ ~44 entries; ~34 on-topic after title screen.

**Q3–Q8 (web, named-method recall):**
`"MatMul-free" language model ternary` · `binary LLM ARB-LLM STBLLM BinaryMoS DB-LLM` ·
`Spectra ternary language models pretraining` · `1-bit LLM spiking neuromorphic` (via results) ·
`BitNet embeddings` (via results) · `sub-1-bit LLM quantization`.
→ recovered named works not surfaced by abs-search: Spectra/TriLM (2407.12327), ARB-LLM (2410.03129), DB-LLM (2402.11960), BinaryMoS (2406.12311), STBLLM (2408.01803), PTQ1.61 (2502.13179), Multi-Boolean (2505.22811), NanoQuant (2602.06694).

## Outcome (run 1)

- **Unique on-topic records identified:** ~78 (incl. the 37 already archived pre-search).
- **New records archived this pass (IC-1..5 pass, in-window):** 33 → now 70 PDFs in `papers/` + 3 `_web/` snapshots.
- **Post-cutoff (> 2026-06-30) → living appendix, not the review:** 5 (listed in `../data/candidates.md`).
- **Pending full-text screening (borderline: HW accelerators, SSM/spiking, robustness):** ~18.
- **Excluded — off-topic false positives from `abs:` search:** ~12 (listed in `../data/candidates.md`).
- `native-ternary-encoding`, previously EXCLUDED as "no identifiable paper", **resolved**: arXiv 2604.03336 (NativeTernary), now archived.

---

## Search run 2 — 2026-09-03 (forward-citation snowball + term expansion)

**Method:** Semantic Scholar `paper/ARXIV:2402.17764/citations` (BitNet b1.58 forward citations, ~280 returned) + 2 more arXiv Atom queries (`abs:"binarization" AND abs:"large language model"`; `abs:"extremely low-bit" OR abs:"sub-1-bit" OR abs:"ternary transformer" OR ...`).

**⚠ Data-quality caveat (must fix in run 3):** the citation list was retrieved through a summarizing fetch, not a raw API client. The first ~150 rows are genuine (specific titles, real venues, IDs verified on download). The **tail of the list (~2405.09876 downward, evenly-spaced IDs, generic titles like "Binary Deep Neural Networks", "Neural Network Quantization Techniques") is confabulated by the summarizer and was discarded.** Every PDF added below was verified by reading its first page. The **frozen PRISMA identification count must come from a raw arXiv OAI-PMH + Semantic Scholar bulk API harvest (run 3), not from a summarizer.**

**Newly archived (run 2): 30** → `papers/` now holds **100 PDFs**. Highlights the seed+run-1 set missed:
QuEST (W1A1 native training, ICML'25), ParetoQ (extreme-low-bit scaling laws, NeurIPS'25), BitNet Distillation (2510.13998), "Low-Bit Quantization Favors Undertrained LLMs" (2411.17691 — the undertraining critique), Scaling Laws for Precision (2411.04330), STE-with-zeroth-order (NeurIPS'25), Low-Precision Training of LLMs survey (TPAMI'25 — positioning), ternary-PTQ line (PTQTP, PT²-LLM, TernaryLM), MoTE (ternary MoE + multimodal), BitTTS / one-bit ASR / VLM ternarization / ternary embeddings (§8), GenBFA (bit-flip attacks, §10), ternary FPGA/CPU accelerators (TerEffic, TeLLMe, T-SAR, Litespark, LLMPi).

**Identified but NOT retrieved (real-looking, deferred to run-3 screening):** ~40, incl.
HARP (2605.29843), Influence-Inspired Spectral Rotations (2605.25203), pQuant (2602.22592), LC-QAT (2606.10531), "Extreme Low-Bit Inference in Reasoning Models" (2606.02011), BWLA (2605.00422), MoBiE (2604.06798), "Fitting Is Not Enough: Smoothness in Extremely Quantized LLMs" (2605.08894), iFairy/Fairy2i complex-LLM line (2508.05571 / 2512.02901), "1-Bit Wonder" (2602.15563), Squeeze10-LLM (2507.18073), ICQuant (2505.00850), TeTRA-VPR (2503.02511), "Investigating 1-bit quantization in top tagging" (2508.07431), TZ-LLM (2511.13717), Bi-Mamba-adjacent Ternary Mamba (2606.18114), and a large ternary-accelerator cluster (RSR-core, Platinum, Vec-LUT, TOM, TeLLMe v2, TerEffic-adjacent, HoloLUT, TeLLMe, Omni-LUT, SingularBit, T-SAR — several already grabbed).

**Post-cutoff (> 2026-06-30), → living appendix:** QTEA (2609.00224), ExTernD (2607.13511), "A Target-Centric Survey of QAT" (2608.29667), BiSCo-LLM (2607.08643), GSRQ (2607.01065), "Cross-Layer Error Compensation..." (2607.14630), + run-1's 5.

---

## Search run 3 — 2026-09-04 (term-space expansion + deferred screening)

**Method:** 4 more arXiv Atom queries (`1.58-bit`/`BitLinear`/`ternary LLM`; `QAT`+`LLM`+(1-bit/ternary/binary);
`binarization`+`LLM`; `extremely low-bit`/`sub-1-bit`/`W1A1`/`ternary transformer`/`1-bit quantization`).
Result: heavy overlap with runs 1-2 → **identification is saturating**.

**Screened the ~40 deferred + run-3 hits; archived 26** → `papers/` now holds **126 PDFs**.
New this pass: HARP, influence-Walsh rotations, pQuant, LC-QAT (ICML'26), extreme-lowbit-reasoning,
BWLA (first W1A6 PTQ), "Fitting Is Not Enough" (smoothness), iFairy + Fairy2i (complex {±1,±i}),
"1-Bit Wonder" (K-means QAT), ICQuant (COLM'25), TZ-LLM (EuroSys'26), Platinum/Vec-LUT/TOM/TeLLMe-v2/PIM-AI (accelerators),
"Resource-Efficient LMs" review, BitMar (multimodal), R2Q, EdgeRazor, RSR-core, TeTRA-VPR, Ternary-Mamba, TernaryCLIP, extra-RMSNorm-1.58.

**Excluded this pass:** Squeeze10-LLM, MiniCPM4, 1-bit-top-tagging (EC-2 / EC-1); MoBiE 2604.06798 (retrieval failed → EC-4, revisit).
**Bad ID caught:** `2408.15962` returned an unrelated math-physics paper — "TermNet" was a confabulated entry from the run-2 summariser tail; file deleted, not counted.
**Post-cutoff added to living appendix:** unified-LUT-signed-digit-KV (2608.03229), QTEA, ExTernD, Target-Centric QAT survey, BiSCo-LLM, GSRQ.

**Provisional PRISMA counts frozen into `../survey-protocol.md` §11** (definitive counts still need a raw OAI-PMH + Semantic-Scholar-bulk pass — flagged there).

---

## Search run 4 — 2026-09-05 (raw arXiv API re-harvest)

**Method:** direct HTTP calls to `export.arxiv.org/api/query` (Atom XML, no summarizer in the
loop) — the core Boolean query from `../survey-protocol.md` §5.1 plus all fifteen seed-name
queries from §5.2, each restricted to `cat:(cs.CL OR cs.LG OR cs.AI OR cs.AR)` and
`submittedDate:[202301010000 TO 202606302359]`. Raw XML responses archived in
`run4_raw/*.xml`; the deduplicated id list is `run4_raw/union_ids.txt`.

**Result: 109 unique arXiv identifiers.** Cross-referenced by exact arXiv id against every
`eprint`/`note` field in `../references.bib`: 69 were already cited somewhere in the
corpus (found by runs 1-3 via other routes); 40 were new and went to full-text screening
via their abstracts (`run4_raw/new_candidates_full.xml`).

**Screened all 40; archived 15** → `papers/` now holds **141 PDFs**. New this pass:
Binary and Ternary NLG (Liu2023, pre-dates BitNet), T-MAC (CPU LUT kernel), CRVQ, OAC,
LieQ, SAGE-PTQ (PTQ line), Co-Designing Binarized Transformer + BAT accelerator (a fifth
algorithm+kernel+hardware co-design), ReTern (fault-tolerant ternary CiM), 2-bit CPU/GPU
microkernels (Georganas), DeltaLLM (temporal-sparsity attention, composes with BitNet
like Q-Sparse already in corpus), PD-Swap and VitaLLM (FPGA/silicon ternary
accelerators), the LUT-accelerator design-space-exploration framework (Geens), BitRL
(1-bit RL agents), BitTP (1.58-bit trajectory prediction).

**Excluded this pass: 25.** Sixteen off-topic (EC-1) — primary contribution outside
language modeling even where a 1-bit/1.58-bit LLM appeared as an incidental example:
error-correcting-code transformers, HEP classification (BitHEP), CNN compression (PROM),
spiking-neuromorphic associative memory (Word2Spike) and spiking LLMs (SpikeLLM, a
temporal/spike-coding paradigm rather than weight quantization), secure multiparty
computation (ENSI), differential-privacy fine-tuning (DP-Adam-AC), general SSM hardware
(IMSSA), general MoE architecture (MH-MoE), general ternary linear-algebra
parameterization (Ternary SVD), an autonomous-research multi-agent system (MAGNET),
memristor device physics (Multi-Level Resistive Synapses), an empirical PTQ bit-width
sweep not primarily 1-bit-focused (openPangu on Ascend NPUs), and one unrelated use of
"bitnet" (binary Bayesian networks) in an information-geometry paper (Ricci curvature
quantization). Seven excluded under IC-2 for spanning a bit-width range rather than
committing to two bits or fewer (SPARQLe at 4-bit weights, LUQ, ADiP, D-Legion,
SlideSparse, the curiosity-driven quantized MoE, and the ultra-low-precision
multiplication-free training paper). One duplicate: VitaLLM v2 (2605.00320) overlaps the
same TINT-Core/BoothFlex-Core silicon project as the earlier VitaLLM (2604.27396,
retained). One re-confirmed exclusion for consistency with run 3: Squeeze10-LLM
(2507.18073), still EC-2.

**Deferred pool from run 3 (~20 borderline hardware/SSM/spiking records): resolved.**
None of the specific titles named there (HARP, pQuant, LC-QAT, etc.) were still
outstanding — all had already been archived in run 3 itself; the checklist below was
stale.

**Not attempted this pass (genuinely still open):**
- [ ] Semantic Scholar bulk API (paginated JSON, api-key) — would sharpen the
      identification count further and catch non-arXiv venues, but is not expected to
      change conclusions given how saturated runs 1-3 + run 4 already are.
- [ ] ACL Anthology + OpenReview + PMLR dumps.
- [ ] Retry MoBiE (2604.06798) and any venue-only accelerator papers (HoloLUT, Omni-LUT,
      SingularBit, BNRV) not already resolved above.
