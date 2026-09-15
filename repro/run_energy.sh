#!/usr/bin/env bash
# Arm B, energy addendum. Runs ONLY on battery: Windows exposes whole-system power to
# WMI as BatteryStatus.DischargeRate (milliwatts) while discharging; on AC it reads 0.
# This is whole-system draw (SoC, RAM, display, everything), NOT CPU-package and NOT
# the vendor's non-embedding accounting, so it is a fair A/B across the three models on
# one machine but is not directly comparable to the model card's 0.028 J/token figure.
set -uo pipefail
cd "$(dirname "$0")"
mkdir -p logs

BIN="${LLAMA_BENCH:-./BitNet/build-static/bin/llama-bench.exe}"
NGEN="${NGEN:-800}"
REP="${REP:-2}"
THREADS="${THREADS:-4}"   # per-model decode optimum on the 14900HX from run_efficiency

MODELS="
bitnet_i2s:models/bitnet-b1.58-2B-4T.i2_s.gguf
qwen_q4_k_m:models/qwen2.5-1.5b-instruct.q4_k_m.gguf
qwen_q8_0:models/qwen2.5-1.5b-instruct.q8_0.gguf
qwen_fp16:models/qwen2.5-1.5b-instruct.fp16.gguf
"

# --- guard: must be on battery ---
online=$(powershell -NoProfile -Command "(Get-CimInstance -Namespace root\wmi -ClassName BatteryStatus).PowerOnline")
if [ "$online" != "False" ]; then
  echo "ON AC POWER (PowerOnline=$online). Unplug the charger and re-run. Aborting."; exit 1
fi

# sampler: append 'epoch_ms,discharge_mW' every ~700 ms until a stop-file appears
sampler () { # outfile stopfile
  powershell -NoProfile -Command "
    \$out='$1'; \$stop='$2'; Remove-Item \$out -ErrorAction SilentlyContinue
    while (-not (Test-Path \$stop)) {
      \$mw = (Get-CimInstance -Namespace root\wmi -ClassName BatteryStatus).DischargeRate
      \$ms = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
      Add-Content \$out \"\$ms,\$mw\"
      Start-Sleep -Milliseconds 700
    }"
}

measure () { # tag command...
  local tag="$1"; shift
  local samp="logs/energy_${tag}_samples.csv" stop="logs/energy_${tag}.stop"
  rm -f "$stop"
  sampler "$samp" "$stop" &
  local spid=$!
  sleep 2
  "$@" > "logs/energy_${tag}_bench.json" 2> "logs/energy_${tag}_bench.err" || echo "  ($tag bench nonzero exit)"
  sleep 2
  touch "$stop"; wait "$spid" 2>/dev/null || true
  rm -f "$stop"
}

# Let the machine quiesce after the charger is pulled: the power-source transition
# leaves the SoC in a high state for tens of seconds and contaminates a leading idle
# baseline (observed: 45 W vs a settled 29 W). Then take idle BEFORE and AFTER the
# model runs and let analysis average the two (cold-leading vs warm-trailing bracket).
SETTLE="${SETTLE:-60}"
echo "=== settle ${SETTLE} s after unplug (leave the machine alone) ==="
sleep "$SETTLE"

echo "=== idle baseline, leading (45 s, leave the machine alone) ==="
measure idle powershell -NoProfile -Command "Start-Sleep -Seconds 45"

for entry in $MODELS; do
  tag="${entry%%:*}"; gguf="${entry#*:}"
  [ -f "$gguf" ] || { echo "MISSING $gguf"; continue; }
  echo "=== $tag : decode ${NGEN} tok x ${REP} @ ${THREADS} threads ==="
  measure "$tag" "$BIN" -m "$gguf" -t "$THREADS" -p 0 -n "$NGEN" -r "$REP" --no-warmup -o json
done

echo "=== idle baseline, trailing (45 s, leave the machine alone) ==="
measure idle_post powershell -NoProfile -Command "Start-Sleep -Seconds 45"

echo
echo "battery after run:"
powershell -NoProfile -Command "(Get-CimInstance -Namespace root\wmi -ClassName BatteryStatus) | Select-Object PowerOnline,DischargeRate,RemainingCapacity | Format-List"
echo "Arm B energy done -> logs/. Next: python analysis_energy.py"
