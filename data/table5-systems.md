# Table 5 (draft) — Systems & hardware corpus

21 works.

| id | year | layers | modality | key contribution |
|---|---|---|---|---|
| Dehghankar2024-EfficientMatmul | 2024 | algorithm | systems | Preprocessing/indexing gives O(n^2/log n) binary/ternary matmul |
| Anon2026-NativeTernary | 2026 | algorithm | storage | Self-delimiting binary encoding for ternary weights (storage layer) |
| Ortega2024-PIMAI | 2024 | hardware | systems | Processing-in-memory (UPMEM) architecture for LLM inference |
| Xu2025-TeLLMe | 2025 | hardware | systems | Energy-efficient ternary LLM prefill+decode accelerator on edge FPGA |
| Chen2025-TerEffic | 2025 | hardware | systems | Highly efficient ternary LLM inference on FPGA |
| Anon2025-BitROM | 2025 | hardware | systems | Weight-reload-free compute-in-ROM for 1.58-bit LLM inference |
| Anon2025-CPUvsGPU | 2025 | hardware | systems | When CPUs outperform GPUs for on-device LLM inference |
| Anon2025-PIMLLM | 2025 | hardware | systems | Hybrid processing-in-memory architecture for 1-bit LLMs |
| Anon2025-TENET | 2025 | hardware | systems | Sparsity-aware LUT-centric architecture for ternary LLM on edge |
| Wang2025-TZLLM | 2025 | hardware | security | Arm TrustZone protection of on-device LLM weights; pipelined restore |
| Shan2025-Platinum | 2025 | hardware | systems | Path-adaptable LUT ASIC for ternary/low-bit mpGEMM; 73x vs baseline |
| Qiao2025-TeLLMev2 | 2025 | hardware | systems | End-to-end ternary LLM prefill+decode FPGA accelerator (v2) |
| Guan2026-TOM | 2026 | hardware | systems | Hybrid ROM-SRAM ternary accelerator; 3306 TPS on BitNet-2B |
| Wang2025-BitNetCPP | 2025 | kernel | systems | bitnet.cpp mpGEMM library: TL lookup + I2_S; up to 6.25x |
| Li2025-VecLUT | 2025 | kernel | systems | Vectorised table-lookup for parallel ultra-low-bit LLM inference on edge |
| Anon2026-Litespark | 2026 | kernel | systems | Ultra-fast SIMD CPU framework for ternary (1.58-bit) LMs |
| Zuo2026-FairyFuse | 2026 | kernel | systems | Multiplication-free CPU inference via fused ternary kernels |
| Dehghankar2026-RSRcore | 2026 | kernel | systems | CPU/CUDA kernels for RSR binary/ternary matrix-vector multiply; 62x CPU |
| Wang2024-1bitAIInfra | 2024 | kernel+hw | systems | bitnet.cpp CPU kernels 2.37-6.17x x86; lossless; 100B on one CPU |
| Ardakani2025-LLMPi | 2025 | kernel+hw | edge-systems | LLM throughput/energy study on Raspberry Pi incl BitNet Q1.58 |
| Oh2025-TSAR | 2025 | kernel+hw | systems | CPU ternary inference via in-register SIMD LUT generation |
