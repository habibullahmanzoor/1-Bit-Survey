# OSF Pre-registration — Systematic survey of native 1-bit / 1.58-bit LLMs

Paste into the OSF "Preregistration" template (or "Open-Ended Registration"). Freeze date: 2026-09-04.
Canonical protocol: `../survey-protocol.md` v1.0. Companion strategy doc: `../MASTER-SURVEY-PLAN.md`.

---

## 1. Title
A Systematic Survey of Native 1-Bit / 1.58-Bit Large Language Models: Architecture, Training, and Systems Co-Design.

## 2. Authors / contributions
[Author list + ORCIDs]. Roles: screening (>=1 reviewer; 20% second-coded), extraction, reproduction study, drafting.

## 3. Research questions
- RQ1 Foundations: how is BitLinear / ternary quantisation formulated and made stable to train natively?
- RQ2 Taxonomy: how do methods partition across weight representation, training paradigm, quantised components, optimisation mechanism, and systems stack?
- RQ3 Activation frontier: how are activation outliers handled and what is the current activation-bit floor?
- RQ4 Systems: what inference speed / memory / energy do ternary kernels and accelerators deliver, on what hardware?
- RQ5 Evidence quality: which headline claims replicate when independently re-run?
- RQ6 Open problems: scaling-law behaviour / capacity ceiling; training stability past ~100B tokens; absence of ternary silicon; safety; sub-1.58-bit.

## 4. Study type
Systematic literature review (PRISMA 2020) + a small independent reproduction study of headline accuracy and efficiency claims.

## 5. Eligibility criteria (frozen)
INCLUDE iff all of:
- IC-1 primarily concerns 1-bit or 1.58-bit (ternary) language models, or a method/kernel/hardware design explicitly targeting <=1.58-bit LLMs;
- IC-2 effective weight precision <= 2 bits (native binary/ternary, or mixed/partial with a <=2-bit backbone);
- IC-3 first public version dated 2023-01-01 .. 2026-06-30;
- IC-4 empirical or theoretical contribution (not blog/opinion);
- IC-5 a freely downloadable full-text version exists AND has been archived locally.
EXCLUDE if: EC-1 vision/other-only with no LM component; EC-2 primary method > 2-bit; EC-3 superseded preprint of an included version; EC-4 no open-access full text.
Classic BNN/STE literature (2013-2022) is cited narratively as background, outside the systematic count.

## 6. Information sources
arXiv (cs.CL/LG/AI/AR), Semantic Scholar API, DBLP, ACL Anthology, OpenReview, PMLR/JMLR, Google Scholar (forward-citation only), Hugging Face Papers, official model/framework repos.

## 7. Search strategy (frozen — full strings in `search-log.md`)
Core Boolean: ("1-bit" OR "1.58-bit" OR "one-bit" OR ternary OR binariz* OR "sub-2-bit")
AND ("language model" OR LLM OR transformer OR "foundation model")
AND (BitNet OR BitLinear OR "quantization-aware training" OR "post-training quantization" OR "straight-through estimator" OR "native low-bit" OR "extreme quantization" OR "matmul-free" OR "ternary weight").
Plus 15 seed-name exact queries and backward+forward snowball on 8 seed papers, 2 iterations.
Date filter 2023-01-01 .. 2026-06-30.

## 8. Selection process
De-duplicate; title/abstract screen; full-text screen with EC code per exclusion; retrieve OA copy in the same pass (fail -> EC-4). >=1 reviewer on 100%; a random 20% is second-screened (Cohen's kappa if two reviewers, else >=14-day-gap intra-rater agreement). PRISMA flow with counts at each stage.

## 9. Data extraction
One row per included paper in `inventory.csv`, coded on: bibliographic fields; the 5 taxonomy axes (weight representation / training paradigm / components quantised / optimisation mechanism / systems stack); scale (params, tokens, base model); reported results (perplexity, zero-shot avg, MMLU/GSM8K, memory, latency, energy); artifact URLs + licence; evidence score 1-5; free-text notes. Two-pass: round 1 from title/abstract (done), round 2 fills numeric result fields from full text.

## 10. Risk-of-bias / evidence appraisal
Each included work scored 1-5 (5 = peer-reviewed + open code + open weights + independently reproduced; 1 = claim-only). All quantitative synthesis stratified by score; single-source and vendor-reported numbers flagged; where feasible re-measured in the reproduction study.

## 11. Synthesis
Structural classification -> taxonomy figure + Table 1. Narrative synthesis per section, each closing with an explicit "what is not known". Quantitative: a normalised cross-paper comparison under one eval protocol + one effective-bits accounting; a quality-vs-energy/memory Pareto frontier; a reproducibility-audit table (code runs? weights load? numbers match? licence?).

## 12. Reproduction study (pre-specified)
Arm A (accuracy, GPU): re-run a pinned `lm-evaluation-harness` commit on >=3 open checkpoints (BitNet b1.58 2B4T; a smaller 1-bit model; a size-matched FP baseline) over the 7-task zero-shot suite + WikiText2 perplexity; report signed deltas vs published numbers. Arm B (efficiency, CPU only): `bitnet.cpp` vs `llama.cpp` on one x86 machine, thread sweep {1,2,4,8}, metrics {decode tok/s, peak RSS, J/token}, 3 repeats. Minimum-tier budget ~8 GPU-hours + ~3 CPU-hours. All scripts + logs in a public repo (`repro/`), Zenodo DOI cited.

## 13. Deviations
Any change to this pre-registration after the full-text coding start date is logged in `../survey-protocol.md` §14 (Amendments) with date and rationale.

## 14. Timeline
Search + screening + extraction: weeks 1-3. Drafting + figures: weeks 4-9. Reproduction study: weeks 7-8. Internal + external review: weeks 10-12. Submission (ACM Computing Surveys, then Artificial Intelligence Review): weeks 13-14.
