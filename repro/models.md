# Checkpoints under test

| role | model | HF id | params | bits | why |
|---|---|---|---|---|---|
| flagship native 1-bit | BitNet b1.58 2B4T | `microsoft/bitnet-b1.58-2B-4T` (+ `-bf16`, `-gguf`) | 2.0B | W1.58A8 | the reference open native 1-bit model; vendor efficiency table is what we re-check |
| smaller native 1-bit | Falcon3-1B-Instruct-1.58bit | `tiiuae/Falcon3-1B-Instruct-1.58bit` | 1.0B | W1.58 | non-Microsoft native 1-bit; second family + smaller scale point |
| (alt smaller) | Spectra TriLM 1.1B | `NolanoOrg/...` (from Spectra suite) | 1.1B | ternary | fallback / third family if Falcon3 tokenizer issues |
| FP16 baseline | Qwen2.5-1.5B-Instruct | `Qwen/Qwen2.5-1.5B-Instruct` | 1.5B | BF16 | size-matched full-precision reference for accuracy + efficiency deltas |
| (alt baseline) | Llama-3.2-1B-Instruct | `meta-llama/Llama-3.2-1B-Instruct` | 1.2B | BF16 | second FP baseline; matches BitNet's own comparison table |

Comfortable-tier adds: a 4th model (second scale point), MMLU+GSM8K on both instruct
models, an ARM SBC for Arm B. Only if the target shifts to Nature MI / IEEE COMST.

## Tasks (Arm A)
`arc_easy, arc_challenge, hellaswag, winogrande, piqa, openbookqa, boolq` (zero-shot) +
`wikitext` (word perplexity). Instruct only: `mmlu` (5-shot), `gsm8k` (8-shot, 3 seeds).

## Published numbers to beat/verify (fill exact values from inventory.csv + _web/ snapshots)
- BitNet b1.58 2B4T: zero-shot avg 54.19; ARC-c 49.91; GSM8K 58.38; MMLU 53.17.
- Efficiency (non-emb): 0.4 GB mem / 29 ms CPU decode / 0.028 J — vs Qwen2.5-1.5B 2.6 GB / 65 ms / 0.347 J.
