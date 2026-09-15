"""Consolidate the three battery energy sessions.

run1  = logs/energy_run1_3model/        (Sep 6; idle 29 W; no Q4_K_M)
run2  = logs/energy_run2_contaminated/  (today; leading-only idle contaminated by unplug transient)
run3  = logs/energy_run3_batterydrain/  (today; REP=3; dual idle; battery draining -> power cap fell)

Whole-system J/tok = mean_discharge_W / decode_tok_per_s is the robust metric.
The idle-subtracted "net" is reported for run1 only; runs 2-3 could not produce a
stable idle baseline (see the printout).
"""
import csv, glob, json, os, statistics

HERE = os.path.dirname(__file__)


def samples_w(path):
    vals = []
    try:
        with open(path) as fh:
            for row in csv.reader(fh):
                if len(row) == 2:
                    try:
                        mw = float(row[1])
                    except ValueError:
                        continue
                    if mw > 0:
                        vals.append(mw / 1000.0)
    except FileNotFoundError:
        return []
    return vals[2:] if len(vals) > 6 else vals


def decode_ts(path):
    try:
        d = json.load(open(path))
    except Exception:
        return None
    tg = [r for r in d if r.get("n_gen", 0) and not r.get("n_prompt", 0)]
    if not tg:
        return None
    return statistics.mean(float(r["avg_ts"]) for r in tg)


RUNS = [
    ("run1 (Sep 6, idle 29W, no Q4)", "logs/energy_run1_3model"),
    ("run2 (today, idle contaminated)", "logs/energy_run2_contaminated"),
    ("run3 (today, REP=3, battery draining)", "logs/energy_run3_batterydrain"),
]
MODELS = [("bitnet_i2s", "BitNet I2_S"), ("qwen_q4_k_m", "Qwen Q4_K_M"),
          ("qwen_q8_0", "Qwen Q8_0"), ("qwen_fp16", "Qwen FP16")]

for label, d in RUNS:
    base = os.path.join(HERE, d)
    il = samples_w(os.path.join(base, "energy_idle_samples.csv"))
    it = samples_w(os.path.join(base, "energy_idle_post_samples.csv"))
    idle_lead = statistics.mean(il) if il else float("nan")
    idle_trail = statistics.mean(it) if it else None
    print(f"\n=== {label} ===")
    if idle_trail is not None:
        print(f"idle: leading {idle_lead:.2f} W, trailing {idle_trail:.2f} W")
    else:
        print(f"idle: {idle_lead:.2f} W (leading only)")
    print(f"{'model':<14}{'t/s':>8}{'mean W':>9}{'J/tok sys':>11}")
    js = {}
    for tag, name in MODELS:
        ts = decode_ts(os.path.join(base, f"energy_{tag}_bench.json"))
        w = samples_w(os.path.join(base, f"energy_{tag}_samples.csv"))
        if ts is None or not w:
            print(f"{name:<14}{'--':>8}")
            continue
        mw = statistics.mean(w)
        j = mw / ts
        js[tag] = j
        print(f"{name:<14}{ts:>8.2f}{mw:>9.2f}{j:>11.3f}")
    if "bitnet_i2s" in js:
        b = js["bitnet_i2s"]
        r = lambda k: f"{b / js[k]:.2f}x" if k in js else "--"
        print(f"  BitNet : Q4_K_M {r('qwen_q4_k_m')}   "
              f": Q8_0 {r('qwen_q8_0')}   : FP16 {r('qwen_fp16')}")
