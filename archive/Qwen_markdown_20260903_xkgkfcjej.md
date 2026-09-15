# Survey Research Paper: 1-Bit Large Language Models

## Full Planning Document for 10+ Impact Factor Journal Publication

\---

## 1\. TARGET JOURNALS (10+ Impact Factor, Open Access Friendly)

|Journal|IF (approx.)|Notes|
|-|-|-|
|**Nature Machine Intelligence**|\~25|High prestige; needs broad AI impact narrative|
|**IEEE Communications Surveys \& Tutorials**|\~34|Excellent for comprehensive surveys|
|**ACM Computing Surveys (CSUR)**|\~23|Premier venue for CS surveys|
|**Information Fusion**|\~18|Good if framed around fusion of quantization + architecture|
|**Artificial Intelligence (Elsevier)**|\~14|Classic AI journal|
|**Journal of Machine Learning Research (JMLR)**|\~6–7\*|\*Borderline; very high prestige though|
|**IEEE TPAMI**|\~24|If framed with pattern recognition angle|
|**Transactions on Machine Learning Research (TMLR)**|\~7\*|\*Open access, growing prestige|

> \*\*Primary Target:\*\* \*ACM Computing Surveys\* or \*IEEE Communications Surveys \& Tutorials\*
> \*\*Backup Target:\*\* \*Information Fusion\* or \*Artificial Intelligence\*

\---

## 2\. PROPOSED TITLE (Options)

* **Option A:** *"One Bit Is All You Need: A Comprehensive Survey on 1-Bit Large Language Models"*
* **Option B:** *"From 32-Bit to 1-Bit: A Systematic Survey of Extreme Quantization for Large Language Models"*
* **Option C:** *"1-Bit Large Language Models: Architecture, Training, Inference, and Open Challenges — A Survey"*

> \*\*Recommendation:\*\* Option C (descriptive, keyword-rich, survey-signalling)

\---

## 3\. FULL PAPER OUTLINE

### Abstract (\~250–300 words)

* Motivation: LLM scaling crisis (memory, energy, cost)
* Emergence of 1-bit / ternary / binary weight models
* Scope of survey: architectures, training, inference, benchmarks, open problems
* Key finding / contribution statement
* Keywords: 1-bit LLM, binary neural network, ternary quantization, BitNet, model compression, efficient inference, quantization-aware training

\---

### 1\. Introduction (\~2,500 words)

#### 1.1 Motivation

* Exponential growth of LLM parameters (GPT-3 175B → GPT-4 \~1.8T → Llama-3 405B)
* Memory bottleneck: FP32/FP16 storage, GPU VRAM limits
* Energy and carbon cost of training and inference
* Edge/mobile deployment impossibility at full precision

#### 1.2 The Quantization Spectrum

* Brief taxonomy: FP32 → FP16 → INT8 → INT4 → INT2 → **1-bit / Ternary**
* Why 1-bit is the "holy grail" of compression
* Historical context: BinaryConnect (2015), XNOR-Net (2016) → modern 1-bit LLMs

#### 1.3 Scope and Contributions of This Survey

* What this survey covers vs. existing surveys on general quantization
* Taxonomy proposed
* Number of papers reviewed (aim for 150–250 references)

#### 1.4 Paper Organization

* Roadmap paragraph

> \*\*Key OA References for this section:\*\*
> - Ma et al., "The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits" (2024) — arXiv:2402.17764
> - Wang et al., "BitNet: Scaling 1-bit Transformers for Large Language Models" (2023) — arXiv:2310.11453
> - Ma et al., "Zero Quantization for Free" / various Microsoft 1-bit papers (arXiv)
> - Rastegari et al., "XNOR-Net" (2016) — arXiv:1603.05279
> - Courbariaux et al., "BinaryConnect" (2015) — arXiv:1511.00363

\---

### 2\. Background and Preliminaries (\~2,000 words)

#### 2.1 Transformer Architecture Recap

* Self-attention, FFN, LayerNorm, positional encoding
* Parameter distribution: where are the weights? (QKV, O-proj, FFN up/down/gate)

#### 2.2 Quantization Fundamentals

* Post-Training Quantization (PTQ) vs. Quantization-Aware Training (QAT)
* Symmetric vs. asymmetric quantization
* Per-tensor vs. per-channel vs. per-group quantization
* Ste function (Straight-Through Estimator)

#### 2.3 Binary and Ternary Representations

* 1-bit: weights ∈ {−1, +1} (binary)
* 1.58-bit: weights ∈ {−1, 0, +1} (ternary) — log₂(3) ≈ 1.58
* Activations: typically kept at INT8 or FP8
* Arithmetic shift: multiplication → addition (XNOR + popcount)

#### 2.4 Information-Theoretic Perspective

* Minimum bits per parameter (Shannon limit arguments)
* Lossless vs. lossy compression view

> \*\*Key OA References:\*\*
> - Vaswani et al., "Attention Is All You Need" (2017) — arXiv:1706.03762
> - Jacob et al., "Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference" (2018) — arXiv:1712.05877
> - Li et al., "Ternary Weight Networks" (2016) — arXiv:1605.04711

\---

3\. Taxonomy of 1-Bit LLM Approaches (\~1,500 words + FIGURE 1)

1-Bit LLM Methods
---

### ├── By Training Strategy

### │ ├── Quantization-Aware Training (QAT) from scratch

### │ │ ├── BitNet (2023)

### │ │ └── BitNet b1.58 (2024)

### │ ├── Post-Training Quantization (PTQ)

### │ │ ├── OneBit

### │ │ └── TriLM

### │ └── Hybrid / Progressive quantization

### │ ├── LLM.int8() lineage

### │ └── QLoRA-style (4-bit → 1-bit)

### ├── By Weight Representation

### │ ├── Binary {−1, +1}

### │ ├── Ternary {−1, 0, +1}

### │ └── Mixed-precision (1-bit weights + higher-bit activations)

### ├── By Architecture Modification

### │ ├── Standard Transformer + 1-bit weights

### │ ├── Custom 1-bit attention mechanisms

### │ └── 1-bit with modified normalization

### └── By Application Domain

### ├── Cloud inference

### ├── Edge / mobile

### └── Specialized (code, vision-language, etc.)



\---



\### 4. Core Methods and Architectures (\~6,000 words)



\#### 4.1 BitNet and BitNet b1.58 (Microsoft Research)

\- Architecture: ternary weights, INT8 activations

\- Training recipe: sub-layer norm, high learning rate, no weight decay on ternary params

\- Scaling behaviour: perplexity curves at 700M, 1.3B, 3.9B

\- Inference: matmul → addition; energy savings

\- \*\*TABLE 1:\*\* Comparison of BitNet b1.58 vs. FP16 baselines (perplexity, accuracy, memory, latency)



\#### 4.2 Binary Neural Network LLMs

\- True 1-bit (binary) approaches

\- XNOR-attention mechanisms

\- Popcount-based matrix multiplication



\#### 4.3 TriLM and OneBit

\- Post-training ternarization

\- Calibration strategies

\- Performance degradation analysis



\#### 4.4 Quantization-Aware Training Pipelines

\- STE variants for 1-bit

\- Knowledge distillation from full-precision teacher

\- Progressive quantization schedules



\#### 4.5 Mixed-Precision and Hybrid Schemes

\- Embedding layers kept at higher precision

\- LayerNorm / positional encoding at FP16

\- Selective 1-bit (certain layers only)



\#### 4.6 Hardware-Aware 1-Bit Designs

\- Custom ASIC / FPGA considerations

\- Bit-serial computation

\- Memory bandwidth savings analysis



> \*\*Key OA References:\*\*

> - Ma et al., "BitNet b1.58" (2024) — arXiv:2402.17764

> - Wang et al., "BitNet" (2023) — arXiv:2310.11453

> - Ma et al., "The Era of 1-bit LLMs" (2024) — arXiv:2402.17764

> - Li et al., "OneBit: 1-bit Quantization for LLMs" (2024) — arXiv

> - Zhang et al., "TriLM" (2024) — arXiv

> - Dettmers et al., "LLM.int8()" (2022) — arXiv:2208.07339

> - Dettmers et al., "QLoRA" (2023) — arXiv:2305.14314



\---



\### 5. Training Strategies for 1-Bit LLMs (\~3,000 words)



\#### 5.1 Training from Scratch in 1-Bit

\- Why post-training quantization fails at 1-bit

\- Initialization strategies

\- Learning rate scheduling for ternary weights



\#### 5.2 Quantization-Aware Training (QAT)

\- Forward pass: quantized weights

\- Backward pass: STE / adaptive STE

\- Annealing / temperature-based quantization



\#### 5.3 Knowledge Distillation

\- Full-precision teacher → 1-bit student

\- Feature-level vs. logit-level distillation

\- Progressive distillation pipelines



\#### 5.4 Data Efficiency and Pre-training Considerations

\- Does 1-bit training need more data?

\- Curriculum learning observations

\- Tokeniser interaction with 1-bit training



\#### 5.5 Fine-Tuning and Adaptation

\- LoRA / QLoRA compatibility with 1-bit backbones

\- Instruction tuning in 1-bit regime

\- RLHF / DPO at 1-bit



> \*\*Key OA References:\*\*

> - Bengio et al., "Estimating or Propagating Gradients Through Stochastic Neurons" (2013) — arXiv:1308.3432

> - Hu et al., "LoRA" (2022) — arXiv:2106.09685

> - Various QAT papers on arXiv



\---



\### 6. Inference, Efficiency, and Deployment (\~3,000 words)



\#### 6.1 Memory Footprint Analysis

\- \*\*TABLE 2:\*\* Memory comparison (FP32 vs. FP16 vs. INT8 vs. INT4 vs. 1.58-bit vs. 1-bit) for models from 125M to 70B parameters

\- KV-cache quantization considerations



\#### 6.2 Computational Efficiency

\- Replace multiply-accumulate with XNOR + popcount

\- Theoretical FLOP reduction

\- Actual wall-clock speedups on GPU / CPU / NPU



\#### 6.3 Energy Efficiency

\- Joules per token comparison

\- Relevance for edge / mobile / IoT

\- Carbon footprint reduction estimates



\#### 6.4 Hardware Ecosystem

\- NVIDIA GPU support (or lack thereof)

\- Custom silicon: bit-serial accelerators

\- CPU inference feasibility (AVX, NEON)

\- FPGA / ASIC prototypes



\#### 6.5 Serving and Scalability

\- Batch inference throughput

\- KV-cache management at 1-bit

\- Speculative decoding compatibility



> \*\*Key OA References:\*\*

> - Ma et al., "BitNet b1.58" inference analysis (2024)

> - Various arXiv papers on efficient LLM inference

> - Frantar et al., "GPTQ" (2023) — arXiv:2210.17323



\---



\### 7. Benchmarks and Empirical Evaluation (\~2,500 words)



\#### 7.1 Evaluation Protocols

\- Perplexity (WikiText-2, C4, Pile)

\- Downstream tasks: MMLU, HellaSwag, ARC, WinoGrande, TruthfulQA

\- Generation quality: BLEU, ROUGE, human eval

\- Multilingual benchmarks



\#### 7.2 Comparative Analysis

\- \*\*TABLE 3:\*\* Master comparison table — all major 1-bit / ternary methods vs. FP16 baselines across model sizes

\- Performance degradation trends as bits decrease

\- Task-specific sensitivity analysis



\#### 7.3 Scaling Laws at 1-Bit

\- Does Chinchilla scaling hold?

\- Compute-optimal training at 1-bit

\- Emergent abilities: preserved or lost?



\#### 7.4 Ablation Studies from Literature

\- Activation bit-width sensitivity

\- Which layers can be 1-bit vs. need higher precision

\- Group size / quantization granularity effects



> \*\*Key OA References:\*\*

> - Hendrycks et al., "MMLU" (2021) — arXiv:2009.03300

> - Gao et al., "The Pile" (2021) — arXiv:2101.00027

> - Hoffmann et al., "Chinchilla Scaling Laws" (2022) — arXiv:2203.15556



\---



\### 8. 1-Bit LLMs in the Broader Ecosystem (\~2,000 words)



\#### 8.1 Relation to Other Compression Techniques

\- Pruning + 1-bit quantization

\- Distillation + 1-bit

\- Architecture search for 1-bit-friendly models



\#### 8.2 Multimodal and Specialized 1-Bit Models

\- Vision-language models at 1-bit

\- Code generation models

\- Speech/audio LLMs



\#### 8.3 1-Bit in the Context of Green AI

\- Carbon accounting

\- Democratization of LLM access

\- Deployment in low-resource settings



\#### 8.4 Relation to Neuromorphic and Spiking Computing

\- Conceptual parallels

\- Hardware convergence possibilities



\---



\### 9. Open Challenges and Future Directions (\~2,500 words)



\#### 9.1 Fundamental Challenges

\- Performance gap at very small model sizes (<1B)

\- Training instability in pure 1-bit

\- Activation quantization bottleneck (activations still INT8)



\#### 9.2 Algorithmic Open Problems

\- Better STE alternatives

\- Optimal ternary threshold selection

\- Mixed-precision allocation (which layers get 1-bit?)

\- Theoretical understanding: why does 1.58-bit work?



\#### 9.3 Hardware and Systems Challenges

\- Lack of native 1-bit support in commercial GPUs

\- Compiler and kernel optimization needs

\- Memory hierarchy implications



\#### 9.4 Scaling and Generalization

\- Does 1-bit work at 100B+ scale?

\- Multilingual and cross-lingual generalization

\- Long-context performance at 1-bit



\#### 9.5 Safety and Alignment at 1-Bit

\- Does quantization affect safety fine-tuning?

\- Alignment tax

\- Robustness to adversarial inputs



\#### 9.6 Standardization and Reproducibility

\- Need for standard 1-bit evaluation protocols

\- Open-source model zoo

\- Reproducibility of training recipes



\---



\### 10. Conclusion (\~800 words)

\- Summary of the field's trajectory (2023–2026)

\- Key takeaways (3–5 bullet points)

\- Vision: will 1-bit become the default?

\- Call to action for the community



\---



\### Appendices

\- \*\*Appendix A:\*\* Full list of reviewed papers with classification

\- \*\*Appendix B:\*\* Glossary of quantization terms

\- \*\*Appendix C:\*\* Summary of all tables and figures



\---



\## 4. FIGURES AND TABLES PLAN



| ID | Type | Description | Section |

|---|---|---|---|

| Fig. 1 | Taxonomy tree | Classification of 1-bit LLM methods | §3 |

| Fig. 2 | Timeline | Evolution: BinaryConnect → XNOR → BitNet → BitNet b1.58 → 2025/26 works | §1 |

| Fig. 3 | Diagram | Ternary weight representation and XNOR+popcount arithmetic | §2 |

| Fig. 4 | Bar chart | Memory footprint comparison across precisions for 7B model | §6 |

| Fig. 5 | Line plot | Perplexity vs. model size for 1-bit vs. FP16 (from literature) | §7 |

| Fig. 6 | Radar chart | Multi-task benchmark comparison of top 1-bit methods | §7 |

| Fig. 7 | Diagram | Training pipeline: QAT from scratch vs. PTQ vs. distillation | §5 |

| Tab. 1 | Table | BitNet b1.58 vs. FP16 baseline comparison | §4.1 |

| Tab. 2 | Table | Memory / latency / energy across precisions and model sizes | §6.1 |

| Tab. 3 | Table | Master comparison of all 1-bit methods (model size, bits, perplexity, accuracy) | §7.2 |

| Tab. 4 | Table | Hardware support landscape for 1-bit inference | §6.4 |

| Tab. 5 | Table | Summary of open challenges and potential solutions | §9 |



\---



\## 5. OPEN-ACCESS PAPER SOURCES (Curated List)



> \*\*All references MUST be open access.\*\* Use these sources:



\### Primary Sources (arXiv preprints — all OA)

1\. Ma, X., et al. \*"The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits."\* arXiv:2402.17764 (2024)

2\. Wang, H., et al. \*"BitNet: Scaling 1-bit Transformers for Large Language Models."\* arXiv:2310.11453 (2023)

3\. Ma, X., et al. \*"BitNet b1.58: 1-bit LLMs with Ternary Weights."\* arXiv:2402.17764 (2024)

4\. Dettmers, T., et al. \*"LLM.int8(): 8-bit Matrix Multiplication for Transformers."\* arXiv:2208.07339 (2022)

5\. Dettmers, T., et al. \*"QLoRA: Efficient Finetuning of Quantized LLMs."\* arXiv:2305.14314 (2023)

6\. Frantar, E., et al. \*"GPTQ: Accurate Post-Training Quantization."\* arXiv:2210.17323 (2023)

7\. Courbariaux, M., et al. \*"BinaryConnect: Training Deep Neural Networks with Binary Weights."\* arXiv:1511.00363 (2015)

8\. Rastegari, M., et al. \*"XNOR-Net: ImageNet Classification Using Binary CNNs."\* arXiv:1603.05279 (2016)

9\. Li, F., et al. \*"Ternary Weight Networks."\* arXiv:1605.04711 (2016)

10\. Vaswani, A., et al. \*"Attention Is All You Need."\* arXiv:1706.03762 (2017)

11\. Hu, E., et al. \*"LoRA: Low-Rank Adaptation of Large Language Models."\* arXiv:2106.09685 (2022)

12\. Hoffmann, J., et al. \*"Training Compute-Optimal Large Language Models."\* arXiv:2203.15556 (2022)

13\. Hendrycks, D., et al. \*"Measuring Massive Multitask Language Understanding (MMLU)."\* arXiv:2009.03300 (2021)

14\. Bengio, Y., et al. \*"Estimating or Propagating Gradients Through Stochastic Neurons."\* arXiv:1308.3432 (2013)

15\. Jacob, B., et al. \*"Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference."\* arXiv:1712.05877 (2018)



\### Additional Search Terms for More OA Papers

\- `"1-bit LLM" OR "1.58-bit" OR "ternary LLM" OR "binary transformer" site:arxiv.org`

\- `"BitNet" OR "TriLM" OR "OneBit" quantization LLM arxiv`

\- `"extreme quantization" "large language model" arxiv 2024 2025 2026`

\- Search \*\*Semantic Scholar\*\* (open API), \*\*OpenReview\*\* (ICML/NeurIPS/ICLR accepted papers are OA), and \*\*DOAJ\*\*



\### OA Repositories to Mine

| Repository | URL | Notes |

|---|---|---|

| arXiv | arxiv.org | All CS.CL, CS.LG, cs.AI preprints |

| OpenReview | openreview.net | NeurIPS, ICLR, ICML accepted papers |

| Semantic Scholar | semanticscholar.org | API access, OA filter |

| Hugging Face Papers | huggingface.co/papers | Daily curated OA papers |

| DOAJ | doaj.org | Directory of OA journals |

| PubMed Central | ncbi.nlm.nih.gov/pmc | If any cross-domain refs needed |



\---



\## 6. WRITING TIMELINE (16-Week Plan)



| Week | Phase | Tasks |

|---|---|---|

| \*\*1–2\*\* | Literature Collection | Search \& collect 200+ OA papers; build Zotero/BibTeX library; read top 30 papers deeply |

| \*\*3–4\*\* | Taxonomy \& Outlining | Finalize taxonomy (Fig. 1); refine outline; identify gaps in existing surveys |

| \*\*5–6\*\* | Draft: §1–§3 | Introduction, Background, Taxonomy sections |

| \*\*7–9\*\* | Draft: §4–§5 | Core Methods + Training Strategies (heaviest writing) |

| \*\*10–11\*\* | Draft: §6–§7 | Inference/Efficiency + Benchmarks; build Tables 1–3 |

| \*\*12\*\* | Draft: §8–§10 | Broader ecosystem, Challenges, Conclusion |

| \*\*13\*\* | Figures \& Tables | Produce all 7 figures + 5 tables; ensure vector quality (PDF/SVG) |

| \*\*14\*\* | Internal Revision | Self-edit; check OA compliance of every reference; coherence pass |

| \*\*15\*\* | Peer Feedback | Send to 2–3 colleagues for feedback; incorporate revisions |

| \*\*16\*\* | Final Polish \& Submit | Format to target journal template; write cover letter; submit |



\---



\## 7. SUBMISSION STRATEGY



\### 7.1 Cover Letter Key Points

\- Emphasize \*\*timeliness\*\*: 1-bit LLMs exploded in 2023–2026

\- Emphasize \*\*comprehensiveness\*\*: first survey dedicated solely to 1-bit/ternary LLMs

\- Emphasize \*\*practical impact\*\*: edge AI, green AI, democratization

\- State all references are open access



\### 7.2 Suggested Reviewers (for submission form)

\- Identify 5–8 researchers active in quantization / 1-bit LLMs

\- Include mix of academia and industry (Microsoft Research, Meta AI, academic labs)



\### 7.3 Pre-submission Checklist

\- \[ ] All references verified as open access (DOI or arXiv link)

\- \[ ] No paywalled citations

\- \[ ] Figures are original (not copied from papers)

\- \[ ] Plagiarism check (Turnitin / iThenticate < 10%)

\- \[ ] Formatted to target journal LaTeX template

\- \[ ] Abstract within word limit

\- \[ ] All tables and figures referenced in text

\- \[ ] Conflict of interest statement

\- \[ ] CRediT author contribution statement (if multi-author)



\---



\## 8. KEY DIFFERENTIATORS TO AIM FOR 10+ IF



1\. \*\*Novel taxonomy\*\* — no existing survey has this specific 1-bit LLM classification

2\. \*\*Quantitative meta-analysis\*\* — don't just describe; aggregate numbers across papers into unified tables

3\. \*\*Scaling law analysis\*\* — synthesize how 1-bit performance scales vs. FP16

4\. \*\*Hardware-aware discussion\*\* — bridge algorithm and systems (journals love this)

5\. \*\*Future roadmap\*\* — concrete, opinionated research directions (not vague)

6\. \*\*Timeliness\*\* — 2024–2026 is the golden window for this topic

7\. \*\*Open-science framing\*\* — all OA references, reproducible comparisons



\---



\## 9. TOOLS AND WORKFLOW



| Task | Tool |

|---|---|

| Reference management | Zotero (free, OA metadata) |

| Writing | LaTeX (Overleaf) or Typst |

| Figures | draw.io / TikZ / matplotlib / Figma |

| Literature search | Semantic Scholar API, Connected Papers, arXiv-sanity |

| Plagiarism check | iThenticate or Turnitin |

| Grammar / style | Grammarly / LanguageTool |

| Project tracking | Notion or GitHub Projects |

| Version control | Git + GitHub (private repo) |



\---



\## 10. RISK MITIGATION



| Risk | Mitigation |

|---|---|

| Topic becomes saturated before submission | Start writing immediately; target 16-week turnaround |

| Key papers behind paywall | Use arXiv preprint versions; contact authors; check PMC |

| Reviewer says "incremental vs. existing quantization surveys" | Emphasize 1-bit specificity, novel taxonomy, hardware analysis |

| Not enough papers for a "survey" | Broaden to include binary/ternary NNs, efficient inference, edge deployment |

| Journal rejects for scope | Have backup journal ready (ACM CSUR → Information Fusion → AI Journal) |



\---



\*Document prepared: September 2026\*

\*Target: Submission by January 2027\*



\---



> \*\*Next immediate actions:\*\*

> 1. Create Zotero library with search queries above

> 2. Read BitNet and BitNet b1.58 papers in full

> 3. Draft the taxonomy figure (Fig. 1)

> 4. Register on target journal's submission portal

> 5. Set up Overleaf project with journal template



> \*\*FIGURE 1:\*\* Taxonomy tree diagram (central contribution figure)

