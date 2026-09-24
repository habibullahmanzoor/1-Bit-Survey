# 1. Introduction

## 1.1 The inference wall

The dominant cost of a deployed large language model (LLM) is no longer training but
inference. Every generated token requires a full forward pass, and for autoregressive
decoding that pass is bounded not by arithmetic throughput but by the movement of
weights from memory into the compute units. Accelerator peak throughput, measured in
floating-point operations per second, has grown far faster than dynamic-memory bandwidth
for a decade: as the Spectra analysis notes, GPU operations per second have
doubled roughly every 1.26 years against every 2.9 years for memory bandwidth
[Kaushal2024-Spectra]. The arithmetic-to-bandwidth ratio of hardware
has therefore drifted steadily away from what dense half-precision inference requires. The practical
consequences are by now familiar: multi-GPU servers are needed for models that would
otherwise fit on a single card; inference energy budgets draw scrutiny on
sustainability grounds; and running a capable model on a phone, a laptop, or an
embedded board without a network round trip remains largely infeasible.

Quantization addresses this wall directly by reducing the number of bits per weight,
and hence the number of bytes that must cross the memory hierarchy. Eight-bit and
four-bit post-training quantization are now routine. Below four bits, however, accuracy
degrades sharply for models that are quantized after training [Huang2024-BiLLM],
[Shang2023-PBLLM], and a growing body of scaling-law analysis indicates that this
degradation is not a transient engineering problem. For a fixed architecture, the loss
added by low-bit quantization grows with the number of training tokens, so that the
better trained the base model, the worse post-hoc compression treats it
[Ouyang2024-QiDScaling], [Kumar2024-ScalingLawsPrecision].

## 1.2 The native 1-bit paradigm

A separate line of work avoids that ceiling by making the low-bit constraint part of
the model from the first optimization step. BitNet introduced the `BitLinear` layer, a
drop-in replacement for a standard linear layer that binarizes weights in the forward
pass and trains through the non-differentiable quantizer using a straight-through
estimator. The resulting 1-bit Transformers follow a loss-versus-scale curve parallel
to that of full-precision models [Wang2023-BitNet], [Wang2025-BitNetJMLR]. BitNet b1.58
then moved from binary weights in the set {-1,+1} to ternary weights in {-1,0,+1},
which carry $\log_2 3 \approx 1.58$ bits of information per parameter, and reported
parity with a half-precision Transformer of equal size and training-token budget from
roughly the 3B-parameter scale upward, at a fraction of the memory, latency, and energy
[Ma2024-BitNetB158]. In 2025 this became concrete with BitNet b1.58 2B4T, an openly
released 2B-parameter model trained natively on 4T tokens that matches similarly sized
full-precision open models on standard benchmarks [Ma2025-BitNet2B4T].

A native 1-bit model is defined by when the low-bit constraint is imposed, during
training rather than after, which is what lets it reach an accuracy a post-hoc
quantization of the same architecture does not (Section 8.2). The inference-time
arithmetic benefit is a separate property of the resulting representation, not of how
the weights got there: whenever every weight lies in {-1,0,+1}, whether from native
training or post-hoc quantization, the multiplication in a matrix-vector
product disappears: each output element is an accumulation of additions and
subtractions of activation values, gated by the sign of the weight. This removes the
multiplier, which is the largest and most power-hungry component of a digital
multiply-accumulate unit, from the inner loop, and it changes what the ideal hardware
looks like [Malekar2024-MatmulOrNot], [Zhu2024-MatmulFree]. It also shifts the binding
constraint. Once weights occupy roughly one bit, activation precision and the memory
traffic of the key-value (KV) cache dominate, which is why the frontier of the field
has moved toward four-bit and lower activations and toward three-bit KV caches
[Wang2024-BitNetA48], [Wang2025-BitNetV2].

## 1.3 Related surveys

The literature has grown from a handful of papers in 2023 to a steady stream through
2026, spanning native pre-training recipes, post-training routes toward one bit,
optimization theory, inference kernels, and a first wave of custom accelerators
(Fig. [fig:timeline]). Four existing surveys touch this area. Gong et al.
[Gong2024-SurveyLowbit] review low-bit LLMs broadly, from eight-bit integer down to
binary, with a systems-and-algorithms structure and a mid-2024 horizon. Liu et al.
[Liu2025-SurveyBNNLLM] survey the binarization of LLMs; this framing under-weights
ternary representations, even though ternary is where native training has succeeded.
Hao et al. [Hao2025-LowPrecTrainingSurvey] survey low-precision training across all
numerical formats in IEEE TPAMI, treating 1-bit models as one subsection and not
covering inference systems or hardware. Jørgensen [Jorgensen2025-ResourceEfficientLMs]
reviews quantization for fast and accessible inference in general and mentions 1-bit
models only in passing. None is scoped to the native 1-bit and 1.58-bit
paradigm as a coherent object of study. And none covers the 2025 and 2026 wave: BitNet
b1.58 2B4T, BitNet a4.8, and BitNet v2; GPU and CPU inference kernels; 1-bit embedding,
speech, and vision-language-action models; ternary mixture-of-experts; and the first
lookup-table ASICs and compute-in-ROM accelerators.

This paper adds two things the existing surveys do not. First, a single common-axis
comparison: every surveyed work is placed on a five-axis taxonomy (Section 4), and that
classification is what lets otherwise incomparable results be tabulated together,
reported accuracy in consistent columns and, more substantively, reported bit-widths
re-stated under one effective-bits accounting, so that a "1.08-bit" post-training method
and a genuine 1.58-bit native one can be read on the same scale (Section 8). Second, and
centrally, an independent re-measurement.

On accuracy, we run a controlled test the vendor comparisons lack: a native ternary model
against its FP16 counterpart at matched parameter count, tokenizer, and training data,
from open artifacts. At the 2.4-billion-parameter scale the two land within 0.6 points on
a seven-task zero-shot suite, with the ternary model's perplexity about 14% higher,
downstream parity with a worse language-modeling loss. A post-hoc 4-bit quantization
loses more of the suite than that, and a 1.58-bit model at the one-billion-parameter
scale loses much more, a pattern the paper's abstract already flags as suggestive rather
than conclusive: two data points, one of them a checkpoint pair whose training match is
undocumented (Section 10.2), cannot on their own settle whether scale is the real
explanation.

On efficiency, the finding is sharper than the literature's framing. We rebuild the
reference runtime and run the flagship open 1-bit model against half-precision, 8-bit,
and three 4-bit builds on one commodity x86 machine. Each of the three 4-bit builds
decodes at least as fast as the ternary model and is smaller on disk; the k-quant format
among them, the one we also measured for energy, is comparable on per-token energy, and
on the two accuracy tasks scored through the same runtime it holds close. The ternary
model's one retained advantage is a 24-to-27% smaller resident set. On
this hardware, then, a 1-bit model shows no observed advantage over a standard 4-bit
quantization on
throughput or on-disk size, and no more than parity on energy; its efficiency case at
this scale holds against half precision and an 8-bit baseline but not against 4-bit, and
a GPU and a second machine are untested. The
reference runtime, moreover, does not run this model correctly as documented, applying
the wrong feed-forward activation until a one-line source fix (Section 10.3), a sign that
the open deployment path for these models is not yet mature. These are the paper's
principal findings.

## 1.4 Contributions

1. **An independent re-evaluation.** For accuracy we run three pairs from
 open matched checkpoints, controlled to varying degrees (Section 10.3): native ternary
 against FP16 at a matched 2.4B parameters (within 0.6 points on a seven-task mean), a
 4-bit quantization against its full-precision source, and a 1B model in 1.58-bit and
 bf16 form whose training match to its comparator is undocumented; and we re-measure MMLU
 and GSM8K, which an earlier version of the study had left out. For efficiency we rebuild the
 reference bitnet.cpp runtime and measure decode and prefill throughput, resident memory,
 and on-disk size for the flagship open 1-bit model against half-precision, 8-bit, and
 three 4-bit builds, on one x86 laptop. We also measure per-token battery energy against
 the half-precision, 8-bit, and 4-bit k-quant builds on the same machine (Section 10.4).
 On that machine the paradigm's
 advantage over half precision does not extend to any 4-bit build: each decodes at least
 as fast and is smaller on disk, and the k-quant format, the one we also checked for
 energy and for accuracy on two tasks, matches the ternary model on per-token energy and
 holds close on accuracy; the 1-bit model keeps only a 24-to-27% resident-memory edge. A by-product of
 the exercise is a symptom worth recording: the reference runtime, built from source as
 its documentation describes, does not run this model correctly, applying a
 half-precision-era feed-forward activation where the model needs a squared-ReLU, so that
 a practitioner following the documented path gets near-broken output until a one-line
 source change (Section 10.3). The open deployment path for these models is not yet
 mature.
2. **A common-axis comparison.** Reported accuracy is re-tabulated in consistent columns
 (still in each source's own evaluation terms), and reported bit-widths are re-stated
 under one effective-bits accounting (nominal code width plus the amortized cost of
 scales, masks, and codebooks), so that
 methods using incompatible setups can be read side by side (Section 8, Table 2).
3. **A curated review and taxonomy.** We survey 135 open-access works of the native
 1-bit and 1.58-bit paradigm from January 2023 to June 2026, plus five foundational
 works from 2013 to 2022 for context, and classify every one on a five-axis taxonomy of
 weight representation, training paradigm, quantized components, optimization mechanism,
 and systems stack, with a secondary cut by modality (Section 4, Fig. [fig:taxonomy],
 Table 1). This is a curated, arXiv-primary review, not a systematic one (Section 3.2).
4. **A research agenda** stated as concrete, testable open problems: the capacity
 ceiling and its dependence on the training-token budget, training stability at frontier
 parameter scale, the activation-precision floor, a convergence theory for
 straight-through training, the absence of a shipping processor with a ternary
 matrix-multiplication primitive, and the robustness and safety profile of 1-bit models
 (Section 11).

## 1.5 Scope

This paper covers the native paradigm, in which the sub-two-bit constraint is present
during training, together with the post-training and quantization-aware branches that
explicitly target 1.58 bits or fewer, the kernels and hardware that execute such models,
and the theory that explains their behavior. General sub-four-bit quantization, pruning,
distillation for speed, and long-context or serving-system work are cited only where
they bear directly on the 1-bit case.

The corpus is open-access only: for every work a freely downloadable version exists on
arXiv, in JMLR or PMLR, in the ACL Anthology, on OpenReview, on a gold open-access
journal page, or in an official model or framework repository, and a local copy has been
archived. This is a deliberate choice, so that every technical claim is re-checkable
without a paywall and so that the re-measurement of Section 10 can use the exact
released artifacts. One work met every other criterion but had no obtainable
open-access copy and was set aside; its abstract, with those of the paywalled records
the search surfaced, was checked against every major conclusion, and none would change
(Section 3).

## 1.6 Organization

Fig. [fig:roadmap] maps the paper. Section 2 fixes notation and background. Section 3
states the scope and how the corpus was assembled. Section 4 presents the taxonomy. Sections 5, 6, and 7 cover architecture,
training, and inference systems. Section 8 presents the common-axis comparison. Section 9
surveys applications and extensions. Section 10 reports the independent re-evaluation,
the analytical core of the paper alongside Section 8. Section 11 sets out the open
problems, and Section 12 concludes.
