#!/usr/bin/env bash
# Arm B - efficiency reproduction. CPU only (no GPU).
# One binary for all models: the statically-linked bitnet.cpp build (patched llama.cpp)
# runs the BitNet I2_S ternary kernel AND ordinary GGUF quant types, so BitNet and the
# Qwen baselines are measured under an identical runtime on one machine.
#
# Build that was used (Windows, VS2022 clang + Ninja):
#   cmake -S BitNet -B BitNet/build-static -G Ninja -DCMAKE_BUILD_TYPE=Release \
#         -DBUILD_SHARED_LIBS=OFF -DGGML_NATIVE=ON \
#         -DLLAMA_BUILD_COMMON=ON -DLLAMA_BUILD_TOOLS=ON
#   cmake --build BitNet/build-static --target llama-bench -j
# BUILD_SHARED_LIBS=OFF is load-bearing: with shared libs the fork's I2_S quantiser
# (quantize_i2_s / dequantize_row_i2_s, defined in ggml-cpu) is an undefined symbol in
# ggml-base.dll, which is why an out-of-the-box shared build fails to link on this base.
#
# Resumable: each (model, threads) result is its own CSV; a re-run skips any that already
# exist and are non-empty. Delete logs/eff_*.csv to force a clean sweep.
set -uo pipefail
cd "$(dirname "$0")"
mkdir -p logs

BIN="${LLAMA_BENCH:-./BitNet/build-static/bin/llama-bench.exe}"
THREADS="${THREADS:-1 2 4 8 16}"
PP="${PP:-128,512,2048}"
TG="${TG:-128}"
REP="${REP:-5}"

MODELS="
bitnet_i2s:models/bitnet-b1.58-2B-4T.i2_s.gguf
qwen_q4_k_m:models/qwen2.5-1.5b-instruct.q4_k_m.gguf
qwen_q8_0:models/qwen2.5-1.5b-instruct.q8_0.gguf
qwen_fp16:models/qwen2.5-1.5b-instruct.fp16.gguf
"

done_ok () { [ -s "$1" ] && grep -q '"CPU"' "$1"; }

for entry in $MODELS; do
  tag="${entry%%:*}"; gguf="${entry#*:}"
  [ -f "$gguf" ] || { echo "MISSING $gguf - skipping $tag"; continue; }
  for t in $THREADS; do
    out="logs/eff_${tag}_t${t}.csv"
    if done_ok "$out"; then echo "skip $tag t=$t (have $out)"; continue; fi
    echo "=== $tag  threads=$t ==="
    "$BIN" -m "$gguf" -t "$t" -p "$PP" -n "$TG" -r "$REP" -o csv \
      > "$out" 2> "logs/eff_${tag}_t${t}.err" || echo "  (nonzero exit for $tag t=$t)"
  done
done

echo
echo "=== peak working set: one tg-only run per model at 8 threads ==="
# llama-bench does not report process RSS; sample PeakWorkingSet64 via PowerShell.
# No energy column: this machine exposes no RAPL / power-meter perf counter and runs on
# AC (battery DischargeRate reads 0), so there is no software wattage source. That axis
# needs an external meter.
for entry in $MODELS; do
  tag="${entry%%:*}"; gguf="${entry#*:}"
  [ -f "$gguf" ] || continue
  [ -s "logs/eff_${tag}_rss.json" ] && { echo "skip rss $tag"; continue; }
  powershell -NoProfile -Command "
    \$p = Start-Process -FilePath '$BIN' -ArgumentList '-m','$gguf','-t','8','-p','0','-n','256','-r','1' -PassThru -NoNewWindow -RedirectStandardOutput 'logs/eff_${tag}_rss.out' -RedirectStandardError 'logs/eff_${tag}_rss.serr'
    \$peak = 0
    while (-not \$p.HasExited) { try { \$p.Refresh(); if (\$p.PeakWorkingSet64 -gt \$peak) { \$peak = \$p.PeakWorkingSet64 } } catch {}; Start-Sleep -Milliseconds 150 }
    [pscustomobject]@{ model='$tag'; peak_working_set_MB = [math]::Round(\$peak/1MB,1) } | ConvertTo-Json -Compress
  " > "logs/eff_${tag}_rss.json" 2>"logs/eff_${tag}_rss.jerr"
  cat "logs/eff_${tag}_rss.json"
done

echo "Arm B done -> logs/. Next: python analysis_eff.py"
