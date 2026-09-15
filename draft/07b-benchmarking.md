# 8. Performance and Benchmarking

## 8.1 The comparison problem

Results in this literature are difficult to align. Papers use different evaluation
harnesses and harness versions, different prompt formats and few-shot counts, and
different perplexity corpora, namely WikiText-2 against C4 validation; on the efficiency
side they differ in hardware, thread count, kernel, and baseline, whether FP16 against
INT8 or a general framework against a custom kernel. The reported number of bits per
weight also varies in what it includes (Section 2.1). We therefore report each claim in
the terms the source used, group claims by what is actually comparable, and flag cases
in which a direct comparison is not sound. Table 1 collects the headline figures; the
common-axis re-tabulation is Table 2; and our own independent measurements are in
Section 10.

## 8.2 Perplexity and the parity claim

The central claim of the native line is parity with a full-precision model of equal size
and training-token budget. BitNet b1.58 reports this from roughly 3B parameters: at 3B,
its WikiText-2 and C4 perplexity matches a reproduced FP16 LLaMA trained on the same
100B RedPajama tokens, its zero-shot average matches from the same scale, and the gap to
FP16 narrows as size grows to 7B [Ma2024-BitNetB158], [Wang2024-BitNetA48]. The Spectra
suites make the stronger claim that a ternary model can match a full-precision model of
equal parameter count: TriLM 3.9B matches FloatLM 3.9B across their benchmark set,
despite a higher perplexity and a size 5.9 times smaller in bits [Kaushal2024-Spectra].
Spectra 1.1 extends this to 1.2T tokens and finds that ternary models gain more from
data than from parameters [Vaidhya2025-Spectra11]. The counter-evidence, discussed in
Section 6.6, is that post-training-quantization degradation grows with training tokens,
so these parity results, all measured at four trillion tokens or fewer, may not
extrapolate [Kumar2024-ScalingLawsPrecision], [Ouyang2024-QiDScaling].

For post-training routes toward one bit, perplexity is the standard yardstick and the
progression is clear: BiLLM reached 8.41 on LLaMA2-70B at roughly 1.08 effective bits
[Huang2024-BiLLM]; DB-LLM cut two-bit perplexity from 9.64 to 7.23 [Chen2024-DBLLM]; the
rotation-and-column-bitmap variant of ARB-LLM was the first binary post-training method
to beat a half-precision model of the same size [Li2024-ARBLLM]; and PTQTP and PT2-LLM
now bring training-free ternary within reach of 1.58-bit quantization-aware-training
accuracy in about an hour, rather than the 10 to 14 GPU-days that training requires
[Xiao2025-PTQTP], [Yan2025-PT2LLM].

## 8.3 Downstream benchmarks

The common zero-shot suite is ARC-Easy, ARC-Challenge, HellaSwag, WinoGrande, PIQA,
OpenBookQA, and BoolQ, run through a standard harness and averaged; native-line papers
report this suite, while post-training-quantization papers more often report perplexity
plus a subset. For instruction-tuned models at the 2B scale, MMLU, GSM8K, and
HumanEval+ are added. BitNet b1.58 2B4T reports a zero-shot average of 54.19 against
55.23 for a full-precision Qwen2.5-1.5B, with the 1-bit model ahead on GSM8K
(58.38 against 56.79, a lead Section 10.3 reproduces) and ARC-Challenge (49.91) and behind
on MMLU (53.17 against 60.25, a deficit Section 10.3 also reproduces), and ahead of an
INT4-AWQ Qwen2.5-1.5B on the average [Ma2025-BitNet2B4T]. The
unified study of ParetoQ is the most useful single reference point: across 1-bit to
4-bit quantization-aware training, ternary, two-bit, and three-bit quantization occupy a
common size-accuracy frontier that beats both four-bit and binary, with a sharp
learning transition between two and three bits below which the representations
reorganize, and a 600M ternary model beats the prior 3B ternary state of the art
[Liu2025-ParetoQ].

## 8.4 Reasoning and generation quality

Two findings from 2025 and 2026 complicate the downstream picture. First, extreme
quantization degrades output smoothness, that is, the number of plausible next tokens in
a prediction neighborhood, independently of perplexity, which sparsifies the decoding
tree and hurts generation quality; a smoothness-preserving term recovers accuracy in
both post-training quantization and quantization-aware training
[Xu2026-FittingNotEnough]. Second, two-bit reasoning models fail not by losing the
answer but by failing to commit to it, which inflates the trace length and negates the
per-token speedup; lightweight FP16 planning and a loop-rescue mechanism recover most of
the gap [Alimaskina2026-ExtremeReasoning]. Whether native 1.58-bit training suffers the
same pathologies as post-hoc two-bit quantization is an open question.

## 8.5 Efficiency

Efficiency is where the numbers are largest and least standardized. On memory, the
non-embedding footprint of BitNet b1.58 2B4T is 0.4 GB against 2.6 GB for a
size-comparable FP16 model [Ma2025-BitNet2B4T], and the size in bits of a TriLM is about
six times smaller than that of an FP16 model with the same parameter count
[Kaushal2024-Spectra]. On latency, the same report gives 29 ms CPU decode against 65 ms,
and BitNet b1.58 at 3B is 2.71 times faster than FP16 LLaMA on GPU, rising to 4.1 times
at 70B as the linear layers come to dominate [Ma2024-BitNetB158]. On throughput, BitNet
b1.58 70B supports about eleven times the batch size and about 8.9 times the throughput
of FP16 LLaMA 70B on two A100 GPUs [Ma2024-BitNetB158]. On energy, the arithmetic saving
for the matrix multiplication alone is about 71 times on a 7-nanometre process, and the
end-to-end decode energy for the 2B model is 0.028 J against 0.186 J to 0.649 J for
full-precision comparators [Ma2024-BitNetB158], [Ma2025-BitNet2B4T]. On the kernel side,
bitnet.cpp reports 2.37 to 6.17 times over FP16 on x86 and 1.37 to 5.07 times on ARM,
with 72% to 82% and 55% to 70% energy reductions and a 100B model at reading speed
on one CPU [Wang2024-1bitAIInfra], [Wang2025-BitNetCPP], though our own run of the 2B
model on an x86 laptop puts the decode speedup over FP16 at about 2 times, below that
range (Section 10.4); the TriRun GPU kernel of
Spectra 1.1 gives a 4.9-times end-to-end speedup for a 70B model on a single L40S GPU
and up to about 78 times on the ternary layer in high-batch settings
[Vaidhya2025-Spectra11]; and LittleBit reports an 11.6-times inference speedup over FP16
at 0.1 bits per weight, compressing Llama2-13B below 0.9 GB [Lee2025-LittleBit].

## 8.6 A common-axis comparison

Table 2 places the field on one set of axes: representation, weight and activation
configuration, a consistent effective-bits figure (the nominal code width plus the
amortized cost of scales, masks, and codebooks), the headline accuracy in the terms of
the source, and the headline efficiency claim, each with its evidence basis (venue and
whether the result has an independent check, per Section 3.3). All numbers
are author-reported; Section 10 substitutes independent measurements for a subset.

Three points become visible only once the numbers are aligned. First, the reported
number of bits often understates real storage. The headline figures for salient-split
binary post-training quantization, such as 1.08 for BiLLM and about 1.1 for ARB-LLM,
count only the code; a strict accounting that includes group-wise scales and bitmaps
puts BiLLM at about 2.88 and STBLLM at about 4.13 effective bits per weight
[Chong2026-NanoQuant]. Native ternary, by contrast, is a genuine 1.58 bits, or between
1.25 and 2.0 bits depending on the packing; Fig. [fig:effbits] plots the reported and
effective figures side by side wherever both are known. Second, the "1-bit post-training quantization"
line and the "native ternary" line are not at the same operating point.
Post-training methods that claim roughly one bit almost always keep something in higher
precision: salient columns (PTQ1.61 at 1.61, PB-LLM at 1.70), a residual branch (RaBiT
at a nominal two bits and an effective 2.02), or higher-precision activations
(DBellQuant and BWLA at A6). Genuine one-bit weights and activations exist only in
native training, and only below about 1B parameters [Panferov2025-QuEST]. Third, the
strongest cross-method claim is comparative rather than absolute. The unified study of
ParetoQ is the reference point: ternary, two-bit, and three-bit quantization occupy a
common size-accuracy frontier that beats four-bit and binary [Liu2025-ParetoQ]. Most
results from 2025 and 2026, including CAT-Q reaching an accuracy comparable to BitNet v2
with a factor of 100,000 fewer tokens through post-training quantization
[Wang2026-CATQ], HESTIA matching 100B-token native training with 10B tokens
[Wang2026-HESTIA], and LC-QAT matching quantization-aware training with 1% to 10% of
the data [Wang2026-LCQAT], concern closing the cost gap at roughly fixed accuracy rather
than pushing accuracy itself.

Splitting Table 2 by evidence basis (Section 3.3) shows that the central claims do not
rest on the least reliable sources. Twenty-eight of the 57 rows are corroborated, that
is peer reviewed or with an independent check, and every source behind the parity claim,
namely BitNet b1.58, BitNet b1.58 2B4T, both Spectra suites, and ParetoQ, is in that
set: Spectra, ParetoQ, and the original BitNet b1.58 corroborate one another, ParetoQ is
also at NeurIPS, and Section 10 re-runs the released BitNet b1.58 2B4T checkpoint and
adds a controlled test of the parity claim on Spectra's matched TriLM and FloatLM pair,
which lands within 0.6 points on a seven-task mean at 2.4B parameters with a higher
perplexity. That bears on the claim at this scale; whether it holds at the frontier is a
separate question that Section 11.1 lists as open. The other 29 rows are single unreproduced preprints, most of
them post-training-quantization results claiming the lowest bit counts (BTC-LLM at 0.8,
HBLLM at 1.08, DBellQuant and BWLA at 1.0), together with the bitnet.cpp infrastructure
report, which moved into this group once we found that its reference runtime does not
compute this model correctly as built (Section 10). Any statement in this section that
rests only on single unreproduced preprints is marked as such, following the convention
set in Section 3.3.

## 8.7 Summary of the benchmarking evidence

Three statements are defensible. Native ternary training is reported, at up to about 7B
parameters and 4T tokens, to match full precision on standard benchmarks; those figures
are author-reported rather than independently re-run at that scale (Section 10 checks a
smaller one), and whether parity holds at the frontier is untested and disputed. Post-training routes have closed most of the
gap to 1.58-bit quantization-aware-training accuracy at a fraction of the cost, but only
down to a two-bit equivalent; genuine one-bit post-training quantization still trails.
The efficiency gains on CPU are large and independently plausible; the GPU and
custom-silicon gains are reported from kernels and simulators rather than deployed
systems, and Section 10 tests the CPU claims directly.
