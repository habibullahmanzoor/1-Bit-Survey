# 12. Conclusion

Native 1-bit and 1.58-bit large language models have moved, in three years, from a
single proof of concept to a coherent research program, with an open 2B-parameter model,
a CPU inference stack, a first wave of custom-silicon proposals, and extensions into
embeddings, speech, vision-language-action models, mixture-of-experts, and state-space
models; the defining idea is not aggressive compression but a change of arithmetic, since
when every weight is ternary the matrix multiplication becomes an addition, and the
questions that follow, how to train through the discrete constraint, how far activation
precision can drop, and what the ideal hardware looks like, are different in kind from
those of four-bit quantization.

We surveyed the 135 open-access works of that program on
a five-axis taxonomy and re-tabulated their reported numbers in consistent columns under
one effective-bits accounting, then re-evaluated the two central claims ourselves. In a
controlled comparison from open matched checkpoints, native ternary against FP16 at the
same 2.4-billion parameters, tokenizer, and training data, the two came within 0.6 points
on a seven-task zero-shot mean, with the ternary model's perplexity about 14% higher:
downstream parity with a worse language-modeling loss. Post-hoc 4-bit quantization of a
full-precision model lost more of that suite, and a 1.58-bit model at the
one-billion-parameter scale, on a checkpoint pair whose training match is undocumented,
lost far more; that pattern is consistent with, but too thin a basis on its own to
establish, a scale dependence for the parity result, and whether it holds above the
measured regime is still open.

The efficiency result cuts the other way: on the one x86 machine we tested, the flagship
1-bit model held no advantage in decode speed, on-disk size, or per-token energy over an
ordinary 4-bit quantization of the full-precision baseline, and stayed only level with it
on the accuracy tasks we could check, leaving a 24-to-27% smaller resident set as the only
advantage that remained. The paradigm's efficiency argument at this scale therefore
stands on the comparison with half precision and with an 8-bit baseline, not with the
tested 4-bit builds, and whether it recovers against those on a GPU, or against a
production 4-bit kernel generally, is the open question that Section 10.7 lays out; that the
reference CPU runtime does not even run the flagship model correctly as documented,
without a one-line source fix, says the same thing from the software side, since the open
deployment path is not yet mature.

The paradigm's promise is thus a change of arithmetic
that current commodity software and hardware do not yet cash in, and the open problems
that remain are concrete: whether native 1.58-bit training reaches full-precision parity
at frontier scale and token budgets is untested and is the most important missing
experiment in the field, and training stability at frontier scale, the
activation-precision floor below four bits, a convergence theory for straight-through
training, and, above all, the absence of any shipping processor with a ternary
matrix-multiplication primitive are the barriers between the current results and a future
in which 1-bit models are a default rather than a curiosity. The evidence so far is that
the paradigm is real; whether it becomes standard depends on co-design work that, for the
most part, has not yet been done.
