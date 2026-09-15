# Battery energy per token (Arm B addendum) -- three sessions

Whole-system energy per token, `mean_discharge_W / decode_tok_per_s`, on the 14900HX
laptop on battery at 4 threads. Windows exposes only `BatteryStatus.DischargeRate` (mW,
whole system), so this is SoC + RAM + display + everything, not CPU-package and not the
vendor's non-embedding accounting.

## Runs

| run | when | notes | idle W |
|---|---|---|---|
| 1 | 2026-09-06 | 800 tok x2; leading idle only; no Q4_K_M | 29.1 |
| 2 | 2026-09-09 | 800 tok x2; leading idle contaminated by the unplug transient (8 s settle) | 44.7 |
| 3 | 2026-09-09 | 800 tok x3; 60 s settle; idle before *and* after; battery draining fast | 48.9 / 46.4 |

Backups: `logs/energy_run1_3model/`, `logs/energy_run2_contaminated/`,
`logs/energy_run3_batterydrain/`. Consolidate with `python analysis_energy_allruns.py`.

## Whole-system J/token

| model | run 1 | run 2 | run 3 |
|---|---|---|---|
| BitNet b1.58 2B4T, I2_S | 1.91 | 2.40 | 2.82 |
| Qwen2.5-1.5B, Q4_K_M | -- | 2.41 | 3.19 |
| Qwen2.5-1.5B, Q8_0 | 2.78 | 3.85 | 4.78 |
| Qwen2.5-1.5B, FP16 | 4.79 | 5.26 | 6.58 |

Decode t/s in the same runs: BitNet 22.7 / 22.6 / 17.8; Q4_K_M -- / 21.6 / 14.3;
Q8_0 13.5 / 12.2 / 9.4; FP16 7.8 / 8.6 / 7.4. The on-battery power cap tightens as the
battery drains (run 3 fell from ~73000 to ~59000 mWh mid-pass), so absolute t/s and
absolute J/token drift downward/upward across runs. Only within-run ratios are stable.

## Stable finding (ratios, BitNet as numerator)

| pair | run 1 | run 2 | run 3 | reading |
|---|---|---|---|---|
| BitNet : Q4_K_M | -- | 1.00x | 0.88x | **parity -- no ternary energy advantage over the 4-bit k-quant** |
| BitNet : Q8_0 | 0.69x | 0.62x | 0.59x | ternary ~0.6x the energy of Q8_0 |
| BitNet : FP16 | 0.40x | 0.46x | 0.43x | ternary ~0.43x the energy of FP16 |

Energy ranking = decode-throughput ranking. BitNet and Q4_K_M decode fastest, so they
amortize the laptop's large idle draw (29-49 W depending on battery state) over the most
tokens. The saving vs FP16/Q8_0 is a speed effect, not a compute-energy effect.

## Not reported: idle-subtracted "net compute energy"

Run 1 gave clean positive nets (BitNet 0.62, Q8_0 0.62, FP16 1.06 J/tok). Runs 2-3 could
not reproduce a stable idle baseline: run 2's leading idle was inflated by the unplug
transient, and in run 3 the bracketing idle windows (battery fuller) drew *more* than the
mid-pass model runs (battery lower), giving physically-impossible negative nets. The
idle draw varied 29 -> 49 W across sessions. So the paper reports whole-system J/token
only and states that the net decomposition did not reproduce.
