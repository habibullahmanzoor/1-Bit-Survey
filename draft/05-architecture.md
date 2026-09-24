# 5. Architectural Design

## 5.1 The BitLinear primitive

The standard native 1-bit LLM is built from a single substitution: the standard linear
layer is
replaced by a `BitLinear` layer that normalizes its input, quantizes the weight to a
low-bit code with a shared scale, quantizes the activation, and back-propagates through
both quantizers with a straight-through estimator [Wang2023-BitNet],
[Wang2025-BitNetJMLR]. In the original BitNet, the weight rule is a sign function
applied after subtracting the mean and dividing by the mean absolute value, and the
activation rule is per-token absolute-max quantization to INT8, offset for
non-linearities that produce non-negative outputs. BitNet b1.58 changes the weight rule
to an absolute-mean ternary quantizer: it divides by the mean absolute value, rounds to
the nearest of {-1,0,+1}, and clamps. This yields the {-1,0,+1} value set and drives
roughly half of the weights to zero [Ma2024-BitNetB158]. Small-model studies report that
using the median in place of the mean in the scale makes the quantizer less sensitive
to a few large weights and can improve accuracy at very small scales
[Nielsen2024-Reloaded].

A recurring architectural detail is the placement of normalization. `BitLinear` applies
its normalization, LayerNorm in BitNet and SubLN in later variants, before quantization,
so that the quantizer sees a controlled input distribution. Several works find that an
additional RMSNorm inserted at the layer boundary stabilizes the transition to 1.58-bit
weights during fine-tuning [Steinmetz2025-ExtraRMSNorm], and BitNet Distillation
combines SubLN with a short continued-pretraining phase before task distillation
[Wu2025-BitNetDistillation].

## 5.2 Ternary versus binary in practice

The move from binary to ternary is the single largest architectural lever in the native
setting. Binary from-scratch training is possible: FBI-LLM demonstrates a fully binary
LLM that matches half precision by relying heavily on an autoregressive distillation
loss [Ma2024-FBILLM], and QuEST reaches stable one-bit weights and activations with a
trust-gradient estimator and Hadamard-normalized fitting [Panferov2025-QuEST]. In each
case, however, more machinery, such as distillation, careful initialization, or a better
gradient estimator, is needed to reach the loss that ternary attains directly. The zero
state of ternary weights doubles as sparsity, unstructured until a method imposes a
pattern on it (Section 5.5), which is why ternary models
compose naturally with N:M sparse tensor cores [Zhang2026-SparseBitNet] and with packing
schemes that store four ternary weights in five bits [Huang2026-Sherry] or approach the
1.6-bit information bound [Vaidhya2025-Spectra11].

## 5.3 Activation quantization

Once weights occupy roughly one bit, activation precision becomes the binding
constraint. Most native models keep activations at INT8 [Ma2024-BitNetB158],
[Ma2025-BitNet2B4T]. Two routes go lower. BitNet a4.8 uses a hybrid scheme: INT4
activations for the inputs to attention and the feed-forward network, but the
outlier-heavy intermediate states, namely the attention output and the feed-forward
down-projection input, are first sparsified with a top-K mask and then quantized to
INT8. The effective configuration is W1.58A4 with only 55% of parameters active and a
three-bit KV cache, and the feed-forward network uses a squared-ReLU gate that produces
about 80% activation sparsity [Wang2024-BitNetA48]. BitNet v2 instead rotates: an
online Hadamard transform inside a modified `H-BitLinear` layer spreads outlier energy
across coordinates so that a plain INT4 or FP4 quantizer suffices for all activations
natively [Wang2025-BitNetV2]. Post-training work has converged on the same rotation
idea with learned or data-adaptive transforms, including butterfly-structured orthogonal
processors [Zagitov2026-HARP], Kronecker-structured rotations [Zhao2026-TWLA],
orthogonal-Kronecker transforms with proximal-SVD refinement that reach W1A6
[Zhao2026-BWLA], and influence-weighted Walsh rescaling [Pavlov2026-InfluenceRotations].
Fig. [fig:datapath] draws the three datapaths side by side: the plain `BitLinear` layer, the
Hadamard-rotated `H-BitLinear` layer, and the hybrid split-and-sparsify path of BitNet
a4.8. The current practical floor for activations alongside roughly one-bit weights is
four bits natively; post-training quantization mostly lands at six bits, though TWLA
reports four through the same Kronecker-rotation family [Zhao2026-TWLA], a result not
yet reproduced independently. Whether A2 is reachable at all is an
open question (Section 11).

## 5.4 KV cache

The KV cache dominates memory for long contexts. BitNet a4.8 and BitNet v2 both quantize
it to three bits with no reported accuracy cost [Wang2024-BitNetA48],
[Wang2025-BitNetV2]. Dedicated KV-cache quantization for ternary models, using
signed-digit lookup schemes and sub-one-bit residual quantization of keys and values,
is an active topic in 2026, although much of it falls after the cutoff of this survey.

## 5.5 Beyond the dense decoder

For mixture-of-experts models, MoTE trains more low-precision experts rather than fewer
high-precision ones. Starting from a dense checkpoint, it up-cycles the feed-forward
network into one shared full-precision expert and many ternary routed experts, keeping
the active-parameter count fixed while eliminating the memory overhead of a
full-precision expert pool [Wang2025-MoTE]. Q-Sparse shows that full activation sparsity
composes with both BitNet b1.58 and mixture-of-experts, and derives an inference-optimal
scaling law for the combination [Wang2024-QSparse].

For state-space models, Bi-Mamba binarizes a Mamba model from scratch with an
autoregressive distillation loss and matches half precision at up to 2.7B parameters,
opening a low-bit path for linear-complexity architectures [Tang2024-BiMamba]; Ternary
Mamba applies grouped quantization-aware training at W1.58A16
[Ganesaraja2026-TernaryMamba].

For sub-1.58-bit representations, Sparse-BitNet observes that ternary models tolerate
N:M structured sparsity far better than full-precision models, since their weights are
already about 42% zero, and applies dynamic N:M sparsification jointly with 1.58-bit
quantization, backed by custom sparse tensor-core kernels [Zhang2026-SparseBitNet].
Sherry regularizes this to a 3:4 pattern that packs to a power-of-two-aligned 1.25 bits
[Huang2026-Sherry]. Structural binarization below one bit [Dong2024-STBLLM] and
latent-factorization schemes that reach about 0.1 bits per weight [Lee2025-LittleBit]
are the current extreme.

## 5.6 One-bit attention and matrix-multiplication-free designs

BitNet quantizes only the projection layers and leaves the attention score computation
in higher precision, which caps the achievable speedup [Malekar2024-MatmulOrNot].
MatMul-free LM removes the remaining matrix multiplications by replacing self-attention
with a gated linear-attention recurrence over ternary `BitLinear` layers, so that the
whole model consists of additions and element-wise operations; it matches an optimized
Transformer baseline up to 2.7B parameters and has been mapped to FPGA and neuromorphic
hardware [Zhu2024-MatmulFree]. One-bit query-key attention and fully additive
accumulation through complex $\{\pm 1, \pm i\}$ codebooks [Wang2025-iFairy],
[Wang2025-Fairy2i] are further points on this line.
