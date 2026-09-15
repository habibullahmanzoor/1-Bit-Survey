"""Arm B energy addendum: combine the battery-discharge samples with llama-bench decode
rate to get whole-system energy per token.

energy/token (J) = mean_discharge_W / decode_tokens_per_second
Also reports the net figure after subtracting the idle baseline.
"""
import csv, glob, json, os, statistics

HERE = os.path.dirname(__file__)
L = os.path.join(HERE, "logs")


def mean_mw(tag):
    f = os.path.join(L, f"energy_{tag}_samples.csv")
    vals = []
    with open(f) as fh:
        for row in csv.reader(fh):
            if len(row) == 2:
                try:
                    mw = float(row[1])
                except ValueError:
                    continue
                if mw > 0:
                    vals.append(mw)
    # drop the first 2 samples (spin-up) if we have enough
    if len(vals) > 6:
        vals = vals[2:]
    return vals


idle_lead = mean_mw("idle")
idle_trail = mean_mw("idle_post")
lead_w = statistics.mean(idle_lead) / 1000 if idle_lead else float("nan")
trail_w = statistics.mean(idle_trail) / 1000 if idle_trail else float("nan")
both = idle_lead + idle_trail
idle_w = statistics.mean(both) / 1000 if both else lead_w
print(f"idle baseline: leading {lead_w:6.2f} W (n={len(idle_lead)}), "
      f"trailing {trail_w:6.2f} W (n={len(idle_trail)}), "
      f"combined {idle_w:6.2f} W used for net")
print()

hdr = f"{'model':<12} {'decode t/s':>10} {'mean W':>8} {'net W':>8} {'J/tok (sys)':>12} {'J/tok (net)':>12}"
print(hdr)
print("-" * len(hdr))

rows = []
for bench in sorted(glob.glob(os.path.join(L, "energy_*_bench.json"))):
    tag = os.path.basename(bench)[len("energy_"):-len("_bench.json")]
    if tag in ("idle", "idle_post"):
        continue
    try:
        data = json.load(open(bench))
    except Exception:
        print(f"{tag}: no/invalid bench json"); continue
    # llama-bench json: list of result objects; take tg (n_gen>0, n_prompt==0) rows
    tg = [r for r in data if r.get("n_gen", 0) and not r.get("n_prompt", 0)]
    if not tg:
        print(f"{tag}: no tg row in bench json"); continue
    ts = statistics.mean(float(r["avg_ts"]) for r in tg)
    w = mean_mw(tag)
    load_w = statistics.mean(w) / 1000 if w else float("nan")
    net_w = load_w - idle_w
    j_sys = load_w / ts
    j_net = net_w / ts
    rows.append((tag, ts, load_w, net_w, j_sys, j_net))
    print(f"{tag:<12} {ts:>10.2f} {load_w:>8.2f} {net_w:>8.2f} {j_sys:>12.3f} {j_net:>12.3f}")

print()
d = {r[0]: r for r in rows}
if "bitnet_i2s" in d:
    b = d["bitnet_i2s"]
    for k in ("qwen_q8_0", "qwen_fp16"):
        if k in d:
            o = d[k]
            print(f"bitnet vs {k}: J/tok(sys) {b[4]/o[4]:.2f}x   J/tok(net) {b[5]/o[5]:.2f}x")
