> **Note (2026-09-04):** authoritative per-paper record is now `inventory.csv` (126 rows). Run-3/4
> screening decisions are logged in `../protocol/search-log.md`. This file is the historical trail
> of runs 1-2 plus the deferred/post-cutoff/excluded lists.

# Candidate list — search run 1 (2026-09-03)

Screening decisions from the seed-expansion pass. Full protocol: `../survey-protocol.md`.
Decision codes: **ARCHIVED** (IC pass, PDF in `papers/`) · **POST-CUTOFF** (→ living appendix) ·
**PENDING** (borderline, retrieve full text in run-2 screening) · **EXCLUDED** (+EC code).

The 37 pre-search seeds are in `../papers/INDEX.md` and not repeated here.

---

## ARCHIVED this pass — 33 new (in-window 2023-01 … 2026-06, IC-1..5 pass)

### Native training / scaling / theory
| arXiv | title | note |
|---|---|---|
| 2406.02528 | Scalable MatMul-free Language Modeling (Zhu et al., NeurIPS 2024) | ternary BitLinear + no matmul; core |
| 2407.12327 | Spectra: Surprising Effectiveness of Pretraining Ternary LMs at Scale (Kaushal et al.) | TriLM suite; largest open non-MSFT ternary family |
| 2506.23025 | Spectra 1.1: Scaling Laws and Efficient Inference for Ternary LMs | scaling-law evidence for §5.6 |
| 2407.10969 | Q-Sparse: All LLMs can be Fully Sparsely-Activated (Microsoft) | sparsity companion to BitNet line |
| 2411.01663 | Unlocking the Theory Behind Scaling 1-Bit Neural Networks (Daliri et al.) | theory; §5 |
| 2412.04787 | Direct Quantized Training of LMs with Stochastic Rounding (ACML 2025) | STE alternative; §5.3 |
| 2308.06744 | Token-Scaled Logit Distillation for Ternary Weight Generative LMs | 2023 ternary-LM distillation |

### Compression toward ≤1-bit (PTQ / QAT / binary)
| arXiv | title | note |
|---|---|---|
| 2408.01803 | STBLLM: Breaking the 1-Bit Barrier w/ structural binarization (<1-bit) | §6.3 |
| 2410.03129 | ARB-LLM: Alternating Refined Binarizations (ICLR 2025) | §6.3 |
| 2402.11960 | DB-LLM: Accurate Dual-Binarization for Efficient LLMs | §6.3 |
| 2406.12311 | BinaryMoS / Mixture of Scales: token-adaptive binarization | §6.2 |
| 2504.05352 | Achieving Binary Weight and Activation for LLMs using PTQ | §6.3 / §7 |
| 2506.12040 | BTC-LLM: sub-1-bit via learnable transform + binary codebook | §6.3 |
| 2502.13179 | PTQ1.61: Push the Real Limit of Extremely Low-Bit PTQ | §6.3 |
| 2502.01705 | Progressive Binarization with Semi-Structured Pruning for LLMs | §6.3 / §4.7 |
| 2505.22811 | Highly Efficient & Effective LLMs with Multi-Boolean Architectures | §6.3 |
| 2505.18724 | LoTA-QAF: Lossless Ternary Adaptation for QA Fine-Tuning | §5.5 |
| 2602.05367 | RaBiT: Residual-Aware Binarization Training for LLMs | §6.3 |
| 2602.05269 | HGF: Hybrid Gated Flow — stabilizing 1.58-bit LLMs via low-rank correction | §5.1 stability |
| 2601.20745 | HESTIA: Hessian-Guided Differentiable QAT for Extremely Low-Bit LLMs | §5.3 |
| 2602.06694 | NanoQuant: Efficient Sub-1-Bit Quantization of LLMs | §6.3 |
| 2606.26650 | CAT-Q: Cost-efficient & Accurate Ternary Quantization for LLMs | §6.3 |
| 2512.00862 | HBLLM: Wavelet-Enhanced High-Fidelity 1-Bit Quantization for LLMs | §6.3 |

### Systems / kernels / hardware (ternary / 1.58-bit specific)
| arXiv | title | note |
|---|---|---|
| 2411.06360 | Efficient Matrix Multiplication Algorithm for Binary & Ternary NNs | §6.1 |
| 2504.01994 | PIM-LLM: Hybrid PIM Architecture for 1-bit LLMs | §6.4 |
| 2509.08542 | BitROM: Weight Reload-Free CiROM for 1.58-bit LLM Inference | §6.4 |
| 2509.13765 | TENET: Sparsity-Aware LUT-Centric Architecture for Ternary LLM Inference on Edge | §6.4 |
| 2510.03275 | SDQ-LLM: Sigma-Delta Quantization for 1-bit LLMs of any size | §6.1 / §4.3 |

### Extensions / theory / robustness
| arXiv | title | note |
|---|---|---|
| 2606.25674 | BitNet Text Embeddings (Microsoft) | §8.3 — the paper behind the HF embedding release |
| 2411.11843 | Bi-Mamba: Towards Accurate 1-Bit State Space Models (TMLR 2025) | §4.6 — 1-bit beyond attention |
| 2604.03336 | NativeTernary: self-delimiting binary encoding for ternary weights | §3 / storage layer; **un-excludes** the earlier placeholder |
| 2606.22249 | On the Expressive Power of Weight Quantization in LLMs | §5.6 / §10 capacity ceiling |
| 2408.04585 | Towards Resilient & Efficient LLMs: efficiency, performance, adversarial robustness | §10 security |

---

## POST-CUTOFF (> 2026-06-30) → living appendix, NOT the systematic review

| arXiv | date | title |
|---|---|---|
| 2609.01962 | 2026-09-02 | Post-Training Ternarization of Qwen3-4B |
| 2608.28809 | 2026-08-28 | Capability-Stratified Degradation in Ternary Language Models |
| 2608.26206 | 2026-08-26 | Ankhdjet: compiler for mask-programmed ternary compute-in-ROM |
| 2608.01078 | 2026-08-02 | Attend to Your Own Thoughts: PTQ of Reasoning LLMs via 1.58-Bit Quantization |
| 2607.21075 | 2026-07-23 | VibeVoice-ASR-BitNet Technical Report |

---

## PENDING full-text screening (run 2) — borderline, likely consolidate to a few citations

HW accelerators (many → one §6.4 paragraph): 2603.27462 RSR-core · 2511.21910 Platinum · 2512.06443 Vec-LUT · 2602.20662 TOM · 2604.25183 LUT-accel HW-gen · 2604.27396 / 2605.00320 VitaLLM · 2602.06252 D-Legion · 2607.03652 ELiTeFormer.
Neuromorphic / spiking / SSM: 2503.18002 Loihi 2 · 2605.13859 BiSpikCLM · 2606.10932 Density-Field SSM 1-bit distill · 2512.23145 Reservoir MatMul-free.
Applications / eval: 2605.29705 BitTP (trajectory) · 2604.24273 BitRL (RL on edge) · 2603.25813 MAGNET · 2512.15335 Bits for Privacy (§10) · 2606.00365 SPARQLe (activation repr) · 2503.12211 Changing Base (GPU matmul alt).
Venue-only (find OA copy): MemeBQ (AAAI 2026 OJS).

---

## EXCLUDED — off-topic false positives from `abs:` fuzzy match (EC-1 / not-a-topic)

2606.30346 (Kesten-Stigum boundary) · 2603.10054 (Ricci curvature) · 2606.22621 (memristive crossbar, not LLM) · 2607.18476 (answer diversity) · 2403.18403 (crypto function ID) · 2605.31481 (rigid-body dynamics) · 2606.29705-adjacent physics hits.

## RESOLVED
- `native-ternary-encoding` — previously EXCLUDED "no paper" → **found & archived** (2604.03336). Removed from EXCLUDED in `../papers/INDEX.md` and plan §10.
- PT-BitNet — **still EXCLUDED** (no OA copy; not seen in this pass).

---

# Search run 2 additions (2026-09-03) — forward-citation snowball on BitNet b1.58

## ARCHIVED this pass — 30 new (→ 100 PDFs total)

### Training / scaling laws / STE theory
| arXiv | title | §use |
|---|---|---|
| 2502.05003 | QuEST: Stable Training of LLMs with 1-Bit Weights and Activations (ICML 2025) | §5.1 native W1A1 |
| 2502.02631 | ParetoQ: Improving Scaling Laws in Extremely Low-bit LLM Quantization (NeurIPS 2025) | §5.6 |
| 2411.17691 | Low-Bit Quantization Favors Undertrained LLMs: Scaling Laws w/ 100T tokens | §5.6 / §10 — the undertraining critique |
| 2411.04330 | Scaling Laws for Precision (Kumar et al., ICLR 2025) | §5.6 |
| 2505.14302 | Scaling Law for Quantization-Aware Training | §5.6 |
| 2510.23926 | Improving the Straight-Through Estimator with Zeroth-Order Information (NeurIPS 2025) | §5.3 |
| 2502.16440 | Compression Scaling Laws: Unifying Sparsity and Quantization | §5.6 |
| 2602.02707 | Every Bit Counts: Precision–Expressivity Tradeoffs in Quantized Transformers | §5.6 / §10 |
| 2510.13998 | BitNet Distillation (Microsoft) | §5.4 — the "BDF" route |

### Ternary / binary PTQ + native
| arXiv | title | §use |
|---|---|---|
| 2509.16989 | PTQTP: Post-Training Quantization to Trit-Planes for LLMs | §6.3 |
| 2510.03267 | PT²-LLM: Post-Training Ternarization for LLMs | §6.3 |
| 2602.07374 | TernaryLM: native 1.5-bit LM w/ adaptive layer-wise scaling | §4 / §6 |
| 2505.11076 | Addition is almost all you need: double binary factorization | §6.3 |
| 2506.13771 | LittleBit: Ultra Low-Bit Quantization via Latent Factorization | §6.3 |
| 2507.01027 | DBellQuant: Double-Bell Transformation for LLM PT binarization | §6.3 |
| 2412.05225 | BEExformer: Binarized Transformer with Early Exits | §4.6 |

### Modalities / applications / security
| arXiv | title | §use |
|---|---|---|
| 2506.14435 | MoTE: Mixture of Ternary Experts for Multimodal LLMs | §4.5 / §8.4 |
| 2506.03515 | BitTTS: Compact TTS using 1.58-bit Quantization (Interspeech 2025) | §8 |
| 2505.21245 | Towards One-bit ASR: Extremely Low-bit Conformer Quantization (Interspeech 2025) | §8 |
| 2504.06298 | Ternarization of Vision-Language Models for edge devices | §8.4 |
| 2411.15438 | Efficient Ternary Weight Embedding Model | §8.3 |
| 2506.00528 | Ultra-Quantisation: Embedding Search via 1.58-bit Encodings | §8.3 / §8.5 |
| 2411.13757 | GenBFA: Bit-Flip Attacks on LLMs | §10 security |

### Systems / hardware
| arXiv | title | §use |
|---|---|---|
| 2511.13676 | T-SAR: CPU-Only Ternary LLM Inference via SIMD ALU reorganization | §6.2 |
| 2502.16473 | TerEffic: Highly Efficient Ternary LLM Inference on FPGA | §6.4 |
| 2504.16266 | TeLLMe: Energy-Efficient Ternary LLM Accelerator on Edge FPGAs | §6.4 |
| 2605.06485 | Litespark: Ultra-Fast SIMD Framework for Ternary (1.58-bit) LMs on CPU | §6.2 |
| 2505.06461 | Challenging GPU Dominance: When CPUs Outperform for On-Device LLM Inference | §6.2 |
| 2504.02118 | LLMPi: Optimizing LLMs for High-Throughput on Raspberry Pi | §6.2 / §8.1 |

### Positioning (prior surveys — add to §1 competitive landscape)
| arXiv | title | note |
|---|---|---|
| 2505.01043 | Low-Precision Training of LLMs: Methods, Challenges, Opportunities | **IEEE TPAMI 2025** — a 3rd overlapping survey; must differentiate |

## DEFERRED to run-3 screening (identified, real, not yet retrieved) — ~40
HARP 2605.29843 · Influence-Inspired Spectral Rotations 2605.25203 · pQuant 2602.22592 · LC-QAT 2606.10531 · Extreme Low-Bit Inference in Reasoning Models 2606.02011 · BWLA 2605.00422 · MoBiE (Mixture of Binary Experts) 2604.06798 · Fitting Is Not Enough (smoothness) 2605.08894 · iFairy 2508.05571 / Fairy2i 2512.02901 (complex {±1,±i}) · 1-Bit Wonder (K-Means QAT) 2602.15563 · Squeeze10-LLM 2507.18073 · ICQuant 2505.00850 · Ternary Mamba 2606.18114 · TeTRA-VPR 2503.02511 · 1-bit top-tagging 2508.07431 · TZ-LLM 2511.13717 · ternary-accelerator cluster (RSR-core 2603.27462, Platinum 2511.21910, Vec-LUT 2512.06443, TOM 2602.20662, TeLLMe v2 2510.15926, HoloLUT, Omni-LUT, SingularBit, PIM-AI 2411.17309) · MiniCPM4 2506.07900 (edge, borderline) · "Resource-Efficient Language Models: Quantization" 2505.08620.

## POST-CUTOFF (>2026-06-30) → living appendix — run-2 additions
QTEA 2609.00224 · ExTernD 2607.13511 · A Target-Centric Survey of QAT 2608.29667 · BiSCo-LLM 2607.08643 · GSRQ (sub-1-bit KV) 2607.01065 · Cross-Layer Error Compensation 2607.14630 · Low-Rank Ternary Adaptation 2608.24469.
