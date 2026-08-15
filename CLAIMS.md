# Claims Registry

| claim_id | claim_text | scope | evidence | status | limitations |
|---|---|---|---|---|---|
| PARE-001 | Simulator replay and benchmark generation are deterministic for fixed seeds. | PARE-Bench | tests + manifests | PROTECTED_SUPPORTED | CSPRNG seed creation is intentionally non-deterministic; replay uses the published seed. |
| PARE-002 | Candidate modules do not directly import evaluator oracle truth. | repository | `tests/test_core.py`, integrity check | PROTECTED_SUPPORTED | Static/runtime isolation is benchmark infrastructure, not a formal information-flow proof. |
| PARE-003 | Selected Candidate-v2 improves protected Recovery Success Rate over strongest eligible baseline. | fresh 72-case PARE-Bench v0.3 | protected paired comparison | PROTECTED_SUPPORTED | Delta 0.2500, bootstrap 95% CI [0.1528, 0.3472]; benchmark-specific. |
| PARE-004 | Candidate-v2 passes the predeclared mandatory recovery safety gates. | fresh 72-case PARE-Bench v0.3 | protected safety metrics | PROTECTED_SUPPORTED | Duplicate side-effect rate remains 0.0278; only destructive-duplicate violations are zero. |
| PARE-005 | Dependency-aware state repair is individually necessary for all gains. | PARE-Bench | ablation | INCONCLUSIVE | Some component ablations are neutral; no universal causal claim. |
| PARE-006 | PARE is universally superior / production-safe. | universal | none | NOT_SUPPORTED | Outside study scope. |
