# Baseline Eligibility

## Required and eligible
B0-B5 are deterministic, CPU-only and implemented in-repo.

## Contextual but not numerical baselines
- AppWorld / τ-bench / TUA-Bench evaluate broader agent competence rather than a drop-in recovery policy and commonly require model inference for published configurations.
- LangGraph and Temporal are orchestration/runtime systems, not matched algorithms that emit PARE RecoveryDecision records over this oracle-isolated benchmark.
- The 2026 verified-tool-call paper is conceptually closest; its verify-before-retry + idempotency behavior is represented by B3/B4. PARE does not claim those primitives as novel.

No stronger zero-cost, CPU-only, directly comparable recovery algorithm with a faithful public implementation was identified in this pre-freeze review.
