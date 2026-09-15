# The reference bitnet.cpp runtime computes the wrong FFN activation for BitNet b1.58 2B4T

Investigated 2026-09-07. **Corrects an earlier note that wrongly blamed the released GGUF.**

## Symptom

`microsoft/bitnet-b1.58-2B-4T-gguf` (`ggml-model-i2_s.gguf`, SHA-256 recorded in
`env/`), run through `llama-perplexity` / `--hellaswag` built from
`BitNet/build-static`:

| path | WikiText-2 ppl | HellaSwag (n=1000) |
|---|---|---|
| bf16 weights via transformers (Arm A)          | 16.67 (word ppl) | 50.8 (acc, 7-task suite) |
| released i2_s GGUF, runtime **as built**       | **86.9** | **38.7%** |
| released i2_s GGUF, runtime **patched**        | **12.99 +/- 0.09** (token ppl) | **62.4%** ([59.4, 65.3]) |
| Qwen2.5-1.5B FP16 GGUF (same tool)             | 8.85 | 65.3% |

## Root cause

`BitNet/3rdparty/llama.cpp/src/models/bitnet.cpp`, the `build_ffn(...)` call for every
layer, passed `LLM_FFN_SILU, LLM_FFN_PAR`. BitNet b1.58 2B4T uses a **gated squared-ReLU**
feed-forward (`config.json`: `"hidden_act": "relu2"`), i.e. `relu(gate(x))^2 * up(x)`.
`LLM_FFN_RELU_SQR` with `LLM_FFN_PAR` produces exactly that (`ggml_relu` -> `ggml_sqr`,
then the post-switch `ggml_mul` by the up projection). This is a known open issue in the
microsoft/BitNet project (issue #588; the reported ppl change 99.8 -> 17.1 brackets the
numbers above).

The one-line fix, applied in this checkout and captured as a patch under `env/`:

```
- LLM_FFN_SILU, LLM_FFN_PAR, il);
+ LLM_FFN_RELU_SQR, LLM_FFN_PAR, il);
```

## What this does and does not mean

- **The released weights are sound.** The defect is entirely in the reference runtime.
- The GGUF also omits `tokenizer.ggml.pre` (llama.cpp warns and uses a default
  pre-tokenizer). With the activation corrected this has little effect on perplexity.
- Perplexity via llama.cpp (token-level, 12.99) and via transformers/lm-eval
  (word-level, 16.67) are different metrics and must not be divided against each other.
- **Efficiency figures (Section 10.4) are unaffected.** A squared-ReLU is no more costly
  than a SiLU, and the activation is a negligible fraction of per-token work. The
  throughput/memory sweep used the patched build.

## Not the "corrupt re-upload" of issue #608

A separate report (microsoft/BitNet issue #608) claims the current
`ggml-model-i2_s.gguf` is a re-upload whose MLP tensors are zero-valued, pointing at its
1,187,801,280-byte size versus an earlier ~1.84 GB artifact. The reproduction here rules
that out for the file actually used:

- SHA-256 `4221b252fdd5fd25e15847adfeb5ee88886506ba50b8a34548374492884c2162`, recorded in
  `env/model-revisions.txt` (HF snapshot `a1f2f1c765812aa8af3f6eda4a313707064bba15`).
- The 1,187,801,280 bytes are the tied-embedding layout: the model shares its input and
  output embedding, so the GGUF carries no separate `output.weight`, and the I2_S body is
  ~1.19 GB. The ~1.84 GB figure corresponds to an untied or higher-precision-embedding
  packing, not to "MLP present vs absent".
- Decisive check: with only the FFN activation constant changed, this exact file reaches
  WikiText-2 ppl 12.99 and HellaSwag 62.4%. Zero-valued `ffn_{gate,up,down}` tensors
  could not produce a low-teens perplexity under any activation. The MLP weights are
  real; the only defect is the runtime's activation.

## Earlier failed repair attempts (superseded)

Before finding the activation bug we tried, and it explains why they "failed":
metadata-patching `tokenizer.ggml.pre` onto the GGUF (writer mis-sizes I2_S tensors),
and a full reconversion from bf16 through the documented pipeline (`convert-ms-to-gguf`
+ `llama-quantize`). Both were then run through the **same unpatched runtime**, so both
produced garbage for a reason unrelated to the conversion.
