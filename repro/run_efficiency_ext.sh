#!/usr/bin/env bash
# Arm B extension (review round 3): more 4-bit formats, so the "no advantage vs 4-bit"
# claim is not tied to Q4_K_M alone. Builds Q4_0 and Q4_K_S GGUFs of the same
# Qwen2.5-1.5B-Instruct checkpoint from the FP16 GGUF, then runs the identical thread
# sweep as run_efficiency.sh. Resumable.
set -uo pipefail
cd "$(dirname "$0")"
mkdir -p logs

BIN="${LLAMA_BENCH:-./BitNet/build-static/bin/llama-bench.exe}"
QNT="./BitNet/build-static/bin/llama-quantize.exe"
SRC="models/qwen2.5-1.5b-instruct.fp16.gguf"
THREADS="${THREADS:-1 2 4 8 16}"
PP="${PP:-128,512,2048}"
TG="${TG:-128}"
REP="${REP:-5}"

# format-name : llama-quantize type string : output file
FMTS="
qwen_q4_0:Q4_0:models/qwen2.5-1.5b-instruct.q4_0.gguf
qwen_q4_k_s:Q4_K_S:models/qwen2.5-1.5b-instruct.q4_k_s.gguf
"

for f in $FMTS; do
  tag="${f%%:*}"; rest="${f#*:}"; qtype="${rest%%:*}"; out="${rest#*:}"
  if [ ! -s "$out" ]; then
    echo "=== quantise $qtype -> $out ==="
    "$QNT" "$SRC" "$out" "$qtype" 2> "logs/${tag}_quantize.err" || echo "  (quantise failed: $tag)"
  fi
done

done_ok () { [ -s "$1" ] && grep -q '"CPU"' "$1"; }

for f in $FMTS; do
  tag="${f%%:*}"; rest="${f#*:}"; gguf="${rest#*:}"
  [ -f "$gguf" ] || { echo "MISSING $gguf - skipping $tag"; continue; }
  for t in $THREADS; do
    o="logs/eff_${tag}_t${t}.csv"
    if done_ok "$o"; then echo "skip $tag t=$t"; continue; fi
    echo "=== $tag threads=$t ==="
    "$BIN" -m "$gguf" -t "$t" -p "$PP" -n "$TG" -r "$REP" -o csv \
      > "$o" 2> "logs/eff_${tag}_t${t}.err" || echo "  (nonzero exit $tag t=$t)"
  done
  # peak RSS at 8 threads, same method as run_efficiency.sh
  if [ ! -s "logs/eff_${tag}_rss.json" ]; then
    powershell -NoProfile -Command "
      \$p = Start-Process -FilePath '$BIN' -ArgumentList '-m','$gguf','-t','8','-p','0','-n','256','-r','1' -PassThru -NoNewWindow -RedirectStandardOutput 'logs/eff_${tag}_rss.out' -RedirectStandardError 'logs/eff_${tag}_rss.serr'
      \$peak = 0
      while (-not \$p.HasExited) { try { \$p.Refresh(); if (\$p.PeakWorkingSet64 -gt \$peak) { \$peak = \$p.PeakWorkingSet64 } } catch {}; Start-Sleep -Milliseconds 150 }
      [pscustomobject]@{ model='$tag'; peak_working_set_MB = [math]::Round(\$peak/1MB,1) } | ConvertTo-Json -Compress
    " > "logs/eff_${tag}_rss.json" 2>"logs/eff_${tag}_rss.jerr"
    cat "logs/eff_${tag}_rss.json"
  fi
done
echo "Arm B ext done -> logs/eff_qwen_q4_0_*, logs/eff_qwen_q4_k_s_*"
