"""Single entry point: regenerate every table the reproduction section reports.

    python analysis.py

Reads the raw logs under logs/ and writes tables/*.md. Also runs the Arm B
throughput and the quantisation-accuracy summaries (analysis_eff.py,
analysis_quant_acc.py). Stdlib only.

Arm A accuracy uses plain `acc` and `word_perplexity`, matching the manuscript
(Section 10.3). `acc_norm` is emitted as an extra column for transparency, not used
in the mean. lm-eval writes timestamped filenames, so globs end in `*`.
"""
from __future__ import annotations
import csv, json, glob, os, runpy, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"
OUT_T = ROOT / "tables"; OUT_T.mkdir(exist_ok=True)

ZS_TASKS = ["arc_easy", "arc_challenge", "hellaswag", "winogrande", "piqa", "openbookqa", "boolq"]
SHORT = {"arc_easy": "ARCe", "arc_challenge": "ARCc", "hellaswag": "HS", "winogrande": "WG",
         "piqa": "PIQA", "openbookqa": "OBQA", "boolq": "BoolQ"}


def _latest(pattern):
    fs = sorted(LOGS.glob(pattern))
    return fs[-1] if fs else None


def arm_a():
    """Zero-shot suite + WikiText-2 word perplexity, per model."""
    keys = sorted({p.name.split("_zeroshot")[0].replace("acc_", "")
                   for p in LOGS.glob("acc_*_zeroshot_*.json")})
    rows = {}
    for key in keys:
        f = _latest(f"acc_{key}_zeroshot_*.json")
        if not f:
            continue
        res = json.loads(f.read_text()).get("results", {})
        r = {}
        accs = []
        for t in ZS_TASKS:
            v = res.get(t, {})
            a = v.get("acc,none")
            if a is not None:
                r[SHORT[t]] = round(a * 100, 2)
                accs.append(a * 100)
            an = v.get("acc_norm,none")
            if an is not None:
                r[SHORT[t] + "_norm"] = round(an * 100, 2)
        if accs:
            r["mean"] = round(statistics.mean(accs), 2)
        wf = _latest(f"acc_{key}_wikitext_*.json")
        if wf:
            wt = json.loads(wf.read_text()).get("results", {}).get("wikitext", {})
            r["word_ppl"] = round(wt.get("word_perplexity,none", 0), 2)
        # HellaSwag determinism re-run
        hf = _latest(f"acc_{key}_hellaswag_rerun_*.json")
        if hf:
            hv = json.loads(hf.read_text()).get("results", {}).get("hellaswag", {})
            if hv.get("acc,none") is not None:
                r["HS_rerun"] = round(hv["acc,none"] * 100, 2)
        rows[key] = r

    cols = [SHORT[t] for t in ZS_TASKS] + ["mean", "word_ppl", "HS_rerun"]
    lines = ["# Arm A - accuracy (plain acc; matches manuscript Section 10.3)", "",
             "| model | " + " | ".join(cols) + " |",
             "|" + "---|" * (len(cols) + 1)]
    for k, r in rows.items():
        lines.append("| " + k + " | " + " | ".join(str(r.get(c, "")) for c in cols) + " |")
    lines += ["", "acc_norm per task (not used in the mean):", ""]
    ncols = [SHORT[t] + "_norm" for t in ZS_TASKS]
    lines += ["| model | " + " | ".join(SHORT[t] for t in ZS_TASKS) + " |",
              "|" + "---|" * (len(ZS_TASKS) + 1)]
    for k, r in rows.items():
        lines.append("| " + k + " | " + " | ".join(str(r.get(c, "")) for c in ncols) + " |")
    (OUT_T / "armA-accuracy.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return rows


def main():
    a = arm_a()
    print("Arm A models:", list(a))
    for sub in ("analysis_eff.py", "analysis_quant_acc.py"):
        p = ROOT / sub
        if p.exists():
            print(f"\n--- {sub} ---")
            runpy.run_path(str(p), run_name="__main__")
    print("\nwrote tables/armA-accuracy.md (+ eff / quant-acc summaries above)")


if __name__ == "__main__":
    main()
