# 10. Independent Re-Evaluation

## 10.1 Rationale and scope

The efficiency figures that motivate this paradigm are almost all author-reported and no
third party has re-checked them, including the efficiency table for BitNet b1.58 2B4T of
0.4 GB, 29 ms, and 0.028 J [web-bitnet2b4tCard] and the 2.37-to-6.17-times bitnet.cpp
speedups [Wang2024-1bitAIInfra], all quoted against a half-precision baseline. This
section re-measures a small, well-defined subset of those claims on commodity hardware,
adding the 8-bit and 4-bit baselines a practitioner would actually compare against. It
verifies published claims; it does not train models or ablate methods.

## 10.2 Setup

For Arm A (the accuracy arm), we use EleutherAI's lm-evaluation-harness at commit
`b954108` (pinned 4 September 2026), on a laptop RTX 4080 with 12 GB of memory shared
with other workloads, with the batch size capped so that memory use stays within budget.
The primary pairing is BitNet b1.58 2B4T [Ma2025-BitNet2B4T], about 2.4 billion
parameters in total and 2.0 billion outside the token embedding, against
Qwen2.5-1.5B-Instruct, about 1.5 billion parameters, the full-precision model the BitNet
2B4T card itself compares against. That pairing is **not a controlled baseline**: the two
differ in parameter count, architecture, tokenizer, and training data. To address that we
add three comparisons from open checkpoints, in decreasing order of how tightly matched
they are. The cleanest is Spectra's TriLM and FloatLM at 2.4 billion parameters,
identical tokenizer, data, and 300-billion-token budget, ternary trained from scratch
against FP16 trained from scratch [Kaushal2024-Spectra]. Next, Qwen2.5-1.5B-Instruct in
bf16 against a 4-bit (nf4) quantization of the same weights, which isolates the cost of
post-hoc 4-bit compression. Least tightly matched is Falcon3-1B in its 1.58-bit and its
bf16 form: TII trains the 1.58-bit model with ternary weights from pre-training and
releases a bf16 checkpoint alongside it [web-falconEdge], but does not document whether
that bf16 checkpoint is a dequantized copy of the same run or the earlier full-precision
Falcon3-1B, so this pair is matched in model family and parameter count but not
demonstrably in training data or schedule. All checkpoints are the
instruction-tuned variants where one exists, evaluated without a chat template as the
harness default; the tables abbreviate Qwen2.5-1.5B-Instruct to Qwen2.5-1.5B. The tasks
are the seven-task zero-shot suite (ARC-Easy, ARC-Challenge, HellaSwag, WinoGrande, PIQA,
OpenBookQA, and BoolQ) reported as plain accuracy, plus WikiText-2 word perplexity and
MMLU at zero shot. Each model is run once, with a HellaSwag determinism check.

MMLU is run at zero shot rather than the card's five: BitNet's native Hugging Face layer
compiles per input shape, and the fifty-seven MMLU subjects each carry a different
five-shot context length, which thrashes the compilation cache; zero shot keeps a fixed
shape and runs at the speed of the rest of the suite. GSM8K, dropped from an earlier
version of this study, is re-measured here (Section 10.3), but on its own terms: it needs
multi-step generation and the model's chat template, so it is run at five shot with the
template applied and generation to 256 tokens, and its numbers are not comparable to the
loglikelihood, template-free suite above. A build note: on Windows, that native layer only compiles at
all with a Triton build matching the installed PyTorch; without it it runs eagerly and
even the zero-shot suite is several times slower.

For Arm B (the efficiency arm), we build the reference bitnet.cpp runtime from source and run
every model through that one binary: its I2_S ternary kernel serves the BitNet
checkpoint, and the llama.cpp code path it is built on serves the Qwen2.5-1.5B
baselines at five quantization levels: FP16, Q8_0, and three 4-bit formats, Q4_0,
Q4_K_S, and the Q4_K_M k-quant that is the common default for local inference. The FP16
baseline here is an FP16 GGUF of the same Qwen checkpoint whose BF16 weights the accuracy
arm loads; the C++ runtime has no BF16 path, and the two formats are numerically close,
so the accuracy and efficiency baselines are the same model in the nearest format each
runtime supports and are not compared against each other. The 4-bit comparison is on this
one x86 machine only; a GPU, a second CPU, and quantizers outside the GGUF family such as
AWQ or GPTQ would each be needed to generalize it further. Every measurement shares a
runtime, a machine, and a harness. The machine is an Intel Core i9-14900HX laptop, eight performance cores
and sixteen efficiency cores, on AC power. We sweep threads over 1, 2, 4, 8, and 16,
take prefill at 128, 512, and 2048 tokens and decode at 128 tokens, and repeat every
point five times through the bundled `llama-bench`. Peak resident memory is sampled from the process working set
during a decode run. Energy is measured in a separate pass on battery, where the
smart-battery controller exposes whole-system power to the operating system as a
discharge rate (it reads zero on AC, and this machine has no running-average
power-limit counter); we sample that rate during a thirty-second idle window and during
a sustained decode, and divide mean power by the decode rate. The energy pass covers the
ternary model and the half-precision, 8-bit, and 4-bit k-quant baselines. On battery the
processor runs at a lower power limit, and that limit tightens as the battery drains, so
the pass is slower than the plugged-in sweep, absolute energy figures drift across runs,
and only within-run model-to-model ratios are compared.

Three notes on getting the runtime to work. It does not link as a shared library on this
toolchain, because the core ggml library references an I2_S quantiser symbol that lives
only in the CPU backend; a static build resolves it. Its BitNet feed-forward activation
is set to SiLU where BitNet b1.58 2B4T uses a gated squared-ReLU, which we changed and
rebuilt (Section 10.3); the throughput figures are the same either way. And the TL2
lookup-table kernel, which needs a per-shape code-generation step shipped only for older
BitNet sizes, was not exercised, so the ternary figures are I2_S only. We built
microsoft/BitNet at commit `0b341e5`, whose `3rdparty/llama.cpp` submodule was at
commit `390c307`; the one-line fix changes `LLM_FFN_SILU` to `LLM_FFN_RELU_SQR` in
`src/models/bitnet.cpp`.

## 10.3 Accuracy results

Table [tab:acc-primary] reports, for the primary pairing, plain accuracy on the
seven-task zero-shot suite, its mean, WikiText-2 word perplexity at a 2048-token stride,
and MMLU at zero shot. Both HellaSwag determinism checks reproduced to the last digit across two
independent runs. Accuracy is the unnormalized figure (`acc`); we report it rather than
the length-normalized `acc_norm` so that one metric is used across all seven tasks. For
HellaSwag the two diverge widely, `acc_norm` is 67.6 for BitNet and 68.3 for Qwen,
because the endings vary in length and an unnormalized log-likelihood favours the shorter
ones; this is why the HellaSwag column reads near 50 while the vendor's length-normalized
figure is near 68, and why the C++ runtime's own HellaSwag scorer (Table [tab:quant-cost]),
which averages log-probability per ending token, lands between the two at about
62 to 66. The metric, not the runtime, accounts for the gap.

| model | ARCe | ARCc | HS | WG | PIQA | OBQA | BoolQ | mean | ppl | MMLU |
|---|---|---|---|---|---|---|---|---|---|---|
| BitNet b1.58 2B4T (W1.58, 2.4B) | 76.8 | 47.0 | 50.7 | 72.5 | 77.0 | 30.8 | 79.0 | 61.98 | 16.67 | 52.07 |
| Qwen2.5-1.5B-Instruct (BF16, 1.5B) | 76.7 | 43.6 | 50.9 | 62.7 | 76.3 | 31.8 | 78.0 | 60.00 | 13.48 | 60.03 |
Table: {#tab:acc-primary} Independent accuracy re-measurement of the primary pairing: unnormalized accuracy (*acc*) on the seven-task zero-shot suite with its mean, WikiText-2 word perplexity at a 2048-token stride, and MMLU at zero shot. One run per model, with a HellaSwag determinism check. HellaSwag's unnormalized *acc* reads near 50 for both models by design (an unnormalized log-likelihood favors shorter endings, discussed below); the length-normalized *acc_norm* both vendors and papers usually quote is near 68 for both.

Two comparisons matter. First, against the vendor figure: the BitNet b1.58 2B4T model
card reports a headline "zero-shot average" of 54.19, below our 61.98 on the seven-task
suite and below its own reference Qwen. That figure averages a broader set that includes
MMLU and GSM8K, and most of the difference is MMLU. Our zero-shot MMLU, 52.07 for BitNet
against 60.03 for Qwen, closely tracks the card's five-shot values (53.17 and 60.25) under a
different protocol, and matches its
roughly eight-point deficit: the ternary model is competitive on commonsense reasoning
but clearly behind on world knowledge, and any average that folds MMLU in inherits that
gap. A single vendor "average" is not portable across evaluation setups; per-task numbers
are the only safe unit of comparison.

Second, the controlled comparisons. The BitNet-versus-Qwen pairing is not size- or
training-matched, so we ran three pairs from open artifacts that are, each in its own
right (Section 10.2):

| pair (most to least matched) | ternary or 4-bit | full precision | Δ mean | ppl | Δ MMLU |
|---|---|---|---|---|---|
| Spectra 2.4B, native ternary vs FP16 (300B tok) | TriLM 51.49 | FloatLM 52.05 | -0.56 | 14.90 vs 13.06 | -2.2 |
| Qwen2.5-1.5B, nf4 4-bit vs bf16 | 57.33 | 60.00 | -2.67 | 14.59 vs 13.48 | -2.0 |
| Falcon3-1B, 1.58-bit vs bf16 (checkpoint relation undocumented) | 45.69 | 57.22 | -11.53 | 32.82 vs 18.85 | -18.4 |
Table: {#tab:acc-controlled} Three pairs from open checkpoints, in decreasing order of how tightly matched they are: change in seven-task mean, WikiText-2 perplexity, and zero-shot MMLU for the ternary or 4-bit member against its full-precision counterpart.

Three things follow (Fig. [fig:controlledpairs] plots the three pairs' seven-task means
against each other directly). The Spectra pair, the cleanest test, puts native ternary within
0.6 points of FP16 on the seven-task mean at 2.4 billion parameters, with perplexity 14%
higher: downstream parity alongside a worse language-modeling loss, the exact shape the
native-training literature reports for itself (Section 8.2), now measured under a matched
protocol rather than inferred. Both Spectra models score near chance on MMLU, so that
column is uninformative for this pair; the 300-billion-token budget simply does not buy
world knowledge at 2.4 billion parameters. Second, post-hoc 4-bit quantization of Qwen
costs 2.7 points on the mean and 2.0 on MMLU, more than native ternary loses at a
comparable scale, consistent with the ParetoQ finding that ternary quantization-aware
training sits ahead of four-bit post-training quantization on the size-accuracy frontier
(Section 8.3).

Third, and this is the part that most constrains how far the parity result generalizes,
the Falcon3-1B pair loses heavily: 11.5 points on the seven-task mean, a 74% higher
perplexity, and MMLU driven to chance. This pair cannot separate a scale effect from a
training-recipe one, both because it is at one-billion rather than multi-billion
parameters and because its two checkpoints are not demonstrably matched in training data
(Section 10.2). What it does establish is a clean negative: the 1.58-bit format at the
one-billion-parameter scale does not inherit the parity that native ternary shows at 2.4
billion, though with the checkpoint match unresolved, that negative could reflect the
pair's mismatch as readily as it could reflect scale. Taken together, the two pairs that
are matched closely enough to compare are consistent with parity being a property of
native ternary pre-training carried out at multi-billion scale rather than a general
consequence of constraining weights to 1.58 bits, but two pairs, one of them confounded,
do not establish that on their own; whether it holds above the roughly 2B, 4T-token
ceiling at which it has been measured is the open question of Section 11.1. The uncontrolled
BitNet-versus-Qwen result, a slight lead for the 2B ternary model on the seven-task mean
and a deficit on perplexity and MMLU, sits consistently between the Spectra and the 4-bit
pairs.

GSM8K is the one benchmark the seven-task suite leaves out, because it needs multi-step
generation rather than a single loglikelihood; we re-measure it separately, at five shot
with each model's chat template and greedy generation to 256 tokens (Table [tab:gsm8k]).
The two extraction rules that the standard harness reports are worth keeping apart:
flexible-extract takes the last number in the output, strict-match accepts only the
canonical answer line. For BitNet and the full-precision Falcon3-1B the two nearly agree;
for the other models they diverge sharply, the model reaching a right answer but not
ending in the canonical form, so the flexible figure is the one that tracks arithmetic
ability and the one we compare on. On it, three things follow. First, the vendor's
GSM8K claim reproduces in direction: BitNet b1.58 2B4T scores 61.9 against our own Qwen2.5-1.5B's 57.5,
a 4.4-point lead where the card reports a 1.6-point one (58.38 against 56.79), so the one
benchmark on which the card puts the 1-bit model ahead holds up under an independent run.
Second, the 4-bit nf4 quantization of Qwen costs 7.8 points on GSM8K, against 2.7 on the
seven-task mean: arithmetic is more fragile under post-hoc quantization than commonsense
reasoning is. Third, the controlled 1B and 2.4B pairs behave as they did elsewhere, the
1.58-bit Falcon3-1B losing 17 points against its bf16 form and both Spectra models sitting
at the GSM8K noise floor, uninformative for that pair exactly as MMLU was.

| model | flexible-extract | strict-match |
|---|---|---|
| BitNet b1.58 2B4T | 61.9 | 59.6 |
| Qwen2.5-1.5B-Instruct, bf16 | 57.5 | 35.0 |
| Qwen2.5-1.5B-Instruct, nf4 4-bit | 49.7 | 36.8 |
| Falcon3-1B-Instruct, bf16 | 44.7 | 42.6 |
| Falcon3-1B-Instruct, 1.58-bit | 27.7 | 7.4 |
|---|---|---|
| Spectra TriLM 2.4B, no template | 3.0 | 1.9 |
| Spectra FloatLM 2.4B, no template | 1.9 | 1.3 |
Table: {#tab:gsm8k} GSM8K exact-match accuracy at five shot, with generation and the chat template for the instruction-tuned models above the rule (the Spectra base models below the rule carry no template, are run template-free, and sit at the GSM8K noise floor rather than being meaningfully tested). flexible-extract takes the last number in the output; strict-match accepts only the canonical answer line. These numbers use a different protocol from the loglikelihood suite of Table [tab:acc-primary] and are not folded into any mean.

We separately checked the accuracy cost of the quantizations used in the efficiency arm,
running WikiText-2 perplexity and a HellaSwag subset (the first 1000 of 10042 items)
through the C++ runtime's own batched evaluators (`llama-perplexity`, whose HellaSwag
mode averages log-probability per ending token) so the three Qwen levels are measured
against each other under one scorer. This is a narrow check, two metrics rather than the
full seven-task suite, and it is not a substitute for running that suite on the 4-bit
model, which the runtime's harness does not support. Quantizing the baseline is cheap on
these two tasks: the 8-bit build costs 0.1% on perplexity, and the 4-bit k-quant costs
4.5% on perplexity (9.25 against 8.85). On the HellaSwag subset the observed differences
were small, 0.5 points for the 8-bit build and 0.3 for the 4-bit k-quant against half
precision's 65.3%, within the
marginal confidence intervals; we did not run a paired significance test, so this rules
out a large accuracy drop but not a small one.

| model | WikiText-2 ppl | HellaSwag (n=1000) |
|---|---|---|
| Qwen2.5-1.5B, FP16 | 8.85 | 65.3% |
| Qwen2.5-1.5B, Q8_0 | 8.86 | 65.8% |
| Qwen2.5-1.5B, Q4_K_M | 9.25 | 65.6% |
Table: {#tab:quant-cost} Accuracy cost of the GGUF quantizations used in the efficiency arm, scored through the C++ runtime's own batched evaluators so the three Qwen levels are measured alike: WikiText-2 perplexity and a 1000-item HellaSwag subset.

The BitNet checkpoint needed a source fix to the runtime before it produced sensible
output at all. Built from the project as documented (commit `0b341e5`, `llama.cpp`
submodule at `390c307`, Section 10.2), the runtime's BitNet graph selects a SiLU
feed-forward activation, whereas BitNet b1.58 2B4T uses a gated squared-ReLU (its
released configuration sets the feed-forward activation to squared-ReLU); this is an open
issue in the project. The fix is a one-line change to the activation selector in the
BitNet model source, from SiLU to squared-ReLU (`LLM_FFN_SILU` to `LLM_FFN_RELU_SQR` in
`src/models/bitnet.cpp`). Left uncorrected, WikiText-2 perplexity through the runtime is 86.9 and
HellaSwag is 38.7%, far below any working model. Changing that one line and rebuilding
brings token-level WikiText-2 perplexity to 12.99 and HellaSwag
to 62.4%, both in line with the transformers implementation of the same weights (16.67
word-level perplexity, HellaSwag near 62 to 68 depending on the metric); the throughput
and memory figures of Section 10.4 are unchanged, since a squared-ReLU costs no more than
a SiLU. The released weights are therefore sound; the defect we traced is in the reference
runtime, not the checkpoint, though it is not the only rough edge we found there (below),
and we did not catch it until the results were scrutinized. One report questions
the checkpoint itself, reading its 1,187,801,280-byte size as a truncated re-upload with
empty feed-forward tensors [web-bitnetIssue608]; this is
the shared-embedding layout, in which the model keeps no separate output projection, and
a checkpoint with zeroed feed-forward weights could not reach a perplexity in the low
teens under any activation, so that reading is inconsistent with the result here. The
file used is pinned to Hugging Face revision `a1f2f1c765812aa8af3f6eda4a313707064bba15`,
SHA-256 `4221b252fdd5fd25e15847adfeb5ee88886506ba50b8a34548374492884c2162`. A separate,
minor issue remains: the GGUF omits the `tokenizer.ggml.pre` field, so the runtime warns
and falls back to a default pre-tokenizer; we did not run a matched-tokenization check
to isolate its effect, but the activation-corrected perplexity and HellaSwag scores
landing in the expected range suggest it is small. The two runtime perplexities that can be
stated, 12.99 from llama.cpp and 16.67 from transformers (the accuracy table above), are
not directly comparable, since one is a token-level and the other a word-level figure on
different tokenizations; both are in the range the model card implies.

## 10.4 Efficiency results

Table [tab:efficiency], and Fig. [fig:efficiency], report decode throughput, prefill throughput,
on-disk size, and peak resident memory. The Qwen baseline is shown at four 4-bit and
low-bit settings, Q4_0, Q4_K_S, Q4_K_M, and Q8_0, plus FP16, so the 4-bit comparison
does not hinge on one format. Throughput is
reported at a common four-thread operating point: that is BitNet's own decode optimum on
this hybrid-core part, and holding it fixed keeps the comparison on one setting. It is
not the global optimum for every model, so we also give each model its own best point
below, and the ordering is the same either way. Prefill is the 512-token point; decode
generates 128 tokens; each throughput figure is the mean of five repeats, with the
standard deviation shown. Disk size is exact; peak resident memory is a single sample
taken at eight threads and is essentially thread-independent.

| configuration | decode tok/s | prefill tok/s | disk (GiB) | peak RAM (GB) |
|---|---|---|---|---|
| BitNet b1.58 2B4T, I2_S | 28.6 (1.6) | 108.9 (5.2) | 1.10 | 1.22 |
| Qwen2.5-1.5B, Q4_0 | 36.3 (1.1) | 116.1 (0.8) | 0.99 | 1.66 |
| Qwen2.5-1.5B, Q4_K_S | 28.7 (4.8) | 109.4 (5.4) | 1.00 | 1.64 |
| Qwen2.5-1.5B, Q4_K_M | 33.8 (0.3) | 107.6 (2.7) | 1.04 | 1.60 |
| Qwen2.5-1.5B, Q8_0 | 24.1 (0.1) | 72.4 (3.1) | 1.76 | 1.64 |
| Qwen2.5-1.5B, FP16 | 14.4 (0.3) | 70.9 (0.8) | 3.31 | 3.02 |
Table: {#tab:efficiency} Independent efficiency re-evaluation on one x86 laptop at a common four-thread operating point: decode and prefill throughput (mean of five repeats, standard deviation in parentheses), on-disk size, and peak resident memory, for the BitNet I2_S checkpoint and Qwen2.5-1.5B at five GGUF quantization levels.

Against FP16 the vendor's direction reproduces: the ternary model decodes 1.99 times as
fast, close to the roughly 2.2-times ratio the card's own table implies. The memory
claim does not carry over as stated: the card's 0.4 GB against 2.6 GB, a 6.5-times
advantage, is a weights-only, non-embedding accounting, whereas the running process
needs 1.22 GB against FP16's 3.02 GB once the 128k-vocabulary embedding, the key-value
cache, and the compute buffers are counted, a 2.5-times advantage. Absolute decode is
35 ms per token against the card's 29 ms, consistent given a different processor.

A comparison closer to deployment is against the 4-bit builds people actually run
locally, and against every one of them, on this machine, the ternary model has no
decode-speed or disk-size advantage and only a narrow memory one. At the common
four-thread point it decodes no faster than any of the three 4-bit formats and slower
than two of them: 28.6 tokens per second against 36.3 for Q4_0, 33.8 for Q4_K_M, and
28.7 for Q4_K_S, whose four-thread run was noisy and which reaches 33.8 at eight
threads. All three 4-bit builds are smaller on disk (0.99 to 1.04 GiB against 1.10) and
tie or beat it on prefill. The ternary model does keep a resident-memory edge, 1.22 GB
against 1.60 to 1.66 GB, about 24 to 27%. Giving each model its own best thread count
does not change the ordering: BitNet's fastest decode is 28.6 at four threads, while
Q4_0 reaches 36.3 at four and the two k-quants reach 33.8 to 34.2 at eight; BitNet's
fastest 512-token prefill is 112 at eight threads against 116 to 132 for the 4-bit
formats at their best. Its 2.4B parameters, only 2.0B of them outside the token
embedding (Section 10.2), are why: a naive estimate from parameter count and nominal
bit-width alone, 2.4B at roughly 1.6 bits, predicts under half a gigabyte, well below
the measured 1.10 GiB. The gap is the token-embedding table, which is not
ternary-packed and is a larger share of this smaller model's parameters than Qwen's
embedding is of its own 1.5B; that overhead, not a straightforward bit-width trade-off,
is most of why the two on-disk sizes land so close together. Against Q8_0 the picture is intermediate: 1.19
times on decode, 0.74 times on memory. Decode throughput for every model peaks at four
or eight threads on this hybrid-core part and falls off at 16 as the efficiency cores
and memory bandwidth become the limit; prefill for every model keeps scaling to 8 or 16
threads. The 2.37-to-6.17-times bitnet.cpp speedups quoted elsewhere
[Wang2024-1bitAIInfra] are measured against FP16 at 3B parameters and above; this 2B,
x86 point sits below that band, and against a 4-bit baseline on this machine it inverts
for all three formats tested. Whether it also inverts on a GPU or a different CPU is not
tested here.

The battery pass covers the ternary model and the 4-bit k-quant (Q4_K_M), the 8-bit
build, and half precision, run three times across two battery-discharge sessions. On
battery the processor runs at a lower power limit and that limit tightens as the battery
drains, so whole-system energy per token drifts across runs, the ternary model measuring
1.9, 2.4, and 2.8 J per token in the three, and only the model-to-model ratios within a
run are stable. Those ratios are consistent. In the mid-range run the ternary model and
the k-quant both cost about 2.4 J per token, the 8-bit build about 3.8, and half
precision about 5.3; across all three runs the ternary model sat at 0.88 to 1.00 times
the energy of the k-quant, 0.59 to 0.69 times the 8-bit build, and 0.40 to 0.46 times
half precision. The energy ranking follows the decode-throughput ranking exactly: the
ternary model and the k-quant emit tokens fastest, so they amortize the machine's large
idle draw, 29 to 49 W depending on battery state, over the most tokens. Against the 4-bit
k-quant, then, the ternary model has no energy-per-token advantage on this machine, the
same result the decode-speed and disk-size comparisons give; its advantage is a little
over half off against half precision and roughly a third off against the 8-bit build, and
that is a speed effect, not a lower compute cost. An idle-subtracted compute-energy
figure did not reproduce across runs, since the idle draw itself varied by almost 20 W
between sessions and on a draining battery some model runs drew less than the bracketing
idle windows, so only whole-system energy is reported. None of these whole-laptop figures
is comparable to the model card's 0.028 J, which is a CPU-side, non-embedding number.

## 10.5 Summary of findings

On the accuracy arm, five things held. Every released checkpoint loaded and ran under a
single pinned harness with no code changes beyond a Windows Triton pin. Every determinism
check reproduced exactly. The controlled Spectra pair put native ternary within 0.6
points of FP16 on the seven-task mean at 2.4 billion parameters, with a 14% higher
perplexity, so the "downstream parity, worse language-modeling loss" pattern of the
native-training literature reproduces under a matched protocol, not just in the
uncontrolled vendor pairing. Our zero-shot MMLU, 52.07 for BitNet b1.58 2B4T against
60.03 for Qwen, closely tracks the card's five-shot values under a different protocol
and matches its roughly eight-point
world-knowledge deficit. And GSM8K, re-measured with generation and the chat template,
reproduces in direction the one benchmark on which the card leads: BitNet b1.58 2B4T scores 61.9 to
our Qwen's 57.5 on flexible-extract (Section 10.3).

What the controlled comparisons also show is a cost, and a boundary on the claim. Post-hoc
4-bit quantization of Qwen loses 2.7 points on the seven-task mean and 7.8 on GSM8K, more
than native ternary loses at a similar scale. The 1.58-bit Falcon3-1B pair loses far more,
11.5 points on the mean, 17 on GSM8K, and essentially all of MMLU; that pair does not
isolate scale from training recipe (Section 10.3), but it does show that constraining
weights to 1.58 bits at the one-billion-parameter scale does not by itself deliver parity.
Parity, where we see it, is a property of native ternary pre-training at multi-billion
scale, and even there it is downstream parity with a worse language-modeling loss, not
equivalence. Whether it survives above the measured regime is still untested (Section 11.1).

One vendor number is not directly comparable rather than reproduced or refuted: the
BitNet b1.58 2B4T model card's single headline "zero-shot average" of 54.19. Our
seven-task suite gives 61.98, but the card's figure is an average over a different and
broader task set, taken with the chat template we did not apply, so the two cannot be
placed side by side. It is a concrete instance of a vendor summary statistic that a
reader cannot check without reconstructing the exact task list and prompt format.

On the efficiency arm the headline result is that, on this commodity x86 machine, a
standard 4-bit quantization of the full-precision baseline matches or beats the flagship
1-bit model on every axis a practitioner would weigh except one. Against all three 4-bit
builds the ternary model shows no decode-speed advantage (it is slower than two of them
and ties the third) and no on-disk-size advantage; against the 4-bit k-quant it shows no
energy-per-token advantage either, the two within 0 to 12% across three battery runs
(Section 10.4). Its one retained edge is a 24-to-27% smaller resident set. On the two
accuracy tasks that could be scored through the same runtime the k-quant stays close
(Section 10.3). All of this holds whether threads are fixed at four or tuned per model.

The vendor's own comparisons, made only against FP16, do reproduce in direction: the
roughly 2-times decode advantage over FP16 holds, the 6.5-times memory advantage becomes
2.5-times once memory is counted as resident set rather than non-embedding weights, and
whole-system energy per token is about 0.43 times FP16, tracking the decode-speed ratio.
Against Q8_0 the decode edge is 1.2-times and the energy ratio about 0.6-times, again a
speed effect. So the paradigm's efficiency case at this scale holds against half
precision and against Q8_0, but not against any of the tested 4-bit builds; it is also a
case about these released checkpoints and this one machine, not a general property of
the representation, since the comparison pairs a 2.4B ternary model against a 1.5B
full-precision one and cannot separate the two. We did not test a GPU or a second
machine; Section 10.7 discusses how far this is likely to carry.

Two further findings came out of the efficiency arm. The 4-bit k-quant of the baseline
costs 4.5% on perplexity and, on the 1000-item HellaSwag subset, a difference of 0.3
points that we did not test for significance (Section 10.3), so the faster, smaller
k-quant stays close in accuracy on the tasks checked. And the reference CPU runtime,
built from the project as documented, does not produce correct output for BitNet b1.58
2B4T until a source constant is changed: its BitNet graph applies a SiLU feed-forward
activation where the model uses gated squared-ReLU, a known open issue. Uncorrected,
WikiText-2 perplexity is 86.9 and HellaSwag 38.7%; the one-line fix brings these to
12.99 and 62.4% (Section 10.3). The released weights are sound. The throughput and
memory figures of Section 10.4 are unchanged by the fix, since a squared-ReLU is no more
costly than a SiLU and the activation is a negligible fraction of the per-token work.

Two benchmarks that an earlier version of this study left out are now re-measured. MMLU,
dropped because five-shot evaluation thrashed BitNet's per-shape compilation cache, is
re-measured at zero shot; GSM8K, which needs generation and a chat template rather than
the loglikelihood path used for everything else, is re-measured at five shot with the
template and reported separately (Section 10.3). Both reproduce the corresponding vendor
figures. Nothing in the accuracy arm now rests on an unverified vendor number.

## 10.6 Reproducibility audit

For the checkpoints in the accuracy arm we record, as a by-product, what license
governs reuse, whether the weights load under a stock harness, and whether our numbers
land near the vendor's. The controlled-comparison checkpoints of Section 10.3, the
Spectra TriLM and FloatLM pair, Falcon3-1B in bf16, and the nf4 quantization of Qwen,
all loaded through the stock `AutoModelForCausalLM` path with no special handling and are
not repeated in Table [tab:repro-audit].

| checkpoint / artifact | license | loads and runs | reproduces |
|---|---|---|---|
| BitNet b1.58 2B4T, bf16 weights (transformers) | MIT | yes | per-task yes, headline average no |
| BitNet b1.58 2B4T, released I2_S GGUF (bitnet.cpp) | MIT | only after a source patch | yes once patched (ppl 12.99) |
| Falcon3-1B-Instruct-1.58bit | Falcon LLM License 2.0 | yes | no public per-task baseline |
| Qwen2.5-1.5B-Instruct | Apache-2.0 | yes | full-precision reference |
Table: {#tab:repro-audit} Reproducibility audit for the accuracy-arm checkpoints: governing license, whether the weights load under a stock harness, and whether our measurements land near the vendor's.

The BitNet rows are the point of this audit. The bf16 weights load as a native
transformers model type, so the model card's `trust_remote_code` instruction is stale,
and on Windows the layer compiles only against a matched Triton build; run that way the
model is competitive (Section 10.3). The released
GGUF, which is the only artifact that delivers the efficiency the whole approach is for,
loads but returns near-broken output from the reference runtime as built, because that
runtime applies the wrong feed-forward activation to this model (Section 10.3); a
one-line source change fixes it, but a practitioner following the documented build would
not know to make it. The released weights themselves are sound. Falcon3 and Qwen load
through the stock `AutoModelForCausalLM` path with no special handling. License terms
vary across the corpus, with MIT, Apache, and vendor-specific licenses all appearing,
which matters for any downstream reuse. A full audit across every released model in the
corpus is beyond this paper's scope.

## 10.7 Threats

Both arms run on a single laptop. For accuracy the GPU is shared with other workloads,
which we mitigate with a fixed batch size and off-peak scheduling; for efficiency the
machine runs under its default thermal and power policy, so the absolute throughput
figures are specific to that part and not a controlled-environment measurement. The
energy figures are coarser still: the discharge-rate sensor is noisy, the on-battery
power limit falls as the battery drains so absolute per-token energy drifts across runs,
and the numbers are whole-system rather than package or component; they support the
within-run model-to-model ratios (Section 10.4) but not an absolute claim, and we do not
report an idle-subtracted figure because it did not reproduce. The author-reported baselines cannot be matched exactly, and benchmark
contamination is a risk in heavily fine-tuned small models, which we note per model.

The efficiency findings are for a CPU datapath and may not transfer to a GPU, and the
transfer is worth reasoning about because the strong claim, that a 4-bit build is at
least as good, could plausibly flip. On a GPU neither ternary nor 4-bit weights map to a
native matrix-multiply instruction: both are unpacked to a supported floating-point or
integer type and run on the tensor cores, or go through a custom kernel. The decode-time
benefit that low-bit weights capture on CPU is memory-bandwidth, and that benefit exists
on GPU too and accrues to a 4-bit kernel as much as to a ternary one, so the CPU result
that a 4-bit kernel captures it is a reasonable prior for the GPU case. Two things could
still separate them there. A ternary-specific GPU kernel that exploits the zero state or
a sub-1.6-bit packing (Section 7.3) might pull ahead of the tuned 4-bit kernels now
standard for served inference, in a way the general-purpose CPU path does not expose.
And prefill and high-batch decode are compute-bound rather than bandwidth-bound, so their
ordering need not follow the single-stream decode ordering measured here. We tested none
of this, and a GPU comparison against a production 4-bit kernel is the obvious next step.

Every part of this reproduction is pinned to a specific commit or file rather than a
moving target: the evaluation harness at commit `b954108` (Section 10.2); microsoft/BitNet
at commit `0b341e5` with its `llama.cpp` submodule at `390c307` and the one-line
`LLM_FFN_SILU`-to-`LLM_FFN_RELU_SQR` activation fix (Section 10.3); and the BitNet GGUF
checkpoint by Hugging Face revision and SHA-256 (Section 10.3). The Qwen GGUF builds were
produced with `llama-quantize` from one pinned FP16 GGUF, and the nf4 quantization with
bitsandbytes 0.50.2. Every accuracy and efficiency number reported in this section is the
direct output of that pinned pipeline on the machine described in Section 10.2, run once
per configuration except where a repeat count is stated.
