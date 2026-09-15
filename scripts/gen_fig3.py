# -*- coding: utf-8 -*-
"""Generate figures/fig3-timeline.drawio (diagrams.net, uncompressed XML).

Field timeline 2023 -> 2026 H1, as a theme (row) x year (column) grid - a curated set
of highlights, not the full corpus (mirrors the earlier fig3-timeline.mmd selection).
Rebuild: python scripts/gen_fig3.py
Then open figures/fig3-timeline.drawio in draw.io and Export as -> PDF (Crop on) ->
figures/fig3-timeline.pdf.
"""
import os, html

os.chdir(os.path.join(os.path.dirname(__file__), ".."))

S_COLHDR = "rounded=1;whiteSpace=wrap;html=1;fillColor=#2563eb;fontColor=#ffffff;strokeColor=#1d4ed8;fontSize=12;fontStyle=1;align=center;"
S_ROWHDR = "rounded=1;whiteSpace=wrap;html=1;fillColor=#1f2937;fontColor=#ffffff;strokeColor=#111827;fontSize=10;fontStyle=1;align=center;verticalAlign=middle;"
S_CELL = "rounded=0;whiteSpace=wrap;html=1;fillColor=#f9fafb;strokeColor=#d1d5db;fontColor=#374151;fontSize=9;align=left;verticalAlign=top;spacingLeft=6;spacingTop=4;"
S_CELL_EMPTY = "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e5e7eb;fontColor=#d1d5db;fontSize=9;align=center;verticalAlign=middle;"
S_CUTOFF = "rounded=1;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#dc2626;fontColor=#7f1d1d;fontSize=9;align=center;verticalAlign=middle;dashed=1;"

cells = []


def node(cid, val, style, x, y, w, h):
    cells.append(
        f'        <mxCell id="{cid}" value="{html.escape(val)}" style="{style}" vertex="1" parent="1">\n'
        f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
        f'        </mxCell>'
    )


# ---- data: theme rows x year columns (curated highlights, not the full corpus) --------
YEARS = ["2023", "2024", "2025", "2026 H1"]

ROWS = [
    ("Foundations &\nnative training", {
        "2023": ["BitNet - BitLinear, 1-bit from scratch", "TSLD - first ternary QAT of a large generative LM"],
        "2024": ["BitNet b1.58 - ternary, FP16 parity from ~3B", "Spectra / TriLM - open ternary suite 99M-3.9B", "MatMul-free LM - removes the attention matmul", "BitNet a4.8 - 4-bit activations"],
        "2025": ["BitNet b1.58 2B4T - first open native 2B model, 4T tok", "BitNet v2 - Hadamard rotation, native A4", "LittleBit - 0.1 bits/weight"],
        "2026 H1": ["Sparse-BitNet - N:M sparsity + ternary", "Sherry - 1.25-bit packing", "NanoQuant - sub-1-bit"],
    }),
    ("Post-training routes\ntoward one bit", {
        "2023": ["PB-LLM - first LLM binarization for compression"],
        "2024": ["BiLLM (1.08-bit)", "BinaryMoS", "DB-LLM", "OneBit", "ARB-LLM", "FBI-LLM"],
        "2025": ["PTQTP", "PT2-LLM", "Tequila", "PTQ1.61", "ICQuant"],
        "2026 H1": ["HARP", "TWLA", "BWLA - first W1A6", "influence-weighted Walsh rotations"],
    }),
    ("Systems &\ninference kernels", {
        "2023": [],
        "2024": ["bitnet.cpp / 1-bit AI Infra 1.1 - CPU ternary kernels"],
        "2025": ["Spectra 1.1 TriRun - GPU ternary kernel"],
        "2026 H1": [],
    }),
    ("Hardware\naccelerators", {
        "2023": [],
        "2024": [],
        "2025": ["PIM-LLM", "BitROM", "TeLLMe", "TerEffic", "Platinum - LUT-ASIC", "T-SAR - SIMD-ISA", "Vec-LUT"],
        "2026 H1": ["TOM - compute-in-ROM"],
    }),
    ("Applications &\nextensions", {
        "2023": [],
        "2024": [],
        "2025": ["BitVLA (robotics)", "BitTTS", "one-bit ASR", "BitNet Distillation", "MoTE (ternary MoE)", "Fairy2i (real -> complex 2-bit)"],
        "2026 H1": ["Ternary Mamba", "BitNet Text Embeddings"],
    }),
    ("Theory &\nscaling analysis", {
        "2023": [],
        "2024": ["Scaling Laws for Precision", "QiD (undertrained-LLM favoring)", "theory of 1-bit NNs"],
        "2025": ["QuEST (stable W1A1)", "CAGE (curvature-aware STE)", "ParetoQ (unified 1-4 bit)"],
        "2026 H1": ["“Fitting is not enough” (smoothness)", "extreme-low-bit reasoning failure modes"],
    }),
]

# ---- geometry ---------------------------------------------------------------
XR, WR = 20, 170          # row-header column
XC0, WC = 200, 230        # first year column, column width
GAP = 6
XCUT, WCUT = XC0 + 4 * (WC + GAP), 140   # cutoff marker column
YHDR, HHDR = 20, 46       # column-header row
Y0 = YHDR + HHDR + GAP

node("corner", "theme  \\  year", S_ROWHDR, XR, YHDR, WR, HHDR)
for j, yr in enumerate(YEARS):
    node(f"col{j}", yr, S_COLHDR, XC0 + j * (WC + GAP), YHDR, WC, HHDR)
node("colcut", "cutoff", S_COLHDR.replace("#2563eb", "#dc2626").replace("#1d4ed8", "#991b1b"),
     XCUT, YHDR, WCUT, HHDR)

y = Y0
for ri, (rlabel, cols) in enumerate(ROWS):
    max_items = max(1, max(len(v) for v in cols.values()))
    h = 22 + max_items * 15
    node(f"row{ri}", rlabel, S_ROWHDR, XR, y, WR, h)
    for j, yr in enumerate(YEARS):
        items = cols.get(yr, [])
        x = XC0 + j * (WC + GAP)
        if items:
            node(f"c{ri}_{j}", "\n".join(f"• {it}" for it in items), S_CELL, x, y, WC, h)
        else:
            node(f"c{ri}_{j}", "–", S_CELL_EMPTY, x, y, WC, h)
    y += h + GAP

# one tall cutoff marker spanning all rows
node("cutoff", "Literature cutoff\n30 June 2026\n\nLater work tracked in\nthe online living appendix",
     S_CUTOFF, XCUT, Y0, WCUT, y - Y0 - GAP)

page_w = XCUT + WCUT + 40
page_h = y + 20

xml = f'''<mxfile host="app.diagrams.net" agent="claude" version="24.7.0" type="device">
  <diagram id="fig3-timeline" name="Figure 3 - Timeline">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{page_w}" pageHeight="{page_h}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
{chr(10).join(cells)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''

open("figures/fig3-timeline.drawio", "w", encoding="utf-8").write(xml)
print("wrote figures/fig3-timeline.drawio", len(xml), "bytes,", len(cells), "cells, page", page_w, "x", page_h)
