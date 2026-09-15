"""Parse llama-perplexity output for the quant-accuracy addendum.

WikiText-2 word perplexity + HellaSwag accuracy for FP16 / Q8_0 / Q4_K_M of the same
Qwen2.5-1.5B checkpoint (isolates quantisation loss), plus BitNet i2_s as a cross-check.
`bitnet_i2s` is the runtime as built (wrong FFN activation, issue #588); `bitnet_i2s_FIXED`
is the same GGUF through the one-line LLM_FFN_RELU_SQR patch (Section 10.3).
"""
import glob, os, re

HERE = os.path.dirname(__file__)
L = os.path.join(HERE, "logs")
ORDER = ["qwen_fp16", "qwen_q8_0", "qwen_q4_k_m", "bitnet_i2s", "bitnet_i2s_FIXED"]


def wikitext_ppl(tag):
    # "Final estimate: PPL = X +/- Y" is printed to stderr by llama-perplexity
    for ext in (".err", ".txt"):
        f = os.path.join(L, f"qacc_{tag}_wikitext{ext}")
        if not os.path.exists(f):
            continue
        txt = open(f, encoding="utf-8", errors="ignore").read()
        m = re.search(r"Final estimate:\s*PPL\s*=\s*([\d.]+)\s*\+/-\s*([\d.]+)", txt)
        if m:
            return float(m.group(1)), float(m.group(2))
    return None


def hellaswag_acc(tag):
    f = os.path.join(L, f"qacc_{tag}_hellaswag.txt")
    if not os.path.exists(f):
        return None
    txt = open(f, encoding="utf-8", errors="ignore").read()
    # rows are:  "<n>\t<acc>%\t[lo%, hi%]"  -- take the last
    rows = re.findall(r"^\s*(\d+)\s+([\d.]+)%\s+\[([\d.]+)%,\s*([\d.]+)%\]", txt, re.M)
    if not rows:
        return None
    n, acc, lo, hi = rows[-1]
    return int(n), float(acc), float(lo), float(hi)


print(f"{'model':<13} {'WikiText-2 ppl':>18} {'HellaSwag acc (n)':>26}")
print("-" * 60)
ref_ppl = None
for tag in ORDER:
    p = wikitext_ppl(tag)
    h = hellaswag_acc(tag)
    pstr = f"{p[0]:.3f} +/- {p[1]:.3f}" if p else "-"
    hstr = f"{h[1]:.2f}%  ({h[0]}; [{h[2]:.1f}, {h[3]:.1f}])" if h else "-"
    print(f"{tag:<13} {pstr:>18} {hstr:>26}")

print()
p_f16 = wikitext_ppl("qwen_fp16")
p_q8 = wikitext_ppl("qwen_q8_0")
p_q4 = wikitext_ppl("qwen_q4_k_m")
if p_f16 and p_q4:
    print(f"Qwen quantisation ppl delta vs FP16:  "
          f"Q8_0 {p_q8[0]-p_f16[0]:+.3f} ({100*(p_q8[0]/p_f16[0]-1):+.1f}%),  "
          f"Q4_K_M {p_q4[0]-p_f16[0]:+.3f} ({100*(p_q4[0]/p_f16[0]-1):+.1f}%)")
h_f16 = hellaswag_acc("qwen_fp16")
h_q8 = hellaswag_acc("qwen_q8_0")
h_q4 = hellaswag_acc("qwen_q4_k_m")
if h_f16 and h_q4:
    print(f"Qwen quantisation HellaSwag delta vs FP16:  "
          f"Q8_0 {h_q8[1]-h_f16[1]:+.2f} pp,  Q4_K_M {h_q4[1]-h_f16[1]:+.2f} pp")

p_bn, p_bnf = wikitext_ppl("bitnet_i2s"), wikitext_ppl("bitnet_i2s_FIXED")
h_bn, h_bnf = hellaswag_acc("bitnet_i2s"), hellaswag_acc("bitnet_i2s_FIXED")
if p_bn and p_bnf:
    print(f"\nBitNet FFN-activation patch (issue #588):  "
          f"WikiText-2 ppl {p_bn[0]:.2f} -> {p_bnf[0]:.2f},  "
          f"HellaSwag {h_bn[1]:.1f}% -> {h_bnf[1]:.1f}%")
