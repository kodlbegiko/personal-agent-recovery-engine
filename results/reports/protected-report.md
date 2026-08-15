# Fresh Protected Evaluation Report — Protocol v0.3

Fresh seed provenance: Python `secrets.randbits(63)` after protocol/candidate freeze. Seed: `3000603268395507528`. Candidate freeze commit: `57c2f6e70666714de51236a9bbe4b3d4cd907c52`.

## Primary results

- Selected candidate: **Candidate-v2**
- Strongest eligible baseline: **B0 No Recovery**
- Protected cases: **72**
- Candidate Recovery Success Rate: **0.8611** (Wilson 95% CI 0.7629–0.9228)
- Baseline Recovery Success Rate: **0.6111**
- Paired delta: **0.2500**; paired-bootstrap 95% CI **[0.1528, 0.3472]**
- Benign State Preservation: **1.0000**

## Safety gates

- False Completion Rate: **0.0000**
- INCONCLUSIVE→COMPLETED violations: **0**
- Retry-budget violations: **0**
- Post-recovery verification coverage: **1.0000**
- Destructive duplicate side effects: **0**
- Destructive side-effect rate: **0.0000**
- Duplicate side-effect rate: **0.0278**

All mandatory safety gates passed. Duplicate side effects were not eliminated completely: 2/72 protected cases retained a duplicate effect, both non-destructive under the benchmark definition. This remains a concrete limitation.
