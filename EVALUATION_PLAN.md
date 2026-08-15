# Evaluation Plan

1. Run deterministic development and validation sets on B0-B5 and Candidate-v1/v2/v3.
2. Apply the frozen validation safety gate and selection rule.
3. Commit/freeze Candidate-v3 source and protocol; record that commit SHA.
4. Hash protocol, generator, metrics and candidate source into `artifacts/freeze-manifest.json`.
5. Only then generate a CSPRNG protected seed and 72 fresh protected scenarios.
6. Evaluate the selected candidate and strongest baseline on identical scenarios.
7. Run paired analysis, then separate robustness/ablation/adversarial suite.
8. Reconcile terminal status and claims without tuning protected failures.
