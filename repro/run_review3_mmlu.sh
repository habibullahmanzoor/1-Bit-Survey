#!/usr/bin/env bash
# Review round 3: MMLU (0-shot) for the models that were left un-reverified.
# 0-shot keeps a fixed context shape, which avoids the per-shape recompilation that made
# 5-shot MMLU impractical for BitNet's native HF layer (Section 10.2). Loglikelihood
# scoring, dataset cached (cais/mmlu). GSM8K is still out: it needs generation + a chat
# template and its dataset is not cached here.
set -uo pipefail
cd "$(dirname "$0")"
mkdir -p logs
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 HF_DATASETS_OFFLINE=1
PY=.venv/Scripts/python.exe

have () { compgen -G "logs/acc_$1_mmlu0"*.json > /dev/null 2>&1; }

ENTRIES=(
  "bitnet-2b4t:pretrained=microsoft/bitnet-b1.58-2B-4T-bf16,dtype=bfloat16:4"
  "qwen2.5-1.5b:pretrained=Qwen/Qwen2.5-1.5B-Instruct,dtype=bfloat16:4"
  "qwen-nf4:pretrained=models/qwen2.5-1.5b-instruct-nf4,dtype=bfloat16:4"
  "falcon3-1b-158:pretrained=tiiuae/Falcon3-1B-Instruct-1.58bit,dtype=bfloat16:4"
  "falcon3-1b-bf16:pretrained=tiiuae/Falcon3-1B-Instruct,dtype=bfloat16:4"
  "trilm-2.4b:pretrained=SpectraSuite/TriLM_2.4B_Unpacked,dtype=bfloat16:2"
  "floatlm-2.4b:pretrained=SpectraSuite/FloatLM_2.4B,dtype=bfloat16:2"
)

for entry in "${ENTRIES[@]}"; do
  IFS=":" read -r key margs bs <<< "$entry"
  have "$key" && { echo "skip $key (have mmlu)"; continue; }
  echo "=== $key MMLU 0-shot ==="
  $PY -m lm_eval --model hf --model_args "$margs" \
    --tasks mmlu --num_fewshot 0 --batch_size "$bs" \
    --output_path "logs/acc_${key}_mmlu0.json" \
    2> "logs/acc_${key}_mmlu0.err" || echo "  (nonzero: $key mmlu)"
done
echo "review3 MMLU pass done -> logs/acc_*_mmlu0*"
