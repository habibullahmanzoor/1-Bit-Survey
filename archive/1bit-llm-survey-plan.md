# 📋 Survey Paper Plan — 1-Bit Language Models

**Target:** Top-tier journal (10+ IF) with open access preference
**Topic:** 1-Bit and 1.58-Bit Large Language Models
**Method:** Systematic review using only open-access sources
**Planned cutoff date for literature:** July 2026

---

## 1. Strategic Snapshot

| Item | Assessment |
|---|---|
| **Topic maturity** | Hot. ~30 core papers from Oct 2023 → Mar 2026, accelerating |
| **Existing surveys** | Only one short low-tier review (IJFMR, Dec 2024, ~4 pages). No systematic, no top-journal survey. **Clear gap to fill.** |
| **Field window** | Actively publishing — write fast and submit by Q4 2026 to own the niche |
| **Risk** | Fast-moving — commit to a literature cutoff date and add an "online appendix" for updates |

---

## 2. Target Journals (10+ IF ∩ Open Access)

Open access is the real constraint. Realistic shortlist, ranked by **fit × acceptance probability**:

| Journal | IF (2024) | OA Mode | Fit for this survey | Realistic? |
|---|---|---|---|---|
| **TACL** (Association for Computational Linguistics) | **15.63** | ✅ Fully OA (gold) | Perfect — NLP/ML core | **Top pick** |
| **AI Open** (Elsevier / KeAi) | **18.17** | ✅ Fully OA | Great — explicitly invites reviews | **Strong backup** |
| **Artificial Intelligence Review** (Springer) | **18.8** | Hybrid (APC ≈ $3.5k) | Survey-friendly, well-known | **High-prestige target** |
| **Information Fusion** (Elsevier) | 17.4 | Hybrid | Less fit — fusion-focused | Skip |
| **Nature Machine Intelligence** | 29.8 | Hybrid (APC ≈ $12k) | Stretch — needs strong societal/energy angle | Stretch |
| **IEEE TPAMI** | 20.4 | Hybrid | Usually extended conference paper; surveys rare | Skip |

**Recommendation: Lead target = TACL.** Fully OA, IF 15.6, ACL prestige, accepts substantive surveys, and the topic (efficient LLM architectures) sits squarely in TACL's wheelhouse. Submit TACL + AI Open as backup.

> ⚠️ Note on "open access": you said you can **only use** OA papers as **sources** — that's separate from the journal's OA status. Addressed in §4.

---

## 3. Proposed Title Options

Pick one or hybrid:

1. **"1-Bit Large Language Models: A Systematic Survey of Architectures, Training, Systems, and Open Challenges"** (most descriptive)
2. **"The Rise of Native 1-Bit LLMs: From BitNet to Ternary Foundation Models"** (catchy, positions as field-defining)
3. **"Ternary Foundations: A Comprehensive Survey on 1-Bit and 1.58-Bit Language Models"** (technically precise)
4. **"Extreme Quantization for Foundation Models: A Survey on 1-Bit LLMs"** (broadens appeal)

**Suggested for journal: #1. Suggested for blog/talk: #2.**

---

## 4. Open-Access Source Strategy

This is the tricky part. You have to build a paper out of OA-only sources. Method:

### A. Vetted OA sources (draw from freely)
- **arXiv** (`cs.CL`, `cs.LG`, `cs.AI`) — every BitNet paper is here
- **JMLR** (gold OA) — *BitNet: 1-bit Pre-training for LLMs* published here (Wang et al. 2025, JMLR 26:125)
- **TACL** (gold OA) — peer NLP work
- **ACL / EMNLP / NeurIPS / ICLR / ICML proceedings** (mostly gold OA via ACL Anthology + OpenReview)
- **PLOS, Frontiers, MDPI, Scientific Reports** (gold OA — useful for application papers)
- **Open-source repos**: `github.com/microsoft/BitNet`, Hugging Face model cards, arXiv technical reports
- **Hugging Face papers** (https://huggingface.co/papers — indexed arXiv)

### B. Avoid (or use only as illustrative citation)
- Closed Nature/Science main articles (only Nature Machine Intelligence is hybrid-OA accessible)
- IEEE Xplore closed papers (unless the authors posted a preprint on arXiv — use that)
- Elsevier closed journal articles (unless a green OA preprint exists)

### C. Practical workflow
1. Start from arXiv listings for `[cs.CL] / [cs.LG]` filtered by "BitNet" OR "1-bit" OR "1.58" OR "ternary LLM"
2. For each paper, find an OA version (arXiv, JMLR, conference proceedings, or author's personal site)
3. For each model release, pull the HF model card and the official GitHub README as cited artifacts
4. Document the search/screening protocol in the paper (PRISMA-style flow diagram) — this is **expected** at 10+ IF journals

---

## 5. Full Paper Outline (target 25–35 pages, ~120 references)

### §1. Introduction (~3 pages)
- 1.1 The cost crisis of modern LLMs (memory, energy, latency, carbon)
- 1.2 Why quantization — and why push to 1-bit
- 1.3 Why a survey now: a new paradigm emerges
- 1.4 Scope, contributions, and paper organization
- 1.5 Survey methodology (PRISMA diagram)

### §2. Background & Mathematical Preliminaries (~4 pages)
- 2.1 Number systems: FP32 / FP16 / BF16 / INT8 / INT4 → binary / ternary
- 2.2 Information-theoretic view: why log₂(3) ≈ 1.58 bits
- 2.3 Quantization taxonomy: PTQ vs QAT vs native low-bit training
- 2.4 The straight-through estimator (STE) and its limitations
- 2.5 Scaling laws: do they still hold at 1 bit?
- 2.6 Evaluation metrics: perplexity, downstream, latency, energy, memory, throughput

### §3. A Taxonomy of 1-Bit LLMs (~3 pages)
- 3.1 Binary {-1, +1} vs Ternary {-1, 0, +1} vs Mixed-precision
- 3.2 From-scratch native training vs post-training quantization
- 3.3 Pre-training only vs continued pre-training vs distillation-based
- 3.4 Decoder-only, encoder-decoder, MoE-1-bit, multimodal-1-bit
- 3.5 **Taxonomy figure (mandatory for high IF)**

### §4. Architectural Design (~4 pages)
- 4.1 BitLinear: the core primitive
- 4.2 Norm placement (pre-norm vs post-norm vs no-norm)
- 4.3 Activation quantization (INT8 → INT4 → sparse 4-bit; BitNet a4.8)
- 4.4 KV-cache quantization (3-bit KV cache)
- 4.5 Mixture-of-Experts with 1-bit weights
- 4.6 1-bit attention and 1-bit FFN alternatives
- 4.7 Sparsity-quantization coupling (Sparse-BitNet)

### §5. Training Methodology (~4 pages)
- 5.1 The native 1-bit training loop
- 5.2 Latent ("shadow") weights and dual-precision optimization
- 5.3 STE and its pathologies (gradient mismatch, instability)
- 5.4 Beyond STE: PV-Tuning, CAGE, denoising reconstruction
- 5.5 Hyperparameters, learning rate schedules, scaling laws for 1-bit
- 5.6 Data efficiency: do 1-bit models need more or fewer tokens?
- 5.7 Distillation from full-precision teachers (BDF, BitDistiller)

### §6. Inference Systems & Hardware (~3 pages)
- 6.1 `bitnet.cpp`: kernel design (I2_S, TL1, TL2)
- 6.2 CPU inference (x86, ARM) — speedups 2.37×–6.17×
- 6.3 GPU inference kernels (since May 2025)
- 6.4 NPU roadmap
- 6.5 Custom 1-bit accelerators and ASIC design
- 6.6 Quantitative table: latency / energy / memory across model sizes

### §7. Performance & Benchmarking (~3 pages)
- 7.1 Perplexity vs full-precision across scales
- 7.2 Downstream: MMLU, GSM8K, HumanEval+, ARC, HellaSwag
- 7.3 Reasoning and chain-of-thought at 1-bit
- 7.4 Long-context behavior
- 7.5 **Quantitative comparison table (mandatory, ~15 models × ~8 metrics)**

### §8. Applications & Extensions (~3 pages)
- 8.1 Edge / on-device deployment
- 8.2 Mobile and embedded systems
- 8.3 1-bit embedding models (BitNet-embedding)
- 8.4 1-bit for multimodal / vision-language
- 8.5 1-bit for retrieval and recommender systems
- 8.6 Environmental / carbon implications

### §9. Challenges, Limitations & Open Problems (~3 pages)
- 9.1 Training stability under extreme quantization
- 9.2 Capacity ceiling: at what scale does 1-bit break?
- 9.3 Reasoning and emergent abilities at 1-bit
- 9.4 Generalization vs full-precision
- 9.5 Security, robustness, adversarial behavior of 1-bit models
- 9.6 Reproducibility and standardized benchmarks

### §10. Future Directions (~2 pages)
- 10.1 Sub-1-bit: spiking neural networks + LLMs
- 10.2 Hardware–software co-design
- 10.3 Mixture-of-experts and 1-bit scaling laws
- 10.4 1-bit for agentic and tool-using models
- 10.5 1-bit multimodal foundation models

### §11. Conclusion (~1 page)

### Appendices
- A. Search & screening protocol (PRISMA)
- B. List of all reviewed papers with metadata
- C. Model release inventory (GitHub, HF, license, parameters)
- D. Reproducibility notes (where to find weights, code)

---

## 6. Survey Methodology (Required for 10+ IF)

This is what separates a 10+ IF survey from a weak one:

1. **Pre-registered search protocol** — write the Boolean query first, freeze it
2. **PRISMA flow diagram** — Identification → Screening → Eligibility → Included counts
3. **Inclusion criteria**: open access + peer-reviewed/arXiv + 1-bit/1.58-bit LLMs + LLMs (not vision-only)
4. **Snowballing**: backward + forward citation chasing on the 5 seed papers
5. **Coding scheme**: extract `(architecture, training, eval, hardware, year, license)` per paper
6. **Inter-rater reliability**: if you have a co-author, compute Cohen's κ on a 20% sample
7. **Quality scoring**: each source gets a 1–5 evidence score; report results stratified

---

## 7. Core Seed Papers (your backbone — all OA on arXiv)

| Paper | Year | OA Source | Why it matters |
|---|---|---|---|
| Wang et al. *BitNet: 1-bit Pre-training for LLMs* | 2023 (JMLR 2025) | arXiv + JMLR | Origin paper |
| Ma et al. *The Era of 1-bit LLMs* (b1.58) | 2024 | arXiv | The 1.58-bit idea |
| Wang et al. *bitnet.cpp* | 2024 | arXiv | First efficient inference |
| Wang et al. *BitNet a4.8* | 2024 | arXiv | 4-bit activations |
| Ma et al. *BitNet b1.58 2B4T Tech Report* | 2025 | arXiv + HF | First open 2B model |
| *Microsoft BitNet GitHub* | 2025 | github.com | Official framework |
| *Sparse-BitNet* | 2026 | arXiv | Sparsity × 1-bit |
| *PV-Tuning* (NeurIPS 2024) | 2024 | NeurIPS proceedings | Beyond STE |
| *CAGE* (arXiv 2510.18784) | 2025 | arXiv | Curvature-aware STE |
| *Rethinking 1-bit Optimization* (arXiv 2508.06974) | 2025 | arXiv | PT-pretrained 1-bit |
| *BitNet Distillation (BDF)* | 2024 | OpenReview | Distillation-based 1-bit |
| *NativeTernary* encoding | 2026 | arXiv | Storage layer |

---

## 8. Writing Timeline (12–14 weeks to submission)

| Week | Deliverable |
|---|---|
| W1 | Lock search protocol, register on OSF (optional but adds rigor) |
| W2 | Run searches, screen titles/abstracts, build Zotero library |
| W3 | Full-text review, extract coding sheet, draft PRISMA diagram |
| W4 | Draft §1 + §2, draw taxonomy figure v1 |
| W5 | Draft §3 + §4, build architecture comparison table |
| W6 | Draft §5 + §6, build training-method comparison table |
| W7 | Draft §7 + §8, build benchmark table (big value-add) |
| W8 | Draft §9 + §10 + §11 |
| W9 | All figures, tables, references, citation formatting |
| W10 | Internal review by 2–3 trusted colleagues, address feedback |
| W11 | Polish, pre-empt common reviewer concerns |
| W12 | Submit to **TACL (primary)** + **AI Open (backup)** |

---

## 9. Strategic Tips to Land in 10+ IF

1. **Add a quantitative contribution, not just a review.** Run benchmarks yourself if you can — even on 2–3 models. This lifts you from "survey" to "survey + empirical study", which is what 10+ IF reviewers want.
2. **Be the first to systematically catalog all 1-bit LLM releases** (a comprehensive table is a citation magnet).
3. **Identify a non-obvious open problem** in §9 that the community hasn't articulated. Reviewers remember papers that frame the field.
4. **Make figures beautiful and original.** Taxonomy figure, architecture comparison, performance Pareto frontier — these get cited on Twitter/LinkedIn and drive citations.
5. **Pre-print on arXiv at submission**, blog on Hugging Face papers. Top journals don't mind arXiv preprints; it boosts visibility.
6. **Get one strong co-author** (someone who has worked on quantization or efficient LLMs). Single-author surveys are harder to land in 10+ IF.

---

## 10. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Field moves too fast; paper outdated by publication | Cutoff date stated explicitly; add an "Online Appendix" link in camera-ready |
| Reviewer says "too descriptive, not critical" | §9 must be sharp and opinionated; identify 3–5 concrete open problems |
| All sources are arXiv (no peer review) | Acknowledge this; rely on quality of synthesis, not source prestige |
| OA-only constraint limits breadth | Frame it as a contribution — "An Open-Access Survey of 1-Bit LLMs" |
| Reproducibility concerns | Link GitHub, HF, model cards; explicitly state what cannot be reproduced |

---

## 11. Next-Step Options

Choose one to dive deeper:

- **(A)** Generate the full PRISMA search protocol with Boolean queries for arXiv/ACL/HF
- **(B)** Draft Section 2 (Background) as a writing sample
- **(C)** Build the master comparison table (all 1-bit LLMs × all key metrics) as a CSV you can iterate on
