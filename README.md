# Personal Agent Recovery Engine (PARE)

Verification-grounded recovery and persistent-state repair research for persistent personal agents.

## Current evidence-backed status

**Terminal state: `READY_FOR_UMBRELLA_INTEGRATION`**

Fresh protected PARE-Bench v0.3 (72 cases): Candidate-v2 achieved **86.11%** Recovery Success vs **61.11%** for the strongest eligible baseline (B0), paired delta **+25.00%** with bootstrap 95% CI **[15.28%, 34.72%]**. False Completion = 0, destructive side effects = 0, INCONCLUSIVE→COMPLETED violations = 0, retry-budget violations = 0, and post-recovery verification coverage = 100%.

The claim is **benchmark-specific**. Duplicate side effects were not completely eliminated (2.78% protected rate), and this repository does not claim universal superiority or production safety.

## Core invariant

`tool/API success != user-goal success`  
`tool/API error != world unchanged`  
`recovery action != recovered state`

Every recovery path is re-verified before completion.

## Research assets
- `RESEARCH_PROTOCOL.md` — frozen v0.3 confirmatory protocol
- `BENCHMARK_CARD.md` — six-domain / sixteen-fault benchmark definition
- `pare/` — simulator, candidates, baselines, evaluation
- `results/reports/final-report.md` — bounded final interpretation
- `artifacts/freeze-manifest.json` — protocol/generator/metrics/candidate hashes
- `evidence/integrity/` — preserved invalidated attempts and integrity history

## Reproduce

```bash
pip install -e '.[dev]'
make reproduce
```

No paid model API is required.
