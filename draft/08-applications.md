# 9. Applications and Extensions

The native 1-bit machinery was built for text-decoder LLMs, but the period from 2024 to
2026 saw it carried into a widening set of modalities and deployment settings. This
section surveys those branches. Each is small today, but each is growing, and together
they are the fastest-moving part of the field.

## 9.1 On-device and edge deployment

The unifying theme of the area is running capable models without a data center. Concrete
demonstrations include BitNet b1.58 2B4T with open CPU and GPU inference
[Ma2025-BitNet2B4T], a 100B model at reading speed on one CPU [Wang2024-1bitAIInfra], an
inference characterization on a Raspberry Pi with BitNet Q1.58 against k-quantized
baselines [Ardakani2025-LLMPi], and analyses of when commodity CPUs beat GPUs for
on-device serving [Anon2025-CPUvsGPU]. The security of the deployed weights is a
separate concern: TZ-LLM protects on-device model parameters inside an Arm TrustZone
enclave, using pipelined restoration to hide decryption latency [Wang2025-TZLLM].

## 9.2 Embedding models

Embedding models are attractive ternary targets, because the downstream operation of
approximate nearest-neighbor search tolerates quantized vectors well. A ternary-weight
fine-tuning framework with self-taught distillation preserves retrieval quality while
reducing memory and latency, and composes with approximate-nearest-neighbor indices
[Chen2024-TernaryEmbedding]; Ultra-Quantisation applies 1.58-bit encodings directly to
the embedding-search problem [Connor2025-UltraQuantisation]; and BitNet Text Embeddings
is a native 1-bit embedding-model family, at 0.27B and 0.6B parameters, released with
the I2_S kernel path of bitnet.cpp [Li2026-BitNetTextEmbeddings], [web-microsoftBitNet].

## 9.3 Speech

BitTTS quantizes both the acoustic model and the vocoder of a text-to-speech system to
1.58-bit with quantization-aware training, together with a weight-indexing scheme that
stores five ternary weights per INT8; the result is an 83% size reduction while
improving quality over an unquantized model of the same size [Kawamura2025-BitTTS]. On
the recognition side, an extremely low-bit Conformer is trained toward one bit with
co-training and stochastic precision [Anon2025-OneBitASR].

## 9.4 Vision-language and vision-language-action models

LLaVaOLMoBitnet1B was the first ternary multimodal LLM, pairing a full-precision vision
encoder with a ternary OLMo-Bitnet backbone [Sundaram2024-LLaVaOLMoBitnet]. BitVLA
extends this to robotics: it builds on BitNet b1.58 2B4T, then compresses the vision
encoder to 1.58-bit weights with eight-bit activations through a quantize-then-distill
stage before robotic fine-tuning, retaining task competence at a fraction of the memory
[Wang2025-BitVLA]. TernaryCLIP compresses a CLIP vision-language model to ternary weights
with distilled knowledge [Zhang2025-TernaryCLIP]; TeTRA ternarizes a vision-transformer
backbone and binarizes its embedding head for compact visual place recognition on drones
[Grainge2025-TeTRAVPR]; and BitMar explores low-bit multimodal fusion with an episodic
memory for edge devices [Aman2025-BitMar].

## 9.5 Mixture-of-experts

MoTE trains many ternary routed experts rather than few full-precision ones, keeping the
active-parameter budget fixed while removing the memory overhead of a full-precision
expert pool; it is competitive with a full-precision MoE-LLaVA at equal expert memory,
and the gap widens as the memory budget tightens [Wang2025-MoTE].

## 9.6 Ecosystem beyond a single laboratory

The paradigm is no longer confined to one laboratory. The Falcon-Edge family from TII,
comprising Falcon3-1.58bit models at 1B and 3B in base and instruction-tuned variants,
is trained with ternary weights during pre-training and ships a fine-tuning library
[web-falconEdge]; the Spectra suites from NolanoOrg release more than 500 intermediate
TriLM checkpoints from 99M to 3.9B parameters [Kaushal2024-Spectra],
[Vaidhya2025-Spectra11]; and independent groups have produced binary and ternary
variants across the OPT, Llama, Qwen, and Mistral families [Li2024-ARBLLM],
[Dong2024-STBLLM], [Xiao2025-PTQTP].

## 9.7 Environmental framing

Several works motivate 1-bit LLMs explicitly on energy and carbon grounds
[Wang2023-BitNet], [Ansar2024-BEExformer], and the reported 70% to 96% energy
reductions for CPU inference [Wang2024-1bitAIInfra], [web-bitnet2b4tCard] are the
strongest lever for that argument. A rigorous life-cycle account, one that includes the
higher training-time cost of native 1-bit models, has not yet been published and is
noted here as a gap.
