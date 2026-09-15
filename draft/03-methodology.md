# 3. Scope and Corpus

## 3.1 Scope and eligibility

A work is in scope if it primarily concerns binary or ternary language models, or a
method, kernel, or hardware design that explicitly targets them. The bit-width gate is
on the **nominal or targeted** weight precision: a work is eligible if it aims at binary
weights, ternary weights, or a partial or salient-split scheme built on a sub-two-bit
backbone. The gate is deliberately not on the effective bits per weight of Section 3.3,
because that figure, which folds in the amortized cost of scales, bitmaps, and
codebooks, is itself one of the survey's findings: several eligible works turn out to
carry two to four effective bits once that cost is counted (BiLLM at about 2.88, STBLLM
at about 4.13), and re-stating those figures on a common scale is the point of Table 2,
not a reason to exclude the works. We include work first made public between January 2023
and June 2026 that makes an empirical or theoretical contribution and for which a freely
downloadable full text exists; a local copy of every included work is archived. A unified
study that sweeps a wider bit-width range, such as a one-to-four-bit
quantization-aware-training comparison, is included for its binary and ternary results
and cited only for those. Work whose method targets only three bits or more, or that has
no language-model component, is cited only where it bears directly on the binary and
ternary case; systems, analysis, and survey works that define no model of their own
appear in the tables with the weight, paradigm, and component axes marked not applicable
rather than forced into a category.
Foundational work on binary networks and the straight-through estimator from 2013 to
2022 is discussed for context and marked separately from the in-window corpus.

The open-access restriction is deliberate. It lets any reader re-check every technical
claim without a paywall, and it lets the re-evaluation of Section 10 run on the exact
released artifacts. Its cost is the possible omission of paywalled work with no preprint.
One work met every other criterion but had no obtainable open-access copy and was set
aside; its abstract, together with those of the paywalled records the search surfaced,
was checked against every principal conclusion of the paper, and none would change.

## 3.2 How the corpus was assembled

The search ran as four passes, all falling between 3 and 5 September 2026, and covers
work public on or before 30 June 2026; the final of the four, a raw arXiv API re-harvest
against the full query set, closed the window on 5 September. The primary source was
arXiv, queried through its API over cs.CL,
cs.LG, cs.AI, and cs.AR with a Boolean query over bit-width terms ("1-bit", "1.58-bit",
"ternary", "binariz*", "sub-2-bit"), model terms, and technique terms ("BitNet",
"BitLinear", "quantization-aware training", "matmul-free", and others), plus fifteen
exact-name queries for known systems. This was supplemented by two iterations of
backward and forward citation chasing on eight seed papers through the Semantic Scholar
citation graph, by targeted web searches for named methods, and by monitoring Hugging
Face Papers and official model and framework release logs. It was not an exhaustive
multi-database search; for a fast-moving subfield that publishes predominantly as
preprints, arXiv plus citation chasing captures the frontier, and the open-access
criterion already excludes venue-only paywalled work.

Candidate records were de-duplicated, screened on title and abstract, then screened in
full text, with the open-access copy retrieved in the same pass and a failure to
retrieve treated as an exclusion. Screening removed off-topic records (most often a
primary contribution outside language modeling, such as error-correcting-code
transformers or high-energy-physics classification, with a 1-bit model as an incidental
example), records whose primary method spanned a bit-width range above two bits, and
records made public after the cutoff, which fall outside the surveyed corpus.

The flow below is the funnel for the final consolidation pass, a raw arXiv API
re-harvest with no summarizer in the loop, together with the cumulative outcome across
all four search passes. The 135 in-window primary studies are not spread
evenly over the four search years; Fig. [fig:growth] gives the year-by-year count.

| stage | count |
|---|---|
| Unique arXiv records, final raw re-harvest (core query + 15 name queries, cs.CL/LG/AI/AR, Jan 2023 to Jun 2026) | 109 |
| Already in the corpus from earlier passes | 69 |
| New, sent to full-text screening | 40 |
| New records included at full text | 15 |
| New records excluded: outside language modeling (EC-1) | 16 |
| New records excluded: bit-width range above two bits (EC-2) | 7 |
| New records excluded: duplicate or re-confirmed prior exclusion | 2 |
| Cumulative full-text eligible, all passes | 136 |
| Excluded, no obtainable open-access copy (IC-5): PT-BitNet | 1 |
| Delayed 20% re-screen (28 sampled, 26 confirmed): removed on second reading | 1 |
| Delayed 20% re-screen: re-included after an open-access copy was located | 1 |
| **In-window primary studies included** | **135** |
| Pre-2023 foundational works, classified in Table 1 for context | 5 |
| **Rows in Table 1** | **140** |
| Non-paper artifacts kept as dated snapshots (two model cards, one framework repository) | 3 |
| Post-cutoff records excluded from this version of the corpus | ~5 |
Table*: **Corpus-assembly funnel.** The final consolidation pass (a raw arXiv API re-harvest with no summarizer in the loop), shown with the cumulative outcome across all four search passes.

The re-screen removed one W4A4 scaling-law study that fails the bit-width criterion and
recovered one native-ternary encoding study once its open-access copy was found; both
revisions are in the counts above. This process departs from the frozen protocol
(`survey-protocol.md`) in three stated ways: screening was by one reviewer rather than
two, the 20% re-screen followed the first pass by a few days rather than the two-week
washout the protocol specifies (Section 3.4), and there was no exhaustive multi-database
harvest or public pre-registration.

## 3.3 Effective-bits accounting and evidence basis

Reported bit-widths in this literature are not comparable as stated, because partial and
salient-split schemes count only the code and omit the group scales, bitmaps, and
codebooks they also store. Throughout, the **effective bits per weight** is the nominal
code width plus the per-weight amortized cost of those structures; where a source's own
strict accounting or an independent one exists, that figure is used and the basis is
noted per row in Table 2.

Rather than collapse source quality into one graded number, each work carries an
**evidence basis** made of two facts that a reader can check directly in Table 1's
"Evidence basis" column. The first is the **venue**: a peer-reviewed conference or journal, or "preprint"
if the only version is on arXiv or under review. The second is whether the **central result has an independent check**, meaning our own reproduction in Section 10 or a separate open study that reaches the same finding; most works have neither. Artifact
availability, whether an open model, code, or weights exist, is recorded as a free-text
note per row where known, since it could not be verified uniformly across all 140 works.

For synthesis we use a single derived split. A source is **corroborated** if it is peer reviewed or has an independent check; otherwise it is a **single unreproduced preprint**. Forty-eight of the 140 works are corroborated. This split is about the
reliability of a source and its artifacts, not about whether its headline claim is
settled: a corroborated source can still make a disputed claim. The parity claim of the
native line is the clearest example. Its sources are all corroborated, BitNet b1.58,
BitNet b1.58 2B4T, both Spectra suites, and ParetoQ, which is also at NeurIPS, and they
corroborate one another; our re-run of the released BitNet b1.58 2B4T checkpoint in
Section 10 confirms that it loads, runs, and is competitive on a common suite. None of
that tests parity at frontier scale, which remains an open problem (Section 11.1). Any
statement in the synthesis that rests only on single unreproduced preprints is marked as
such.

## 3.4 Limitations

The corpus is preprint-heavy, because the field publishes faster than journal review
cycles; this is mitigated by the corroborated-versus-single-preprint split of Section
3.3, by anchoring to peer-reviewed versions where they exist (BitNet in JMLR; OneBit,
BinaryMoS, PV-Tuning, ParetoQ, and LittleBit at NeurIPS; ARB-LLM and PT2-LLM at ICLR;
BiLLM and LC-QAT at ICML; ICQuant at COLM), and by the re-evaluation of Section 10. The search is arXiv-primary rather than exhaustive, so
open-access work in society and publisher venues with no preprint may be missed.
Screening was done by one reviewer; a re-screen of a random 20% sample (28
studies) confirmed 26 of the 28 inclusion decisions (93% raw intra-rater agreement), and
the two revisions it prompted are folded into the counts above. That re-screen followed
the first pass by a few days rather than the two-week washout the protocol specified, so
it measures the stability of the eligibility criteria more than blind intra-rater
agreement. One automated citation list retrieved during the
search contained unverifiable entries, which were discarded; every archived record was
confirmed against its primary source. Finally, some relevant work will appear between the
cutoff and publication; that is an inherent limitation of any fixed-cutoff survey.
