# Reproduction study — setup and run

Pre-specified in `../survey-protocol.md` §12 and `../draft/09-reproduction.md`.
Budget: Arm A ~8 GPU-hours (shared RTX 4080, minimum tier); Arm B ~3 CPU-hours.

## Layout
```
repro/
├── README.md            (this file)
├── models.md            checkpoints under test + why
├── ENVIRONMENT.md       machine, OS build, toolchains, build flags, power plan
├── env/                  pinned environment
│   ├── harness-commit.txt      lm-evaluation-harness commit hash
│   ├── submodule-commits.txt   BitNet + 3rdparty/llama.cpp commits
│   ├── model-revisions.txt     HF revision hashes + GGUF SHA-256
│   ├── bitnet-cpp-relu2.patch  the one source change to the runtime
│   ├── requirements.lock.txt   full pip freeze
│   └── requirements.txt        loose pins
├── run_accuracy.sh      Arm A — lm-eval-harness on the 1-bit checkpoints + FP baseline
├── run_efficiency.sh    Arm B — bitnet.cpp vs llama.cpp CPU benchmark + thread sweep
├── logs/                raw harness JSON + bench CSV (git-tracked)
└── analysis.py          single entry point: rebuilds every tables/*.md from logs/
```

## One-time setup

1. `python -m venv .venv && . .venv/Scripts/activate` (Windows) and `pip install -r env/requirements.txt`.
2. Clone `lm-evaluation-harness`, check out a specific commit, record it in `env/harness-commit.txt`, `pip install -e .`.
3. Build `bitnet.cpp` (`git clone https://github.com/microsoft/BitNet`, needs cmake + a recent clang). On Windows / MSVC-clang the stock shared build fails to link (`quantize_i2_s` / `dequantize_row_i2_s` undefined in `ggml-base`): configure static instead —
   `cmake -S BitNet -B BitNet/build-static -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DGGML_NATIVE=ON -DLLAMA_BUILD_COMMON=ON -DLLAMA_BUILD_TOOLS=ON` then `cmake --build BitNet/build-static --target llama-bench llama-cli -j`.
   That one binary runs the BitNet I2_S kernel *and* ordinary GGUF quants, so it is the baseline framework too (no separate llama.cpp build needed for Arm B).
4. Fetch GGUFs into `models/`: `microsoft/bitnet-b1.58-2B-4T-gguf` (`ggml-model-i2_s.gguf`) and `Qwen/Qwen2.5-1.5B-Instruct-GGUF` (`q8_0`, `fp16`). For Arm A, HF safetensors as in `models.md`.
5. VRAM guard: export `LM_EVAL_BATCH_SIZE=4` so the shared 4080 keeps ~10 GB free.

## Run

- `bash run_accuracy.sh`   → `logs/acc_<model>_<task>.json`  (Arm A, HF/transformers; run overnight; ~1-3 h/model)
- `bash run_efficiency.sh` → `logs/eff_<model>_t<threads>.csv` + `logs/eff_<model>_rss.json`  (Arm B throughput/memory; 4 GGUFs incl. Qwen Q4_K_M; ~90 min, CPU; resumable per model/thread; run on a quiet machine)
- `bash run_energy.sh`     → `logs/energy_<model>_samples.csv` + `_bench.json`  (~6 min; **unplug the charger first** — reads `BatteryStatus.DischargeRate`, 0 on AC. On battery the CPU power cap is lower, so decode is ~20% slower than `run_efficiency`; the models are only compared to each other.)
- `bash run_quant_accuracy.sh` → `logs/qacc_<model>_{wikitext,hellaswag}.{txt,err}`  (WikiText-2 ppl + HellaSwag via `llama-perplexity` for FP16/Q8_0/Q4_K_M Qwen + BitNet i2_s; ~2-3 h, CPU)
- `python analysis.py`  → rebuilds every `tables/*.md` (Arm A accuracy, Arm B
  throughput/memory/energy, quant-accuracy addendum, reproducibility-audit table); it
  chains `analysis_eff.py` and `analysis_quant_acc.py`. Run `analysis_energy.py`
  separately after `run_energy.sh`.

**Note:** `FINDINGS-gguf-defect.md` documents the real cause of the ~87 perplexity
through llama.cpp/bitnet.cpp: the runtime, as built, applies a SiLU feed-forward
activation where BitNet b1.58 2B4T uses a gated squared-ReLU (upstream issue #588). The
one-line source fix (`env/bitnet-cpp-relu2.patch`) brings token-level WikiText-2
perplexity to 12.99 and HellaSwag to 62.4%. The released weights are sound; the missing
`tokenizer.ggml.pre` field is a separate, minor issue. That doc also rebuts the
"corrupt re-upload" reading of the checkpoint's 1,187,801,280-byte size (issue #608).

## Reporting
`analysis.py` emits our numbers beside published ones (from `../data/inventory.csv` +
`../papers/_web/*`), with signed deltas, and the reproducibility-audit table. Commit
`logs/` and `tables/`.
