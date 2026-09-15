# 4. A Taxonomy of Binary and Ternary LLMs

A survey of this area must impose structure, because the phrase "1-bit LLM" is used for
at least three different research programs: training a model under a sub-two-bit
constraint from scratch, compressing a trained model down toward one bit, and building
hardware that executes ternary weights efficiently. We organize the field along five
orthogonal axes (Table 1). Four of them, weight representation, training paradigm,
quantized components, and systems stack, partition the corpus, so their category counts
sum to the full 140 works; the fifth, optimization mechanism, is a non-exclusive tally,
since one work can combine mechanisms. The axes are deliberately independent, so that a
work's position on one does not determine its position on another, and the most
influential works are those that advance the state of the art on several axes at once.

## 4.1 Axis 1: weight representation

The first choice is the value set. Binary weights, drawn from {-1,+1}, give the largest
nominal compression and the simplest kernel, but they cannot express the absence of a
connection. Thirty-four surveyed works are primarily binary, and most of them are
post-training or fine-tuning methods that apply the binary constraint to an
already-trained model [Huang2024-BiLLM], [Li2024-ARBLLM], [Xu2024-OneBit],
[Ma2024-FBILLM]. Ternary weights, drawn from {-1,0,+1}, add a zero state. This both
restores sparsity, since roughly 40% to 60% of weights go to zero in practice, and
makes optimization markedly easier in experiments. Sixty-two works are ternary, and
this is where native from-scratch training has succeeded [Ma2024-BitNetB158],
[Kaushal2024-Spectra], [Zhu2024-MatmulFree]; an early instance, predating BitNet,
demonstrated the first ternary and binary sequence-to-sequence Transformers for
summarization and machine translation [Liu2023-BinTernNLG]. Mixed or partial schemes, of which there
are 21, keep a small set of salient columns, or a low-rank residual branch, in higher
precision. Examples are the roughly 1.08 effective bits of BiLLM [Huang2024-BiLLM], the
tunable fraction of PB-LLM [Shang2023-PBLLM], the dedicated high-precision expert
branch of pQuant [Zhang2026-pQuant], and the saliency-graph-guided scaling of SAGE-PTQ
[Abdalla2026-SAGEPTQ]; each trades a fraction of a bit for a substantial accuracy
recovery. A small but distinct line uses complex-valued weights in
$\{\pm 1, \pm i\}$, which costs two bits of storage but supports multiplication-free
accumulation [Wang2025-iFairy], [Wang2025-Fairy2i]. The remaining 23 works, kernels,
accelerators, theory, and surveys, define no weight format of their own and are counted
separately in Fig. [fig:taxonomy].

## 4.2 Axis 2: training paradigm

The second choice is when the low-bit constraint enters. Native from-scratch training,
in 27 works, places a quantizer in `BitLinear` from the first optimization step; this is
the defining paradigm of the survey and the one that has demonstrated full-precision
parity at scale [Wang2023-BitNet], [Ma2024-BitNetB158], [Ma2025-BitNet2B4T],
[Kaushal2024-Spectra]. Continual quantization-aware pre-training, in 2 works, begins in
full precision and transitions to 1.58-bit training part-way through, which reduces
total cost but introduces a loss spike at the switch that must be managed
[Nielsen2025-ContinualQAT], [Tu2025-Rethink1bitOpt]. Quantization-aware fine-tuning, in
37 works, inserts the quantizer into a fine-tuning or short continued-training loop over
a pretrained full-precision model [Xu2024-OneBit], [Du2024-BitDistiller],
[Wu2025-BitNetDistillation]. Post-training quantization, in 30 works, uses only a
calibration set and no gradient updates [Huang2024-BiLLM], [Li2024-ARBLLM],
[Xiao2025-PTQTP], [Yan2025-PT2LLM], [Xu2024-CRVQ], [Edalati2024-OAC]. At a fixed
bit-width, the accuracy ordering is
generally native, then quantization-aware training, then post-training quantization,
and the cost ordering is the reverse; the practical question each paper answers is where
on that trade-off a given deployment sits. The remaining 44 works, systems papers,
analyses, and surveys with no training procedure of their own, carry no value on this
axis and are counted separately in Fig. [fig:taxonomy].

## 4.3 Axis 3: quantized components

The third axis is what is quantized beyond the weight matrices. Weight-only methods, in
80 works, leave activations at FP16 or INT8 and capture the memory-bandwidth benefit
without changing the precision of the compute path. Weight-and-activation methods, in 30
works, quantize activations as well, typically starting at INT8 and pushing toward INT4;
this is where the outlier problem of Section 2.4 becomes acute and where hybrid and
rotation methods are needed [Wang2024-BitNetA48], [Wang2025-BitNetV2], [Zhao2026-TWLA],
[Zhao2026-BWLA]. Two works quantize only activations, through sparsification. A small
frontier additionally quantizes the KV cache to three bits [Wang2024-BitNetA48],
[Wang2025-BitNetV2] and couples activation or weight sparsification to quantization
[Wang2024-QSparse], [Zhang2026-SparseBitNet], [Huang2026-Sherry], [Qi2025-DeltaLLM]. The
other 28 works have no model of their own and carry no value on this axis.

## 4.4 Axis 4: optimization mechanism

The fourth axis is how the discrete constraint is optimized. The default is a scaled
straight-through estimator, with absolute-mean or absolute-max normalization, sometimes
the median, applied through both weights and activations; roughly 20 works use this in
essentially unmodified form. A group of about six works treats the estimator as the
object of study, through curvature-aware corrections [Tabesh2025-CAGE], a trust-region
gradient [Panferov2025-QuEST], or zeroth-order augmentation [Anon2025-STE-ZerothOrder].
Distillation-driven methods, roughly 13, close the accuracy gap to a full-precision
teacher through autoregressive, logit, attention, or feature losses [Ma2024-FBILLM],
[Wu2025-BitNetDistillation], [Du2024-BitDistiller], [Tang2024-BiMamba]. Reconstruction
and calibration methods, roughly 20, minimize a layer-output error over calibration
data, often with salient-weight handling and Hessian information, and are the workhorse
of post-training quantization toward one bit [Huang2024-BiLLM], [Li2024-ARBLLM],
[Xiao2025-PTQTP], [Li2025-ICQuant], [Xu2024-CRVQ], [Edalati2024-OAC],
[Xiao2025-LieQ], [Abdalla2026-SAGEPTQ]. Rotation and incoherence methods, roughly seven,
apply a structured orthogonal change of basis before quantization to spread outlier
energy; examples are the fixed Hadamard transform of BitNet v2 [Wang2025-BitNetV2] and
its learned or data-adaptive generalizations [Zagitov2026-HARP], [Zhao2026-TWLA],
[Pavlov2026-InfluenceRotations]. Decomposition and factorization methods, roughly ten,
represent the weight as a product or sum of low-rank or binary factors [Xu2024-OneBit],
[Lee2025-LittleBit], [Xiao2025-PTQTP], [Wang2026-LCQAT]. Stochastic rounding without any
STE is a minority alternative that removes the shadow-weight memory cost
[Zhao2024-DQT]. Finally, sparsity-coupled optimization ties an N:M or top-K mask to the
quantizer [Zhang2026-SparseBitNet], [Huang2026-Sherry], [Dong2024-STBLLM],
[Wang2024-QSparse].

## 4.5 Axis 5: systems stack

The fifth axis records how far down the stack a work reaches, and it partitions the 140
works into four exclusive bins: algorithm only, contributes a kernel, is a
hardware design, or not applicable. Ninety-five works are algorithm only. Twenty-five
contribute a kernel: the I2_S and TL1 or
TL2 lookup kernels of bitnet.cpp [Wang2024-1bitAIInfra], [Wang2025-BitNetCPP], the fused
ternary CPU kernels of FairyFuse [Zuo2026-FairyFuse], the matrix-vector engine of
RSR-core [Dehghankar2026-RSRcore], the in-register SIMD lookup of T-SAR [Oh2025-TSAR],
the CPU table-lookup renaissance of T-MAC [Wei2024-TMAC], the 2-bit CPU and GPU
microkernels of [Georganas2025-UltraLowBitKernels], and the GPU kernels of QuEST and
Spectra 1.1 [Panferov2025-QuEST], [Vaidhya2025-Spectra11]. This bin includes the five
works that reach all the way to a hardware design as well, namely BitNet b1.58, BitNet
b1.58 2B4T, MatMul-free LM, Sparse-BitNet, and BMT-BAT [Ma2024-BitNetB158],
[Ma2025-BitNet2B4T], [Zhu2024-MatmulFree], [Zhang2026-SparseBitNet], [Ji2024-BMTBAT];
they are counted once here, not separately, and closing the gap between them and the
rest of the field is one of the open problems of Section 11. Sixteen works are a
hardware design with no algorithmic contribution of their own:
lookup-table ASICs [Shan2025-Platinum], [Anon2025-TENET], the design-space-exploration
LUT-accelerator framework of [Geens2026-LUTAccelDesign], compute-in-ROM designs
[Zhang2025-BitROM], [Guan2026-TOM], processing-in-memory designs [Malekar2025-PIMLLM],
[Ortega2024-PIMAI], the fault-tolerant compute-in-memory design of ReTern
[Malhotra2025-ReTern], and edge-FPGA accelerators [Xu2025-TeLLMe],
[Qiao2025-TeLLMev2], [Chen2025-TerEffic], [Zhang2025-PDSwap], together with the
silicon-validated ternary accelerator VitaLLM [Lin2026-VitaLLM]. The four remaining works are surveys
with no systems contribution of their own.

## 4.6 A secondary classification by modality

Seventy-two works target text-decoder LLMs, and this is where the technical core of the
survey sits. A fast-growing minority applies the same machinery elsewhere: to 1-bit
text-embedding models [Li2026-BitNetTextEmbeddings], [Chen2024-TernaryEmbedding],
[Connor2025-UltraQuantisation]; to speech, in the form of 1.58-bit text-to-speech
[Kawamura2025-BitTTS] and one-bit automatic speech recognition [Anon2025-OneBitASR]; to
vision-language and vision-language-action models [Wang2025-BitVLA],
[Sundaram2024-LLaVaOLMoBitnet], [Zhang2025-TernaryCLIP]; to ternary mixture-of-experts
[Wang2025-MoTE]; to state-space models [Tang2024-BiMamba],
[Ganesaraja2026-TernaryMamba]; and, further afield, to reinforcement-learning agents
[Sajid2026-BitRL] and autonomous-system trajectory prediction [Kang2026-BitTP]. These
branches are surveyed in Section 9.

## 4.7 Reading the taxonomy

The value of the taxonomy is comparative. It shows that native training has concentrated
on ternary weights while binary has remained largely a post-training target
(Fig. [fig:heatmap]); that
activation quantization and the systems stack are where the field is currently moving
fastest; and that the most influential works, namely the BitNet line, Spectra,
MatMul-free LM, ParetoQ, and Sparse-BitNet, are precisely those that advance the state
of the art on three or more axes at once. Table 1 gives the full classification, and
Fig. [fig:taxonomy] depicts it as a tree. Cut by year instead of pooled, binary's
share of new work peaked at a third in 2024 and had fallen to under a tenth by 2026,
while ternary stayed the largest or second-largest category throughout (Fig. [fig:weightyear]).
