# 11. Challenges and Open Problems

Each of the following is stated as a gap that could be closed, not as a wish list.

## 11.1 The capacity ceiling and its dependence on the token budget

The first open problem is whether the full-precision parity of BitNet b1.58 is a
property that survives to frontier scale and token budgets, or an artifact of the two-
to four-trillion-token regime in which it has been measured. The two bodies of evidence
point in opposite directions, though, as Section 6.6 notes, they measure different
quantities: precision-aware scaling laws and the quantization-induced degradation study
are about post-training quantization of a fixed model, and find that its degradation
grows with training tokens, projecting that a model quantized to low bits after being
trained on 20 to 100 trillion tokens would fall progressively further behind its FP16
source [Kumar2024-ScalingLawsPrecision], [Ouyang2024-QiDScaling]. These findings motivate
testing whether an analogous degradation appears in native ternary training itself, at
frontier token counts; they do not, by themselves, establish that it will. The native
ternary suites and ParetoQ report the opposite trend
within their range: ternary improves on a bits-for-bits basis as data scales, and a
600M ParetoQ ternary model beats a 3B prior-state-of-the-art ternary model
[Kaushal2024-Spectra], [Vaidhya2025-Spectra11], [Liu2025-ParetoQ]. Our controlled re-run
of Spectra's matched pair (Section 10.3) confirms downstream parity at 2.4B parameters
and 300B tokens, with a 14% higher perplexity, but that is well inside the measured
regime. These findings have not been reconciled, because no native 1-bit model has been
trained at both a frontier parameter count and a frontier token count. This is the single
most important experiment that the field is missing, and it is expensive but not
prohibitively so.

## 11.2 Training stability at frontier scale

The second open problem is whether native 1.58-bit pre-training becomes unstable, with
loss spikes or divergence, once the model is much larger than today's and the token
budget grows with it, and whether the current mitigations only delay that instability.
The largest reported native run is 4T tokens at 2B parameters [Ma2025-BitNet2B4T], so
every stability claim in the literature is at or below that scale; a 20B or 200B native
model on tens of trillions of tokens is untried. Continual quantization-aware training
already documents loss spikes at the full-precision-to-1.58-bit transition and partial
fixes, namely optimizer-state retention and a quantization warmup
[Nielsen2025-ContinualQAT], [Tu2025-Rethink1bitOpt], and the deadzone-trapping analysis
of Tequila and the gated low-rank correction of HGF address related instabilities
[Huang2025-Tequila], [Anon2026-HGF]. Whether these mitigations compose into a stable run
an order of magnitude larger is unknown.

## 11.3 The activation-precision floor

The third open problem is whether four bits is the practical floor for activations
alongside roughly one-bit weights, or whether rotation together with sparsification can
reach two-bit activations. Native A4 is solved by hybrid quantization and sparsification
[Wang2024-BitNetA48] and by an online Hadamard transform [Wang2025-BitNetV2];
post-training quantization mostly reaches A6 [Zhao2026-BWLA], [Ye2025-DBellQuant], with
one single-preprint report of A4 through rotation [Zhao2026-TWLA] not yet corroborated;
and QuEST
demonstrates one-bit weights and activations but only below 1B parameters
[Panferov2025-QuEST]. Nobody has demonstrated W1.58A2 at multi-billion scale with
acceptable accuracy. Given that activation traffic now dominates once weights occupy
roughly one bit, this is where the next efficiency step must come from.

## 11.4 A theory of straight-through training

The fourth open problem is the absence of a general convergence theory for
straight-through training of 1-bit Transformers; only special cases are understood. CAGE
proves convergence for its curvature-corrected estimator in the smooth non-convex
setting [Tabesh2025-CAGE]; a kernel-limit analysis proves a scaling law for 1-bit
networks as width grows [Daliri2024-Theory1bit]; and precision-expressivity trade-offs
are being formalized [Anon2026-EveryBitCounts], [Anon2026-ExpressivePowerWQ]. What is
missing is an account that connects the estimator bias to the observed instabilities and
predicts which schedules and estimators avoid them.

## 11.5 Hardware co-design

The fifth open problem is that no shipping processor exposes a ternary
matrix-multiplication primitive, and only five works in the corpus co-design across
algorithm, kernel, and hardware [Ma2024-BitNetB158], [Ma2025-BitNet2B4T],
[Zhu2024-MatmulFree], [Zhang2026-SparseBitNet], [Ji2024-BMTBAT]. The accelerator
literature on lookup-table ASICs, compute-in-ROM, processing-in-memory, and edge FPGAs
[Shan2025-Platinum], [Guan2026-TOM], [Malekar2025-PIMLLM], [Qiao2025-TeLLMev2],
[Lin2026-VitaLLM], [Zhang2025-PDSwap] reports simulator and single-chip results. An add-and-subtract matrix-multiplication unit with a
matching memory layout and a small instruction-set extension, co-designed with the
training recipe and the sparsity pattern, does not exist. This gap is why the efficiency
case does not close on today's hardware: our re-evaluation (Section 10) finds that on a
commodity CPU the flagship ternary model has no throughput, footprint, or per-token
energy advantage over a 4-bit baseline, because the ternary matrix multiplication still
runs on a general-purpose datapath that a 4-bit kernel uses at least as well. The Sparse-BitNet
result, that ternary models tolerate structured sparsity far better than full-precision
models [Zhang2026-SparseBitNet], suggests that the co-design target should be sparse
ternary rather than dense ternary.

## 11.6 Reasoning, generation quality, and smoothness

The sixth open problem concerns generation quality. Extreme quantization degrades output
smoothness, that is, the diversity of plausible next tokens, independently of
perplexity, which sparsifies the decoding tree [Xu2026-FittingNotEnough]; and two-bit
reasoning models fail by not committing to an answer, which inflates the trace length
[Alimaskina2026-ExtremeReasoning]. Whether native 1.58-bit training, as opposed to
post-hoc two-bit quantization, suffers the same pathologies, and whether
smoothness-preserving objectives fix them at scale, is open.

## 11.7 Robustness, safety, and security

The seventh open problem is that the robustness and security of ternary models are
under-studied. GenBFA shows that three bit-flips can collapse a quantized
billion-parameter LLM [Das2024-GenBFA]; MatMul-free LM is reported as more robust to
word-level adversarial attacks than a standard Transformer, with a mixed picture at the
character level [Fan2024-ResilientEfficient]; and the
fault tolerance of compute-in-memory ternary LLMs is beginning to be studied. Whether
ternary weights are systematically more or less fragile than FP16, with respect to
bit-flips, adversarial inputs, backdoors, and membership inference, is not established,
and the deployment story of models on phones and in enclaves makes the question urgent.

## 11.8 Sub-1.58-bit and alternative representations

The eighth open problem is whether a representation past ternary is the better place to
push. Structural binarization below one bit [Dong2024-STBLLM], latent factorization to
about 0.1 bits [Lee2025-LittleBit], 1.25-bit regularized sparsity [Huang2026-Sherry], and
complex $\{\pm 1, \pm i\}$ codebooks [Wang2025-iFairy], [Wang2025-Fairy2i] all push past
1.58 bits. Whether any of these is a better operating point than ternary, once kernel
and hardware support is accounted for, is unresolved.

## 11.9 Evaluation and contamination

The ninth open problem is that the field lacks a standard evaluation harness and a
contamination control of its own. Native 1-bit models are small and heavily fine-tuned,
which raises the risk of benchmark contamination; different papers use different harness
versions, prompt formats, and few-shot counts (Section 8). A shared, versioned evaluation
protocol for 1-bit LLMs would make the literature comparable.
