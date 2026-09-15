# GSM8K re-measurement (2026-09-09)

Run through the same lm-eval harness/commit as Arm A, but **generative** (`gsm8k`,
5-shot, `max_gen_toks=256`, greedy) and **with each instruct model's chat template**
(`--apply_chat_template --fewshot_as_multiturn`). This differs from the loglikelihood,
template-free protocol of the seven-task suite and MMLU, so these numbers are reported
on their own and not folded into any mean. Spectra's base models carry no chat template
and were run template-free.

`flexible-extract` = last number in the output. `strict-match` = the canonical `#### N`
line only.

| model | flexible-extract | strict-match |
|---|---|---|
| BitNet b1.58 2B4T (ternary, 2.4B) | **61.9** (±1.3) | 59.6 (±1.4) |
| Qwen2.5-1.5B-Instruct (bf16) | 57.5 (±1.4) | 35.0 (±1.3) |
| Qwen2.5-1.5B-Instruct (nf4) | 49.7 (±1.4) | 36.8 (±1.3) |
| Falcon3-1B-Instruct (bf16) | 44.7 (±1.4) | 42.6 (±1.4) |
| Falcon3-1B-Instruct-1.58bit | 27.7 (±1.2) | 7.4 (±0.7) |
| Spectra TriLM 2.4B (no template) | 3.0 (±0.5) | 1.9 (±0.4) |
| Spectra FloatLM 2.4B (no template) | 1.9 (±0.4) | 1.3 (±0.3) |

Vendor card (`Ma2025-BitNet2B4T`): BitNet GSM8K **58.38**, Qwen2.5-1.5B **56.79**.

## Which metric

flexible-extract (last number in the output) is the one that tracks arithmetic ability.
strict-match (canonical answer line only) is depressed for Qwen bf16 (57.5 -> 35.0),
Qwen nf4 (49.7 -> 36.8) and Falcon3-1.58bit (27.7 -> 7.4): under `--apply_chat_template
--fewshot_as_multiturn` these models solve the problem but do not reliably end with the
`#### N` line. BitNet (61.9 -> 59.6) and Falcon3 bf16 (44.7 -> 42.6) keep the format.
So compare on flexible-extract.

## Reading (flexible-extract)

- **The card's GSM8K claim for BitNet reproduces.** BitNet 61.9 vs our Qwen bf16 57.5 =
  **+4.4 pt**; the card reports +1.6 (58.38 vs 56.79). GSM8K is the one benchmark on which
  the card puts the 1-bit model ahead, and it holds up under an independent run.
- **4-bit nf4 costs 7.8 pt on GSM8K** (49.7 vs bf16 57.5), against only 2.7 on the
  seven-task mean -- arithmetic is more quantization-fragile than commonsense reasoning.
- **Falcon3-1B 1.58-bit loses 17 pt** (27.7 vs bf16 44.7), consistent with its seven-task
  (-11.5) and MMLU (-18) losses.
- **Spectra TriLM/FloatLM: noise floor** (3.0 / 1.9). 300B-token base models, no
  instruction tuning; GSM8K uninformative for this pair, exactly as MMLU was.

## Provenance

- Script `run_gsm8k.sh` (5-shot, `max_gen_toks=256`, greedy; `--apply_chat_template
  --fewshot_as_multiturn` for the instruct models, template-free for Spectra base models).
  Parser `analysis_gsm8k.py`. Raw JSON `logs/gsm8k_*.json`, console `logs/gsm8k_*.err`.
  Sweep log `scratchpad/gsm8k_sweep.log`.
- Two Qwen bf16 attempts: the first failed on a transient DNS error fetching
  `openai/gsm8k`; the rerun (2026-09-09 22:43Z) succeeded.
