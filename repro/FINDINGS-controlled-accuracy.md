# Controlled accuracy comparisons (review round 3, 2026-09-08)

Run through the same lm-eval harness / commit as Arm A. Seven-task zero-shot suite
(ARCe, ARCc, HellaSwag, WinoGrande, PIQA, OpenBookQA, BoolQ), plain `acc`; WikiText-2
word perplexity; MMLU at zero shot.

## All models

| model | mean (7-task) | WikiText ppl | MMLU 0-shot |
|---|---|---|---|
| BitNet b1.58 2B4T (ternary, 2.4B, transformers bf16) | 61.98 | 16.67 | 52.07 |
| Qwen2.5-1.5B-Instruct (bf16) | 60.00 | 13.48 | 60.03 |
| Qwen2.5-1.5B-Instruct (nf4, bitsandbytes) | 57.33 | 14.59 | 58.06 |
| Falcon3-1B-Instruct-1.58bit | 45.69 | 32.82 | 25.43 |
| Falcon3-1B-Instruct (bf16) | 57.22 | 18.85 | 43.79 |
| Spectra TriLM 2.4B (native ternary, 300B tok) | 51.49 | 14.90 | 22.97 |
| Spectra FloatLM 2.4B (FP16, 300B tok) | 52.05 | 13.06 | 25.18 |

## Controlled pairs (matched model family / tokenizer / data)

| pair | Δ mean | Δ ppl | Δ MMLU |
|---|---|---|---|
| Spectra 2.4B: TriLM (native ternary) vs FloatLM (FP16), 300B tok | **-0.56** | +1.84 (+14%) | -2.2 (both near chance) |
| Qwen 1.5B: nf4 4-bit vs bf16 | -2.67 | +1.11 (+8%) | -1.97 |
| Falcon3-1B: 1.58-bit continued-QAT vs bf16 | -11.53 | +14.0 (+74%) | -18.36 |

## Reading

- **Spectra is the clean native-ternary-vs-FP16 test.** At 2.4B / 300B tok, matched
  everything, ternary is within 0.6 pt of FP16 on the seven-task mean, with perplexity
  14% higher: downstream parity, worse LM loss, the same shape the native line reports
  for itself. Both models are near chance on MMLU (300B tok does not buy world knowledge
  at 2.4B), so that column is uninformative for this pair.
- **Post-hoc 4-bit (nf4) costs more than native ternary at comparable scale** (-2.7 vs
  -0.6 on the mean), consistent with ParetoQ's frontier ordering (ternary QAT ahead of
  4-bit PTQ). Note nf4 is more aggressive than the Q4_K_M used in the efficiency arm.
- **Falcon3-1B 1.58-bit is far from parity** (-11.5 mean, MMLU at chance). Continued-QAT
  to 1.58-bit at 1B parameter scale does not preserve capability; supports "parity is a
  multi-billion-parameter, native-from-scratch property".
- **MMLU (0-shot) is now measured for all seven models.** BitNet 2B4T 52.07 vs the card's
  5-shot 53.17; Qwen 60.03 vs card 60.25 -- both reproduce, and BitNet's ~8-pt MMLU
  deficit vs Qwen is what pulls the card's MMLU-inclusive "average" (54.19) below Qwen's.

## Provenance

- nf4: `models/qwen2.5-1.5b-instruct-nf4/` -- `BitsAndBytesConfig(load_in_4bit=True,
  bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=bfloat16)`, bitsandbytes 0.50.2,
  quantised at load from `Qwen/Qwen2.5-1.5B-Instruct` and saved.
- Spectra: `SpectraSuite/TriLM_2.4B_Unpacked`, `SpectraSuite/FloatLM_2.4B` (HF).
- Falcon3: `tiiuae/Falcon3-1B-Instruct-1.58bit`, `tiiuae/Falcon3-1B-Instruct` (HF).
- Scripts: `run_review3_accuracy.sh`, `run_review3_mmlu.sh`; parser `analysis_review3.py`.
- Raw JSON: `logs/acc_{qwen-nf4,falcon3-1b-bf16,trilm-2.4b,floatlm-2.4b}_*.json`,
  `logs/acc_*_mmlu0*.json`.
