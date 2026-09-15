#!/usr/bin/env bash
# Arm A addendum - accuracy of the GGUF quantisations used in the Arm B efficiency
# comparison. The point: does a 4-bit / 8-bit Qwen keep its accuracy while beating
# BitNet on speed and size?
#
# All three metrics run through llama.cpp's own batched evaluators (llama-perplexity),
# so the comparison is internally consistent: FP16 vs Q8_0 vs Q4_K_M of the SAME Qwen
# checkpoint isolates the quantisation loss. BitNet i2_s is included as a cross-check
# against the Arm A Hugging Face numbers.
#
# lm-eval's `gguf` model type was tried first but is incompatible with this
# llama-server build's logprobs schema (returns logprobs.content, not the OpenAI-style
# text_offset/token_logprobs lm-eval expects), so the native evaluators are used.
set -uo pipefail
cd "$(dirname "$0")"
mkdir -p logs

PPL="./BitNet/build-static/bin/llama-perplexity.exe"
T=8
HS_N="${HS_N:-1000}"     # hellaswag examples (full set is 10042; 1000 gives ~+-3% CI, enough for a delta)
RUN_WG="${RUN_WG:-0}"    # winogrande is least quant-sensitive; off by default

MODELS="
qwen_fp16:models/qwen2.5-1.5b-instruct.fp16.gguf
qwen_q8_0:models/qwen2.5-1.5b-instruct.q8_0.gguf
qwen_q4_k_m:models/qwen2.5-1.5b-instruct.q4_k_m.gguf
bitnet_i2s:models/bitnet-b1.58-2B-4T.i2_s.gguf
"

for entry in $MODELS; do
  tag="${entry%%:*}"; gguf="${entry#*:}"
  [ -f "$gguf" ] || { echo "MISSING $gguf"; continue; }

  o="logs/qacc_${tag}_wikitext.txt"
  if [ -s "$o" ]; then echo "skip $tag wikitext"; else
    echo "=== $tag : WikiText-2 perplexity (ctx 2048) ==="
    "$PPL" -m "$gguf" -f data/wikitext-2-raw/wiki.test.raw -t $T -ngl 0 -c 2048 \
      > "$o" 2> "logs/qacc_${tag}_wikitext.err" || echo "  (nonzero exit)"
  fi

  o="logs/qacc_${tag}_hellaswag.txt"
  if [ -s "$o" ]; then echo "skip $tag hellaswag"; else
    echo "=== $tag : HellaSwag (${HS_N}) ==="
    "$PPL" -m "$gguf" -f data/hellaswag_val_full.txt --hellaswag --hellaswag-tasks "$HS_N" \
      -t $T -ngl 0 -c 2048 > "$o" 2> "logs/qacc_${tag}_hellaswag.err" || echo "  (nonzero exit)"
  fi

  o="logs/qacc_${tag}_winogrande.txt"
  if [ "$RUN_WG" = "1" ] && [ ! -s "$o" ]; then
    echo "=== $tag : Winogrande (1267) ==="
    "$PPL" -m "$gguf" -f data/winogrande-debiased-eval.csv --winogrande \
      -t $T -ngl 0 -c 2048 > "$o" 2> "logs/qacc_${tag}_winogrande.err" || echo "  (nonzero exit)"
  fi
done

echo "Arm A addendum done -> logs/qacc_*. Next: python analysis_quant_acc.py"
