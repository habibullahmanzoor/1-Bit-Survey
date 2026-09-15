# -*- coding: utf-8 -*-
"""Generate figures/fig5-efficiency.drawio (diagrams.net, uncompressed XML).

Independent efficiency re-evaluation (Section 10.4): four small-multiple bar charts
(decode tok/s, prefill tok/s, disk GiB, peak RAM GB) plus a decode-vs-RAM Pareto
scatter, for the released BitNet b1.58 2B4T I2_S checkpoint against Qwen2.5-1.5B at
Q4_K_M, Q8_0, and FP16. Numbers are Table tab:efficiency (draft/09-reproduction.md).
Rebuild: python scripts/gen_fig5.py
Then open figures/fig5-efficiency.drawio in draw.io and Export as -> PDF (Crop on) ->
figures/fig5-efficiency.pdf.
"""
import os, html

os.chdir(os.path.join(os.path.dirname(__file__), ".."))

# ---- palette: matches the bnAccent / q4Blue / q8Blue / f16Blue used in the paper's
# other efficiency exhibits, so this figure reads as the same study.
BN_COLOR, Q4_COLOR, Q8_COLOR, F16_COLOR = "#D95F0E", "#2166AC", "#6BAED6", "#C6DBEF"
ORDER = ["BN", "Q4", "Q8", "F16"]
COLORS = {"BN": BN_COLOR, "Q4": Q4_COLOR, "Q8": Q8_COLOR, "F16": F16_COLOR}

S_PANEL_BG = "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#94a3b8;fontColor=#f8fafc;fontSize=1;verticalAlign=top;strokeWidth=2;"
S_TITLE = "text;html=1;align=left;verticalAlign=middle;fontSize=12;fontColor=#0f172a;fontStyle=1;"
S_GRID = "rounded=0;whiteSpace=wrap;html=1;fillColor=#e1e0d9;strokeColor=none;"
S_AXIS = "rounded=0;whiteSpace=wrap;html=1;fillColor=#94a3b8;strokeColor=none;"
S_YTICK = "text;html=1;align=right;verticalAlign=middle;fontSize=8;fontColor=#898781;"
S_XTICK = "text;html=1;align=center;verticalAlign=middle;fontSize=8;fontColor=#898781;"
S_VALLABEL = "text;html=1;align=center;verticalAlign=bottom;fontSize=9;fontColor=#0f172a;fontStyle=1;"
S_CATLABEL = "text;html=1;align=center;verticalAlign=top;fontSize=9;fontColor=#52514e;fontStyle=1;"
S_SUBNOTE = "text;html=1;align=left;verticalAlign=top;fontSize=9;fontColor=#52514e;fontStyle=2;"
S_AXISNAME = "text;html=1;align=center;verticalAlign=middle;fontSize=9;fontColor=#52514e;"


def bar_style(hexcolor):
    return f"rounded=0;whiteSpace=wrap;html=1;fillColor={hexcolor};strokeColor=#334155;strokeWidth=1;"


def dot_style(hexcolor):
    return f"ellipse;whiteSpace=wrap;html=1;fillColor={hexcolor};strokeColor=#334155;strokeWidth=1.2;"


cells = []


def node(cid, val, style, x, y, w, h, extra=""):
    cells.append(
        f'        <mxCell id="{cid}" value="{html.escape(val)}" style="{style}{extra}" vertex="1" parent="1">\n'
        f'          <mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry" />\n'
        f'        </mxCell>'
    )


# ============================================================ one small-multiple bar panel
def bar_panel(pid, px, py, title, values, ymax, yticks, fmt):
    PW, PH = 290, 232
    node(f"{pid}_bg", "", S_PANEL_BG, px, py, PW, PH)
    node(f"{pid}_ttl", title, S_TITLE, px + 10, py + 6, PW - 20, 18)

    chart_x0, chart_y0 = px + 40, py + 32
    chart_w, chart_h = PW - 56, 150
    baseline_y = chart_y0 + chart_h

    for t in yticks:
        gy = baseline_y - (t / ymax) * chart_h
        node(f"{pid}_gl{t}", "", S_GRID, chart_x0, gy, chart_w, 1)
        node(f"{pid}_yl{t}", fmt(t), S_YTICK, px + 2, gy - 7, 34, 14)
    node(f"{pid}_axis", "", S_AXIS, chart_x0, baseline_y, chart_w, 1.5)

    n = len(ORDER)
    bw, gap = 32, 16
    bars_w = n * bw + (n - 1) * gap
    start_x = chart_x0 + (chart_w - bars_w) / 2
    for i, label in enumerate(ORDER):
        v = values[label]
        bh = max(2.0, (v / ymax) * chart_h)
        bx = start_x + i * (bw + gap)
        by = baseline_y - bh
        node(f"{pid}_bar{i}", "", bar_style(COLORS[label]), bx, by, bw, bh)
        node(f"{pid}_val{i}", fmt(v), S_VALLABEL, bx - 10, by - 15, bw + 20, 14)
        node(f"{pid}_cat{i}", label, S_CATLABEL, bx - 10, baseline_y + 4, bw + 20, 14)
    return px + PW, py + PH


def fmt1(v):
    return f"{v:g}"


# ============================================================ Pareto scatter panel
def scatter_panel(pid, px, py, pw, points, xmin, xmax, xticks, ymin, ymax, yticks, labels_anchor):
    PH = 300
    node(f"{pid}_bg", "", S_PANEL_BG, px, py, pw, PH)
    node(f"{pid}_ttl", "decode throughput vs. peak resident memory", S_TITLE, px + 10, py + 6, pw - 20, 18)

    chart_x0, chart_y0 = px + 60, py + 34
    chart_w, chart_h = pw - 100, 190
    baseline_y = chart_y0 + chart_h

    def X(v):
        return chart_x0 + (v - xmin) / (xmax - xmin) * chart_w

    def Y(v):  # smaller v (lower RAM) plots higher on the panel
        return chart_y0 + (v - ymin) / (ymax - ymin) * chart_h

    for t in yticks:
        gy = Y(t)
        node(f"{pid}_ygl{t}", "", S_GRID, chart_x0, gy, chart_w, 1)
        node(f"{pid}_yl{t}", f"{t:g}", S_YTICK, px + 2, gy - 7, 50, 14)
    for t in xticks:
        gx = X(t)
        node(f"{pid}_xgl{t}", "", S_GRID, gx, chart_y0, 1, chart_h)
        node(f"{pid}_xl{t}", f"{t:g}", S_XTICK, gx - 15, baseline_y + 4, 30, 14)
    node(f"{pid}_axisL", "", S_AXIS, chart_x0, chart_y0, 1.5, chart_h)
    node(f"{pid}_axisB", "", S_AXIS, chart_x0, baseline_y, chart_w, 1.5)

    r = 9
    for label, (xv, yv) in points.items():
        cx, cy = X(xv), Y(yv)
        node(f"{pid}_pt_{label}", "", dot_style(COLORS[label]), cx - r / 2, cy - r / 2, r, r)
        anchor = labels_anchor[label]
        ly = cy - 20 if anchor == "above" else cy + 8
        node(f"{pid}_lb_{label}", label, S_VALLABEL, cx - 20, ly, 40, 14)

    node(f"{pid}_xname", "decode tok/s  (higher is better)", S_AXISNAME, chart_x0, baseline_y + 20, chart_w, 14)
    node(f"{pid}_yname", "peak RAM, GB<br>(lower is better)", S_AXISNAME, px + 2, chart_y0 - 6, 48, chart_h + 12,
         extra="rotation=270;")
    return px + pw, py + PH


# ---- data (Table tab:efficiency, draft/09-reproduction.md) -----------------------
DECODE = {"BN": 28.6, "Q4": 33.8, "Q8": 24.1, "F16": 14.4}
PREFILL = {"BN": 108.9, "Q4": 107.6, "Q8": 72.4, "F16": 70.9}
DISK = {"BN": 1.10, "Q4": 1.04, "Q8": 1.76, "F16": 3.31}
RAM = {"BN": 1.22, "Q4": 1.60, "Q8": 1.64, "F16": 3.02}

# ---- layout: a row of four bar panels, then the scatter panel below --------------
PX, GAP = 20, 20
y = 20
x = PX
x, _ = bar_panel("p1", x, y, "decode tok/s", DECODE, 40, [0, 10, 20, 30, 40], fmt1)
x += GAP
x, _ = bar_panel("p2", x, y, "prefill tok/s", PREFILL, 130, [0, 50, 100], fmt1)
x += GAP
x, _ = bar_panel("p3", x, y, "disk (GiB)", DISK, 3.6, [0, 1, 2, 3], fmt1)
x += GAP
x, y_bottom = bar_panel("p4", x, y, "peak RAM (GB)", RAM, 3.6, [0, 1, 2, 3], fmt1)

row_w = x - PX
y2 = y_bottom + 30
points = {"BN": (28.6, 1.22), "Q4": (33.8, 1.60), "Q8": (24.1, 1.64), "F16": (14.4, 3.02)}
anchors = {"BN": "above", "Q4": "below", "Q8": "above", "F16": "below"}
_, y3 = scatter_panel("sc", PX, y2, row_w, points, 12, 38, [15, 20, 25, 30, 35], 0.9, 3.4, [1, 2, 3], anchors)

note_y = y3 + 10
node("note", "BN = BitNet b1.58 2B4T (I2_S). Q4, Q8, F16 = Qwen2.5-1.5B-Instruct at Q4_K_M, Q8_0, and FP16.<br>"
             "Common four-thread operating point, mean of five repeats; disk and peak RAM are single measurements.<br>"
             "In the scatter, BitNet and the k-quant sit on the Pareto frontier together; Q8_0 and FP16 are dominated on both axes.",
     S_SUBNOTE, PX, note_y, row_w, 46)

page_w = row_w + 2 * PX
page_h = note_y + 56

xml = f'''<mxfile host="app.diagrams.net" agent="claude" version="24.7.0" type="device">
  <diagram id="fig5-efficiency" name="Figure 5 - efficiency re-evaluation">
    <mxGraphModel dx="1400" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{page_w:.0f}" pageHeight="{page_h:.0f}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
{chr(10).join(cells)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''

open("figures/fig5-efficiency.drawio", "w", encoding="utf-8").write(xml)
print("wrote figures/fig5-efficiency.drawio", len(xml), "bytes,", len(cells), "cells, page", page_w, "x", page_h)
