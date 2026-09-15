# Table 7.2 — Normalised comparison of 1-bit / ternary LLM methods

Built 2026-09-04 from `results.csv` + full-text extraction (`scratchpad/results*.txt` archived in `../protocol/`).
All numbers are **author-reported** unless a Section-9 re-measurement replaces them. "Eff. bits" is a
**consistent effective-bits-per-weight** figure = nominal code width + amortised scales / masks / codebooks
(see notes); where a paper and an independent accounting disagree, both are given (e.g. BiLLM 1.08 / 2.88).
Perplexity is WikiText-2 unless noted. "ZS avg" = mean zero-shot over that paper's suite (suites differ —
5 vs 7 tasks — so cross-row ZS gaps < ~2 pts are not meaningful).

## A. Native / from-scratch models

| method | id | repr | W/A | eff. bits | accuracy (reported) | efficiency (reported) | ev |
|---|---|---|---|---|---|---|---|
| BitNet b1 | Wang2025-BitNetJMLR | binary | W1A8 | 1.0 | competitive vs 8-bit PTQ + FP16 baselines | add-only matmul | 5 |
| BitNet b1.58 | Ma2024-BitNetB158 | ternary | W1.58A8 | 1.58 | matches FP16 LLaMA @3B (ppl + ZS); gap narrows to 7B | 3B: 2.71x faster, 3.55x less GPU mem; 70B: 4.1x, 8.9x throughput; ~71x less matmul energy (7nm) | 5 |
| BitNet b1.58 2B4T | Ma2025-BitNet2B4T | ternary | W1.58A8, 4T tok | 1.58 | ZS avg 54.19 (Qwen2.5-1.5B 55.23); GSM8K 58.38 > 56.79; MMLU 53.17 < 60.25 | 0.4 GB non-emb; 29 ms CPU decode; 0.028 J/decode (Qwen ref 2.6 GB / 65 ms / 0.347 J) | 5 |
| BitNet a4.8 | Wang2024-BitNetA48 | ternary | W1.58A4 hybrid + 3-bit KV | 1.58 | ~= b1.58 avg (std err 1.06 %) | 55 % params active; INT4 kernels; 3-bit KV negligible loss | 4 |
| BitNet v2 | Wang2025-BitNetV2 | ternary | W1.58A8 / native A4 (Hadamard) | 1.58 | +0.16 / 0.49 / 0.61 % avg over b1.58 @1.3 / 3 / 7B; native A4 > a4.8 downstream @3-7B; > QuaRot / SpinQuant @W1.58A4 | native 4-bit compute path | 5 |
| Spectra / TriLM | Kaushal2024-Spectra | ternary | W1.58A16, 300B tok | 1.58 | TriLM 3.9B matches FloatLM 3.9B across suite (higher ppl); > QuantLM & FloatLM per-bit @>1B | ~6x smaller in bits; max speedup plateau ~10x (vs 4x INT4); toxicity == FloatLM 3.9B | 5 |
| Spectra 1.1 | Vaidhya2025-Spectra11 | ternary | W1.58, up to 1.2T tok | 1.6 (TQ1) / 2.0 (TQ2) | > Spectra @ matched size (MMLU); data > params | TriRun GPU 4.9x e2e @70B (L40S), ~78x layer high-batch; CPU TQ1/TQ2 packing on M4 | 5 |
| MatMul-free LM | Zhu2024-MatmulFree | ternary | W1.58A8, GLA (no attn matmul) | 1.58 | ~= Transformer++ up to 2.7B; gap narrows with scale | −61 % training mem; >10x inference mem; FPGA + neuromorphic impl | 5 |
| FBI-LLM | Ma2024-FBILLM | binary | W1A16 (AR distillation) | 1.0 | ~ matches FP16 ppl @130M / 1.3B / 7B | fully-open models + data | 4 |
| Bi-Mamba | Tang2024-BiMamba | binary | W1A16 SSM (AR distillation) | 1.0 | ~= FP16 @780M / 1.3B / 2.7B; > PTB-Mamba & BAT-Transformer | linear-complexity low-bit | 4 (TMLR) |
| Direct Quantized Training | Zhao2024-DQT | ternary | W-ternary/8, stochastic rounding, no STE | 1.58–8 | 8-bit DQT surpasses BitNet b1.58 @1B; ternary-only feasible | lower training memory (no shadow weights) | 4 |
| iFairy | Wang2025-iFairy | complex {±1,±i} | W2A8 native | 2.0 | 700M avg ppl 11.13 (BitNet b1.58 11.51 repro / 12.87 rep.); 1.3B 10.14 (11.29); full-precision iFairy 700M 10.08 < FP16 LLaMA 12.33 | mult-free accumulation | 3 |
| TernaryLM | Nargund2026-TernaryLM | ternary | W1.5, adaptive layer scaling | 1.5 | native 1.5-bit LM (small scale) | — | 3 |

## B. QAT / fine-tuning toward ≤ 2-bit

| method | id | repr | eff. bits | accuracy (reported) | efficiency / cost | ev |
|---|---|---|---|---|---|---|
| OneBit | Xu2024-OneBit | binary + value vectors | ~1.3 | ≥ 81 % of FP16 perf on LLaMA 7-13B | robust QAT | 4 |
| BinaryMoS | Jo2024-BinaryMoS | binary + token-adaptive scales | ~1.0 | > binarisation methods; > 2-bit methods | ~ static-binary size | 4 |
| QuEST | Panferov2025-QuEST | binary/uniform | 1.0 (W1A1) | stable scaling laws W1A1 … W4A4; optimal at 4-bit | GPU kernels provided | 4 |
| BitDistiller | Du2024-BitDistiller | uniform 2-3 bit | 2–3 | 2-bit: +3.54 % avg over LLM-QAT, +12.43 % over best PTQ; best 3/2-bit code-gen scaling | fewer data + resources | 4 |
| EfficientQAT | Chen2024-EfficientQAT | uniform 2-4 bit | 2–4 | 2-bit Llama2-70B: 69.48 vs 72.41 FP (<3 pt); ~5 pt over uniform 2-bit | 2-bit 70B on 1×A100-80GB in 41 h | 4 |
| PV-Tuning | Malinovskii2024-PVTuning | 1-2-bit VQ | ~2 | SOTA 1-2-bit; first Pareto-optimal 2-bit Llama-2 | same calibration data as base method; kernel-compatible | 5 (NeurIPS oral) |
| LC-QAT | Wang2026-LCQAT | 2-bit VQ | ~2 | matches / beats SQ + VQ QAT with 0.1–10 % of training data | custom CUDA 1.68x vs FP16 | 4 (ICML'26) |
| CAGE | Tabesh2025-CAGE | uniform W3A3/W4A4 | 3–4 | halves quantisation error vs QuEST/MXFP4 on GSM8K/HS/WG (Llama-3.2-3B); W3A3 = prior W4A4 | optimizer-agnostic; convergence proof | 4 (MLSys'26) |
| HESTIA | Wang2026-HESTIA | ternary (soft-to-hard) | 1.58 | Llama-3.2-1B ZS +5.39 % (0.519→0.547 vs Tequila); 3B +4.34 %; 10B-token HESTIA ~ 100B-token BitNet/Spectra | Hessian-trace temperature schedule | 3 |
| Tequila | Huang2025-Tequila | ternary | 1.58 | +>4 % ARC vs SoTA; <1 % gap to FP | 3.0x inference speedup; ~0 overhead | 4 |
| Sherry | Huang2026-Sherry | ternary 3:4-sparse | 1.25 | zero accuracy loss vs SoTA ternary (1B, LLaMA-3.2) | Intel i7-14700HX: 25 % bit savings, 10 % speedup | 4 |
| Sparse-BitNet | Zhang2026-SparseBitNet | ternary + N:M | 1.58 (+mask) | at 2:4 (50 % sparsity): BitNet +5.7 % ppl vs BF16 +18.8 % | up to 1.30x train + inference (6:8 sparse op) | 4 |
| Q-Sparse | Wang2024-QSparse | ternary/FP + top-K | 1.58 | ~40 % sparsity matches dense; optimal sparsity 61.25 % for 1.58-bit | inference-optimal sparse scaling law | 4 |
| RaBiT | You2026-RaBiT | binary residual (matmul-free) | 2.02 (nom. 2) | Llama2-7B ppl 5.78 (MBOK 6.99, DBF 6.10, QTIP-VQ 5.86); ZS avg 61.51 % > QTIP 58.97 %; Qwen3-4B 66.66 % | matmul-free execution | 3 |
| HGF | Anon2026-HGF | ternary + gated LoRA | 1.58 (+12–15 % mem) | recovers ~55 % of the BitNet↔FP16 gap (TinyStories, small models) | +12–15 % memory over ternary backbone | 2 |
| TSLD | Kim2023-TSLD | ternary | 1.58 | < 1.0 ppl degradation; improved CSQA + arithmetic | first ternary QAT of large generative LMs | 4 |
| BitNet Distillation | Wu2025-BitNetDistillation | ternary | 1.58 | ~ FP task performance (task-specific) | ~10x memory; ~2.6x CPU speedup | 4 |

## C. PTQ toward ≤ 2-bit (calibration only)

| method | id | repr | eff. bits | headline ppl / accuracy | notes | ev |
|---|---|---|---|---|---|---|
| BiLLM | Huang2024-BiLLM | binary (salient split) | 1.08 (paper) / **2.88** (metadata-strict) | 8.41 ppl LLaMA2-70B | binarise 7B in 0.5 h / 1 GPU | 5 (ICML) |
| PB-LLM | Shang2023-PBLLM | partial binary | 1.70 | recovers reasoning at low bit | salient + Hessian recon | 4 (ICLR) |
| ARB-LLM | Li2024-ARBLLM | binary (alt. refined) | ~1.1 | first binary PTQ to beat FP16 of same size | column bitmap | 4 (ICLR) |
| DB-LLM | Chen2024-DBLLM | 2-bit dual-binary | ~2 | 2-bit ppl 9.64 → 7.23 | +20 % compute reduction vs SoTA | 4 |
| PTQ1.61 | Zhao2025-PTQ161 | mixed-partial | **1.61** (mask 0.0002-bit) | LLaMA-7B ppl 12.50 | first true sub-2-bit PTQ | 4 (ACL) |
| PT2-LLM | Yan2025-PT2LLM | ternary | 1.58 | rivals SoTA 2-bit PTQ, lower memory | iterative ternary grid fitting; ~1 h | 4 (ICLR'26) |
| PTQTP | Xiao2025-PTQTP | dual trit-plane | ~1.58 | rivals 1.58-bit QAT | ~1 h vs 10-14 GPU-days; 4.63x decode vs FP16 | 4 |
| CAT-Q | Wang2026-CATQ | ternary | 1.58 | W1.58 ~ BitNet v1/v2 @100B tok using 512 calib samples; > TernaryLLM-8B (1T tok + KD) | 100,000x fewer tokens; scales to 235B incl MoE | 3 |
| HBLLM | Chen2025-HBLLM | binary (Haar wavelet) | 1.08 | LLaMA2-13B ppl 6.71; 1.22-2.48x FP16 ppl; retains 73.8-88.8 % QA | frequency decomposition | 3 |
| DBellQuant | Ye2025-DBellQuant | binary + A6 | ~1 (+A6) | LLaMA2-13B ppl 14.39 (BiLLM 21.35 weight-only); LLaMA2-7B 21.69 @A6 / 23.04 @A4 | +12 min vs BiLLM | 3 |
| BWLA | Zhao2026-BWLA | binary + A6 | ~1 (+A6) | first high-accuracy W1AX pure PTQ; Qwen3-32B ppl 11.92 @A6 (SoTA 38); +>70 % on 5 ZS | 3.26x speedup | 3 |
| binary W+A PTQ | Anon2025-BinaryWA-PTQ | W(1+1) + A(1-4) | ~2 (W2 eff.) | W2A4 LLaMA-7B ppl 8.58 / LLaMA2-7B 8.89 (FP 5.68 / 5.47) | 4-bit KV | 3 |
| ICQuant | Li2025-ICQuant | any + index-coded outliers | +0.3 overhead | 2.3 bits/wt beats 4-bit RTN; 2-bit Llama3-70B +130 % / +150 % over QTIP / QuIP# | 0.3-bit vs 1-bit outlier flag | 4 (COLM) |
| HARP | Zagitov2026-HARP | any + learned rotation | +0.02-0.08 (int8 packed) | best gains at 2-bit; Llama 1B-70B ppl improved over fixed RHT | Llama2-7B @2-bit 128 tok/s (RHT 142; FP16 61) | 3 |
| Double Binary Factorisation | Anon2025-DoubleBinaryFactorization | binary factors | any (scale vec +0.012) | > single-matrix binarisation; competitive with leading quant | 2-3.5x speedup @2-bit | 4 (TMLR'26) |
| Multi-Boolean | Anon2025-MultiBoolean | K Boolean kernels | ~2 (2 kernels) | close to FP16; > binarisation + 2-bit; 3-4 kernels optimal | Boolean-space optimisation, no FP latent | 4 (ICLR'26) |
| TWLA | Zhao2026-TWLA | ternary + A4 | 1.58 (+A4) | W1.58A4 accuracy retained | Kronecker rotation for outliers; e2e acceleration | 4 |
| LBLLM | Song2026-LBLLM | binary W(1+1) + A4 | ~2 (W2 eff.) | surpasses SoTA binarisation @W2A4; > CBQ W4A4 | 0.016B tokens, few dozen GPU-h, 1 GPU | 3 |

## D. Sub-1-bit

| method | id | eff. bits | headline | ev |
|---|---|---|---|---|
| STBLLM | Dong2024-STBLLM | < 1 nominal / **4.13** metadata-strict | first structural binarisation < 1-bit (N:M); beats other <1-bit binary; custom CUDA kernel | 4 (ICLR'25) |
| BTC-LLM | Gu2025-BTCLLM | 0.7-1.11 | binary baseline 6.06 ppl LLaMA2-7B (beats 2-bit); 0.7-bit 11.02 ppl @22x mem; +5.0 % over STBLLM @0.8-bit; W0.8A8 best (59.6 % mean acc) | 3 |
| NanoQuant | Chong2026-NanoQuant | 1-bit and sub-1-bit (genuine) | competitive with higher-BPW binary PTQ; approaches binary QAT with orders-of-magnitude less data | 3 |
| LittleBit | Lee2025-LittleBit | 0.1 | beats 0.7-BPW methods; Llama2-13B < 0.9 GB (31x); 11.6x inference speedup vs FP16 | 4 (NeurIPS'25) |

## E. Scaling / theory anchors (not model rows)

| work | id | finding |
|---|---|---|
| Scaling Laws for Precision | Kumar2024-ScalingLawsPrecision | low precision = fewer effective params; weight-precision gains saturate ~6-7 bits; PTQ degradation grows with pretraining data |
| QiD | Ouyang2024-QiDScaling | quantisation-induced degradation grows with training tokens (2-bit qLoss ~2.0 on 12B Pythia); 100T-token projection unfavourable for low-bit |
| ParetoQ | Liu2025-ParetoQ | unified 1-4 bit; learning transition between 2 and 3 bits; ternary / 2 / 3-bit share a frontier that beats 4-bit and binary; 600M ternary > prior 3B ternary SoTA |
| Compression Scaling Laws | Anon2025-CompressionScalingLaws | unified scaling law across sparsity + quantisation |
| Unlocking Theory of 1-bit NNs | Daliri2024-Theory1bit | kernel-limit proof of a scaling law for 1-bit networks |

## Effective-bits accounting notes

- **Native ternary** = 1.58 nominal; packed formats TQ1 ≈ 1.6, TQ2 = 2.0 (Spectra 1.1); Sherry 3:4 = 1.25.
- **Salient-split binary PTQ** headline figures (BiLLM 1.08, ARB-LLM ~1.1) count only the code; a strict
  accounting that includes group-wise scales and bitmaps puts BiLLM at ~2.88 and STBLLM at ~4.13 BPW
  (NanoQuant, Table 4) — the table shows both.
- **Outlier / rotation overhead**: index-coding +0.3 (ICQuant); learned-rotation int8 params +0.02-0.08 (HARP);
  binary-flag outlier marking +1.0; semi-structured pruning mask +0.25.
- **Residual / factor overhead**: RaBiT nominal 2 → 2.02 effective; DBF scaling vectors +0.012.
- Rows marked "+A6" / "+A4" quantise activations too; their weight eff-bits is ~1 but end-to-end compute
  precision is set by the activation.
