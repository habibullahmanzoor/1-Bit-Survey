"""Parse the GSM8K sweep JSONs into one table (5-shot, generative, chat template
for the instruct models; Spectra base models run template-free)."""
import glob, json, os

HERE = os.path.dirname(__file__)
L = os.path.join(HERE, "logs")

NAMES = {
    "bitnet-2b4t": "BitNet b1.58 2B4T",
    "qwen2.5-1.5b": "Qwen2.5-1.5B-Instruct (bf16)",
    "qwen-nf4": "Qwen2.5-1.5B-Instruct (nf4)",
    "falcon3-1b-bf16": "Falcon3-1B-Instruct (bf16)",
    "falcon3-1b-158": "Falcon3-1B-Instruct-1.58bit",
    "trilm-2.4b": "Spectra TriLM 2.4B (no template)",
    "floatlm-2.4b": "Spectra FloatLM 2.4B (no template)",
}
ORDER = ["bitnet-2b4t", "qwen2.5-1.5b", "qwen-nf4",
         "falcon3-1b-bf16", "falcon3-1b-158", "trilm-2.4b", "floatlm-2.4b"]

rows = {}
for f in glob.glob(os.path.join(L, "gsm8k_*.json")):
    base = os.path.basename(f)
    key = base[len("gsm8k_"):].split("_2026")[0]
    d = json.load(open(f, encoding="utf-8"))
    r = d["results"]["gsm8k"]
    rows[key] = {
        "flex": r.get("exact_match,flexible-extract"),
        "flex_se": r.get("exact_match_stderr,flexible-extract"),
        "strict": r.get("exact_match,strict-match"),
        "strict_se": r.get("exact_match_stderr,strict-match"),
    }

print(f"{'model':<34}{'flexible-extract':>18}{'strict-match':>16}")
print("-" * 68)
for k in ORDER:
    if k not in rows:
        print(f"{NAMES[k]:<34}{'(missing)':>18}")
        continue
    v = rows[k]
    print(f"{NAMES[k]:<34}{v['flex']*100:>10.1f} ({v['flex_se']*100:.1f}){v['strict']*100:>9.1f} ({v['strict_se']*100:.1f})")

print()
print("Vendor card (Ma2025-BitNet2B4T): BitNet GSM8K 58.38, Qwen2.5-1.5B GSM8K 56.79")
if "bitnet-2b4t" in rows and "qwen2.5-1.5b" in rows:
    b, q = rows["bitnet-2b4t"], rows["qwen2.5-1.5b"]
    print(f"BitNet - Qwen (flexible): {(b['flex']-q['flex'])*100:+.1f} pt   (strict): {(b['strict']-q['strict'])*100:+.1f} pt")
for pair, hi, lo in [("Falcon3-1B", "falcon3-1b-bf16", "falcon3-1b-158"),
                     ("Qwen nf4 vs bf16", "qwen2.5-1.5b", "qwen-nf4"),
                     ("Spectra", "floatlm-2.4b", "trilm-2.4b")]:
    if hi in rows and lo in rows:
        dh, dl = rows[hi], rows[lo]
        print(f"{pair}: flex {dl['flex']*100:.1f} vs {dh['flex']*100:.1f} "
              f"(delta {(dl['flex']-dh['flex'])*100:+.1f})   "
              f"strict {dl['strict']*100:.1f} vs {dh['strict']*100:.1f} "
              f"(delta {(dl['strict']-dh['strict'])*100:+.1f})")
