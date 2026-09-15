# Project rules — 1-Bit LLM Survey

## RULE 1 (MUST — never skip): download every referenced paper

Whenever this survey **cites or refers to a paper** — in the plan, the draft, the
`inventory.csv`, or anywhere else — the paper's full text **must** be downloaded and
saved into `papers/` in this directory. No exceptions. Do this in the same turn the
reference is added; never defer it.

- **Format:** PDF. Use the open-access source (arXiv `/pdf/<id>`, JMLR PDF, ACL
  Anthology PDF, OpenReview PDF, PMLR PDF).
- **Filename:** `<year>_<firstauthorLastname>_<short-slug>.pdf`
  (e.g. `2024_Ma_bitnet-b1.58-era.pdf`, `2023_Wang_bitnet-scaling-1bit.pdf`).
- **arXiv:** also record the arXiv id in the filename slug if handy, e.g.
  `2402.17764_2024_Ma_bitnet-b1.58-era.pdf`.
- **Non-papers** (Hugging Face model cards, GitHub repos, release notes): save a
  dated snapshot instead — `papers/_web/<date>_<slug>.md` (or `.pdf`) — so the
  reference is still archived.
- **inventory.csv** must carry a `local_file` column pointing to the saved file.

### The gate (absolute)

**If we cannot download it, we do not cite it.** No PDF in `papers/` (or an
approved snapshot in `papers/_web/` for a non-paper artifact) → the work is
**excluded** from the survey. This is not a "flag and revisit later" — it is a
hard inclusion gate (IC-5). Excluded items are listed in `papers/INDEX.md` under
"EXCLUDED" with the reason, and must not appear in the references, tables, or prose
of the paper.

Before finishing any turn that added or changed a paper reference, verify the file
exists in `papers/`. If it does not and cannot be fetched, remove the reference.

## Context

Full strategy: `MASTER-SURVEY-PLAN.md` (supersedes the three older plan drafts).
Evidence base is open-access only; target journal IF ≥ 10; literature cutoff 30 Jun 2026.
