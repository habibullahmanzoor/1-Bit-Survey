"""RULE 1 cross-check: every cited key -> bib entry -> downloaded PDF -> right paper.

Outputs a report. Flags:
  MISSING-BIB   cited in .tex but no references.bib entry
  MISSING-FILE  bib entry with no downloaded PDF / _web snapshot
  NO-INVENTORY  bib entry (non-web) with no data/inventory.csv row
  TITLE-MISMATCH pdf first-page title shares few tokens with bib title
  ORPHAN-BIB    bib entry never cited
  ORPHAN-PDF    papers/*.pdf not referenced by any inventory local_file
"""
import csv, os, re, subprocess, sys, glob, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = r"c:\python experiments\survy papers\1 bit"
TEX = os.path.join(ROOT, "1bit-llm-survey.tex")
BIB = os.path.join(ROOT, "references.bib")
INV = os.path.join(ROOT, "data", "inventory.csv")
PAPERS = os.path.join(ROOT, "papers")
WEB = os.path.join(PAPERS, "_web")

STOP = set("a an the of for and or to in on with without via using toward towards is are "
           "be by from at as into over under near not no we our their its it this that these "
           "large language models model llms llm neural network networks bit bits low high "
           "efficient effective fast accurate accurate towards".split())


def norm(s):
    s = s.lower()
    s = re.sub(r"\{|\}|\\[a-z]+|[^a-z0-9 ]", " ", s)
    return [w for w in s.split() if w not in STOP and len(w) > 2]


# ---- cited keys ----
tex = open(TEX, encoding="utf-8").read()
cited = set()
for m in re.finditer(r"\\cite[a-z]*\{([^}]+)\}", tex):
    for k in m.group(1).split(","):
        cited.add(k.strip())
cited.discard("")

# ---- bib entries ----
bib = {}
raw = open(BIB, encoding="utf-8").read()
for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", raw, re.S):
    key = m.group(2).strip()
    body = m.group(3)
    t = re.search(r"title\s*=\s*\{(.+?)\}\s*,?\s*\n", body, re.S)
    note = re.search(r"(note|howpublished)\s*=\s*\{(.+?)\}", body, re.S)
    bib[key] = {"title": (t.group(1).strip() if t else ""),
                "note": (note.group(2).strip() if note else "")}

# ---- inventory ----
inv = {}
with open(INV, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        inv[row["id"]] = row

# ---- files on disk ----
pdfs = {os.path.basename(p) for p in glob.glob(os.path.join(PAPERS, "*.pdf"))}
webfiles = os.listdir(WEB) if os.path.isdir(WEB) else []

report = []
def add(tag, key, msg=""):
    report.append((tag, key, msg))

# ---- 1. cited -> bib ----
for k in sorted(cited):
    if k not in bib:
        add("MISSING-BIB", k, "cited but not in references.bib")

# ---- 2/3. bib -> file -> title ----
title_rows = []
for key in sorted(bib):
    if key.startswith("web-"):
        # expect a _web snapshot; match loosely by any 4+ char fragment
        kt = re.sub(r"[^a-z0-9]", "", key.replace("web-", "").lower())
        frags = re.findall(r"[a-z]{4,}", key.replace("web-", "").lower()) + \
                re.findall(r"[a-z]{4,}", re.sub(r"([a-z])([A-Z])", r"\1 \2", key).lower())
        joined = " ".join(wf.lower().replace("-", " ").replace("_", " ") for wf in webfiles)
        if not any(fr in joined for fr in set(frags)):
            add("MISSING-FILE", key, f"_web snapshot not found (have: {webfiles})")
        continue
    r = inv.get(key)
    if not r:
        add("NO-INVENTORY", key, "no inventory row")
        continue
    lf = (r.get("local_file") or "").strip()
    if not lf:
        add("MISSING-FILE", key, "inventory local_file empty")
        continue
    if lf not in pdfs:
        add("MISSING-FILE", key, f"file not in papers/: {lf}")
        continue
    # title check
    path = os.path.join(PAPERS, lf)
    try:
        txt = subprocess.run(["pdftotext", "-f", "1", "-l", "2", "-layout", path, "-"],
                             capture_output=True, text=True, timeout=60,
                             encoding="utf-8", errors="ignore").stdout
    except Exception as e:
        add("PDF-UNREADABLE", key, f"{lf}: {e}")
        continue
    head = " ".join(txt.split()[:120])
    bt = set(norm(bib[key]["title"]))
    ht = set(norm(head))
    if not bt:
        add("BIB-NO-TITLE", key, "")
        continue
    overlap = len(bt & ht) / len(bt)
    title_rows.append((overlap, key, lf, bib[key]["title"][:70]))
    if overlap < 0.34:
        add("TITLE-MISMATCH", key,
            f"overlap {overlap:.0%} | bib='{bib[key]['title'][:80]}' | pdf-head='{head[:120]}'")

# ---- 4. orphans ----
for key in sorted(bib):
    if key not in cited:
        add("ORPHAN-BIB", key, "in bib, never \\cite'd")
inv_files = {(r.get("local_file") or "").strip() for r in inv.values()}
for p in sorted(pdfs):
    if p not in inv_files:
        add("ORPHAN-PDF", p, "pdf not referenced by any inventory row")

# ---- output ----
print(f"cited keys: {len(cited)} | bib entries: {len(bib)} | inventory rows: {len(inv)} "
      f"| papers/*.pdf: {len(pdfs)} | _web: {len(webfiles)}")
print()
by = {}
for tag, key, msg in report:
    by.setdefault(tag, []).append((key, msg))
if not report:
    print("ALL CLEAN - every cited key resolves to a downloaded PDF with a matching title.")
for tag in ("MISSING-BIB", "NO-INVENTORY", "MISSING-FILE", "PDF-UNREADABLE",
            "BIB-NO-TITLE", "TITLE-MISMATCH", "ORPHAN-BIB", "ORPHAN-PDF"):
    rows = by.get(tag, [])
    print(f"\n### {tag}  ({len(rows)})")
    for key, msg in rows:
        print(f"  {key}: {msg}")

print("\n\n### 20 LOWEST title-overlap (manual eyeball) ###")
for ov, key, lf, bt in sorted(title_rows)[:20]:
    print(f"  {ov:5.0%}  {key:38s} {lf}")
