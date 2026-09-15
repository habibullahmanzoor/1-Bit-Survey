# Arm A - accuracy (plain acc; matches manuscript Section 10.3)

| model | ARCe | ARCc | HS | WG | PIQA | OBQA | BoolQ | mean | word_ppl | HS_rerun |
|---|---|---|---|---|---|---|---|---|---|---|
| bitnet-2b4t | 76.81 | 47.01 | 50.75 | 72.45 | 77.04 | 30.8 | 78.96 | 61.98 | 16.67 | 50.75 |
| falcon3-1b-158 | 55.3 | 26.11 | 36.11 | 55.09 | 65.61 | 18.8 | 62.78 | 45.69 | 32.82 | 36.11 |
| qwen2.5-1.5b | 76.68 | 43.6 | 50.86 | 62.75 | 76.33 | 31.8 | 78.01 | 60.0 | 13.48 | 50.86 |

acc_norm per task (not used in the mean):

| model | ARCe | ARCc | HS | WG | PIQA | OBQA | BoolQ |
|---|---|---|---|---|---|---|---|
| bitnet-2b4t | 73.95 | 47.78 | 67.6 |  | 77.09 | 40.2 |  |
| falcon3-1b-158 | 51.81 | 29.18 | 44.6 |  | 66.54 | 32.2 |  |
| qwen2.5-1.5b | 76.01 | 46.76 | 68.29 |  | 75.63 | 40.4 |  |
