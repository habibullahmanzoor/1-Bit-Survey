# Environment of record

Everything the reproduction ran on, in one place. Cross-referenced from
`draft/09-reproduction.md` §10.2 and §10.7.

## Machine

| item | value |
|---|---|
| CPU | Intel Core i9-14900HX (8 performance cores + 16 efficiency cores, 32 threads) |
| RAM | 32 GiB DDR5 |
| GPU (Arm A only) | NVIDIA GeForce RTX 4080 Laptop, 12 GiB, shared with the desktop session |
| OS | Windows 11 Pro, build 10.0.26200 |
| Power plan | Windows default "Balanced"; Arm B plugged in (AC), energy pass on battery (see below) |
| Firmware | vendor BIOS as shipped; no undervolt or power-limit override applied |

Arm B throughput and memory were taken on AC power under the default thermal/power
policy, so absolute numbers are specific to this part. The energy pass runs on battery,
where Windows exposes whole-system draw as `BatteryStatus.DischargeRate` (mW); the CPU
power cap is lower on battery and tightens further as the battery drains, so those runs
are slower than the AC sweep and absolute energy per token drifts across runs. It was run
three times (bitnet, Q4_K_M, Q8_0, FP16); only within-run model-to-model ratios are used.
See `FINDINGS-energy.md`.

## Toolchains

| component | version / commit |
|---|---|
| Python | 3.10.x, venv at `repro/.venv` |
| Python packages | full freeze in `env/requirements.lock.txt` (loose pins in `env/requirements.txt`) |
| lm-evaluation-harness | commit in `env/harness-commit.txt`, installed `-e` |
| bitnet.cpp / BitNet | submodule under `repro/BitNet`; llama.cpp third-party commit recorded by `env/submodule-commits.txt` |
| C++ compiler | Visual Studio 2022 bundled clang, Ninja generator |
| CUDA (Arm A) | as bundled with the pinned torch wheel |

## bitnet.cpp build (Arm B)

Static, because the stock shared build does not link on this toolchain (the fork's
`quantize_i2_s` / `dequantize_row_i2_s` live only in the CPU backend and are undefined in
`ggml-base`):

```
cmake -S BitNet -B BitNet/build-static -G Ninja -DCMAKE_BUILD_TYPE=Release \
      -DBUILD_SHARED_LIBS=OFF -DGGML_NATIVE=ON -DCMAKE_RC_COMPILER=llvm-rc \
      -DLLAMA_BUILD_COMMON=ON -DLLAMA_BUILD_TOOLS=ON
cmake --build BitNet/build-static --target llama-bench llama-perplexity llama-cli -j 10
```

One source change is applied before building, and only that one: the FFN activation
constant in `BitNet/3rdparty/llama.cpp/src/models/bitnet.cpp`, from `LLM_FFN_SILU` to
`LLM_FFN_RELU_SQR` (BitNet b1.58 2B4T uses a gated squared-ReLU). Captured as
`env/bitnet-cpp-relu2.patch`; rationale in `FINDINGS-gguf-defect.md`.

## Models

Revision hashes and SHA-256 of every checkpoint and GGUF are in `env/model-revisions.txt`.

## Regenerating the paper's numbers

`python analysis.py` is the single entry point: it reads `logs/` and rewrites every
table under `tables/` (Arm A accuracy, Arm B throughput/memory/energy, the
quantization-accuracy addendum, and the reproducibility-audit table). It does not
re-run the measurements; to redo those from scratch, run `run_accuracy.sh`,
`run_efficiency.sh`, `run_energy.sh`, and `run_quant_accuracy.sh` first (hardware and
timing notes in each script header and in `README.md`).
