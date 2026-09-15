#!/usr/bin/env bash
# Review round 3, accuracy experiments. Same lm-eval harness / commit / tasks as
# run_accuracy.sh. Resumable via have().
#
#  qwen-nf4      : Qwen2.5-1.5B-Instruct at 4-bit (bitsandbytes nf4) -> full 7-task suite
#                 for the 4-bit baseline (was only ppl + a HellaSwag subset before).
#  falcon3-1b-bf16 : the bf16 counterpart of the cached Falcon3-1B-Instruct-1.58bit.
#                    Same model, same tokenizer, same data, QAT-1.58bit vs full precision:
#                    a controlled ternary-vs-FP16 pair.
#  trilm-2.4b / floatlm-2.4b : Spectra's matched ternary/FP16 pair (params, tokenizer,
#                    data, 300B tokens all matched) -- the cleanest controlled comparison.
set -uo pipefail
cd "$(dirname "$0")"
mkdir -p logs
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 HF_DATASETS_OFFLINE=1
PY=.venv/Scripts/python.exe
ZS="arc_easy,arc_challenge,hellaswag,winogrande,piqa,openbookqa,boolq"

have () { compgen -G "logs/acc_$1"*.json > /dev/null 2>&1; }

# key : model_args (after --model hf --model_args) : batch_size
ENTRIES=(
  "qwen-nf4:pretrained=models/qwen2.5-1.5b-instruct-nf4,dtype=bfloat16:4"
  "falcon3-1b-bf16:pretrained=tiiuae/Falcon3-1B-Instruct,dtype=bfloat16:4"
  "trilm-2.4b:pretrained=SpectraSuite/TriLM_2.4B_Unpacked,dtype=bfloat16:2"
  "floatlm-2.4b:pretrained=SpectraSuite/FloatLM_2.4B,dtype=bfloat16:2"
)

for entry in "${ENTRIES[@]}"; do
  IFS=":" read -r key margs bs <<< "$entry"
  echo "=== $key ==="

  have "${key}_zeroshot" || $PY -m lm_eval --model hf --model_args "$margs" \
    --tasks "$ZS" --num_fewshot 0 --batch_size "$bs" \
    --output_path "logs/acc_${key}_zeroshot.json" --log_samples \
    2> "logs/acc_${key}_zeroshot.err" || echo "  (nonzero: $key zeroshot)"

  have "${key}_wikitext" || $PY -m lm_eval --model hf --model_args "${margs},max_length=2048" \
    --tasks wikitext --num_fewshot 0 --batch_size 1 \
    --output_path "logs/acc_${key}_wikitext.json" \
    2> "logs/acc_${key}_wikitext.err" || echo "  (nonzero: $key wikitext)"

  have "${key}_hellaswag_rerun" || $PY -m lm_eval --model hf --model_args "$margs" \
    --tasks hellaswag --num_fewshot 0 --batch_size "$bs" \
    --output_path "logs/acc_${key}_hellaswag_rerun.json" \
    2> "logs/acc_${key}_hellaswag_rerun.err" || echo "  (nonzero: $key hs-rerun)"
done
echo "review3 accuracy pass done -> logs/acc_*"
