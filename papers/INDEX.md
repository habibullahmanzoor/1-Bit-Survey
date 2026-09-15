# Papers archive — index

Per **Rule R1** (`../CLAUDE.md`): every paper cited/referenced in this survey is downloaded here as a PDF from its open-access source. **The gate is absolute — no local copy, no citation.** **140 archived** as of 2026-09-07 (135 in-window primary studies, 2023--2026, plus 5 pre-2023 foundational works classified in Table 1 for context; `data/inventory.csv` has one row per archived work). Three non-paper artifacts (two model cards, one framework repo) are kept as dated snapshots under `_web/`. One work, PT-BitNet, met every other criterion but had no obtainable open-access copy and is excluded under IC-5 (`_excluded/`).

`local_file` names follow `<year>_<firstAuthor>_<slug>.pdf`. The authoritative per-paper coding is now `../data/inventory.csv`; this file is the human-readable grouped index.

> Run 3/4 additions (26): HARP, influence-Walsh rotations, pQuant, LC-QAT, extreme-lowbit-reasoning, BWLA, "fitting is not enough", iFairy, Fairy2i, "1-bit wonder", ICQuant, TZ-LLM, Platinum, Vec-LUT, TOM, TeLLMe-v2, PIM-AI, resource-efficient-LMs review, BitMar, R2Q, EdgeRazor, RSR-core, TeTRA-VPR, Ternary-Mamba, TernaryCLIP, extra-RMSNorm-1.58. Bad ID caught + removed: `2408.15962` (TermNet was a confabulated entry — that arXiv id is an unrelated math-physics paper).

## Foundational — BitNet lineage

| local_file | arXiv / venue | title | first author |
|---|---|---|---|
| 2023_Wang_bitnet-scaling-1bit-transformers.pdf | 2310.11453 | BitNet: Scaling 1-bit Transformers for LLMs | H. Wang (MSR) |
| 2025_Wang_bitnet-1bit-pretraining-JMLR.pdf | JMLR 26 (2025) 1-29 | BitNet: 1-bit Pre-training for LLMs | H. Wang |
| 2024_Ma_era-of-1bit-llms-bitnet-b1.58.pdf | 2402.17764 | The Era of 1-bit LLMs: All LLMs are in 1.58 Bits | S. Ma |
| 2025_Ma_bitnet-b1.58-2b4t-tech-report.pdf | 2504.12285 | BitNet b1.58 2B4T Technical Report | S. Ma |
| 2024_Wang_bitnet-a4.8-4bit-activations.pdf | 2411.04965 | BitNet a4.8: 4-bit Activations for 1-bit LLMs | H. Wang |
| 2025_Wang_bitnet-v2-native-4bit-hadamard.pdf | 2504.18415 | BitNet v2: Native 4-bit Activations w/ Hadamard | H. Wang |

## Training / analysis / theory

| local_file | arXiv | title | first author |
|---|---|---|---|
| 2024_Nielsen_bitnet-b1.58-reloaded.pdf | 2407.09527 | BitNet b1.58 Reloaded: SOTA Also on Smaller Networks | J. Nielsen (SDU) |
| 2024_Nielsen_when-are-1.58-bits-enough.pdf | 2411.05882 | When are 1.58 bits enough? A Bottom-up Exploration | J. Nielsen |
| 2025_Nielsen_continual-qat-pretraining-16bit-to-1.58bit.pdf | 2502.11895 | Continual QA Pre-Training: when to transition 16→1.58-bit | J. Nielsen |
| 2025_Tu_rethinking-1bit-optimization-pretrained-llms.pdf | 2508.06974 | Rethinking 1-bit Optimization Leveraging Pre-trained LLMs | Z. Tu (Huawei) |
| 2025_Tabesh_CAGE-curvature-aware-gradient-estimation.pdf | 2510.18784 (MLSys'26) | CAGE: Curvature-Aware Gradient Estimation for QAT | S. Tabesh (ISTA) |

## Inference systems / kernels / hardware

| local_file | arXiv | title | first author |
|---|---|---|---|
| 2024_Wang_1bit-ai-infra-1.1-bitnet-cpp.pdf | 2410.16144 | 1-bit AI Infra Part 1.1: Fast & Lossless BitNet b1.58 Inference on CPUs | J. Wang (MSR) |
| 2025_Wang_bitnet-cpp-efficient-edge-inference-ternary.pdf | 2502.11880 | Bitnet.cpp: Efficient Edge Inference for Ternary LLMs | J. Wang |
| 2024_Malekar_matmul-or-no-matmul-era-1bit-llms.pdf | 2408.11939 | MatMul or No MatMul in the Era of 1-bit LLMs | J. Malekar (USC) |
| 2026_Zuo_FairyFuse-multiplication-free-cpu-fused-ternary.pdf | 2604.20913 | FairyFuse: Multiplication-Free LLM Inference on CPUs via Fused Ternary Kernels | F. Zuo (BMW) |

## Compression toward 1-bit — PTQ / QAT / distillation

| local_file | arXiv | title | first author |
|---|---|---|---|
| 2024_Xu_onebit-extremely-lowbit-llms.pdf | 2402.11295 | OneBit: Towards Extremely Low-bit LLMs | Y. Xu (HIT) |
| 2024_Huang_billm-ptq-limit.pdf | 2402.04291 | BiLLM: Pushing the Limit of PTQ for LLMs | W. Huang (HKU) |
| 2023_Yuan_pb-llm-partially-binarized.pdf | 2310.00034 | PB-LLM: Partially Binarized LLMs | Y. Shang / Z. Yuan |
| 2024_Ma_fbi-llm-fully-binarized.pdf | 2407.07093 | FBI-LLM: Fully Binarized LLMs from Scratch via Autoregressive Distillation | L. Ma (MBZUAI) |
| 2024_Du_bitdistiller.pdf | 2402.10631 | BitDistiller: Sub-4-Bit LLMs via Self-Distillation | D. Du (HKUST-GZ) |
| 2024_Chen_efficientqat.pdf | 2407.11062 | EfficientQAT: Efficient Quantization-Aware Training for LLMs | M. Chen (HKU) |
| 2026_Zhao_TWLA-ternary-weights-lowbit-activations-ptq.pdf | 2606.13054 | TWLA: Ternary Weights & Low-Bit Activations for LLMs via PTQ | Z. Zhao (Houmo AI) |
| 2025_Huang_Tequila-trapping-free-ternary-quantization.pdf | 2509.23809 | Tequila: Trapping-free Ternary Quantization for LLMs | H. Huang (CityU HK / Tencent) |
| 2025_Hoang_rethinking-output-alignment-1bit-ptq.pdf | 2512.21651 | Rethinking Output Alignment for 1-bit PTQ of LLMs | H. A. Dung (Monash) |
| 2026_Song_LBLLM-lightweight-binarization-3stage-distillation.pdf | 2604.19167 | LBLLM: Lightweight Binarization of LLMs via Three-Stage Distillation | S. Song (CASIA) |

## New bit-widths / sparsity coupling

| local_file | arXiv | title | first author |
|---|---|---|---|
| 2026_Huang_Sherry-1.25bit-ternary-fine-grained-sparsification.pdf | 2601.07892 | Sherry: Hardware-Efficient 1.25-Bit Ternary Quantization via Fine-grained Sparsification | H. Huang (CityU HK / Tencent) |
| 2026_Zhang_sparse-bitnet-semi-structured-sparsity.pdf | 2603.05168 | Sparse-BitNet: 1.58-bit LLMs are Naturally Friendly to Semi-Structured Sparsity | Zhang et al. (MSR + PKU) |

## Training theory — beyond STE

| local_file | arXiv / venue | title | first author |
|---|---|---|---|
| 2024_Malinovskii_pv-tuning-beyond-ste.pdf | 2405.14852 · NeurIPS 2024 (oral) | PV-Tuning: Beyond Straight-Through Estimation for Extreme LLM Compression | V. Malinovskii (Yandex / ISTA) |

## Multimodal / applications / extensions

| local_file | arXiv | title | first author |
|---|---|---|---|
| 2025_Wang_bitvla-1bit-vision-language-action.pdf | 2506.07530 | BitVLA: 1-bit Vision-Language-Action Models for Robotics Manipulation | H. Wang (CAS) |
| 2024_Sundaram_llavaolmobitnet1b-ternary-llm-multimodal.pdf | 2408.13402 | LLaVaOLMoBitnet1B: Ternary LLM goes Multimodal | J. Sundaram (Intel) |

## Background — classic BNN / STE

| local_file | arXiv | title | first author |
|---|---|---|---|
| 2013_Bengio_estimating-propagating-gradients-STE.pdf | 1308.3432 | Estimating or Propagating Gradients Through Stochastic Neurons (STE) | Y. Bengio |
| 2015_Courbariaux_binaryconnect.pdf | 1511.00363 | BinaryConnect: Training DNNs with Binary Weights | M. Courbariaux |
| 2016_Rastegari_xnor-net.pdf | 1603.05279 | XNOR-Net: ImageNet Classification Using Binary CNNs | M. Rastegari |
| 2020_Bai_binarybert.pdf | 2012.15701 | BinaryBERT: Pushing the Limit of BERT Quantization | H. Bai (CUHK) |
| 2022_Qin_bibert.pdf | 2203.06390 (ICLR'22) | BiBERT: Accurate Fully Binarized BERT | H. Qin (Beihang) |

## Positioning — prior surveys (competitors)

| local_file | arXiv / venue | title | first author |
|---|---|---|---|
| 2024_Gong_survey-low-bit-llms.pdf | 2409.16694 · Neural Networks 192 (2025) 107856 | A Survey of Low-bit LLMs: Basics, Systems, and Algorithms | R. Gong (Beihang) |
| 2025_Liu_survey-binary-neural-networks-llm.pdf | 2502.19008 | Binary Neural Networks for LLM: A Survey | L. Liu (OPPO) |

## Non-paper artifacts — snapshots in `_web/`

| file | source | use |
|---|---|---|
| _web/2026-09-03_microsoft-BitNet_readme.md | github.com/microsoft/BitNet | §6 systems; covers BitNet-embedding + VibeASR.cpp releases |
| _web/2026-09-03_bitnet-b1.58-2B-4T_hf-card.md | huggingface.co/microsoft/bitnet-b1.58-2B-4T | §1/§6/§9 headline efficiency + benchmark numbers |
| _web/2026-09-03_falcon-edge_hf-blog.md | huggingface.co/blog/tiiuae/falcon-edge | §8 non-Microsoft native 1-bit; model inventory |

---

## EXCLUDED under R1 — no downloadable OA copy → not cited anywhere in the survey

| work | why excluded |
|---|---|
| **PT-BitNet** (Guo et al., "Scaling up the 1-Bit LLM with PTQ", Neurocomputing 2025 / SSRN 4987078) | Closed at ScienceDirect; SSRN blocks direct PDF (403); no arXiv preprint. |

If it later appears in open access, download it and move it up into the corpus.
*(Resolved 2026-09-03: "native ternary encoding" is arXiv 2604.03336 "NativeTernary" — now archived, see run-1 additions.)*

## EXCLUDED on the 20% re-screen (2026-09-06) — failed IC-1 / IC-2 on second read

| work | why excluded |
|---|---|
| **Scaling Law for Quantization-Aware Training** (Chen et al., arXiv:2505.14302, added run 2) | PDF moved to `_excluded/`. The paper is a **W4A4** QAT scaling-law study: it neither concerns 1-bit/1.58-bit models nor commits to an effective weight precision of two bits or fewer (EC-2), and it is cited nowhere in the survey prose. Swept in on a broad "QAT + scaling law" query in run 2; caught by the delayed re-screen (Section 3.8). Corpus 141 → 140 rows. |

---

## Search run 1 additions (2026-09-03) — 33 papers

Grouped; `local_file` = `<year>_<author-or-slug>_<slug>.pdf` in this folder. Coding into `../data/inventory.csv` pending.

**Native training / scaling / theory**
- 2406.02528 — Scalable MatMul-free Language Modeling (Zhu et al., NeurIPS 2024)
- 2407.12327 — Spectra: Pretraining Ternary LMs at Scale (Kaushal et al.) · 2506.23025 — Spectra 1.1
- 2407.10969 — Q-Sparse (Microsoft) · 2411.01663 — Unlocking the Theory Behind Scaling 1-Bit NNs (Daliri)
- 2412.04787 — Direct Quantized Training w/ Stochastic Rounding (ACML 2025) · 2308.06744 — Token-Scaled Logit Distillation for Ternary Generative LMs

**Compression toward ≤1-bit (PTQ / QAT / binary)**
- 2408.01803 STBLLM · 2410.03129 ARB-LLM (ICLR 2025) · 2402.11960 DB-LLM · 2406.12311 BinaryMoS
- 2504.05352 Binary W+A via PTQ · 2506.12040 BTC-LLM · 2502.13179 PTQ1.61 · 2502.01705 Progressive Binarization + Semi-Structured Pruning
- 2505.22811 Multi-Boolean LLMs · 2505.18724 LoTA-QAF · 2602.05367 RaBiT · 2602.05269 HGF (stabilizing 1.58-bit)
- 2601.20745 HESTIA · 2602.06694 NanoQuant · 2606.26650 CAT-Q · 2512.00862 HBLLM

**Systems / kernels / hardware (ternary-specific)**
- 2411.06360 Efficient MatMul for Binary/Ternary NNs · 2504.01994 PIM-LLM · 2509.08542 BitROM · 2509.13765 TENET · 2510.03275 SDQ-LLM

**Extensions / theory / robustness**
- 2606.25674 BitNet Text Embeddings (Microsoft) · 2411.11843 Bi-Mamba (TMLR 2025) · 2604.03336 NativeTernary
- 2606.22249 Expressive Power of Weight Quantization in LLMs · 2408.04585 Resilient & Efficient LLMs (adversarial robustness)

---

## Search run 2 additions (2026-09-03) — 30 papers (BitNet b1.58 forward-citation snowball)

**Training / scaling / STE:** 2502.05003 QuEST · 2502.02631 ParetoQ · 2411.17691 Undertrained-LLMs scaling · 2411.04330 Scaling Laws for Precision · 2505.14302 Scaling Law for QAT · 2510.23926 STE + zeroth-order · 2502.16440 Compression Scaling Laws · 2602.02707 Every Bit Counts · 2510.13998 BitNet Distillation
**Ternary/binary PTQ + native:** 2509.16989 PTQTP · 2510.03267 PT²-LLM · 2602.07374 TernaryLM · 2505.11076 Double Binary Factorization · 2506.13771 LittleBit · 2507.01027 DBellQuant · 2412.05225 BEExformer
**Modalities / apps / security:** 2506.14435 MoTE · 2506.03515 BitTTS · 2505.21245 One-bit ASR · 2504.06298 VLM ternarization · 2411.15438 Ternary Weight Embedding · 2506.00528 Ultra-Quantisation · 2411.13757 GenBFA
**Systems / HW:** 2511.13676 T-SAR · 2502.16473 TerEffic · 2504.16266 TeLLMe · 2605.06485 Litespark · 2505.06461 CPU>GPU on-device · 2504.02118 LLMPi
**Positioning:** 2505.01043 Low-Precision Training of LLMs (**IEEE TPAMI 2025** — 3rd overlapping survey)
