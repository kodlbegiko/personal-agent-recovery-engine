# Architecture

```text
Scenario -> World -> ActionAttempt -> Agent-visible observation -> VerificationRecord
   |                                                        |
   | evaluator-only oracle                                  v
   +------------------------------------------------ RecoveryDecision
                                                            |
                                                   minimal repair / retry
                                                            |
                                                   post-recovery verify
                                                            |
                                                     terminal state
```

`pare.candidates` is forbidden from importing `pare.simulator.oracle`. The evaluator alone compares resulting world state to the expected postcondition. Persistent assertions carry provenance and are repaired only when derived from the affected action.

## Recovery dependency model
Each benchmark action owns a resource id and, in personal-state/composite domains, a provenance-linked state assertion. The candidate may remove/reconstruct the affected resource and assertion but must preserve the independent `benign_anchor` assertion. This is the benchmark's executable minimal-recovery contract.
