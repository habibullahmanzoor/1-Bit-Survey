# 6. Training Methodology and Theory

## 6.1 The native training loop

Native 1-bit training keeps a full-precision shadow weight in the optimizer and derives
the quantized weight from it on the fly in every forward pass. The forward pass uses
the quantized weight; the backward pass computes gradients with respect to the
quantized weight and applies them to the shadow weight through the straight-through
estimator, usually clipped to the active range of the quantizer
[Wang2023-BitNet], [Ma2024-BitNetB158]. At the end of
training, the shadow weights are quantized once and discarded, leaving a model that
stores about 1.58 bits per weight and, with an appropriate kernel, replaces its matrix
multiplications with integer additions. The cost of this scheme is training-time memory:
the shadow weights and their optimizer state are full precision, adding the memory
footprint of a full-precision copy of the model on top of the quantized forward pass,
and the compression saving is realized entirely at inference time. Direct Quantized Training questions the shadow copy itself,
keeping only low-precision weights and using stochastic rounding to carry sub-quantum
information between steps; it reports that ternary-only training is feasible and that
widening to eight-bit weights matches BitNet b1.58 at reduced training memory
[Zhao2024-DQT].

## 6.2 Recipes

The published recipes share a common shape. There is a two-stage schedule for the
learning rate and weight decay, with higher values early, when the quantized landscape
is rough, and lower values later; a warmup on the quantization strength; and, for
instruction-tuned models, a standard supervised fine-tuning stage followed by direct
preference optimization, applied while the weights remain ternary [Ma2025-BitNet2B4T].
Data scale matters more than parameter scale for ternary models: the Spectra suites
find that TriLM performance improves faster with training tokens than with parameters,
and Spectra 1.1 trains to 1.2T tokens on that basis [Kaushal2024-Spectra],
[Vaidhya2025-Spectra11]. Continual schemes trade a small amount of accuracy for a large
training saving by running most of pre-training in full precision and only the final
phase in 1.58-bit; the loss spike at the transition is reduced by retaining the
optimizer state across the switch and by phasing in the quantization strength gradually
[Nielsen2025-ContinualQAT], [Tu2025-Rethink1bitOpt].

## 6.3 The straight-through estimator and its alternatives

The straight-through estimator is biased: the gradient it supplies is not the gradient
of the expected quantized loss, and the mismatch grows as the bit-width falls,
producing slow convergence and instability. Recent work treats the estimator as a
design object, along several lines.

The first line is curvature-aware estimation. CAGE frames quantization-aware training as
a multi-objective optimization that simultaneously minimizes the task loss and the
quantization error, derives a Pareto-optimality condition, and adds a curvature-
dependent correction term to the STE gradient, with a convergence proof in the smooth
non-convex setting; it matches the accuracy of a prior W4A4 method at W3A3
[Tabesh2025-CAGE].

The second line is trust-region estimation. QuEST fits the continuous weight and
activation distributions with a Hadamard normalization and an MSE-optimal grid, and then
uses a trust gradient that explicitly minimizes the distance between the quantized-state
gradient and the unknown true gradient; this is what allows it to train stably at
one-bit weights and activations [Panferov2025-QuEST].

The third line adds zeroth-order information: a finite-difference estimate of the true
gradient, added to the STE gradient, reduces its bias at low bit-width
[Anon2025-STE-ZerothOrder]. A fourth line replaces the uniform quantizer with a
non-uniform one; a k-means codebook improves low-bit quantization-aware training by
placing levels where the weight mass is [Maskey2026-1BitWonder].

A final line moves beyond the STE for fine-tuning. PV-Tuning shows that the STE is
suboptimal for extreme fine-tuning specifically, and replaces it with a
representation-agnostic coordinate descent that alternates updates of the discrete
assignment and the continuous parameters, achieving the first Pareto-optimal 2-bit
Llama-2 [Malinovskii2024-PVTuning]. LC-QAT makes vector-quantized training
differentiable by parameterizing each codeword as a linear map of a discrete vector,
which avoids the codebook lookup in the training forward pass [Wang2026-LCQAT].

## 6.4 Distillation

Distillation from a full-precision teacher is the most common way to close the last
accuracy gap. FBI-LLM trains a binary model from scratch with an autoregressive
distillation loss and finds that a pretrained initialization is not required
[Ma2024-FBILLM]; Bi-Mamba does the same for state-space models [Tang2024-BiMamba].
BitDistiller pairs quantization-aware training with a confidence-aware
Kullback-Leibler objective in a self-distillation loop for sub-four-bit weights
[Du2024-BitDistiller]; token-scaled logit distillation was the first method to bring
ternary quantization-aware training of large generative models to within one perplexity
point of the teacher [Kim2023-TSLD]. BitNet Distillation adds SubLN, a short
continued-pretraining phase, and combined logit-and-attention distillation to convert a
full-precision LLM into a 1.58-bit task model [Wu2025-BitNetDistillation]. LBLLM stages
the process into a post-training-quantization initialization, layer-wise weight
distillation, and finally learning of the activation scales [Song2026-LBLLM].

## 6.5 Post-training routes toward one bit

The post-training-quantization branch, 30 works on the training-paradigm axis of
Section 4.2, approaches one bit without gradient updates. The techniques cluster into a few families. The first is salient-
weight handling with binary residual approximation, as in the roughly 1.08 effective
bits of BiLLM [Huang2024-BiLLM] and the partial binarization of PB-LLM
[Shang2023-PBLLM]. The second is alternating refinement of the binarization parameters,
as in ARB-LLM, which was the first binary post-training method to beat a half-precision
model of equal size [Li2024-ARBLLM]. The third is ternary-specific quantizers with
iterative grid fitting and column reordering [Yan2025-PT2LLM], [Xiao2025-PTQTP]. The
fourth is explicit outlier handling, whether by index coding at a 0.3-bit overhead
[Li2025-ICQuant] or by learned distribution transforms [Ye2025-DBellQuant],
[Zhao2026-BWLA]. The fifth is output-alignment objectives that correct the error
accumulation and representation-space anisotropy from which naive output-matching
post-training quantization suffers in the one-bit regime [Hoang2025-OutputAlign1bit].

## 6.6 Scaling laws at one bit

Whether native 1.58-bit models genuinely match full precision, or only appear to do so
under limited training-token budgets, is the central empirical dispute in the field.
Precision-aware scaling laws model low-precision training as a reduction of the
effective parameter count and predict that post-training-quantization degradation
increases with pre-training data, eventually making additional data harmful for a model
that will be quantized [Kumar2024-ScalingLawsPrecision]. The quantization-induced
degradation study reaches a compatible conclusion from more than 1,500 checkpoints:
degradation grows with the number of training tokens, so that projections to
100-trillion-token models are pessimistic for low-bit quantization
[Ouyang2024-QiDScaling]. On the other side, the native ternary suites show TriLMs
overtaking quantized and full-precision models on a bits-for-bits basis beyond about 1B
parameters [Kaushal2024-Spectra], [Vaidhya2025-Spectra11], and the unified 1-bit to
4-bit study of ParetoQ finds a learning transition between two and three bits, with
ternary, two-bit, and three-bit quantization sharing a size-accuracy frontier that
beats four-bit and binary [Liu2025-ParetoQ]. A partial reconciliation is that the two
camps measure different quantities, namely post-training quantization of a fixed model
against training under the constraint, and that the crossover point, not its existence,
is what matters in practice. Theory is beginning to bear on this: a kernel-limit
analysis proves a scaling law for 1-bit networks [Daliri2024-Theory1bit], and
precision-expressivity trade-offs are being formalized for quantized transformers
[Anon2026-EveryBitCounts], [Anon2026-ExpressivePowerWQ].

## 6.7 Training stability and smoothness

Beyond the loss value, extremely quantized models show a degradation of smoothness: a
rapid reduction in the number of plausible next tokens within a prediction
neighborhood, which sparsifies the decoding tree and hurts generation quality
independently of perplexity. A smoothness-preserving term added to either post-training
quantization or quantization-aware training recovers additional accuracy
[Xu2026-FittingNotEnough]. Tequila identifies deadzone trapping, in which ternary
weights become stuck at the {-1,0} or {0,+1} boundary and receive only noise gradients,
and repurposes the trapped weights as dynamic biases so that they receive a meaningful
signal, at near-zero inference overhead [Huang2025-Tequila]. HGF stabilizes 1.58-bit
training with a per-layer gated low-rank correction [Anon2026-HGF]. These are early
steps toward the training stability that a native 1-bit model an order of magnitude
larger than today's 2B, 4T-token ceiling would require (Section 11).
