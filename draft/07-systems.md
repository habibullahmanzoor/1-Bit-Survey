# 7. Inference Systems and Hardware

## 7.1 The need for a software stack

A ternary weight matrix stored at two bits already reduces memory traffic by roughly
eight times relative to BF16, but a naive kernel still dequantizes to floating point and
runs an ordinary matrix multiplication, capturing none of the arithmetic saving.
Realizing the add-and-subtract inner product requires either bit-serial computation or
lookup tables, and both need dedicated kernels. The dominant cost in ternary inference
is the mixed-precision matrix multiplication of ternary weights against INT8
activations, so this is what the kernels target [Wang2025-BitNetCPP].

## 7.2 bitnet.cpp and CPU kernels

bitnet.cpp is the reference CPU stack for BitNet b1.58 and ternary models
[Wang2024-1bitAIInfra], [Wang2025-BitNetCPP]. It provides two kernel families. The I2_S
kernel packs ternary weights as two-bit integers with a shared scale and performs
lossless integer inference. The TL1 and TL2 kernels are ternary lookup tables: TL1
precomputes the products of a small block of ternary weights against the possible
activation values and indexes into them, and TL2 refines the packing to reduce the
spatial footprint of the table. Reported speedups over an FP16 baseline are 2.37 to 6.17
times on x86 and 1.37 to 5.07 times on ARM, with energy reductions of 72% to 82% on
x86 and 55% to 70% on ARM, and the headline demonstration is a 100B-parameter BitNet
b1.58 model running at five to seven tokens per second, comparable to human reading
speed, on a single CPU [Wang2024-1bitAIInfra]. A 2026 update adds parallel kernels with
configurable tiling for a further 1.15 to 2.1 times [web-microsoftBitNet]. Independent
CPU frameworks pursue the same goal by different means: Litespark uses hand-tuned SIMD
code [Anon2026-Litespark], FairyFuse uses fused ternary kernels that avoid materializing
intermediates [Zuo2026-FairyFuse], T-SAR repurposes the SIMD register file for
in-register lookup-table generation with a small instruction-set change [Oh2025-TSAR],
and RSR-core implements the Redundant Segment Reduction algorithm as production CPU and
CUDA kernels, with a reported 62-times CPU speedup on ternary LLMs
[Dehghankar2026-RSRcore]. A more general theoretical result gives an
$O(n^2 / \log n)$ matrix-vector algorithm for binary and ternary matrices by
preprocessing the fixed weight matrix into an index [Dehghankar2024-EfficientMatmul].

## 7.3 GPU

GPUs are optimized for dense floating-point matrix multiplication, so ternary weights
initially offered little benefit on them. This has changed. An official GPU kernel for
BitNet shipped in 2025 [web-microsoftBitNet]; the TriRun kernel of Spectra 1.1
accelerates end-to-end ternary inference by up to five times over a floating-point
baseline by packing two ternary weights per byte [Vaidhya2025-Spectra11]; and QuEST
provides GPU kernels for its W1 through W4 models [Panferov2025-QuEST]. The
matrix-multiplication-free design sidesteps the question altogether by removing the
operation that GPUs are built for [Zhu2024-MatmulFree].

## 7.4 Custom accelerators

Ternary weights change what the ideal processor looks like, and a first wave of designs
explores the space. Lookup-table ASICs precompute partial products and index into them.
Platinum uses offline-generated construction paths and adaptive bit-serial or
ternary-weight execution, reporting a 73-times speedup over a spiking baseline and a
2.15-times speedup over a 16-thread CPU implementation in under one square millimetre of
chip area [Shan2025-Platinum]; TENET is a sparsity-aware, lookup-table-centric edge
architecture [Anon2025-TENET]; and Vec-LUT vectorizes the table lookup for parallelism
[Li2025-VecLUT]. Compute-in-ROM designs store the rarely updated ternary base model as
standard-cell logic, exploiting the zero state to eliminate area for zero-valued
weights, with an SRAM layer of low-rank adapters for on-device adaptation: BitROM
targets billion-parameter models [Zhang2025-BitROM] and TOM reports 3,306 tokens per
second on a BitNet-2B model with dynamic power gating of inactive ROM banks
[Guan2026-TOM]. Processing-in-memory designs [Malekar2025-PIMLLM], [Ortega2024-PIMAI]
and edge-FPGA accelerators with table-lookup matrix multiplication for both the prefill
and decode phases [Xu2025-TeLLMe], [Qiao2025-TeLLMev2], [Chen2025-TerEffic] complete the
picture. The fault tolerance of compute-in-memory ternary LLMs, which can exploit the
natural redundancy of the zero state, is itself a research topic.

## 7.5 Summary of the systems corpus

Three observations stand out. First, the CPU story is mature: several independent
frameworks now beat FP16 by factors of two to six with lossless accuracy, and the claim
that a capable model can run without a GPU is genuine. Second, the GPU and custom-silicon
work is early: the accelerator papers report simulator or single-chip results rather
than shipping parts, and no commercial processor exposes a ternary
matrix-multiplication primitive. Third, only five works in the entire corpus co-design
across algorithm, kernel, and hardware (Fig. [fig:systemsvenn]); the rest optimize one layer while assuming the
others. Closing that gap, by building an add-and-subtract matrix-multiplication unit
with a matching memory layout and instruction-set extension, co-designed with the
training recipe, is the clearest systems opportunity (Section 11). Section 10 reports
our own CPU measurements against the figures cited above.
