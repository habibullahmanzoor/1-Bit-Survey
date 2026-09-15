#!/usr/bin/env bash
# Chained review-3 campaign: waits for the CPU efficiency-ext sweep to finish (so its
# throughput numbers are measured uncontended), then downloads the controlled-comparison
# models, then runs the accuracy suite, then MMLU. One background job.
set -uo pipefail
cd "$(dirname "$0")"
mkdir -p logs
EFF_PID="${1:-}"

if [ -n "$EFF_PID" ]; then
  echo "[chain] waiting for efficiency-ext pid $EFF_PID ..."
  while kill -0 "$EFF_PID" 2>/dev/null; do sleep 30; done
  echo "[chain] efficiency-ext done at $(date)"
fi

echo "[chain] downloading controlled-comparison models ..."
.venv/Scripts/python.exe - <<'PY'
from huggingface_hub import snapshot_download
for r in ["tiiuae/Falcon3-1B-Instruct",
          "SpectraSuite/TriLM_2.4B_Unpacked",
          "SpectraSuite/FloatLM_2.4B"]:
    print("[dl]", r, flush=True)
    try:
        snapshot_download(r, allow_patterns=["*.safetensors","*.json","*.model","tokenizer*","*.txt","*.py"])
        print("[dl]  ok", flush=True)
    except Exception as e:
        print("[dl]  FAIL", type(e).__name__, e, flush=True)
PY

echo "[chain] === accuracy suite ==="
bash run_review3_accuracy.sh || echo "[chain] accuracy suite returned nonzero"

echo "[chain] === MMLU ==="
bash run_review3_mmlu.sh || echo "[chain] mmlu returned nonzero"

echo "[chain] DONE at $(date)"
