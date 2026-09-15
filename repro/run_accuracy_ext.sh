#!/usr/bin/env bash
# Arm A, extension pass (review round 3). Adds:
#  - a controlled native-ternary-vs-FP16 comparison from open artifacts:
#      Spectra TriLM 2.4B  vs  FloatLM 2.4B   (matched params / tokenizer / data / 300B tok)
#      Falcon3-1B-Instruct-1.58bit vs Falcon3-1B-Instruct  (same model, QAT-to-1.58bit vs bf16)
#  - the actual Q4_K_M / Q8_0 / FP16 GGUF baselines run through the SAME 7-task lm-eval
#    suite as the main table (transformers dequantises the GGUF; accuracy reflects the
#    quantisation error), so the "4-bit stays close in accuracy" claim gets a full-suite,
#    same-harness number rather than perplexity + a HellaSwag subset.
#
# Same harness commit, tasks, and settings as run_accuracy.sh. Resumable via the have() guard.
set -uo pipefail
cd "$(dirname "$0")"
mkdir -p logs
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PY=.venv/Scripts/python.exe

ZS="arc_easy,arc_challenge,hellaswag,winogrande,piqa,openbookqa,boolq"
QDIR="$(pwd)/models"

have () { compgen -G "logs/acc_$1"* > /dev/null 2>&1; }

# key : loader-spec : batch_size
# loader-spec is passed straight into --model_args after pretrained=
ENTRIES=(
  "qwen-gguf-q4km:pretrained=${QDIR},gguf_file=qwen2.5-1.5b-instruct.q4_k_m.gguf,dtype=bfloat16:4"
  "qwen-gguf-q8:pretrained=${QDIR},gguf_file=qwen2.5-1.5b-instruct.q8_0.gguf,dtype=bfloat16:4"
  "qwen-gguf-fp16:pretrained=${QDIR},gguf_file=qwen2.5-1.5b-instruct.fp16.gguf,dtype=bfloat16:4"
  "falcon3-1b-bf16:pretrained=tiiuae/Falcon3-1B-Instruct,dtype=bfloat16:4"
  "trilm-2.4b:pretrained=SpectraSuite/TriLM_2.4B_Unpacked,dtype=bfloat16:2"
  "floatlm-2.4b:pretrained=SpectraSuite/FloatLM_2.4B,dtype=bfloat16:2"
)

for entry in "${ENTRIES[@]}"; do
  IFS=":" read -r key margs bs <<< "$entry"
  echo "=== $key ==="

  have "${key}_zeroshot" || $PY -m lm_eval --model hf \
    --model_args "$margs" \
    --tasks "$ZS" --num_fewshot 0 --batch_size "$bs" \
    --output_path "logs/acc_${key}_zeroshot.json" --log_samples \
    2> "logs/acc_${key}_zeroshot.err" || echo "  (nonzero exit: $key zeroshot)"

  have "${key}_wikitext" || $PY -m lm_eval --model hf \
    --model_args "${margs},max_length=2048" \
    --tasks wikitext --num_fewshot 0 --batch_size 1 \
    --output_path "logs/acc_${key}_wikitext.json" \
    2> "logs/acc_${key}_wikitext.err" || echo "  (nonzero exit: $key wikitext)"

  have "${key}_hellaswag_rerun" || $PY -m lm_eval --model hf \
    --model_args "$margs" \
    --tasks hellaswag --num_fewshot 0 --batch_size "$bs" \
    --output_path "logs/acc_${key}_hellaswag_rerun.json" \
    2> "logs/acc_${key}_hellaswag_rerun.err" || echo "  (nonzero exit: $key hs-rerun)"
done
echo "ext accuracy pass done -> logs/acc_*"
