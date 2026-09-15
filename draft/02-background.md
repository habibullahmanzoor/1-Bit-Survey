# 2. Background and Preliminaries

## 2.1 Number formats and effective bits per weight

A dense linear layer multiplies an input vector by a weight matrix to produce an
output vector, and that weight matrix is stored in some numeric format. Full-precision
training uses 32-bit floating point (FP32) or, in practice, the 16-bit BF16 or FP16
formats, each consisting of a sign, an exponent, and a mantissa. Integer quantization
replaces each weight with an integer code multiplied by a shared floating-point scale;
8-bit and 4-bit integer codes are the common operating points. Binary quantization
restricts the code to the two values -1 and +1, that is, one bit. Ternary quantization
restricts the code to the three values -1, 0, and +1, which carries
$\log_2 3 \approx 1.58$ bits of information and is usually stored in two bits, or in
packed schemes that approach the information bound [Kaushal2024-Spectra],
[Anon2026-NativeTernary].

The reported number of bits per weight is not always the nominal code width. Partial
schemes keep a small fraction of salient columns in higher precision: BiLLM reports
about 1.08 effective bits and PB-LLM a tunable figure above one [Huang2024-BiLLM],
[Shang2023-PBLLM]. Structural-sparsity schemes push below one bit by storing only the
nonzero ternary positions [Dong2024-STBLLM], [Lee2025-LittleBit]. Packing choices for
ternary weights trade a fraction of a bit against kernel speed [Vaidhya2025-Spectra11],
[Huang2026-Sherry]. A consistent effective-bits accounting, defined as the code width
plus the per-weight amortized cost of scales, masks, and codebooks, is therefore a
prerequisite for comparing methods; Section 8 adopts one.

The benefit of a small integer code width is memory and bandwidth. A 2B-parameter model occupies four
to five GB in BF16 and about 0.4 GB with ternary weights in a non-embedding accounting,
and because the decode step is memory-bound, it speeds up in roughly the same proportion
[Ma2025-BitNet2B4T]; Section 10.4 measures the fuller resident-memory figure once the
embedding and runtime buffers are counted too. The second benefit is arithmetic. With each weight restricted to
-1, 0, or +1, the per-weight multiplication becomes a conditional add or subtract, so the
inner product reduces to a masked accumulation [Malekar2024-MatmulOrNot].

## 2.2 The binary neural network lineage

Training networks with binary weights predates LLMs. BinaryConnect binarizes weights in
the forward and backward pass while retaining a full-precision "shadow" copy in which
gradients accumulate, and it observes a regularizing effect
[Courbariaux2015-BinaryConnect]. XNOR-Net binarizes both weights and activations so that
a convolution becomes a bitwise XNOR followed by a population count, and it introduces
per-filter scaling factors to reduce the approximation error [Rastegari2016-XNORNet].
The transfer to language models proved harder. BinaryBERT finds the loss landscape of a
directly binarized BERT too rugged to optimize and instead initializes the model by
splitting a trained half-width ternary network [Bai2021-BinaryBERT]. BiBERT identifies
information loss in the forward pass and gradient-direction mismatch in the backward
pass as the two failure modes, and addresses them with an information-preserving
attention operator and a direction-matching distillation loss [Qin2022-BiBERT]. Three
lessons carried into the LLM era: a full-precision shadow weight is what makes
gradient-based training of a discrete variable work; ternary is markedly easier to
optimize than binary; and distillation from a full-precision teacher is often what
closes the last accuracy gap.

## 2.3 The straight-through estimator and its pathologies

The quantizer, which maps a full-precision weight to its quantized code, is piecewise
constant, so its gradient is zero almost everywhere and training cannot back-propagate
through it. The straight-through estimator (STE) replaces that gradient with the
identity, often clipped to the quantizer's input range, so that the forward pass sees
the quantized value while the backward pass updates the shadow weight as if the
quantizer were absent [Bengio2013-STE] (Fig. [fig:ste]).
Practically all native 1-bit training uses a scaled STE. BitNet's `BitLinear` layer
centers the weights and divides by their mean absolute value before applying the sign
function, quantizes activations to INT8 per token, and applies the STE through both
[Wang2023-BitNet], [Wang2025-BitNetJMLR]. BitNet b1.58 uses an absolute-mean ternary
rule [Ma2024-BitNetB158], and small-model studies find the median a more
outlier-robust divisor [Nielsen2024-Reloaded].

The STE is biased, and the bias manifests as slow convergence and instability that
worsen as the bit-width decreases. Recent work treats the estimator itself as the
object of study. CAGE adds a curvature-aware correction term derived from a
multi-objective view of quantization-aware training (QAT) and proves convergence in the
smooth non-convex setting [Tabesh2025-CAGE]. QuEST fits the weight and activation
distributions with a Hadamard normalization and an MSE-optimal grid, and it introduces
a trust gradient that minimizes the error between the quantized-state gradient and the
true gradient, reporting stable training down to one-bit weights and activations
[Panferov2025-QuEST]. A further line augments the STE with zeroth-order information
[Anon2025-STE-ZerothOrder]. An orthogonal alternative removes the STE entirely: Direct
Quantized Training keeps only low-precision weights and uses stochastic rounding to
carry information between steps, eliminating the shadow copy and its memory cost
[Zhao2024-DQT]. For extreme fine-tuning specifically, PV-Tuning shows that the STE
assumption is suboptimal and replaces it with a representation-agnostic
coordinate-descent procedure [Malinovskii2024-PVTuning].

## 2.4 Transformer-specific obstacles

Two properties of Transformers make sub-two-bit quantization harder than the
convolutional case.

The first is activation outliers. A small number of channels in the attention output
and in the feed-forward down-projection carry values one to two orders of magnitude
larger than the rest. Quantizing weights to roughly one bit sharply increases
sensitivity to these outliers, so most 1-bit-weight methods keep activations at INT8
[Ma2024-BitNetB158]. Two routes go lower. The first is a hybrid scheme: BitNet a4.8 uses
INT4 for the attention and feed-forward inputs but keeps 8 bits for the outlier-heavy
intermediate states, which it sparsifies first, reaching an effective W1.58A4
configuration with only 55% of parameters active and a three-bit KV cache
[Wang2024-BitNetA48]. The second is rotation: the `H-BitLinear` layer of BitNet v2
applies an online Hadamard transform that spreads outlier energy across coordinates
before quantization, which enables native four-bit activations [Wang2025-BitNetV2].
Learnable and data-adaptive rotations generalize the fixed Hadamard [Zagitov2026-HARP],
[Zhao2026-TWLA], [Zhao2026-BWLA], and the same idea drives several post-training routes
toward one-bit weights.

The second obstacle is the placement of normalization relative to the quantized
projection, which affects stability. `BitLinear` places a LayerNorm or SubLN before
quantization, and inserting an additional RMSNorm has been reported to stabilize
fine-tuning to 1.58 bits [Steinmetz2025-ExtraRMSNorm]. Continual schemes that begin in
full precision and transition to 1.58-bit training part-way through pre-training must
manage loss spikes at the switch; both retaining the optimizer state and phasing in the
quantization strength mitigate them [Nielsen2025-ContinualQAT].

## 2.5 Scaling behavior

Whether the full-precision parity of BitNet b1.58 is a genuine scaling property or an
artifact of limited training-token budgets is contested, and it is central to the open
problems of Section 11. Precision-aware scaling laws model low-precision training as a
reduction of the effective parameter count and predict that post-training quantization
degrades further as the amount of pre-training data increases
[Kumar2024-ScalingLawsPrecision], [Ouyang2024-QiDScaling]. Against this, native ternary
suites show ternary models overtaking quantized and even full-precision models on a
bits-for-bits basis beyond about 1B parameters, with gains that grow when training data
rather than parameter count is scaled [Kaushal2024-Spectra], [Vaidhya2025-Spectra11].
ParetoQ unifies one-bit to four-bit QAT in a single framework and reports a learning
transition between two and three bits, below which the representations reorganize
substantially; ternary, two-bit, and three-bit quantization occupy a comparable
size-accuracy frontier that generally beats four-bit and binary [Liu2025-ParetoQ].
Theory has begun to catch up: a kernel-limit analysis establishes a scaling law for
1-bit networks [Daliri2024-Theory1bit], and precision-expressivity trade-offs are being
formalized [Anon2026-EveryBitCounts], [Anon2026-ExpressivePowerWQ].

## 2.6 Evaluation metrics

The corpus reports, with varying completeness, the following quantities. On the accuracy
side: perplexity on WikiText-2 and C4; zero-shot accuracy on ARC-Easy, ARC-Challenge,
HellaSwag, WinoGrande, PIQA, OpenBookQA, and BoolQ, usually reported as an average; and,
for instruction-tuned models at the 2B scale, MMLU, GSM8K, and HumanEval or HumanEval+.
On the systems side: decode throughput in tokens per second and time per output token;
prefill latency and time to first token; peak resident memory; and energy per token or
per inference. Cross-paper comparison is complicated by different harness versions,
prompt formats, and few-shot counts, and, on the efficiency side, by different
hardware, thread counts, and baselines, such as FP16 against INT8, or a general
inference framework against a custom kernel. Section 8 states the effective-bits
convention and the axes used to place these results on one scale, and Section 10
reports independently measured values for a subset.
