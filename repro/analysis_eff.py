"""Arm B analysis: parse llama-bench CSVs in logs/ into a compact efficiency table.

Emits, per model and thread count, prefill and decode tok/s (mean +/- sd across
repeats as reported by llama-bench), plus on-disk size and sampled peak working set.
No energy column: this machine has no software power source (see run_efficiency.sh).
"""
import csv, glob, json, os

HERE = os.path.dirname(__file__)
L = os.path.join(HERE, "logs")

rows = []
for f in sorted(glob.glob(os.path.join(L, "eff_*_t*.csv"))):
    tag = os.path.basename(f).replace("eff_", "").rsplit("_t", 1)[0]
    with open(f) as fh:
        for r in csv.DictReader(fh):
            if not r.get("model_type"):
                continue
            rows.append({
                "tag": tag,
                "model_type": r["model_type"],
                "size_gib": int(r["model_size"]) / 1024**3,
                "params_b": int(r["model_n_params"]) / 1e9,
                "threads": int(r["n_threads"]),
                "n_prompt": int(r["n_prompt"]),
                "n_gen": int(r["n_gen"]),
                "ts": float(r["avg_ts"]),
                "ts_sd": float(r["stddev_ts"]),
            })

def kind(r):
    if r["n_prompt"] and not r["n_gen"]:
        return f"pp{r['n_prompt']}"
    if r["n_gen"] and not r["n_prompt"]:
        return f"tg{r['n_gen']}"
    return f"pp{r['n_prompt']}+tg{r['n_gen']}"

print(f"{'model':<22} {'thr':>3} {'test':>12} {'tok/s':>12} {'+/- sd':>8}")
print("-" * 62)
for r in sorted(rows, key=lambda x: (x["tag"], x["threads"], x["n_prompt"], x["n_gen"])):
    print(f"{r['tag']:<22} {r['threads']:>3} {kind(r):>12} {r['ts']:>12.2f} {r['ts_sd']:>8.2f}")

print()
sizes = {}
for r in rows:
    sizes.setdefault(r["tag"], (r["model_type"], r["size_gib"], r["params_b"]))
for tag, (mt, gib, pb) in sorted(sizes.items()):
    rssf = os.path.join(L, f"eff_{tag}_rss.json")
    peak = ""
    if os.path.exists(rssf):
        try:
            peak = f"{json.load(open(rssf))['peak_working_set_MB']:.0f} MB peak WS"
        except Exception:
            t = open(rssf).read().strip().splitlines()
            peak = t[-1] if t else ""
    print(f"{tag:<22} {mt:<22} {gib:5.2f} GiB on disk  {pb:4.2f} B params   {peak}")

print()
for thr in (8, 16):
    d_tg, d_pp = {}, {}
    for r in rows:
        if r["threads"] != thr:
            continue
        if r["n_gen"] and not r["n_prompt"]:
            d_tg[r["tag"]] = r["ts"]
        if r["n_prompt"] == 128 and not r["n_gen"]:
            d_pp[r["tag"]] = r["ts"]
    if "bitnet_i2s" not in d_tg:
        continue
    b = d_tg["bitnet_i2s"]
    print(f"decode @ {thr} threads: bitnet_i2s {b:.1f} t/s = {1000/b:.1f} ms/token")
    for k in ("qwen_q8_0", "qwen_fp16"):
        if k in d_tg:
            print(f"   {k:<10} {d_tg[k]:.1f} t/s = {1000/d_tg[k]:.1f} ms/token   (bitnet {b/d_tg[k]:.2f}x)")
    if "bitnet_i2s" in d_pp:
        pb = d_pp["bitnet_i2s"]
        line = f"prefill128 @ {thr} threads: bitnet_i2s {pb:.1f} t/s"
        for k in ("qwen_q8_0", "qwen_fp16"):
            if k in d_pp:
                line += f" | {k} {d_pp[k]:.1f} ({pb/d_pp[k]:.2f}x)"
        print(line)
    print()
