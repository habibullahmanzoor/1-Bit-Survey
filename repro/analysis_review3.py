"""Summarise the review-round-3 accuracy experiments.

Controlled ternary-vs-FP16 pairs (matched model / tokenizer / data):
    falcon3-1b-158  vs  falcon3-1b-bf16     (Falcon3-1B, QAT-to-1.58bit vs bf16)
    trilm-2.4b      vs  floatlm-2.4b        (Spectra, native ternary vs FP16, 300B tok)
4-bit accuracy on the full suite:
    qwen-nf4        vs  qwen2.5-1.5b (Arm A, bf16)
Plus MMLU 0-shot for every model that has it.

Reads logs/acc_<key>_{zeroshot,wikitext,mmlu0}*.json (latest timestamp per key). Stdlib only.
"""
import csv, glob, json, os, statistics

L = os.path.join(os.path.dirname(__file__), "logs")
ZS = ["arc_easy", "arc_challenge", "hellaswag", "winogrande", "piqa", "openbookqa", "boolq"]
SHORT = {"arc_easy": "ARCe", "arc_challenge": "ARCc", "hellaswag": "HS", "winogrande": "WG",
         "piqa": "PIQA", "openbookqa": "OBQA", "boolq": "BoolQ"}


def latest(pat):
    fs = sorted(glob.glob(os.path.join(L, pat)))
    return fs[-1] if fs else None


def zs(key):
    f = latest(f"acc_{key}_zeroshot*.json")
    if not f:
        return None
    r = json.loads(open(f, encoding="utf-8").read()).get("results", {})
    out = {}
    accs = []
    for t in ZS:
        v = r.get(t, {})
        a = v.get("acc,none")
        if a is not None:
            out[SHORT[t]] = round(a * 100, 1)
            accs.append(a * 100)
        an = v.get("acc_norm,none")
        if an is not None:
            out[SHORT[t] + "n"] = round(an * 100, 1)
    if accs:
        out["mean"] = round(statistics.mean(accs), 2)
    return out


def wt(key):
    f = latest(f"acc_{key}_wikitext*.json")
    if not f:
        return None
    return round(json.loads(open(f, encoding="utf-8").read())["results"]["wikitext"]["word_perplexity,none"], 2)


def mmlu(key):
    f = latest(f"acc_{key}_mmlu0*.json")
    if not f:
        return None
    r = json.loads(open(f, encoding="utf-8").read()).get("results", {})
    m = r.get("mmlu", {})
    a = m.get("acc,none")
    return round(a * 100, 2) if a is not None else None


KEYS = ["bitnet-2b4t", "qwen2.5-1.5b", "qwen-nf4",
        "falcon3-1b-158", "falcon3-1b-bf16", "trilm-2.4b", "floatlm-2.4b"]

print(f"{'model':<18} " + " ".join(f"{SHORT[t]:>5}" for t in ZS) + f" {'mean':>6} {'wtppl':>7} {'MMLU0':>6}")
print("-" * 88)
rows = {}
for k in KEYS:
    z = zs(k) or {}
    rows[k] = z
    line = f"{k:<18} " + " ".join(f"{z.get(SHORT[t], ''):>5}" for t in ZS)
    line += f" {z.get('mean', ''):>6} {str(wt(k) or ''):>7} {str(mmlu(k) or ''):>6}"
    print(line)

print()
def gap(a, b, label):
    ra, rb = rows.get(a, {}), rows.get(b, {})
    if "mean" in ra and "mean" in rb:
        print(f"{label}: mean {ra['mean']:.2f} (ternary/4bit) vs {rb['mean']:.2f} (FP)  "
              f"-> {ra['mean']-rb['mean']:+.2f} pp;  wtppl {wt(a)} vs {wt(b)}")
    if mmlu(a) and mmlu(b):
        print(f"    MMLU0 {mmlu(a):.2f} vs {mmlu(b):.2f}  -> {mmlu(a)-mmlu(b):+.2f} pp")

gap("falcon3-1b-158", "falcon3-1b-bf16", "Falcon3-1B  1.58bit vs bf16 (controlled)")
gap("trilm-2.4b", "floatlm-2.4b", "Spectra 2.4B TriLM vs FloatLM (controlled, native)")
gap("qwen-nf4", "qwen2.5-1.5b", "Qwen2.5-1.5B  nf4-4bit vs bf16 (controlled)")
