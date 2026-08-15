# Final Research Report

## Research question
Whether verification-grounded, risk-aware, dependency-aware minimal recovery can restore consistent persistent-agent state under ambiguous/non-atomic tool failures better than zero-cost baselines while preventing false completion and unnecessary collateral state destruction.

## Methods and benchmark
PARE-Bench is a deterministic, oracle-isolated simulator covering six personal-agent domains and sixteen fault classes. The pre-protected corpus contains 180 development + 120 validation cases. The final confirmatory evaluation used 72 fresh cases generated only after Candidate-v2 was selected by the frozen validation rule and commit `57c2f6e70666714de51236a9bbe4b3d4cd907c52` was recorded. Ground truth is machine-testable world state; no human labels or paid APIs were used.

## Baselines and selected candidate
Required baselines B0-B5 were implemented. The strongest safety-eligible comparator under the frozen rule was B0 No Recovery. Candidate-v2 was selected on validation (Recovery Success 0.875) over Candidate-v1 (0.85); Candidate-v3 tied Candidate-v2 on preceding endpoints, so the frozen simplicity tie-break retained Candidate-v2.

## Protected result
Candidate-v2 achieved **86.11%** Recovery Success versus **61.11%** for B0. The paired improvement was **25.00%**, with paired-bootstrap 95% CI **[15.28%, 34.72%]**. Benign State Preservation was **100%**. False Completion was **0%**, Verified Success Precision **100%**, destructive side effects **0%**, mandatory destructive-duplicate violations **0**, retry-budget violations **0**, INCONCLUSIVE→COMPLETED violations **0**, and post-recovery verification coverage **100%**.

## Negative results and failure analysis
The candidate did not recover every protected case. The remaining failures concentrated in PRE_DISPATCH_FAILURE, CRASH_BEFORE_COMMIT, and a subset of DUPLICATE_DELIVERY cases. Protected duplicate side-effect rate was **2.78%** even though destructive side-effect rate was 0%; therefore the system does not establish duplicate-free recovery. The fail-closed correctness secondary metric was 0.20 under this benchmark's definition, reflecting that many failed end states were not resolved specifically through FAIL_CLOSED.

Ablations also produced null results for idempotency, verify-before-retry, dependency graph, and minimal rollback on the fixed 96-case robustness split; these components cannot individually claim causal benefit from this ablation alone. State repair and re-verification did show measurable benchmark-specific effects.

## Adversarial robustness
A separate 28-case synthetic adversarial suite covering timeout-after-success, stale/false observations, concurrent mutation, duplicate response, crash/recovery paths and corrupted state references achieved 28/28 oracle recovery success under the implemented mapping. This is a stress-test result only, not independent external evidence; the adversarial generator is intentionally synthetic and shares the same simulator assumptions.

## Integrity history
Two earlier outputs are explicitly excluded: an uncommitted pre-confirmatory Candidate-v2 dry run lacking the full required metric/ledger surface, and a v0.2 confirmatory attempt invalidated because its H1 text named Candidate-v3 while the frozen selection rule selected Candidate-v2. Both are preserved under `evidence/integrity/`; neither was used to tune the final candidate. Protocol v0.3 changed hypothesis wording only and used a fresh protected seed.

## Valid claim boundary
The evidence supports a **benchmark-specific protected claim** that the frozen Candidate-v2 recovery policy outperformed the strongest eligible in-repo baseline on PARE-Bench while satisfying the predeclared mandatory safety gates. It does **not** establish universal superiority, production readiness, real-provider safety, or human preference.

## Terminal decision
**READY_FOR_UMBRELLA_INTEGRATION**. Scientific success: **True**. Capability success under the frozen PARE-Bench criteria: **True**.
