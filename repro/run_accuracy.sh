#!/usr/bin/env bash
# Arm A - accuracy reproduction. Shared RTX 4080: keep batch size small.
# ~1-3 h per model; run overnight. Requires: lm-evaluation-harness at env/harness-commit.txt.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs

# Windows-specific fixes, confirmed necessary at the harness-commit.txt pin (transformers 5.16.1):
# - PYTHONUTF8/PYTHONIOENCODING: lm-eval's results table prints a Unicode arrow; Windows'
#   legacy console codepage otherwise crashes the process AFTER the eval has already run,
#   losing the pretty-printed table (the JSON output is unaffected either way, but don't rely on that).
# - triton-windows==3.1.0.post17 (env/requirements.txt) supplies the Triton build that
#   torch 2.5.1's inductor backend expects, so BitNet's native `autobitlinear` layer can
#   torch.compile. Without it the layer falls back to eager, which is ~35x slower for the
#   5-shot / 8-shot contexts of MMLU and GSM8K (measured) - impractical, not just slow.
#   Do NOT set TORCHDYNAMO_DISABLE here.
# - PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True: over ~69k requests the caching
#   allocator fragments badly on the 12 GB card, and the memory-heavy WikiText rolling-
#   perplexity pass at the end then OOMs even though each earlier request fit. Expandable
#   segments plus running WikiText as its own process (below) keeps it inside the budget.
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

BS="${LM_EVAL_BATCH_SIZE:-4}"
ZS="arc_easy,arc_challenge,hellaswag,winogrande,piqa,openbookqa,boolq"
PPL="wikitext"

# model_key : HF id : is_instruct
# bitnet-2b4t uses the -bf16 repo variant: the base `microsoft/bitnet-b1.58-2B-4T` repo has
# no configuration_bitnet.py for trust_remote_code to resolve (transformers 5.16.1 recognizes
# model_type "bitnet" natively instead - trust_remote_code=True actively breaks loading here,
# so it is dropped for all three models below, not just BitNet).
MODELS=(
  "bitnet-2b4t:microsoft/bitnet-b1.58-2B-4T-bf16:1"
  "falcon3-1b-158:tiiuae/Falcon3-1B-Instruct-1.58bit:1"
  "qwen2.5-1.5b:Qwen/Qwen2.5-1.5B-Instruct:1"
)

# Resume guard: lm-eval writes a timestamped file under the --output_path stem, so a
# rerun of an interrupted sweep would otherwise redo completed invocations. Skip any
# whose output already exists. Delete the stale file to force a re-run.
have () { compgen -G "logs/acc_$1"* > /dev/null 2>&1; }

for entry in "${MODELS[@]}"; do
  IFS=":" read -r key hfid instr <<< "$entry"
  echo "=== $key ($hfid) ==="

  # zero-shot multiple-choice suite
  have "${key}_zeroshot" || lm_eval --model hf \
    --model_args "pretrained=${hfid},dtype=bfloat16" \
    --tasks "${ZS}" --num_fewshot 0 --batch_size "$BS" \
    --output_path "logs/acc_${key}_zeroshot.json" --log_samples

  # WikiText word-perplexity: its own process (fresh CUDA memory), batch size 1, and
  # max_length=2048 (the classic WikiText-2 perplexity stride). Without the cap the
  # rolling-window logit tensor uses the model's full native context (32k for Qwen2.5)
  # against a ~150k vocab and OOMs the 12 GB card. The cap is applied to all three models
  # so the perplexities stay comparable.
  have "${key}_wikitext" || lm_eval --model hf \
    --model_args "pretrained=${hfid},dtype=bfloat16,max_length=2048" \
    --tasks "${PPL}" --num_fewshot 0 --batch_size 1 \
    --output_path "logs/acc_${key}_wikitext.json"

  # determinism check: repeat hellaswag once
  have "${key}_hellaswag_rerun" || lm_eval --model hf \
    --model_args "pretrained=${hfid},dtype=bfloat16" \
    --tasks hellaswag --num_fewshot 0 --batch_size "$BS" \
    --output_path "logs/acc_${key}_hellaswag_rerun.json"

  # MMLU (5-shot) and GSM8K (8-shot) are intentionally omitted. BitNet's native HF layer
  # torch.compiles per input shape; MMLU's 57 subjects each have a different context
  # length, so the few-shot sweep thrashes the compile cache and runs about an order of
  # magnitude slower than the fixed-shape zero-shot suite - many days for three models on
  # one shared laptop GPU. Section 10.2 records this. The vendors' MMLU/GSM8K figures stay
  # flagged as author-reported and un-reverified. To restore them, add back an
  #   lm_eval ... --tasks mmlu --num_fewshot 5 --limit 100 ...
  # block here on hardware where compile is cheap or the full sets are affordable.
done
echo "Arm A done -> logs/. Next: python analysis.py"
