# Master Plan — A Systematic Survey of Native 1‑Bit Large Language Models

**Status:** supersedes `1-Bit-LLMs-Survey-Plan.md`, `1bit-llm-survey-plan.md`, and `Qwen_markdown_20260903_xkgkfcjej.md` (kept for reference).
**Prepared:** 2026‑09‑03
**Goal:** publish in a journal with 2024 JCR impact factor ≥ 10, using an evidence base of open‑access sources only.
**Literature cutoff:** 30 June 2026 (frozen); living appendix in a public repo for post‑cutoff work.

---

## Working rules (non‑negotiable)

- **R1 — Archive every referenced paper, or don't cite it.** Any paper cited or referred to
  anywhere in this project MUST be downloaded (PDF, from its open‑access source) into `papers/`
  in the same turn the reference is added. Filename: `<year>_<firstAuthor>_<slug>.pdf`.
  Non‑paper references (HF model cards, GitHub repos, release notes) get a dated snapshot in
  `papers/_web/`. `inventory.csv` carries a `local_file` column.
  **The gate is absolute: no local copy → excluded from the survey (IC‑5), not "revisit later."**
  Excluded works are logged in `papers/INDEX.md` and must not appear in references, tables, or
  prose. See `CLAUDE.md`. **Never skip this.**

---

## 0. TL;DR — the strategy in one page

1. **Do not write "another low‑bit quantization survey."** Two already exist (one peer‑reviewed in *Neural Networks* 2025, one on arXiv/OpenReview). We win by being the **first systematic (PRISMA), reproducible, deployment‑centered survey scoped tightly to the *native* 1‑bit / 1.58‑bit training paradigm**, covering the 2025–2026 wave (BitNet b1.58 2B4T, a4.8, v2, GPU kernels, BitVLA, 1‑bit embedding/ASR, Falcon‑E) that both competitors predate.
2. **Add an empirical contribution.** Re‑run `lm-evaluation-harness` on ≥3 open 1‑bit checkpoints (GPU, ~8 h on a shared RTX 4080) + `bitnet.cpp` latency/energy microbenchmarks (CPU only, ~3 h). A "survey + reproduction study" clears a 10+ IF bar that a pure descriptive review does not.
3. **Lead target: ACM Computing Surveys** (2024 JCR IF 23.8, ACM Open covers most institutions). **Co‑primary / fastest path: Artificial Intelligence Review** (2024 IF ≈ 19.6, fully gold OA since Jan 2024, APC ≈ £2,490). Moonshots with pre‑submission inquiry: *IEEE COMST* (edge/6G framing) and *Nature Machine Intelligence* (Review Article).
4. **Turn the OA‑only constraint into a selling point:** "an openly verifiable, fully reproducible evidence base" — every cited artifact is on arXiv / JMLR / ACL Anthology / Hugging Face / GitHub. State it in the methodology as a deliberate inclusion criterion, not an apology.
5. **Ship an artifact repo** (taxonomy data, benchmark scripts, model inventory CSV, PRISMA records). Reproducibility is a stated review criterion at NMI and a differentiator everywhere.

---

## 1. Competitive landscape — what already exists and where the gap is

| Work | Venue / status | Scope | Cutoff (approx.) | Why it does **not** close our gap |
|---|---|---|---|---|
| Gong et al., *A Survey of Low‑bit LLMs: Basics, Systems, and Algorithms* | **Neural Networks (Elsevier) 2025**, vol. 192, art. 107856 · arXiv 2409.16694 | All low‑bit (INT8/4/2, FP4, binary, ternary); systems + algorithms | mid‑2024 | Breadth over depth: 1‑bit is one slice; no PRISMA; predates BitNet 2B4T, a4.8, v2, GPU kernels, BitVLA; no independent reproduction |
| Liu et al., *Binary Neural Networks for LLM: A Survey* | arXiv 2502.19008 (Feb 2025) · OpenReview `tDoRelofr7` (not in a ≥10 IF venue) | Binarization of LLMs (PTQ/QAT/native) | late 2024 | Closest competitor, but: "binary" framing (misses ternary‑as‑central); descriptive taxonomy; no systematic protocol; no systems/hardware depth; no empirical component; predates the 2025–2026 wave |
| Hao et al., *Low‑Precision Training of LLMs: Methods, Challenges, and Opportunities* | **IEEE TPAMI 2025** · arXiv 2505.01043 | Low‑precision *training* (FP8/INT8/FP4… incl. 1‑bit) | early 2025 | Training‑only lens across all precisions; 1‑bit is a subsection; no systematic protocol; no native‑1‑bit taxonomy; no inference/hardware systems treatment; no reproduction. Highest‑IF competitor — must differentiate explicitly. |
| IJFMR short review (Dec 2024) | Low‑tier journal, ~4 pp. | 1‑bit LLMs, informal | 2024 | Not systematic, not comprehensive, negligible impact |
| General "efficient LLM" / "model compression for LLM" surveys | Various (2023–2025) | Pruning + distillation + quantization + KV cache | varies | 1‑bit gets a paragraph, not a treatment |

**The unoccupied niche (our contribution):**

> The first **systematic, PRISMA‑compliant survey dedicated to the native 1‑bit / 1.58‑bit LLM paradigm** — from `BitLinear` (2023) to the 2026 deployment ecosystem — that (a) unifies architecture, training, and systems under one taxonomy, (b) is built on an **openly verifiable evidence base**, and (c) contributes an **independent empirical reproduction** of headline efficiency and accuracy claims.

No existing survey is scoped to native‑1‑bit, systematic, *and* current to 2026. That is defensible novelty for a top‑tier reviewer.

---

## 2. Framing — pick the angle per journal family

The same core content, reframed in the introduction and abstract:

| Framing | Thesis sentence | Best for |
|---|---|---|
| **A. Paradigm survey** (default) | "Native 1‑bit training is a distinct modeling paradigm — not a compression trick — and this survey charts its architecture, training theory, and systems stack." | ACM CSUR, AI Review, TACL |
| **B. Edge‑deployment / green‑AI survey** | "1‑bit LLMs move the memory‑bandwidth wall and make GPT‑class inference feasible on CPUs and edge SoCs; here is the algorithm–kernel–hardware co‑design that gets us there." | IEEE COMST (add 6G/IoT/on‑device section), Nature MI (carbon/energy angle) |
| **C. Quantization‑theory survey** | "What breaks at 1 bit and why: STE pathologies, activation outliers, scaling‑law behavior, and the capacity ceiling." | TPAMI (with a vision extension), ML journals |

Recommendation: **write to Framing A**, keep a strong §on systems so Framing B is a 2‑week pivot if we redirect to COMST.

---

## 3. Target journals — ranked, with a submission ladder

2024 JCR impact factors (released mid‑2025; treat as ±volatile). "OA" = whether the *evidence base* constraint and the *publication* can both be satisfied cheaply.

| Rank | Journal | 2024 IF | OA route & cost | Fit | Verdict |
|---|---|---|---|---|---|
| **1** | **ACM Computing Surveys (CSUR)** | **23.8** | ACM Open — APC waived at most subscribing institutions; arXiv preprint allowed | Charter *is* classification + trend synthesis; ~35 pp incl. refs; abstract ≤ 100 words | **Primary.** Best prestige‑per‑fit. |
| **2** | **Artificial Intelligence Review** (Springer) | **≈ 19.6** | **Fully gold OA** since Jan 2024; APC ≈ £2,490 / $3,390 (institutional deals common) | Survey‑native journal; no hard page cap; fast‑ish | **Co‑primary / fastest.** Submit here if we want a decision in months, or as the immediate fallback from CSUR. |
| 3 | **IEEE Communications Surveys & Tutorials** | **≈ 53** | Hybrid; green OA via arXiv | Only with Framing B + a substantive edge/6G/on‑device deployment section | **Moonshot.** Pre‑submission scope query to EiC first. Highest ceiling, real reframing cost. |
| 4 | **Nature Machine Intelligence** | ≈ 18–21 (JCR 2024) | Hybrid; APC ≈ €9,500 | Review Article; needs energy/societal narrative + flawless reproducibility | **Moonshot.** Presubmission inquiry with a 1‑page outline. Long odds, huge payoff. |
| 5 | **TACL** (ACL / MIT Press) | ≈ 11.7 | Fully gold OA, no APC | **Hard 10‑page limit** → forces a *narrow* "survey + insight" paper, not a comprehensive one. No special survey category; bar = "an expert learns something new." | **Only** if we accept a tightly scoped variant (e.g., "Training theory of 1‑bit LLMs"). Keep as a Plan C or a spin‑off paper. |
| 6 | **AI Open** (KeAi/Elsevier) | ~10–18 (source‑dependent, volatile) | Fully OA, no/low APC | Explicitly invites reviews | **Backup** if 1–2 reject. |
| — | Neural Networks (7–8), Neurocomputing (5.5), Expert Systems w/ Apps (7.5), Machine Learning/Springer (4.2), ACM TIST (7–8) | < 10 | — | Below threshold — excluded. |
| — | *npj Artificial Intelligence* (Nature, new) | no IF yet | Fully gold OA | Nature brand, but unrated | Watch; not a target until it has an IF. |

**Submission ladder (do not submit in parallel except where allowed):**

1. Pre‑submission inquiry to **NMI** and **IEEE COMST** (1‑page outline) while drafting — costs nothing, may fast‑track.
2. Submit to **ACM CSUR**.
3. On reject → **Artificial Intelligence Review** (minimal reformatting; gold OA guaranteed).
4. On reject → **AI Open** or a scoped **TACL** spin‑off.
5. Keep the **arXiv preprint updated** at every stage (all target journals permit it).

---

## 4. The open‑access constraint, handled as methodology

Two distinct requirements, both satisfied:

- **Evidence base = OA only.** Inclusion criterion IC‑5 (see §6): a source is eligible only if a freely accessible version exists on arXiv, JMLR, ACL Anthology, OpenReview, PMLR, a Nature/Springer/Elsevier gold‑OA page, an official GitHub repo, or a Hugging Face model/dataset card. Closed IEEE Xplore / Elsevier / Springer articles are cited **only** when a green‑OA preprint exists (cite the preprint). This is stated up front as a deliberate design choice for **verifiability and reproducibility**, and a `PRISMA`‑style note records how many records were excluded for lack of an OA version.
- **Publication = OA.** CSUR (ACM Open), AI Review (gold), TACL (gold), AI Open (gold) all yield an openly readable paper. Budget line item: up to ~£3–4k APC for AI Review if institutional coverage does not apply; £0 expected for CSUR/TACL.

Reviewer‑facing framing: *"Every technical claim in this survey can be re‑checked by any reader without a paywall, and every efficiency number we report we also reproduced."* That is a strength, not a limitation — say so in §1 and §Methodology.

---

## 5. Title options

Descriptive (journal): 
- **"Native 1‑Bit Large Language Models: A Systematic Survey of Architecture, Training, and Systems Co‑Design"**
- "The 1.58‑Bit Paradigm: A Systematic and Reproducible Survey of 1‑Bit Large Language Models"

Higher‑visibility (arXiv/talks): 
- "From BitLinear to the Edge: A Systematic Survey of 1‑Bit LLMs"
- "One Bit, Full Scale: A Survey of Native 1‑Bit Large Language Models"

Recommendation: title = option 1; arXiv abstract can lead with the "BitLinear to the Edge" phrasing.

---

## 6. Survey methodology (the part that earns the ≥10 IF)

> **The full frozen protocol is `survey-protocol.md` (v1.0, frozen 2026-09-03).** This section is the summary; the protocol is the operative document and the thing to pre-register.

### 6.1 Protocol
- **Pre‑register** the protocol (OSF, free) before full‑text screening. Freeze search strings and inclusion criteria.
- Report with a **PRISMA 2020 flow diagram**: Identification → Screening → Eligibility → Included, with counts and exclusion reasons.

### 6.2 Databases & sources
arXiv (`cs.CL`, `cs.LG`, `cs.AI`, `cs.AR`), Semantic Scholar API, ACL Anthology, OpenReview, PMLR/JMLR, DBLP, Google Scholar (forward citations), Hugging Face Papers, and the `microsoft/BitNet` + related GitHub release logs.

### 6.3 Search strings (freeze these)
```
("1-bit" OR "1.58-bit" OR "one-bit" OR ternary OR binariz*) 
AND ("large language model" OR LLM OR transformer)
AND (BitNet OR BitLinear OR "quantization-aware training" OR "native low-bit"
     OR "straight-through estimator" OR "post-training quantization")
```
Plus targeted seed queries: `BitNet`, `BitLinear`, `H-BitLinear`, `1.58 bit`, `ternary LLM`, `1-bit inference kernel`.

### 6.4 Inclusion criteria (IC) / exclusion criteria (EC)
- **IC‑1** Concerns 1‑bit or 1.58‑bit (ternary) *language models* or their training/inference/hardware.
- **IC‑2** Weights ≤ 2 bits effective (native binary/ternary), OR a method whose explicit target is ≤ 1.58‑bit LLMs.
- **IC‑3** 2023‑01 → 2026‑06.
- **IC‑4** Empirical or theoretical contribution (not a blog/opinion).
- **IC‑5** An open‑access version exists (see §4).
- **EC‑1** Vision‑only / CNN binarization with no LLM component (cited only as background).
- **EC‑2** > 2‑bit quantization as the primary method (INT4/INT8 papers → background only).
- **EC‑3** Duplicate/superseded preprint versions (keep latest).

### 6.5 Snowballing
Backward + forward citation chasing on **8 seed papers**: BitNet (JMLR'25), BitNet b1.58, BitNet b1.58 2B4T, BitNet a4.8, BitNet v2, bitnet.cpp / 1‑bit AI Infra 1.1, OneBit, FBI‑LLM.

### 6.6 Data extraction / coding scheme (one row per paper → `inventory.csv`)
`id, title, year, venue, OA_source, paradigm{native|QAT|PTQ|hybrid}, weight_repr{binary|ternary|mixed}, activation_bits, kv_bits, components_quantized, params, train_tokens, base_model, datasets, benchmarks_reported, ppl_wikitext2, zeroshot_avg, mem_GB, latency_ms, energy_J, hardware, kernel, code_url, weights_url, license, evidence_score{1-5}`

### 6.7 Rigor add‑ons
- Two coders on a 20 % sample; report **Cohen's κ**; resolve disagreements by discussion.
- **Evidence score (1–5)** per source; stratify all synthesis by score; flag single‑source claims.
- Explicit **threats‑to‑validity** subsection (publication bias toward positive efficiency results; vendor‑reported numbers; benchmark contamination).

---

## 7. Taxonomy (the mandatory figure + the organizing spine)

Five orthogonal axes. Figure 1 = a faceted tree; Table = every surveyed model classified on all five.

1. **Weight representation:** true binary {−1,+1} · ternary {−1,0,+1} (1.58‑bit) · mixed/partial (salient columns in higher precision).
2. **Training paradigm:** native from‑scratch · continual QAT (16‑bit → 1.58‑bit transition) · QAT fine‑tune · post‑training quantization (no gradient).
3. **What is quantized:** weights only · weights + activations (W1.58A8 → A4) · + KV cache (3‑bit) · + attention sparsification.
4. **Optimization mechanism:** vanilla STE · scaled/clipped STE · curvature‑aware (CAGE) · distillation‑driven (autoregressive / three‑stage) · reconstruction / output‑alignment · stochastic rounding.
5. **Systems stack:** algorithm (recipe) · kernel (`I2_S`, `TL1`, `TL2`, fused ternary, GPU) · hardware target (x86 · ARM · GPU · NPU · custom ASIC).

Secondary cut for §Applications: **modality/use** — decoder LLM · MoE‑1‑bit · vision‑language / VLA · embedding models · ASR · agentic.

---

## 8. Full paper outline (target 28–35 pp; ~130–160 refs)

Page budgets assume the CSUR format; compress §6/§8 for a COMST/AI Review variant.

### §1 Introduction (3 pp)
- 1.1 The inference cost wall: memory bandwidth, energy, carbon, edge infeasibility at FP16.
- 1.2 Why 1‑bit is qualitatively different: MAC → add/sub; the ternary information‑theoretic argument (log₂3 ≈ 1.58).
- 1.3 Why now / why a survey: the 2023→2026 acceleration; two prior surveys and what they miss (§1 states the gap explicitly).
- 1.4 Contributions (enumerate the 5 below).
- 1.5 Scope, non‑goals, and the open‑access evidence principle.
- 1.6 Survey methodology summary + PRISMA figure pointer.

### §2 Background & preliminaries (4 pp)
- 2.1 Number formats: FP32/16, BF16, INT8/4/2 → binary/ternary; effective bits‑per‑weight.
- 2.2 Classic BNN lineage: BinaryConnect, XNOR‑Net, BinaryBERT, BiBERT — what transferred and what didn't.
- 2.3 The straight‑through estimator: definition, bias, known pathologies.
- 2.4 Transformer‑specific obstacles: activation outlier channels, LayerNorm placement, attention logits.
- 2.5 Metrics: perplexity, zero‑shot suites, MMLU/GSM8K/HumanEval, latency (TPOT/TTFT), energy (J/token), memory, throughput. Define how we normalize cross‑paper comparisons.

### §3 A taxonomy of native 1‑bit LLMs (3 pp)
- The five axes (§7), Figure 1, and the classification table skeleton.

### §4 Architecture (5 pp)
- 4.1 `BitLinear`: LayerNorm → abs‑mean weight quantization → activation quantization; drop‑in for `nn.Linear`.
- 4.2 Ternary vs binary in practice: the b1.58 change and its accuracy effect.
- 4.3 Activation quantization: INT8 → INT4; BitNet a4.8 hybrid quant+sparsification (55 % active params), ReLU²‑GLU.
- 4.4 Outlier suppression: BitNet v2 `H‑BitLinear` online Hadamard transform; rotation‑based alternatives.
- 4.5 KV‑cache at 3‑bit; long‑context behavior.
- 4.6 Beyond dense decoders: MoE‑1‑bit, sparsity–quantization coupling (1.25‑bit fine‑grained sparsification), sub‑1.58‑bit encodings.
- Table: architecture components × models.

### §5 Training methodology & theory (5 pp)
- 5.1 The native training loop; latent ("shadow") FP weights + dual‑precision optimizer state.
- 5.2 Recipes: two‑stage LR/weight‑decay, data schedules, `RedPajama`/4T‑token pipelines; SFT + DPO on ternary weights.
- 5.3 STE and beyond: scaled/clipped STE, curvature‑aware estimation (CAGE), stochastic rounding.
- 5.4 Distillation routes: FBI‑LLM autoregressive distillation, three‑stage binarization, BitDistiller‑style self‑distillation.
- 5.5 Continual / conversion training: when to switch 16‑bit → 1.58‑bit; PTQ‑then‑heal; output‑alignment PTQ.
- 5.6 Scaling laws at 1 bit: parity crossover (~3B) claims and the "undertrained‑model advantage" critique ("when are 1.58 bits enough?"); the capacity‑ceiling question.
- 5.7 Data efficiency: token budget vs full precision.

### §6 Inference systems & hardware (4 pp)
- 6.1 `bitnet.cpp`: `I2_S`, `TL1`, `TL2` kernels; lossless CPU inference; the 1‑bit AI Infra design.
- 6.2 CPU results: x86 2.37–6.17×, ARM 1.37–5.07×; 100B‑param model at reading speed on a single CPU; Jan‑2026 parallel‑kernel speedups.
- 6.3 GPU 1‑bit kernels (May 2025 onward); fused ternary matmul‑free designs.
- 6.4 NPU / custom accelerators / ASIC sketches; an ISA for add/sub‑only matmul.
- 6.5 `matmul`‑free LLMs and the boundary with 1‑bit.
- Table: latency / energy / memory across model sizes and hardware (partly our own measurements — §9).

### §7 Performance & benchmarking (3 pp)
- 7.1 Perplexity vs FP baselines across scales.
- 7.2 Downstream: ARC‑e/c, HellaSwag, WinoGrande, PIQA, OBQA, BoolQ; MMLU, GSM8K, HumanEval+ for the 2B4T generation.
- 7.3 Reasoning / CoT at 1‑bit; instruction following after SFT+DPO.
- 7.4 **Master comparison table** (~15–20 models × ~10 metrics) — the citation magnet.
- 7.5 Reproducibility caveats: vendor‑reported vs independently measured (leads into §9).

### §8 Applications & extensions (3 pp)
- On‑device / mobile / embedded; 1‑bit embedding models (0.6B / 270M); 1‑bit ASR; vision‑language & VLA (BitVLA) for robotics; retrieval/recommenders; agentic/tool use; carbon accounting.
- Non‑Microsoft native 1‑bit efforts (e.g., Falcon‑E / Falcon‑Edge 1.58‑bit) — the field is broader than one lab.

### §9 Independent reproduction study (3 pp) — our empirical contribution

**Principle:** this study *verifies published claims*; it does not extend the method. **Out of scope:** any training, pre‑training reproduction, or BitNet‑internal ablation — that is a separate paper.

**Hardware / framework split (deliberate):**
- **Arm A (accuracy) → GPU.** `lm-evaluation-harness` on an **RTX 4080 (16 GB)**, shared with other work: cap `--batch_size` so VRAM stays ≤ 5–6 GB (models are 1–2.4 B params; ~10 GB stays free), run as evening/overnight jobs.
- **Arm B (efficiency) → CPU only.** `bitnet.cpp` is a CPU ternary‑kernel framework — this is the whole "no‑GPU inference" claim. Arm B uses **zero** GPU budget.

#### 9.1 Models

| Role | Minimum tier | Comfortable tier (NMI / COMST) |
|---|---|---|
| Flagship native 1‑bit | BitNet b1.58 2B4T (open weights, HF) | + one more family: Falcon‑E 1.58‑bit (~1 B) |
| Smaller 1‑bit scale point | BitNet b1.58 ~700 M **or** Falcon‑E 1 B | + a second scale point |
| Full‑precision baseline | Qwen2.5‑1.5B **or** Llama‑3.2‑1B (BF16), size‑matched | same |
| **Model count** | **3** | **4–5** |

#### 9.2 Arm A — accuracy reproduction (GPU)

Tasks: 7‑task zero‑shot suite (ARC‑e, ARC‑c, HellaSwag, WinoGrande, PIQA, OpenBookQA, BoolQ) + WikiText2 perplexity, at the BitNet papers' exact protocol. MMLU (5‑shot) and GSM8K (8‑shot, generative) **only on the instruct checkpoints**. Pinned `lm-evaluation-harness` commit; determinism confirmed by a repeat run; 3 seeds on generative tasks in the comfortable tier only.

| Per model, RTX 4080, ~40–50 % shared | Time |
|---|---|
| 7‑task zero‑shot suite | 30–60 min |
| WikiText2 perplexity | 2–5 min |
| MMLU 5‑shot (instruct only) | 30–90 min |
| GSM8K 8‑shot generative (instruct only) | 30–75 min |

| Tier | Scope | Pure compute | + iteration tax¹ | **GPU‑hours** | Wall‑clock (shared) |
|---|---|---|---|---|---|
| **Minimum** | 3 models × (7‑task + PPL) | ~2–3 h | ~4–5 h | **~7–8** | **~3 evening/overnight sessions** |
| **Comfortable** | 5 models zero‑shot; MMLU+GSM8K on 2 instruct models; 3 seeds on generative | ~12–16 h | ~8–10 h | **~22–28** | ~1.5–2 weeks of overnight runs |

¹ Kernel install, tokenizer, prompt formatting, and harness task configs always cost several hours of re‑runs and sanity checks.

#### 9.3 Arm B — efficiency reproduction (CPU only, no GPU budget)

`bitnet.cpp` (ternary kernels) vs `llama.cpp` (FP16 / Q8) baseline.

| Axis | Minimum | Comfortable |
|---|---|---|
| Model pairs | 1‑bit model + size‑matched FP counterpart | + a second pair |
| Machines | 1 × x86 (the dev box CPU) | + 1 × ARM SBC (Raspberry‑Pi‑class — the "runs on a Pi" figure) |
| Thread sweep | {1, 2, 4, 8} | + sequence length {128, 512, 2048} for prefill |
| Metrics | decode tok/s, peak RSS, J/token (RAPL / wall meter) | + TTFT |
| Repeats | 3 | 5 |

~16–24 short configs × repeats; each run seconds‑to‑minutes → **~2–4 h CPU wall‑clock total**.

#### 9.4 Analysis & reporting
- Our numbers next to published ones, with signed deltas; flag any > 1–2 pt accuracy gap or > 15 % efficiency gap.
- §9.4 narrative: **what replicated cleanly, what didn't, and why** (thread counts, kernel selection `I2_S`/`TL1`/`TL2`, tokenizer, chat template, prefill vs decode).
- Feeds **Fig 5** (Pareto: quality vs energy/token), **Fig 6** (accuracy retention vs scale), **Tab 4** (master benchmark), **Tab 5** (systems).
- Threats to validity: vendor‑reported baselines, benchmark contamination in heavily‑SFT'd small models, single‑machine efficiency numbers.

#### 9.5 Artifact
Pinned harness commit, `bitnet.cpp` build notes, all run scripts, raw logs, and energy traces in `repro/` of the artifact repo; Zenodo DOI cited in the paper.

**Total compute for the submission:** ~**8 GPU‑hours** (Arm A, 3 nights) + ~**3 CPU‑hours** (Arm B). Comfortable tier only if the target shifts to Nature MI / IEEE COMST.

### §10 Open problems & research agenda (3 pp) — must be sharp and opinionated
- Training stability and loss spikes past ~100B tokens.
- The capacity ceiling: at what scale/task does native 1‑bit provably lose to FP? Is the crossover a scaling‑law artifact of undertraining?
- Activation precision is the real frontier — is A4 the floor, or does rotation+sparsification reach A2?
- Theory of STE: convergence guarantees, curvature‑aware estimators, links to noisy‑gradient analysis.
- Hardware co‑design: no shipping silicon exploits ternary; what would an add/sub matmul unit and memory layout look like?
- Standard benchmark + contamination controls specific to 1‑bit (small models, heavy SFT).
- Safety/robustness: are 1‑bit models more or less adversarially fragile? Watermarking/backdoor surface.
- Sub‑1.58‑bit: spiking + LLM, learned ternary codes, product/vector quantization at the storage layer.

### §11 Conclusion (1 pp)

### Appendices
- A. PRISMA records + full search logs.
- B. Complete reviewed‑paper table with all coded fields.
- C. Model release inventory (name, lab, params, tokens, license, weights URL, kernel support).
- D. Reproduction study: hardware, configs, raw logs, what cannot be reproduced and why.

---

## 9. Figures & tables (make these beautiful — they drive citations)

| # | Asset | Type | Notes |
|---|---|---|---|
| Fig 1 | Taxonomy tree (5 axes) | vector | The signature figure; every model tagged |
| Fig 2 | PRISMA 2020 flow | vector | Required for "systematic" |
| Fig 3 | Timeline 2023→2026 | vector | Models + kernels + downstream, swimlanes by lab |
| Fig 4 | `BitLinear` vs `H‑BitLinear` vs a4.8 datapath | schematic | Redrawn consistently from OA papers |
| Fig 5 | Pareto frontier: quality vs energy/token (and vs memory) | scatter | Uses our §9 measurements + reported points; the "tweetable" figure |
| Fig 6 | Accuracy retention vs scale | line | Parity‑crossover visualization; overlay the undertraining critique |
| Tab 1 | Taxonomy classification (models × 5 axes) | — | |
| Tab 2 | Architecture components × models | — | |
| Tab 3 | Training recipes × models | — | |
| Tab 4 | Master benchmark table (~20 × ~10) | — | Headline value‑add |
| Tab 5 | Systems: latency/energy/memory × hardware | — | Partly our data |
| Tab 6 | Model release inventory | — | Appendix C, also a living CSV |

Follow the `dataviz` skill for Fig 5/6 palettes and the `artifact-diagramming` guidance for Fig 1/4 if any of these are also rendered as an artifact.

---

## 10. Core corpus (all open‑access; ~40 seeds, expand via snowballing to ~140)

**Foundational (BitNet lineage)**
- BitNet: Scaling 1‑bit Transformers — arXiv 2310.11453 (Oct 2023); **JMLR v26(125), 2025** — peer‑reviewed gold‑OA anchor.
- The Era of 1‑bit LLMs / BitNet b1.58 — arXiv 2402.17764 (Feb 2024).
- BitNet b1.58 2B4T Technical Report — arXiv 2504.12285 (Apr 2025); open weights on HF.
- BitNet a4.8: 4‑bit Activations — arXiv 2411.04965 (Nov 2024).
- BitNet v2: Native 4‑bit Activations with Hadamard — arXiv 2504.18415 (Apr 2025).

**Training / analysis**
- BitNet b1.58 Reloaded (smaller networks) — arXiv 2407.09527.
- When are 1.58 bits enough? — arXiv 2411.05882.
- Continual QA Pre‑Training: 16‑bit → 1.58‑bit transition — arXiv 2502.11895.
- Rethinking 1‑bit Optimization Leveraging Pre‑trained LLMs — arXiv 2508.06974.
- CAGE: Curvature‑Aware Gradient Estimation — arXiv 2510.18784 (MLSys 2026).
- PV‑Tuning: Beyond Straight‑Through Estimation for Extreme LLM Compression — NeurIPS 2024 (proceedings PDF, gold OA).

**Systems / kernels / hardware**
- 1‑bit AI Infra Part 1.1 (bitnet.cpp) — arXiv 2410.16144.
- bitnet.cpp: Efficient Edge Inference for Ternary LLMs — arXiv 2502.11880.
- Matmul or No Matmul in the Era of 1‑bit LLMs — arXiv 2408.11939.
- FairyFuse: Multiplication‑Free LLM Inference on CPUs via Fused Ternary Kernels — arXiv 2604.20913 (2026).
- `github.com/microsoft/BitNet` — framework; GPU kernels (May 2025); parallel CPU kernels (Jan 2026).

**Compression toward 1‑bit (QAT / PTQ / distillation)**
- OneBit: Towards Extremely Low‑bit LLMs — arXiv 2402.11295.
- BiLLM: Pushing the Limit of PTQ — arXiv 2402.04291.
- PB‑LLM: Partially Binarized LLMs — arXiv 2310.00034.
- FBI‑LLM: Fully Binarized LLMs from Scratch (autoregressive distillation) — arXiv 2407.07093.
- BitDistiller (QAT sub‑4‑bit via self‑distillation) — arXiv 2402.10631.
- EfficientQAT — arXiv 2407.11062.
- ~~PT‑BitNet (PTQ scale‑up of 1‑bit to 70B)~~ — **EXCLUDED (R1):** Neurocomputing 2025 / SSRN only, no downloadable OA copy. Do not cite.
- TWLA: Ternary Weights + Low‑bit Activations via PTQ — arXiv 2606.13054 (2026).
- Tequila: Trapping‑free Ternary Quantization — arXiv 2509.23809 (2025).
- Rethinking Output Alignment for 1‑bit PTQ — arXiv 2512.21651 (Dec 2025).
- LBLLM: Lightweight Binarization via Three‑Stage Distillation — arXiv 2604.19167 (2026).

**New bit‑widths / sparsity coupling**
- Sherry: Hardware‑Efficient 1.25‑Bit Ternary Quantization via Fine‑grained Sparsification — arXiv 2601.07892 (2026).
- Sparse‑BitNet: 1.58‑bit LLMs are Naturally Friendly to Semi‑Structured Sparsity — arXiv 2603.05168 (2026, MSR + PKU).
- NativeTernary: self‑delimiting binary encoding for ternary weights — arXiv 2604.03336 (2026). *(was the "native ternary storage" placeholder; found in search run 1.)*
- STBLLM (structural binarization, <1‑bit) — arXiv 2408.01803; ARB‑LLM (ICLR 2025) — arXiv 2410.03129; Progressive Binarization + semi‑structured pruning — arXiv 2502.01705.

**Multimodal / applications / extensions**
- BitVLA: 1‑bit Vision‑Language‑Action Models for Robotics — arXiv 2506.07530 (Jun 2025).
- LLaVaOLMoBitnet1B: Ternary LLM goes Multimodal — arXiv 2408.13402 (2024).
- BitNet‑embedding‑0.6B / 270M, VibeASR.cpp — captured in the `microsoft/BitNet` snapshot (`papers/_web/`); non‑paper artifacts.
- Falcon‑E / Falcon‑Edge 1.58‑bit (TII) — HF blog snapshot (`papers/_web/`); non‑paper artifact, no arXiv report exists.

**Background / classic BNN**
- STE (Bengio et al.) — arXiv 1308.3432.
- BinaryConnect — arXiv 1511.00363.
- XNOR‑Net — arXiv 1603.05279.
- BinaryBERT — arXiv 2012.15701 (ACL 2021); BiBERT — arXiv 2203.06390 (ICLR 2022).

**Positioning (prior surveys)**
- A Survey of Low‑bit LLMs — Neural Networks 2025 / arXiv 2409.16694.
- Binary Neural Networks for LLM: A Survey — arXiv 2502.19008.

> **Archive status (2026-09-03):** **100 papers** downloaded to `papers/` (37 seeds + 33 run 1 + 30 run 2) + 3 `_web/` snapshots.
> See `papers/INDEX.md` for the `local_file` map, `protocol/search-log.md` and `data/candidates.md` for the search history.
> **Excluded under R1** (no downloadable OA copy): PT‑BitNet only.
> **~40 identified-not-yet-retrieved** (deferred to run 3) + ~12 post‑cutoff (→ living appendix). Run 2 also surfaced a **3rd overlapping survey** (Hao et al., TPAMI 2025) — added to §1.
> **Pipeline status (2026-09-04):**
> - Corpus: **126 papers archived** in `papers/` (+3 `_web/`); 1 excluded (PT-BitNet, no OA copy).
> - `data/inventory.csv`: all 126 coded on 15 fields, vocab normalised. Tallies — weight: ternary 53 / binary 32 / mixed-partial 19 / n/a 22; paradigm: QAT-finetune 33 / native-scratch 27 / PTQ 26 / systems 21 / analysis 12 / survey 4 / continual-QAT 2 / background 1.
> - `data/taxonomy.md`: 5-axis taxonomy + Figure-1 Mermaid tree + Table-1 spec — **done**.
> - `survey-protocol.md` §11: provisional PRISMA flow **frozen**.
> - `protocol/osf-preregistration.md`: OSF text **drafted**.
> - `data/table1-classification.md` (88 method papers) + `data/table5-systems.md` — generated from CSV.
> - `draft/` — first drafts of **all 11 sections** + `00-assembly.md` map (~12k words). All cite `inventory.csv` keys.
> - `data/results.csv` (57 rows) + **`data/table72-normalised-comparison.md`** — the normalised comparison: 60+ methods in 5 groups, each with a *consistent effective-bits* figure (reported vs metadata-strict BPW shown where they differ, e.g. BiLLM 1.08 / 2.88).
> - `figures/` — `fig1-taxonomy.mmd`, `fig2-prisma.mmd`, `fig3-timeline.mmd`, `fig4-datapath.md` — diagram source ready to render.
> - **`1bit-llm-survey.tex`** — full assembled paper (auto-generated from `draft/*.md`); **`references.bib`** — 129 entries (auto-generated); `tables/table1.tex` + `tables/table5.tex`; `scripts/build_paper.py` + `Makefile` + `TEX-BUILD.md`. All 109 cite keys resolve; braces/environments/non-ASCII checks pass. Not compile-tested (no TeX toolchain here).
> - **`STYLE-GUIDE.md`** — survey-writing conventions distilled from the 3 competitor surveys + CS-survey guidance, and **fully applied in a prose pass**: all 12 sections rewritten; no table of contents; `unsrtnat` so references are `[1],[2],...` in ascending order of first citation and grouped as `[1, 2]` / `[1]--[3]`; **no em dashes**; American spelling throughout; real `$...$` math; `Index Terms` line; declarative open-problems; section numbering finalised as 1..12 with Methodology as §3. Body ~12,300 words. Remaining: expand bib author lists, fill §10 reproduction tables after the run, render figures.
> - `repro/` — reproduction scaffold ready to run (~8 GPU-h + ~3 CPU-h).
> - **Remaining:** run `repro/` → §9 + Figs 5/6 + reproducibility audit; render figures + hand-polish Fig 4; expand `references.bib` author lists (currently `<first-author> and others`); 16 `Anon` first-author fixes; swap `article`→`acmart` for CSUR; OSF upload (author); optional raw-API run 4.

---

## 11. Timeline — 14 weeks to first submission

| Week | Deliverable |
|---|---|
| 1 | Lock + pre‑register protocol (OSF). Finalize search strings, IC/EC. Create artifact repo skeleton. Send NMI + COMST pre‑submission inquiries. |
| 2 | Run all searches; dedupe; title/abstract screening; build Zotero library; PRISMA counts v1. |
| 3 | Full‑text screening; complete `inventory.csv` coding; second coder on 20 % sample; κ. PRISMA figure. |
| 4 | Draft §1 + §2; Figure 1 (taxonomy) v1; Figure 3 (timeline). |
| 5 | Draft §3 + §4; Tables 1–2; Figure 4 (datapaths). |
| 6 | Draft §5; Table 3. |
| 7 | Draft §6; set up §9 reproduction — pin `lm-eval-harness` commit, build `bitnet.cpp`, smoke‑test the BitNet GPU kernel. |
| 8 | Run §9 minimum tier — Arm A ~8 GPU‑h over ~3 nights on the shared 4080, Arm B ~3 CPU‑h; collect logs; Table 5; Figure 5 (Pareto). |
| 9 | Draft §7 + Table 4 (master benchmark); Figure 6. |
| 10 | Draft §8 + §9 writeup; Appendices C–D. |
| 11 | Draft §10 (open problems) + §11; full internal read‑through. |
| 12 | 2–3 external reviewers (quantization / systems background); address feedback. |
| 13 | Polish; CSUR compliance (≤ 35 pp incl. refs, abstract ≤ 100 words, CCS concepts, ORCID, LaTeX template); cover letter. |
| 14 | Post arXiv preprint; submit to ACM CSUR via Manuscript Central. |

Parallelizable with 2 authors: one owns §4–§6 + systems reproduction, the other §2–§3 + §5 + §7; both on §10.

---

## 12. Authorship & positioning

- **Get one co‑author with a quantization or efficient‑inference track record.** Single‑author comprehensive surveys are materially harder to land at ≥10 IF; a recognizable name also helps the CSUR/NMI editor triage.
- Consider inviting someone who has shipped a 1‑bit kernel or trained a low‑bit model to co‑author §6/§9 — turns the reproduction study from "outsider re‑runs numbers" into "community reference."
- ORCID for all authors before submission (CSUR requires it).
- Declare any Microsoft / TII / vendor ties (or absence thereof) — independence is part of the pitch.

---

## 13. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Field moves faster than review cycle | Hard cutoff stated in abstract; living appendix repo; commit to a "changes since submission" paragraph at camera‑ready. |
| "Descriptive, not critical" (top‑journal killer) | §10 must name 5–8 concrete, falsifiable open problems; every synthesis subsection ends with a "what we don't know" note. |
| Competitor survey upgrades to a top venue first | Our differentiators (systematic protocol + native‑1‑bit scope + 2026 coverage + reproduction study) are structural, not cosmetic — restate them in the rebuttal. Move fast. |
| Evidence base is mostly arXiv (no peer review) | Evidence‑score stratification; JMLR/ACL/NeurIPS anchors where they exist; the reproduction study *is* our peer review of the headline claims. |
| Vendor‑reported efficiency numbers can't all be reproduced | Report our deltas honestly in §9.4; frame partial reproduction as a finding, not a failure. |
| APC cost if AI Review and no institutional deal | Try CSUR (ACM Open, ~£0) first; confirm institutional Springer agreement before choosing AI Review; TACL as £0 fallback. |
| Scope creep into general low‑bit | IC‑2 is the fence: > 2‑bit primary method → background only. Enforce in screening. |

---

## 14. Reproducibility artifact (build alongside the paper)

Public repo (`github.com/<you>/onebit-llm-survey`) containing:
- `protocol/` — frozen search strings, IC/EC, OSF link, PRISMA records.
- `data/inventory.csv` — the coded paper table (also Appendix B) + `models.csv` (Appendix C), kept updated post‑publication.
- `repro/` — pinned `lm-evaluation-harness` commit, `bitnet.cpp` build notes, run scripts, raw logs, energy traces.
- `figures/` — source for Figs 1, 3, 4, 5, 6.
- `CHANGELOG.md` — the living record of post‑cutoff developments.

Cite the repo with a Zenodo DOI in the paper.

---

## 15. Do next (this week)

1. Confirm journal choice order: **ACM CSUR → AI Review** (recommended) — or say if you want to lead with AI Review for speed, or gamble on COMST.
2. Confirm whether a co‑author is realistic (changes the timeline and the NMI odds).
3. §9 hardware is settled: shared **RTX 4080** for Arm A (~8 GPU‑h, minimum tier), the dev‑box CPU for Arm B. An ARM SBC is the only optional add.
4. Pick the title.
5. I can then generate: (a) the OSF‑ready protocol document with final Boolean strings, (b) the `inventory.csv` schema + first ~40 rows pre‑filled from the corpus above, or (c) a drafted §2 (Background) as a writing sample. Say which.
