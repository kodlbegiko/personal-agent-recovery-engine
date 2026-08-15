# PARE Research Protocol v0.2 — FROZEN BEFORE PROTECTED EVALUATION

Freeze date: 2026-08-15 (Asia/Taipei).

## Research question
Can verification-grounded, risk-aware, dependency-aware minimal recovery improve recovery efficacy/minimality over reproducible zero-cost baselines under deterministic non-atomic faults while satisfying strict false-completion and retry-safety gates?

## Hypotheses
- H1: the selected Candidate-v3 lineage has higher Recovery Success Rate than the strongest safety-eligible baseline on a fresh protected set.
- H2: it preserves benign state at least as well as that baseline.
- H3: it satisfies every mandatory safety gate.

## Fixed domains
Messaging, Calendar, Files, Task Management, Persistent Personal State, Composite Workflow.

## Fixed fault taxonomy
PRE_DISPATCH_FAILURE, POST_COMMIT_TIMEOUT, DELAYED_VISIBILITY, PARTIAL_MUTATION, DUPLICATE_DELIVERY, STALE_READ, CONCURRENT_MUTATION, WRONG_TARGET, STATE_WRITE_CORRUPTION, CRASH_BEFORE_COMMIT, CRASH_AFTER_COMMIT, VERIFIER_UNAVAILABLE, RECOVERY_FAILURE, ROLLBACK_FAILURE, COMPENSATION_FAILURE, OUT_OF_ORDER_OBSERVATION.

## Fixed development partitions
- Development: 180 logical cases, seed 1101.
- Validation: 120 logical cases, seed 2202.
- Protected: 72 fresh logical cases generated only after freeze with OS CSPRNG-derived seed.
- Robustness/ablation: 96 cases, seed 3303, used only after protected evaluation.

## Required baselines
B0 No Recovery; B1 Blind Retry Once; B2 Bounded Retry; B3 Verify Before Retry; B4 Idempotency-Aware; B5 Conservative Fail-Closed.

Frontier methods are eligible only when a faithful, zero-cost, CPU-compatible implementation can be incorporated without a paid model/service. Otherwise they remain contextual comparators, not numerical baselines.

## Candidate lineage
- Candidate-v1: verification-grounded risk-aware recovery without dependency-aware minimal rollback/state repair.
- Candidate-v2: adds dependency-scoped minimal rollback and provenance-aware state repair.
- Candidate-v3: contract-complete lineage adding an explicit ImpactGraph and StateRepairLedger plus the full predeclared secondary metric surface; no discarded v2 protected-like case is reused for tuning.

## Primary endpoints
1. Efficacy: Recovery Success Rate.
2. Safety: False Completion Rate; Duplicate/Destructive Side-Effect Rate.
3. Minimality: Benign State Preservation Rate.

## Secondary endpoints
Verified Success Precision, Unnecessary Recovery Rate, Affected-State Invalidation Recall, State Repair Precision/Recall, Mean Recovery Actions, Mean Verification Actions, Recovery Latency, Recovery Cost Proxy, Fail-Closed Correctness, Retry Budget Violations, INCONCLUSIVE-to-COMPLETED Violations, Post-Recovery Verification Coverage.

## Mandatory safety gates
- INCONCLUSIVE -> COMPLETED violations = 0.
- Unbounded/retry-budget violations = 0.
- Post-recovery verification coverage = 1.00.
- Destructive duplicate side effects = 0.
- False Completion Rate <= 0.05.

## Candidate selection rule
A candidate must first pass all safety gates on validation. Among qualifying candidates choose, in order: (1) highest validation Recovery Success Rate, (2) highest Benign State Preservation, (3) lowest Duplicate Side-Effect Rate, (4) fewer recovery actions, (5) simpler candidate.

## Strongest-baseline rule
Apply the same safety qualification to B0-B5. Compare protected results against the qualifying baseline with highest Recovery Success Rate, then Benign State Preservation, then lower Duplicate Side-Effect Rate. If no baseline qualifies, choose the highest-efficacy B0-B5 baseline and explicitly report that it is non-qualifying.

## Statistics
Report exact counts, Wilson 95% CI for binary success, failure/domain stratification, and paired bootstrap 95% CI for protected candidate-minus-baseline success difference (4,000 resamples, fixed analysis seed 20260815).

## Capability-success rule
Capability passes only if every safety gate passes AND the candidate has a positive protected improvement on at least one predeclared efficacy/minimality endpoint without safety degradation. For Recovery Success Rate, a paired-bootstrap interval with lower bound >= 0 is required for a superiority-style pass; otherwise the terminal result is negative or inconclusive.

## No post-hoc rescue
Protected observations cannot change thresholds, cases, labels, primary metrics, or frozen candidate code. Any later candidate must be a new lineage with a fresh protected seed.
