# A Survey on 1-Bit Large Language Models: From Ternary Quantization to Efficient Deployment — Full Paper Plan for High-Impact Publication

## Executive Summary

1-bit Large Language Models (LLMs) replace conventional FP16/BF16 weights with ternary values {-1, 0, 1}, representing 1.58 bits of information per parameter, enabling order-of-magnitude gains in memory, latency, and energy while matching full-precision performance at scale [[1]](https://arxiv.org/abs/2504.12285v2) [[2]](https://arxiv.org/abs/2402.17764v1). The foundational line — BitNet (2023) [[3]](https://huggingface.co/papers/2310.11453), BitNet b1.58 (2024) [[2]](https://arxiv.org/abs/2402.17764v1), BitNet b1.58 2B4T (2025) [[1]](https://arxiv.org/abs/2504.12285v2), BitNet a4.8 (2024) [[4]](https://arxiv.org/html/2411.04965v1) and BitNet v2 (2025) [[5]](https://arxiv.org/pdf/2504.18415v2) — provides a complete open-access corpus that can support a survey meeting the 10+ impact factor threshold when combined with parallel open-access branches: FBI-LLM [[6]](https://arxiv.org/abs/2407.07093), OneBit [[7]](https://arxiv.org/abs/2402.11295v5), BiLLM [[8]](https://arxiv.org/abs/2402.04291), and PB-LLM [[9]](https://arxiv.org/abs/2310.00034v1).

This report provides a publication-ready structure, a strictly open-access bibliography, a taxonomy, methodology for PRISMA-compliant survey search, and a target journal strategy centered on ACM Computing Surveys (IF 23.8) [[10]](https://en.wikipedia.org/wiki/ACM_Computing_Surveys), IEEE TPAMI (IF 20.8-23.6) [[11]](https://en.wikipedia.org/wiki/IEEE_Transactions_on_Pattern_Analysis_and_Machine_Intelligence) [[12]](https://open.ieee.org/wp-content/uploads/IEEE-Title-List-November-2023.pdf), Nature Machine Intelligence (IF 25.9) [[13]](https://github.com/yonas-t-a/nlper-conferences-journals-survey) [[14]](https://www.scijournal.org/nature-machine-intelligence), and IEEE Communications Surveys & Tutorials (IF 35.6) [[15]](https://en.wikipedia.org/wiki/IEEE_Communications_Surveys_and_Tutorials).

## Sources

Sources 1-16 listed at end. All are open-access.

## 1. Research Scope and Research Questions

> **Definition**: A 1-bit LLM is a Transformer-based LLM where weight matrices are quantized to binary {-1,+1} or ternary {-1,0,1} values during training, eliminating multiplication in matrix multiplication and replacing it with addition/subtraction [[3]](https://huggingface.co/papers/2310.11453).

For a high-IF survey, the paper must answer:

**RQ1 — Foundations**: How do BitNet and BitNet b1.58 formulate BitLinear and ternary quantization with straight-through estimator (STE) training from scratch?
**RQ2 — Variants**: What are the two main research branches: (a) native 1-bit training from scratch vs (b) post-training quantization (PTQ) and quantization-aware training (QAT) compression of existing LLMs?
**RQ3 — Efficiency**: What are the quantified gains in memory (0.4GB vs 2-4.8GB), CPU latency (29ms vs 48-124ms), and energy (0.028J vs 0.186-0.649J, 96% reduction) reported in open-access evaluations? [[16]](https://huggingface.co/microsoft/bitnet-b1.58-2B-4T)
**RQ4 — Activation bottleneck**: How do BitNet a4.8 and BitNet v2 solve the activation outlier problem via hybrid quantization-sparsification and online Hadamard transformation?
**RQ5 — Benchmarking**: Which open benchmarks are used (perplexity on WikiText2/C4, zero-shot on ARC-Easy, ARC-Challenge, Hellaswag, Winogrande, PIQA, OpenbookQA, BoolQ) [[17]](https://arxiv.org/html/2402.17764v1)?
**RQ6 — Future**: What are scaling laws, hardware co-design, and multimodal extensions?

## 2. Strictly Open-Access Bibliography (Eligible for Your Paper)

All papers below are arXiv or Microsoft Research open-access, meeting your constraint.

| Category | Paper | Year | Key Contribution | Open Access Link |
| --- | --- | --- | --- | --- |
| Foundation | BitNet: Scaling 1-bit Transformers | 2023 | BitLinear as drop-in replacement for nn.Linear, 1-bit weights from scratch | [[3]](https://huggingface.co/papers/2310.11453) |
| Foundation | The Era of 1-bit LLMs: All LLMs are in 1.58 Bits (BitNet b1.58) | 2024 | Ternary {-1,0,1} weights, 1.58-bit, matches FP16 at same scale | [[2]](https://arxiv.org/abs/2402.17764v1) |
| Foundation | BitNet b1.58 2B4T Technical Report | 2025 | First open-source 2B native 1-bit LLM trained on 4T tokens, open weights | [[1]](https://arxiv.org/abs/2504.12285v2) |
| Activation | BitNet a4.8: 4-bit Activations | 2024 | Hybrid quantization + sparsification, 55% active params, 3-bit KV cache | [[4]](https://arxiv.org/html/2411.04965v1) |
| Activation | BitNet v2: Native 4-bit with Hadamard | 2025 | H-BitLinear with online Hadamard to smooth outliers | [[5]](https://arxiv.org/pdf/2504.18415v2) |
| Full Binary | FBI-LLM: Fully Binarized via Autoregressive Distillation | 2024 | First fully binary {-1,+1} LLM from scratch (not ternary) matching FP16 | [[6]](https://arxiv.org/abs/2407.07093) |
| QAT | OneBit: Towards Extremely Low-bit LLMs | 2024 | 1-bit QAT framework with novel representation + matrix decomposition init, 81-83% non-quantized perf | [[7]](https://arxiv.org/abs/2402.11295v5) |
| PTQ | BiLLM: Pushing Limit of PTQ | 2024 | Residual approximation, salient weight handling, 1.09-bit avg | [[8]](https://arxiv.org/abs/2402.04291) |
| PTQ | PB-LLM: Partially Binarized LLMs | 2023 | First work using network binarization for LLM compression, partial binarization | [[9]](https://arxiv.org/abs/2310.00034v1) |
| Survey Reference | Binary Neural Networks for LLM: A Survey | 2025 | Comprehensive review of BNN techniques applied to LLMs, taxonomy of PTQ/QAT/native | [[18]](https://arxiv.org/abs/2502.19008) |
| Infrastructure | BitNet.cpp + 1-bit AI Infra Part 1.1 | 2024-2025 | Fast lossless inference kernels, x86 2.37x-6.17x speedup, ARM 1.37x-5.07x | [[19]](https://github.com/microsoft/BitNet) |

## 3. Taxonomy for Survey (Your Core Contribution)

A high-IF survey must propose a taxonomy, not just list papers. Use:

**Dimension 1 — Quantization Granularity:**
- True Binary (1-bit): FBI-LLM {-1,+1}
- Ternary (1.58-bit): BitNet b1.58 {-1,0,1} [[2]](https://arxiv.org/abs/2402.17764v1)
- Hybrid low-bit: BitNet a4.8 W1.58A4 [[4]](https://arxiv.org/html/2411.04965v1)

**Dimension 2 — Training Paradigm:**
- Native from scratch: BitNet, BitNet b1.58, BitNet 2B4T, FBI-LLM
- PTQ (no retraining): BiLLM, PB-LLM
- QAT (fine-tune quantized): OneBit, EfficientQAT

**Dimension 3 — Components Quantized:**
- Weights only vs Weights+Activations vs Weights+Activations+KV Cache
- BitNet b1.58: W1.58A8, BitNet a4.8: W1.58A4 + 50% sparsity on attention output [[4]](https://arxiv.org/html/2411.04965v1)

**Dimension 4 — Efficiency Stack:**
- Algorithm (STE, two-stage LR/weight decay, 100B RedPajama recipe) [[20]](https://arxiv.org/html/2504.18415v1)
- Kernel (bitnet.cpp fused ternary kernels, lossless)
- Hardware (CPU-first, GPU, NPU roadmap)

## 4. Full Paper Outline — Compliant with ACM CSUR / TPAMI / NMI

### Title Options (Impact-oriented)
- "A Survey on 1-Bit Large Language Models: Ternary Quantization, Efficient Training, and Hardware Co-Design"
- "The Era of 1.58-bit Intelligence: A Systematic Survey of 1-bit LLMs from BitNet to BitNet v2"

### Abstract (100 words max for CSUR) [[21]](https://dlnext.acm.org/journal/csur/author-guidelines)
Write short, direct, no first person, no math. Example skeleton:
> Objectives: synthesize open-access research on 1-bit LLMs. Methods: PRISMA search of arXiv/open repositories 2023-2025, 11 core papers, taxonomy by granularity/paradigm/component. Results: native 1.58-bit models match FP16 from 3B scale while reducing memory to 0.4GB, latency to 29ms, energy by 96%. Conclusion: identifies activation outliers, scaling laws, hardware co-design as next frontiers.

### Keywords
1-bit LLM, ternary quantization, BitNet, binary neural network, efficient inference, quantization-aware training

### Sections

**1. Introduction**
- Motivation: LLMs energy crisis, MAC to addition-only
- Why 1-bit now: BitNet scaling law similar to full-precision [[3]](https://huggingface.co/papers/2310.11453)
- Contributions: first survey restricted to reproducible open-access artifacts, new taxonomy, quantitative efficiency table, roadmap

**2. Methodology of Survey**
- PRISMA flow
- Databases: arXiv cs.CL, cs.LG, cs.AI, Microsoft Research open publications
- Inclusion: only CC-BY/open-access papers with code or weights, 2023-2026
- Exclusion: closed-access, no artifact
- Search strings: "BitNet OR 1-bit LLM OR ternary LLM OR binary LLM"
- This addresses open-access constraint transparently for reviewers

**3. Background: From Quantization to Binarization**
- 3.1 Quantization fundamentals (uniform, absmean, absmax)
- 3.2 Binary Neural Networks history
- 3.3 Transformer-specific challenges (outlier channels)

**4. Foundational Architectures: BitNet Family**
- 4.1 BitNet: BitLinear design, layernorm → binarize → absmax quantization [[3]](https://huggingface.co/papers/2310.11453)
- 4.2 BitNet b1.58: ternary {-1,0,1}, 1.58-bit information theory [[2]](https://arxiv.org/abs/2402.17764v1)
- 4.3 BitNet b1.58 2B4T: 4T tokens, open weights, conversational/math/coding eval [[1]](https://arxiv.org/abs/2504.12285v2)

**5. Training Recipes and Optimization**
- 5.1 STE: forward quantize, backward identity within clipping range
- 5.2 Two-stage weight decay and LR scheduling, RedPajama 100B tokens (95B W1.58A8 + 5B W1.58A4) [[20]](https://arxiv.org/html/2504.18415v1)
- 5.3 Direct quantized training with stochastic rounding (alternative to STE) — cite open discussion
- 5.4 Mixed-precision latent weights

**6. Variants and Comparative Methods (Open-Access Only)**
- 6.1 Full binarization: FBI-LLM via autoregressive distillation [[6]](https://arxiv.org/abs/2407.07093)
- 6.2 QAT: OneBit matrix decomposition init [[7]](https://arxiv.org/abs/2402.11295v5)
- 6.3 PTQ: BiLLM residual approximation [[8]](https://arxiv.org/abs/2402.04291), PB-LLM partial binarization [[9]](https://arxiv.org/abs/2310.00034v1)
- 6.4 Table comparing bit-width, retraining need, avg bits per weight

**7. Activation Quantization: The New Bottleneck**
- 7.1 Outlier analysis: Gaussian vs sharp long-tailed distributions in attention output and FFN down [[4]](https://arxiv.org/html/2411.04965v1)
- 7.2 BitNet a4.8: INT4 for QKV/up/gate, INT8+Top-K sparsification for out/down, ReLU^2 GLU achieving 80% sparsity [[4]](https://arxiv.org/html/2411.04965v1)
- 7.3 BitNet v2: H-BitLinear with online Hadamard transform [[5]](https://arxiv.org/pdf/2504.18415v2)
- 7.4 FP4 vs INT4

**8. Hardware Efficiency and Systems**
- 8.1 bitnet.cpp: fused ternary kernels, lossless inference, CPU-first design [[19]](https://github.com/microsoft/BitNet)
- 8.2 Quantitative results: 0.4GB memory (87% reduction), 29ms TPOT (77% improvement), 0.028J energy (96% reduction) vs LLaMA 3.2 1B / Qwen2.5 1.5B etc. [[16]](https://huggingface.co/microsoft/bitnet-b1.58-2B-4T)
- 8.3 Speedups: x86 2.37-6.17x, ARM 1.37-5.07x [[19]](https://github.com/microsoft/BitNet)
- 8.4 Scaling equivalence: 13B BitNet b1.58 more efficient than 3B FP16 [[17]](https://arxiv.org/html/2402.17764v1)
- 8.5 100B model on single CPU at 5-7 tokens/sec human reading speed

**9. Evaluation Methodology**
- 9.1 Perplexity: WikiText2, C4 validation
- 9.2 Zero-shot: ARC-e/c, Hellaswag, Winogrande, PIQA, OpenbookQA, BoolQ via lm-evaluation-harness [[17]](https://arxiv.org/html/2402.17764v1)
- 9.3 Performance parity threshold: from 3B scale BitNet b1.58 matches FP16

**10. Challenges and Future Directions**
- Scaling laws beyond 7B/13B/70B — cited as future work in 2B4T report [[1]](https://arxiv.org/abs/2504.12285v2)
- Hardware co-design: new ISA for ternary matmul (add/sub only)
- KV-cache quantization to 3-bit
- Multimodal 1-bit: vision-language-action models
- Training stability at >100B tokens

**11. Conclusion**

**References**: Only open-access entries above.

## 5. Target Journals with Impact Factor >10 and Strategy

| Journal | IF | Why Fit | Survey Requirements | Open Access Cost | Strategy |
| --- | --- | --- | --- | --- | --- |
| **ACM Computing Surveys** | 23.8 (2023) [[10]](https://en.wikipedia.org/wiki/ACM_Computing_Surveys) | Top CS survey venue, accepts long surveys up to 35 pages incl refs [[21]](https://dlnext.acm.org/journal/csur/author-guidelines) | Classification of literature, perspective, trends; abstract max 100 words; ACM CCS terms; LaTeX template | Hybrid: author can pay for Gold OA or post pre-print version (except Version of Record) to arXiv per ACM rights [[21]](https://dlnext.acm.org/journal/csur/author-guidelines) | **Primary target**. Your open-access-only constraint aligns with ACM Open. Emphasize taxonomy + PRISMA. |
| **IEEE TPAMI** | 20.8 (2023) [[11]](https://en.wikipedia.org/wiki/IEEE_Transactions_on_Pattern_Analysis_and_Machine_Intelligence), 23.6 (2022 JIF) [[12]](https://open.ieee.org/wp-content/uploads/IEEE-Title-List-November-2023.pdf) | Highest IF vision/AI trans, publishes surveys | Needs novel perspective, benchmark reproduction | Hybrid OA | Second target if you add vision extensions (BitVLA). |
| **Nature Machine Intelligence** | 25.9 trend 2024 [[13]](https://github.com/yonas-t-a/nlper-conferences-journals-survey), 22.28 SciJournal [[14]](https://www.scijournal.org/nature-machine-intelligence) | Nature-level impact, likes efficiency/hardware co-design stories | Non-primary articles not eligible for Gold OA? Check: primary research eligible, but reviews may be subscription only — verify. APC £9390/$12850 [[22]](https://www.nature.com/natmachintell/submission-guidelines/publishing-options?error=cookies_not_supported&code=3b413fc8-634f-4cd9-ad4d-e69045868898) | Gold OA APC high | Submit as Review Article, contact editor first. Best for visibility. |
| **IEEE Communications Surveys & Tutorials** | 35.6 (2022) [[15]](https://en.wikipedia.org/wiki/IEEE_Communications_Surveys_and_Tutorials) | Highest IF among IEEE, loves efficient deployment surveys | Tutorial style, must include communication/efficiency angle | Hybrid | Frame as edge deployment of 1-bit LLMs for 6G/IoT. |

**Recommendation**: Start with **ACM Computing Surveys** — its charter explicitly wants classification and trend evaluation [[21]](https://dlnext.acm.org/journal/csur/author-guidelines), matches your open-access limitation, and has IF >10.

## 6. Publication Timeline and Writing Plan (12 weeks)

**Weeks 1-2 — Search & Extraction**
- Implement PRISMA in Zotero, extract all 11 papers above, build comparison table in LaTeX

**Weeks 3-4 — Taxonomy & Figures**
- Create Figure 1: taxonomy tree (granularity x paradigm x component)
- Figure 2: BitLinear vs H-BitLinear diagram (based on open papers)
- Figure 3: efficiency bar chart using numbers: Memory 0.4GB, Latency 29ms, Energy 0.028J [[16]](https://huggingface.co/microsoft/bitnet-b1.58-2B-4T)

**Weeks 5-7 — Draft Core**
- Write Sections 4-8 (technical core). Each subsection must cite at least one open-access source inline.

**Weeks 8-9 — Evaluation & Future**
- Re-run lm-evaluation-harness on BitNet b1.58 2B4T open checkpoint for independent verification (optional but strengthens IF journal)

**Week 10 — Full Draft & Compliance**
- Check CSUR 35-page limit incl refs [[21]](https://dlnext.acm.org/journal/csur/author-guidelines), abstract 100 words, CCS terms, ORCID for all authors

**Week 11 — Internal Review**
- Use checklist from From Literature to Insights: topic timeliness, importance, scope, differentiation [[23]](https://arxiv.org/pdf/2509.25828)

**Week 12 — Submission**
- Submit via Manuscript Central for CSUR [[21]](https://dlnext.acm.org/journal/csur/author-guidelines), include cover letter highlighting open-access reproducibility.

## 7. Key Arguments to Make for High IF Reviewers

1. **Reproducibility as virtue**: By restricting to open-access papers with open weights/code (BitNet b1.58 2B4T on Hugging Face [[16]](https://huggingface.co/microsoft/bitnet-b1.58-2B-4T)), survey is fully reproducible — a Nature MI criterion.
2. **New scaling law**: BitNet exhibits scaling law akin to full-precision Transformers [[3]](https://huggingface.co/papers/2310.11453) — defines new recipe for cost-effective LLMs [[2]](https://arxiv.org/abs/2402.17764v1).
3. **Shift of bottleneck**: From memory bandwidth to compute, solved by 4-bit activations and Hadamard transform [[5]](https://arxiv.org/pdf/2504.18415v2).
4. **Real deployment impact**: 100B model on single CPU at human reading speed [[19]](https://github.com/microsoft/BitNet) — edge AI narrative for COMST.

## 8. Open Access Compliance Note for Your Thesis

Document in methodology: all cited works retrieved from arXiv (CC-BY) or Microsoft Research open-access pages, inference framework from GitHub microsoft/BitNet (MIT-like), model weights from Hugging Face open-source. No closed-access IEEE Xplore papers used for technical claims. This satisfies your constraint and is acceptable for CSUR because ACM permits arXiv pre-prints as references and allows authors to post versions to non-commercial repositories [[21]](https://dlnext.acm.org/journal/csur/author-guidelines).

## Sources
[1] arXiv — [BitNet b1.58 2B4T Technical Report](https://arxiv.org/abs/2504.12285v2)
[2] arXiv — [The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits](https://arxiv.org/abs/2402.17764v1)
[3] Hugging Face — [BitNet: Scaling 1-bit Transformers for Large Language Models](https://huggingface.co/papers/2310.11453)
[4] arXiv — [BitNet a4.8: 4-bit Activations for 1-bit LLMs](https://arxiv.org/html/2411.04965v1)
[5] arXiv — [BitNet v2: Native 4-bit Activations with Hadamard Transformation](https://arxiv.org/pdf/2504.18415v2)
[6] arXiv — [FBI-LLM: Scaling Up Fully Binarized LLMs from Scratch via Autoregressive Distillation](https://arxiv.org/abs/2407.07093)
[7] arXiv — [OneBit: Towards Extremely Low-bit Large Language Models](https://arxiv.org/abs/2402.11295v5)
[8] arXiv — [BiLLM: Pushing the Limit of Post-Training Quantization for LLMs](https://arxiv.org/abs/2402.04291)
[9] arXiv — [PB-LLM: Partially Binarized Large Language Models](https://arxiv.org/abs/2310.00034v1)
[10] Wikipedia — [ACM Computing Surveys](https://en.wikipedia.org/wiki/ACM_Computing_Surveys)
[11] Wikipedia — [IEEE Transactions on Pattern Analysis and Machine Intelligence](https://en.wikipedia.org/wiki/IEEE_Transactions_on_Pattern_Analysis_and_Machine_Intelligence)
[12] IEEE Open — [IEEE Title List November 2023 JIF](https://open.ieee.org/wp-content/uploads/IEEE-Title-List-November-2023.pdf)
[13] GitHub — [NLPer Conferences Journals Survey - Impact Factor Trends](https://github.com/yonas-t-a/nlper-conferences-journals-survey)
[14] SciJournal — [Nature Machine Intelligence — Impact Factor](https://www.scijournal.org/nature-machine-intelligence)
[15] Wikipedia — [IEEE Communications Surveys and Tutorials](https://en.wikipedia.org/wiki/IEEE_Communications_Surveys_and_Tutorials)
[16] Hugging Face — [microsoft/bitnet-b1.58-2B-4T model card efficiency table](https://huggingface.co/microsoft/bitnet-b1.58-2B-4T)
[17] arXiv — [The Era of 1-bit LLMs HTML benchmarks](https://arxiv.org/html/2402.17764v1)
[18] arXiv — [Binary Neural Networks for Large Language Model: A Survey](https://arxiv.org/abs/2502.19008)
[19] GitHub — [microsoft/BitNet official inference framework](https://github.com/microsoft/BitNet)
[20] arXiv — [BitNet v2 training recipe RedPajama](https://arxiv.org/html/2504.18415v1)
[21] ACM DL — [ACM Computing Surveys Author Guidelines](https://dlnext.acm.org/journal/csur/author-guidelines)
[22] Nature — [Nature Machine Intelligence Publishing Options APC](https://www.nature.com/natmachintell/submission-guidelines/publishing-options?error=cookies_not_supported&code=3b413fc8-634f-4cd9-ad4d-e69045868898)
[23] arXiv — [From Literature to Insights: Guidelines for Survey Writing](https://arxiv.org/pdf/2509.25828)
