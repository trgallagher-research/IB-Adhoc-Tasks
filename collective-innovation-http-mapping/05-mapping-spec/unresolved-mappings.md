# Unresolved mappings report

Generated 2026-07-28 by `scripts/build_reports.py`.

## Open unresolved/probable mappings: 0

**None.** The existing flow's labelled-submission construction (EV‑2, captured 2026‑07‑28) pairs every question label with its response key, and the live schema (EV‑1) resolves every destination. All prior Probables and candidate sets resolved consistently with the dummy-test evidence — zero contradictions.

## Permanently unexplained keys (documented, harmless)

The body carries 7 keys beyond the 41 questions — blank in every observed response and referenced nowhere in the flow. Most plausibly deleted questions or section elements. They are mapped to nothing and require no action:

- `r1b7b5f6d2bb2486db74f1f1ebb0cb067`
- `r1c4bea10de144dcdb6cbc8830f7c3e31`
- `r208f7c57b79d432da596a8fc1dc1e5e6`
- `r6957ab38b1994a988463479662e02998`
- `r758fbc5c9ddf44d9a1f7ef377c0dafba`
- `rb797d6da9e514447b235f1c6897d06e4`
- `rb8a1472f55ed4f58b6932b6284ba874e`

## Residual items outside the mapping itself

- Five of the eight Select actions were not Peek-code captured (names and join expressions are evidenced via Create item; the AI layer is preserved as-is, so this is non-blocking).
- Live behaviour items are covered by the test matrix, not by mapping evidence.
