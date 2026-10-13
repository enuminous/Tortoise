# Shared Lean 4 verification for Tortoise

The selected formal core is maintained in the shared [Monolithic Zoo package](https://github.com/enuminous/Monolithic-Zoo-Lean4).

- Checked module: [Tortoise.lean](https://github.com/enuminous/Monolithic-Zoo-Lean4/blob/44d9881e8878a702fdfa47da53d80436276d92a6/Tortoise.lean).
- Verified package commit: `44d9881e8878a702fdfa47da53d80436276d92a6`.
- Successful workflow: [38484522045](https://github.com/enuminous/Monolithic-Zoo-Lean4/actions/runs/38484522045).
- Selected upstream source revision: [`6658128fd2df96ff6c32fce219bfc9ee3e8876da`](https://github.com/enuminous/Tortoise/commit/6658128fd2df96ff6c32fce219bfc9ee3e8876da); preserved source blobs and hashes are in the shared package's `UPSTREAM_SOURCES.json`.
- Scope: ordered split; temporal separation contract; Brier gain.
- Named theorem declarations: `Zoo.Tortoise.split_reconstructs`, `Zoo.Tortoise.train_precedes_test`.

The run passed the pinned Lean build, strict axiom audit, audit rejection controls,
90 finite reference comparisons across the shared package, and the 46-module roster.
These are package-level checks; they do not mean that 90 tests belong to this animal.

This evidence covers the selected core and its stated hypotheses. It does not
certify this repository's complete Python pipeline, feature extraction, training,
all floating-point edge cases, or empirical effectiveness. The shared
[coverage ledger](https://github.com/enuminous/Monolithic-Zoo-Lean4/blob/main/COVERAGE.md)
and [remaining obligations](https://github.com/enuminous/Monolithic-Zoo-Lean4/blob/main/FORMALIZATION_NOTES.md)
preserve those limits. Future source changes require a fresh correspondence review.

Reuse the pinned shared package instead of maintaining a divergent proof copy here.
