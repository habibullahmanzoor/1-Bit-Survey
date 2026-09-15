#!/usr/bin/env bash
# GSM8K (5-shot, generative) for the accuracy arm -- the one benchmark left un-reverified.
# Unlike the loglikelihood suite this needs text generation + the chat template, so it is
# its own table and its numbers are not directly comparable to the template-free §10.3 ones.
#
# Order = priority. Tier 1 (qwen, bitnet) is the primary pairing / the card's numbers.
# Tier 2 (falcon3 x2, qwen-nf4) are the controlled pairs. Tier 3 (spectra x2) are base
# 300B-token models that will score near zero -- included only for table completeness.
#
# Resumable: have() skips any model whose output already exists. Kill and re-run freely.
set -uo pipefail
cd "$(dirname "$0")"
mkdir -p logs
# NOTE: offline flags deliberately NOT set -- openai/gsm8k is not cached. Models resolve
# from the HF cache (all used in earlier passes). triton-windows is installed so BitNet's
# autobitlinear layer torch.compiles (eager is ~35x slower for few-shot contexts; see
# run_accuracy.sh). Do NOT set TORCHDYNAMO_DISABLE.
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PY=.venv/Scripts/python.exe
GEN="max_gen_toks=256"

# key : model_args : batch_size : is_instruct(1/0)
ENTRIES=(
  "qwen2.5-1.5b:pretrained=Qwen/Qwen2.5-1.5B-Instruct,dtype=bfloat16:8:1"
  "bitnet-2b4t:pretrained=microsoft/bitnet-b1.58-2B-4T-bf16,dtype=bfloat16:1:1"
  "falcon3-1b-bf16:pretrained=tiiuae/Falcon3-1B-Instruct,dtype=bfloat16:8:1"
  "falcon3-1b-158:pretrained=tiiuae/Falcon3-1B-Instruct-1.58bit,dtype=bfloat16:8:1"
  "qwen-nf4:pretrained=models/qwen2.5-1.5b-instruct-nf4,dtype=bfloat16:4:1"
  "trilm-2.4b:pretrained=SpectraSuite/TriLM_2.4B_Unpacked,dtype=bfloat16:2:0"
  "floatlm-2.4b:pretrained=SpectraSuite/FloatLM_2.4B,dtype=bfloat16:2:0"
)

have () { compgen -G "logs/gsm8k_$1"*.json > /dev/null 2>&1; }

for entry in "${ENTRIES[@]}"; do
  IFS=":" read -r key margs bs instr <<< "$entry"
  if have "$key"; then echo "=== skip $key (have gsm8k) ==="; continue; fi
  echo "=== $key : gsm8k 5-shot $(date -u +%H:%M:%SZ) ==="
  ct=()
  [ "$instr" = "1" ] && ct=(--apply_chat_template --fewshot_as_multiturn)
  $PY -m lm_eval --model hf --model_args "$margs" \
    --tasks gsm8k --num_fewshot 5 --gen_kwargs "$GEN" --batch_size "$bs" \
    "${ct[@]}" \
    --output_path "logs/gsm8k_${key}.json" --log_samples \
    2> "logs/gsm8k_${key}.err" || echo "  (nonzero exit: $key)"
  echo "=== $key done $(date -u +%H:%M:%SZ) ==="
done
echo "=== GSM8K SWEEP DONE $(date -u +%H:%M:%SZ) -> logs/gsm8k_*.json ==="
