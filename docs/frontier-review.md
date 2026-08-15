# External Frontier Review — 2026-08-15

Primary-source review performed before protected evaluation.

| Source | Date | Relevant capability | Reproducibility / cost | PARE decision |
|---|---:|---|---|---|
| AppWorld (Trivedi et al., arXiv:2407.18901) | 2024 | 9 simulated apps, 457 APIs, state-based unit-test evaluation including collateral damage | Public framework; broader and heavier than PARE | Adopt state-based/collateral-damage evaluation principle; not a recovery baseline. |
| τ-bench (Yao et al., arXiv:2406.12045) | 2024 | Dynamic tool-agent-user tasks; final database state evaluation; repeated-trial reliability metric | Public benchmark but model-dependent | Context benchmark, not eligible numerical recovery baseline under zero-paid-model rule. |
| LangGraph official persistence/execution docs | reviewed 2026-08-15 | Durable checkpoints; re-execution can repeat side effects; recommends idempotency/read-before-write | Open-source framework | Engineering prior supporting idempotent, verify-before-retry design; not a benchmark baseline. |
| Temporal official docs | reviewed 2026-08-15 | Durable workflow execution and crash/network recovery | Open-source/self-hostable | Contextual systems prior; not a matched recovery-policy baseline. |
| TUA-Bench (Chen et al., arXiv:2606.28480) | 2026 | 120 execution-based real terminal tasks | Public; published frontier runs require model providers | Context benchmark only. |
| Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures (Mansoor et al., arXiv:2608.02645) | 2026 | Postcondition verification, verify-before-retry, idempotency under non-atomic failures | Primary paper; closest conceptual prior | Candidate-v1 must not claim novelty for these primitives. PARE tests dependency-aware persistent-state repair/minimal recovery beyond the wrapper pattern. |

## Frontier conclusion
The closest conceptual prior already motivates verified tool calls, idempotency and verify-before-retry. PARE therefore narrows its scientific question to whether these primitives combined with dependency-aware minimal state repair improve persistent-agent recovery without collateral state destruction. Broader agent benchmarks inform realism but are not fair zero-cost algorithmic baselines for this deterministic recovery-policy study.
