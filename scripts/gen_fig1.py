# -*- coding: utf-8 -*-
"""Generate figures/fig1-taxonomy.drawio (diagrams.net, uncompressed XML).

Per-axis counts are derived from data/inventory.csv so the figure stays in sync
with the corpus. Rebuild:  python scripts/gen_fig1.py
Then open figures/fig1-taxonomy.drawio in draw.io and Export as -> PDF (Crop on).
"""
import csv, collections, html, os

os.chdir(os.path.join(os.path.dirname(__file__), ".."))
rows = list(csv.DictReader(open("data/inventory.csv", encoding="utf-8")))
N = len(rows)


def c(col):
    return collections.Counter(r[col].strip() for r in rows)


wr = c("weight_repr")
pa = c("paradigm")
sl = c("systems_layers")
md = c("modality")

# Axis 5 partition (matches the prose in section 4.5): algorithm-only / +kernel / +hardware / n-a
kernel_ct = sum(v for k, v in sl.items() if "kernel" in k)   # any work contributing a kernel
hw_only_ct = sl.get("hardware", 0)                           # dedicated-hardware papers
coae_ct = sl.get("algo+kernel+hw", 0)                        # full algo+kernel+hw co-design
na_sys = sl.get("NA", 0)

# modality roll-up
text_dec = md.get("text-decoder", 0)
sys_m = md.get("systems", 0) + md.get("edge-systems", 0)
theory_m = (md.get("theory", 0) + md.get("analysis", 0) + md.get("survey", 0)
            + md.get("theory/text-decoder", 0) + md.get("analysis-security", 0))
vlm_m = md.get("VLM", 0) + md.get("VLA", 0) + md.get("VLM/MoE", 0)
emb_speech = md.get("embedding", 0) + md.get("TTS", 0) + md.get("ASR", 0)
ssm_m = md.get("SSM", 0)
other_m = N - (text_dec + sys_m + theory_m + vlm_m + emb_speech + ssm_m)

pa_other = N - pa['native-scratch'] - pa['continual-QAT'] - pa['QAT-finetune'] - pa['PTQ']
c3_w = sum(1 for r in rows if r['components'].strip() in ('W', 'W-experts', 'W+sparsify'))
c3_wa = sum(1 for r in rows if r['components'].strip().startswith('W+A'))
c3_as = sum(1 for r in rows if r['components'].strip() == 'A-sparsify')
c3_na = sum(1 for r in rows if r['components'].strip() == 'NA')
print(f"N={N}  ternary={wr['ternary']} binary={wr['binary']} mixed={wr['mixed-partial']} n/a={wr['n/a']}  "
      f"[sum {wr['ternary']+wr['binary']+wr['mixed-partial']+wr['n/a']}]")
print(f"paradigm: native={pa['native-scratch']} continual={pa['continual-QAT']} qat-ft={pa['QAT-finetune']} "
      f"ptq={pa['PTQ']} not-a-method={pa_other}  [sum {pa['native-scratch']+pa['continual-QAT']+pa['QAT-finetune']+pa['PTQ']+pa_other}]")
print(f"components: w-only={c3_w} w+a={c3_wa} act-only={c3_as} n/a={c3_na}  [sum {c3_w+c3_wa+c3_as+c3_na}]")
print(f"systems: algo-only={sl['algorithm']} +kernel={kernel_ct} hw-only={hw_only_ct} n/a={na_sys}  "
      f"[sum {sl['algorithm']+kernel_ct+hw_only_ct+na_sys}]")
print(f"modality: text={text_dec} sys={sys_m} theory={theory_m} vlm={vlm_m} emb+speech={emb_speech} "
      f"ssm={ssm_m} other={other_m}  [sum {text_dec+sys_m+theory_m+vlm_m+emb_speech+ssm_m+other_m}]")

# --------------------------------------------------------------------------- styles
# fontSize 15 / strokeWidth 3 across nodes, to match the rest of the figure set.
S_ROOT = "rounded=1;whiteSpace=wrap;html=1;fillColor=#1f2937;fontColor=#ffffff;strokeColor=#111827;fontSize=15;strokeWidth=3;fontStyle=1;"
S_AXIS = "rounded=1;whiteSpace=wrap;html=1;fillColor=#2563eb;fontColor=#ffffff;strokeColor=#1d4ed8;fontSize=15;strokeWidth=3;fontStyle=1;"
S_SEC = "rounded=1;whiteSpace=wrap;html=1;fillColor=#6b7280;fontColor=#ffffff;strokeColor=#4b5563;fontSize=15;strokeWidth=3;fontStyle=1;dashed=1;"
S_LEAF = "rounded=1;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#2563eb;fontSize=15;strokeWidth=3;align=left;spacingLeft=8;"
S_SLEAF = "rounded=1;whiteSpace=wrap;html=1;fillColor=#f9fafb;strokeColor=#9ca3af;fontSize=15;strokeWidth=3;align=left;spacingLeft=8;fontColor=#374151;"
S_LEAF_G = "rounded=1;whiteSpace=wrap;html=1;fillColor=#f3f4f6;strokeColor=#6b7280;fontSize=15;strokeWidth=3;align=left;spacingLeft=8;"
S_BADGE = "shape=note;whiteSpace=wrap;html=1;fillColor=#fef9c3;strokeColor=#ca8a04;fontSize=15;strokeWidth=3;align=left;spacingLeft=6;size=10;"
S_EDGE = "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=none;strokeColor=#9ca3af;exitX=1;exitY=0.5;entryX=0;entryY=0.5;"
S_EDGE_D = S_EDGE + "dashed=1;"
S_TITLE = "text;html=1;align=left;verticalAlign=middle;fontSize=11;fontColor=#6b7280;"

cells = []


def node(cid, val, style, x, y, w, h):
    cells.append(
        f'        <mxCell id="{cid}" value="{html.escape(val)}" style="{style}" vertex="1" parent="1">\n'
        f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
        f'        </mxCell>'
    )


def edge(cid, src, tgt, style=S_EDGE):
    cells.append(
        f'        <mxCell id="{cid}" style="{style}" edge="1" parent="1" source="{src}" target="{tgt}">\n'
        f'          <mxGeometry relative="1" as="geometry" />\n'
        f'        </mxCell>'
    )


# geometry columns
XA, WA = 300, 230          # axis column
XL, WL = 600, 360          # leaf column
XS, WS = 1000, 340         # sub-leaf column
HL, PITCH = 30, 44         # leaf height / vertical pitch

# ---- data: (axis label, [(leaf text, [subleaf texts])]) --------------------
axes = [
    ("1  Weight representation", [
        (f"ternary  {{-1, 0, +1}}   n = {wr['ternary']}", []),
        (f"binary  {{-1, +1}}   n = {wr['binary']}", []),
        (f"mixed / partial   n = {wr['mixed-partial']}", [
            "salient-column split  (BiLLM, PB-LLM, PTQ1.61)",
            "residual / low-rank factor branch  (RaBiT, pQuant)",
            "complex  {±1, ±i}  (iFairy, Fairy2i)",
        ]),
        (f"not applicable  (kernels, accelerators, theory, surveys)   n = "
         f"{N - wr['ternary'] - wr['binary'] - wr['mixed-partial']}", []),
    ]),
    ("2  Training paradigm", [
        (f"native, from scratch   n = {pa['native-scratch']}", []),
        (f"continual QAT  (FP → 1.58-bit)   n = {pa['continual-QAT']}", []),
        (f"QAT fine-tune / short continued train   n = {pa['QAT-finetune']}", []),
        (f"post-training quantization  (calibration only)   n = {pa['PTQ']}", []),
        (f"not a training method  (systems, analysis, surveys)   n = "
         f"{N - pa['native-scratch'] - pa['continual-QAT'] - pa['QAT-finetune'] - pa['PTQ']}", []),
    ]),
    ("3  Components quantized", [
        (f"weights only   n = {sum(1 for r in rows if r['components'].strip() in ('W', 'W-experts', 'W+sparsify'))}", []),
        (f"weights + activations   n = {sum(1 for r in rows if r['components'].strip().startswith('W+A'))}", []),
        (f"activations only  (sparsification)   n = {sum(1 for r in rows if r['components'].strip() == 'A-sparsify')}", []),
        (f"not applicable  (no model of its own)   n = {sum(1 for r in rows if r['components'].strip() == 'NA')}", []),
        ("subset: + 3-bit KV cache   n = 2", []),
    ]),
    ("4  Optimization mechanism", [
        ("scaled STE + minor variants  (absmean / absmax / median)   ~20", []),
        ("STE as object of study: curvature / trust-region / zeroth-order   ~6", []),
        ("distillation-driven  (logit, attention, feature, autoregressive)   ~13", []),
        ("reconstruction / calibration PTQ  (salient weights, Hessian)   ~16", []),
        ("rotation / incoherence  (Hadamard, butterfly, Walsh)   ~7", []),
        ("decomposition / factorization  (low-rank, binary factors)   ~10", []),
        ("stochastic rounding, no STE, no shadow weight   1", []),
        ("sparsity-coupled  (N:M, top-K, 3:4)   ~5", []),
    ]),
    ("5  Systems stack", [
        (f"algorithm only   n = {sl['algorithm']}", []),
        (f"+ custom kernel  (I2_S, TL1 / TL2, fused, GPU)   n = {kernel_ct}", []),
        (f"+ custom hardware  (LUT-ASIC, compute-in-ROM, PIM, FPGA)   n = {hw_only_ct}", []),
        (f"not applicable  (surveys)   n = {na_sys}", []),
    ]),
]

sec_axis = ("Secondary cut:  modality / use", [
    f"text-decoder LLM   n = {text_dec}",
    f"inference systems, kernels, hardware   n = {sys_m}",
    f"theory, analysis, surveys   n = {theory_m}",
    f"VLM / VLA / MoE   n = {vlm_m}",
    f"embedding + speech  (ASR, TTS)   n = {emb_speech}",
    f"state-space / Mamba   n = {ssm_m}",
    f"other  (vision, encoder, security, misc)   n = {other_m}",
])

# ---- lay out -------------------------------------------------------------------
# (no in-canvas title: the LaTeX \caption on the figure float supplies it, so the
#  exported crop is just the diagram)
y = 40
axis_ids = []
leaf_rows = []
sub_rows = []
for ai, (alabel, leaves) in enumerate(axes):
    lids = []
    direct_ys = []
    for li, (ltext, subs) in enumerate(leaves):
        lid = f"a{ai}l{li}"
        leaf_rows.append((lid, S_LEAF, ltext, y))
        lids.append(lid)
        direct_ys.append(y)
        if subs:
            sy = y
            for si, stext in enumerate(subs):
                sub_rows.append((f"{lid}s{si}", stext, sy, lid))
                sy += PITCH - 4
            y = max(sy, y + PITCH)
        else:
            y += PITCH
    aid = f"axis{ai}"
    axis_cy = (direct_ys[0] + direct_ys[-1] + HL) / 2 - 22  # centre on direct leaves only
    axis_ids.append((aid, alabel, axis_cy, lids))
    y += 34

sec_top = y
sec_lids = []
for si, stext in enumerate(sec_axis[1]):
    sid = f"secl{si}"
    leaf_rows.append((sid, S_LEAF_G, stext, y))
    sec_lids.append(sid)
    y += PITCH
sec_bot = y

total_h = y + 40
root_y = 70 + (total_h - 70) / 2 - 30

node("root", f"Native 1-bit / 1.58-bit LLMs\n(n = {N})", S_ROOT, 40, root_y, 200, 64)

for aid, alabel, ay, lids in axis_ids:
    node(aid, alabel, S_AXIS, XA, ay, WA, 44)
    edge(f"e-root-{aid}", "root", aid)
    for lid in lids:
        edge(f"e-{aid}-{lid}", aid, lid)

node("secaxis", sec_axis[0], S_SEC, XA, (sec_top + sec_bot) / 2 - 22, WA, 44)
edge("e-root-sec", "root", "secaxis", S_EDGE_D)
for lid in sec_lids:
    edge(f"e-sec-{lid}", "secaxis", lid, S_EDGE_D)

for lid, style, text, ly in leaf_rows:
    node(lid, text, style, XL, ly, WL, HL)

for sid, text, sy, parent in sub_rows:
    node(sid, text, S_SLEAF, XS, sy, WS, HL - 2)
    edge(f"e-{parent}-{sid}", parent, sid)

badge_y = axis_ids[4][2] + 60
node("badge5", f"{coae_ct} works co-design all three layers\n(algorithm + kernel + hardware)", S_BADGE, XA - 6, badge_y, WA + 12, 44)
edge("e-axis4-badge5", "axis4", "badge5", S_EDGE + "dashed=1;")

lg_y = total_h - 4
node("lg1", "primary axis  (all works classified)", S_AXIS, 40, lg_y, 250, 26)
node("lg2", "secondary cut  (modality)", S_SEC, 310, lg_y, 210, 26)

page_w = XS + WS + 60
page_h = int(total_h + 60)

xml = f'''<mxfile host="app.diagrams.net" agent="claude" version="24.7.0" type="device">
  <diagram id="fig1-taxonomy" name="Figure 1 - Taxonomy">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{page_w}" pageHeight="{page_h}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
{chr(10).join(cells)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''

open("figures/fig1-taxonomy.drawio", "w", encoding="utf-8").write(xml)
print("wrote figures/fig1-taxonomy.drawio", len(xml), "bytes,", len(cells), "cells, page", page_w, "x", page_h)
