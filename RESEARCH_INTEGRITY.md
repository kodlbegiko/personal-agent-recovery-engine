# Research Integrity

1. Research question, fault taxonomy, metrics, safety gates, candidate selection and protected-evaluation procedure are frozen before protected generation.
2. Protected seeds are generated only after the freeze manifest is written.
3. Protected results never tune the frozen lineage.
4. Negative and inconclusive outcomes are retained.
5. Candidate code cannot access evaluator oracle truth or answer fields.
6. README claims must not exceed `CLAIMS.md`.
7. Synthetic benchmark evidence is not a universal SOTA claim.
