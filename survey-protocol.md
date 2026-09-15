# Review Protocol — Binary and Ternary Large Language Models

**Companion to:** `MASTER-SURVEY-PLAN.md` · **Rules:** `CLAUDE.md` (R1) · **Corpus:** `papers/INDEX.md`
**Protocol version:** v1.0 (frozen 2026-09-03) · **Search executed:** 2026-09-03 to 2026-09-05

> **Scope note (2026-09-07).** The final paper is a *structured, arXiv-primary survey with an
> independent re-evaluation*, not a systematic review. It does not claim an exhaustive
> multi-database PRISMA harvest, a two-reviewer screen, or OSF pre-registration; the
> deviations from this frozen protocol are stated in manuscript Section 3.2 and Section 3.4.
> The eligibility criteria, effective-bits accounting, and evidence-score rubric below are
> the parts that remain operative. PRISMA-style counts appear in `data/` and are indicative.

**Literature cutoff:** 2026-06-30 (inclusive). Post-cutoff work goes to the living appendix.

> **This protocol was frozen before full-text coding began.** Later changes are recorded in §14 (Amendments) with date and rationale.

---

## 1. Rationale

1-bit / 1.58-bit (ternary) LLMs trained natively — `BitLinear` (2023) onward — are a distinct modeling paradigm, not a compression post-process. Two prior surveys exist: Gong et al. (*Neural Networks* 2025, arXiv 2409.16694), broad "low-bit"; and Liu et al. (arXiv 2502.19008), "binary NN for LLM". Neither is systematic (no protocol, no PRISMA), neither is scoped to the native paradigm, and both predate the 2025–2026 wave (BitNet b1.58 2B4T / a4.8 / v2, GPU kernels, BitVLA, 1-bit embedding/ASR, Falcon-Edge, Sparse-BitNet, and ~15 subsequent arXiv papers). This review fills that gap with a pre-registered protocol, an openly verifiable evidence base, and an independent reproduction of headline claims.

## 2. Objectives & research questions

**Aim:** systematically identify, classify, and synthesize the openly accessible literature on native 1-bit / 1.58-bit LLMs (architecture, training, systems), and independently reproduce its headline accuracy and efficiency claims.

- **RQ1 — Foundations.** How is `BitLinear` / ternary quantization formulated, and how is native low-bit training made stable (STE, latent weights, recipes)?
- **RQ2 — Taxonomy.** How do the methods partition across weight representation, training paradigm, quantized components, optimization mechanism, and systems stack (§7 of the plan)?
- **RQ3 — Activation frontier.** How are activation outliers handled (INT4, hybrid quant+sparsification, Hadamard/rotation), and what is the current activation-bit floor?
- **RQ4 — Systems & hardware.** What inference speed / memory / energy do ternary kernels (`I2_S`, `TL1`, `TL2`, fused, GPU) deliver, and on what hardware?
- **RQ5 — Evidence quality.** Which claims are supported by independent evidence vs single-source / vendor-reported? What replicates when we re-run it?
- **RQ6 — Open problems.** Scaling-law behavior and the capacity ceiling; training stability past ~100B tokens; absence of ternary silicon; safety/robustness; sub-1.58-bit.

## 3. Eligibility criteria

A record is **included** iff **all** IC are met and **no** EC applies.

### Inclusion (IC)
- **IC-1 — Topic.** Primarily concerns 1-bit or 1.58-bit (ternary) *language models*, or a method/kernel/hardware design whose explicit target is ≤ 1.58-bit LLMs.
- **IC-2 — Bit-width.** Effective weight precision ≤ 2 bits (native binary/ternary or mixed/partial with a ≤ 2-bit backbone). Papers whose primary method is INT3/INT4/INT8 are background only (EC-2).
- **IC-3 — Window.** First public version dated 2023-01-01 → 2026-06-30.
- **IC-4 — Substance.** Empirical or theoretical contribution (architecture, training method, analysis, system, benchmark, or application). Not a blog post, slide deck, or opinion piece.
- **IC-5 — Open access + archived (ABSOLUTE, per R1).** A freely downloadable full-text version exists (arXiv, JMLR/PMLR, ACL Anthology, OpenReview, NeurIPS/ICML/ICLR proceedings, a gold-OA journal page, or an official code/model repo for non-paper artifacts) **and has been saved to `papers/`** (or `papers/_web/` for a non-paper artifact). No local copy → **excluded**, logged in `papers/INDEX.md`, cited nowhere.

### Exclusion (EC)
- **EC-1 — Vision/other only.** Binarization of CNNs / ViT / SSM with no language-model component. (Classic BNN papers — BinaryConnect, XNOR-Net, BinaryBERT, BiBERT — are cited narratively as background, outside the systematic count; see §12.)
- **EC-2 — Bit-width out of scope.** Primary method is > 2-bit quantization; 1-bit mentioned only in passing.
- **EC-3 — Superseded/duplicate.** Earlier preprint of an included later version; keep the latest, note the version.
- **EC-4 — Not retrievable.** No open-access full text (see IC-5). Recorded separately in the PRISMA "excluded — no OA copy" count.

## 4. Information sources

1. **arXiv** — `cs.CL`, `cs.LG`, `cs.AI`, `cs.AR` (full-text + metadata).
2. **Semantic Scholar** (API) — cross-venue coverage + citation graph.
3. **DBLP** — venue/author completeness check.
4. **ACL Anthology** — *CL, ACL/EMNLP/NAACL/EACL/Findings.
5. **OpenReview** — ICLR, NeurIPS D&B, TMLR, COLM.
6. **PMLR / JMLR** — ICML, AISTATS, JMLR.
7. **Google Scholar** — forward-citation chasing only (not primary identification; capped at first 100 results/seed).
8. **Hugging Face Papers** — arXiv-indexed, catches fast-moving releases.
9. **Official repos** — `github.com/microsoft/BitNet` release log; TII Falcon-LM; vendor model cards (non-paper artifacts → `papers/_web/`).

## 5. Search strategy (FROZEN)

Executed on _[fill date]_. Exact strings recorded verbatim in `protocol/search-log.md` with per-source hit counts.

### 5.1 Core Boolean query (adapt syntax per source)

```
(  "1-bit" OR "1 bit" OR "1.58-bit" OR "1.58 bit" OR "one-bit" OR "one bit"
   OR ternary OR binariz* OR binarised OR "sub-2-bit" OR "sub-1-bit" OR "1.58 bits" )
AND
(  "language model" OR "language models" OR LLM OR LLMs OR transformer
   OR "foundation model" OR GPT OR LLaMA OR "decoder-only" )
AND
(  BitNet OR BitLinear OR "H-BitLinear" OR "quantization-aware training" OR QAT
   OR "post-training quantization" OR PTQ OR "straight-through estimator" OR STE
   OR "native low-bit" OR "extreme quantization" OR "ternary weight"
   OR "matmul-free" OR "multiplication-free" )
```

### 5.2 Seed-name exact queries (run each separately, union the results)

`"BitNet"`, `"BitNet b1.58"`, `"BitNet a4.8"`, `"BitNet v2"`, `"BitLinear"`, `"H-BitLinear"`,
`"FBI-LLM"`, `"OneBit"`, `"BiLLM"`, `"PB-LLM"`, `"bitnet.cpp"`, `"Sparse-BitNet"`,
`"ternary LLM"`, `"1.58-bit LLM"`, `"1-bit LLM"`.

### 5.3 Snowballing (8 seeds)

Backward (references) + forward (citations, via Semantic Scholar) on:
BitNet (JMLR'25), BitNet b1.58, BitNet b1.58 2B4T, BitNet a4.8, BitNet v2,
1-bit AI Infra 1.1 / bitnet.cpp, OneBit, FBI-LLM.
Two iterations, or until no new IC-passing records appear.

### 5.4 Date filter
Submitted/published 2023-01-01 … 2026-06-30. arXiv: use `submittedDate`. Keep latest version ≤ cutoff.

## 6. Selection process

1. **De-duplication** — by DOI / arXiv id / normalized title.
2. **Title + abstract screening** — against IC-1..IC-4. Liberal: "maybe" → keep for full text.
3. **Full-text screening** — against all IC + EC. Record an EC code for every exclusion.
4. **IC-5 retrieval** — attempt OA download for every full-text-included record in the same pass; on failure → EC-4, logged in `INDEX.md`.
5. **Reviewers.**
   - *Two reviewers:* independent screening at stages 2–3 on 100%; compute **Cohen's κ**; disagreements resolved by discussion, third party if needed.
   - *Solo (fallback):* single-pass screening, then **re-screen a random 20% after a ≥ 14-day gap** (intra-rater agreement); report the percentage agreement and treat solo screening as a stated limitation (§13).
6. **PRISMA flow** — counts recorded at every stage (§11).

## 7. Data extraction — `inventory.csv` coding scheme

One row per included record. Coder fills every field; `NR` = not reported, `NA` = not applicable. Ambiguous codings flagged in `notes` and reviewed.

| Field | Values / format | Notes |
|---|---|---|
| `id` | `AuthorYear-tag` (e.g. `Ma2024-b158`) | stable key |
| `local_file` | filename in `papers/` | R1 link |
| `title`, `authors`, `year` | — | `year` = first public version |
| `venue`, `oa_type` | arXiv / JMLR / NeurIPS / … ; gold / green-arxiv / proceedings | |
| `oa_url`, `code_url`, `weights_url`, `license` | URL / SPDX id / `NR` | reproducibility audit inputs |
| `include`, `exclude_reason` | Y/N ; EC-code | |
| `evidence_score` | 1–5 (§8) | |
| `reviewer1`, `reviewer2`, `disagreement`, `resolution` | initials ; Y/N ; text | omit reviewer2 if solo |
| **`weight_repr`** | `binary` / `ternary` / `mixed-partial` | taxonomy axis 1 |
| **`training_paradigm`** | `native-scratch` / `continual-QAT` / `QAT-finetune` / `PTQ` | axis 2 |
| **`components_quantized`** | `W` / `W+A` / `W+A+KV` / `+sparsify` | axis 3 |
| `activation_bits`, `kv_bits` | int / `NR` | |
| **`optimization_mechanism`** | `vanilla-STE` / `scaled-STE` / `curvature-aware` / `distillation` / `reconstruction` / `stochastic-rounding` / `other` | axis 4 |
| **`systems_layers`** | any of `algorithm` / `kernel` / `hardware` | axis 5 |
| **`modality`** | `text-decoder` / `MoE` / `VLM` / `VLA` / `embedding` / `ASR` / `other` | secondary cut |
| `params` | list, e.g. `{130M,1.3B,7B}` | |
| `train_tokens`, `base_model`, `datasets` | — | |
| `benchmarks_reported` | list | |
| `ppl_wikitext2`, `ppl_c4` | float / `NR` | |
| `zeroshot_avg` | 7-task avg (ARC-e/c, HellaSwag, WinoGrande, PIQA, OBQA, BoolQ) / `NR` | normalization target |
| `mmlu`, `gsm8k`, `humaneval` | float / `NR` | |
| `mem_gb`, `latency_ms`, `energy_j`, `throughput_tps` | float / `NR` | |
| `hardware_reported`, `kernel_reported` | text | |
| `independently_reproduced` | `Y` / `N` / `partial` / `NA` | filled from §9 of the plan |
| `notes` | free text | caveats, version, contamination flags |

## 8. Evidence appraisal

Each included record gets an **evidence score 1–5**:

| Score | Criteria |
|---|---|
| 5 | Peer-reviewed venue **and** open code **and** open weights **and** results reproduced by ≥ 1 independent party |
| 4 | Peer-reviewed **or** (open code + open weights); results used by others |
| 3 | Preprint with open code or weights; internally consistent; not yet independently checked |
| 2 | Preprint, partial artifacts, or vendor-reported numbers only |
| 1 | Claim-only, no artifacts, or single unreplicated data point |

All quantitative synthesis is **stratified by score**; any claim resting solely on score ≤ 2 is labelled as such in the prose. Vendor-reported efficiency numbers are always flagged and, where feasible, checked in the reproduction study.

## 9. Synthesis

- **Structural:** classify every record on the 5 taxonomy axes → Figure 1 (tree) + Table 1 (matrix).
- **Narrative:** per plan §4–§8, each subsection closes with an explicit "what is not known."
- **Quantitative — normalized comparison (novelty add-back):** re-tabulate reported accuracy/efficiency under one eval protocol and one effective-bits accounting; where sources are incomparable, say so rather than tabulating raw.
- **Pareto frontier:** quality vs energy/token and vs memory, combining our measurements (§9 of plan) with normalized reported points.
- **Reproducibility audit table:** per released model — code runs? weights load? numbers match? license? (near-zero compute, high value).
- **Reproduction study:** protocol in `MASTER-SURVEY-PLAN.md` §9 (Arm A accuracy on shared RTX 4080, ~8 GPU-h; Arm B efficiency on CPU, ~3 h). Scripts + logs in `repro/`.

## 10. Threats to validity / limitations

- **OA-only evidence base.** Mitigation: search covers all-source indexes (Semantic Scholar, DBLP), so records are *identified* regardless of access; the OA filter is applied at retrieval and its impact quantified — PRISMA "excluded, no OA copy: n = X" + those titles listed in Appendix; abstracts of excluded records are read and checked against every major conclusion (sensitivity check reported). Framed in §1 and Methodology as a deliberate design choice for verifiability, not an apology.
- **Preprint-heavy corpus.** Mitigation: evidence scoring + stratified synthesis + the reproduction study as our own check on headline claims.
- **Vendor-reported efficiency numbers.** Mitigation: flagged everywhere; re-measured where feasible; deltas reported honestly.
- **Fast-moving field.** Mitigation: frozen cutoff stated in the abstract; living appendix; "changes since submission" paragraph at camera-ready.
- **Solo screening (if applicable).** Mitigation: 20% delayed re-screen; stated limitation.
- **Benchmark contamination** in heavily-SFT'd small models. Mitigation: noted per-model in `inventory.csv`; discussed in §7/§10 of the paper.

## 11. PRISMA 2020 flow

**Provisional (2026-09-04)** — after scoping runs 1-2 + snowball run 3. Definitive counts await the
run-3 raw-API harvest (arXiv OAI-PMH + Semantic Scholar bulk); the numbers below will only grow at
"identified" and shift a little at the margins.

Identification and screening counts across the four search runs remain aggregate
estimates (the search log has the exact per-run figures); the Included block below is exact.

```
Identification
  Records identified — arXiv API (runs 1-4) + Semantic Scholar forward-citation + named-method web search   ~300
  Duplicates / superseded preprints removed                                                       ~40
Screening
  Records screened (title / abstract)                                                            ~260
    -> excluded, off-topic (EC-1 non-LM / not-a-topic; fuzzy-match false positives)               ~30
    -> excluded, bit-width out of scope (EC-2, >2-bit primary method)                             ~19
    -> post-cutoff > 2026-06-30 (-> living appendix, not the review)                              ~20
  Reports sought for retrieval                                                                   ~141
    -> not retrieved, no open-access copy (EC-4 / IC-5)                                              1  (PT-BitNet)
  Reports assessed for eligibility                                                                ~140
    -> excluded on delayed 20% re-screen (fails IC-1 and IC-2, W4A4 scaling-law study)              1  (Scaling Law for QAT, 2505.14302)
Included
  Primary studies included in review                                                             135
  Foundational works (2013-2022), classified in Table 1 for context, outside the count             5   (table has 140 rows)
  Non-paper artifacts (model cards / repo / blog snapshots)                                          3
```

Archived: **135 primary studies + 5 foundational works** (`papers/INDEX.md`, `data/inventory.csv`) + 3 `_web/` snapshots.
Excluded under IC-5 (no OA copy): **PT-BitNet**. Excluded on the delayed 20% re-screen (2026-09-06): **Scaling Law for QAT** (2505.14302), moved to `papers/_excluded/`.
Delayed 20% re-screen: 28-study random sample, 26/28 inclusion decisions confirmed (93% raw intra-rater agreement).
Resolved: `native-ternary-encoding` -> found (arXiv 2604.03336, NativeTernary), archived.
Data-quality note: one snowball list was fetched via a summariser and its fabricated tail was
discarded (`protocol/search-log.md`); every archived PDF was verified against its own first page.

## 12. Background sources (outside the systematic count)

Foundational BNN / STE literature (2013–2022) is cited narratively for context, not screened: Bengio et al. 2013 (STE), Courbariaux et al. 2015 (BinaryConnect), Rastegari et al. 2016 (XNOR-Net), Bai et al. 2021 (BinaryBERT), Qin et al. 2022 (BiBERT). All five are archived in `papers/` for verifiability.

## 13. Deliverables

- `protocol/` — this file, `search-log.md`, OSF record.
- `data/inventory.csv` — coded table (= Appendix B) + `models.csv` (= Appendix C).
- `repro/` — pinned `lm-evaluation-harness` commit, `bitnet.cpp` build, scripts, logs, energy traces.
- `figures/` — Fig 1 (taxonomy), 2 (PRISMA), 3 (timeline), 4 (datapaths), 5 (Pareto), 6 (accuracy-vs-scale).
- Zenodo DOI for the repo, cited in the paper.

## 14. Amendments log

| Date | Section | Change | Rationale |
|---|---|---|---|
| 2026-09-03 | — | Protocol v1.0 frozen | initial |

## 15. Immediate execution checklist

- [ ] Upload this protocol to OSF; paste DOI into header.
- [ ] Run §5 searches; save every string + hit count to `protocol/search-log.md`; set the "Search executed" date.
- [ ] De-dupe + title/abstract screen; fill PRISMA identification/screening counts.
- [ ] Full-text screen; for each include, download to `papers/` (R1) or mark EC-4.
- [ ] Seed `data/inventory.csv` from the 37 archived papers using §7 scheme.
- [ ] Two-reviewer κ (or 20% delayed re-screen if solo).
