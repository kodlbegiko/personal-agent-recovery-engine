# Ablation Report

96-case robustness split (seed 3303), executed after protected evaluation.

| Variant | Recovery success | State repair recall | Post-recovery verification |
|---|---:|---:|---:|
| full | 0.8542 | 1.0000 | 1.0000 |
| no_idempotency | 0.8542 | 1.0000 | 1.0000 |
| no_verify_before_retry | 0.8542 | 1.0000 | 1.0000 |
| no_risk_layer | 0.8750 | 1.0000 | 1.0000 |
| no_dependency_graph | 0.8542 | 1.0000 | 1.0000 |
| no_minimal_rollback | 0.8542 | 1.0000 | 1.0000 |
| no_state_repair | 0.8333 | 0.5714 | 1.0000 |
| no_reverification | 0.8542 | 1.0000 | 0.6250 |

Interpretation: removing state repair reduced robustness recovery success from 0.8542 to 0.8333 and state-repair recall to 0.5714. Removing re-verification collapsed verification coverage to 0.625. Several other components were neutral on this robustness split; those null effects are preserved rather than omitted. Removing the risk layer increased raw recovery success to 0.875, which illustrates the expected efficacy/safety tension rather than evidence that the risk layer is unnecessary.
