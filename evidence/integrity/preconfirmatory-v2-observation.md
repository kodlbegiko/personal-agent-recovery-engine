# Pre-confirmatory Candidate-v2 observation — excluded from confirmatory evidence

Before the repository-level candidate freeze commit existed, an uncommitted local dry run of the end-to-end harness generated a protected-like 72-case set. The run exposed results before the mission's full required secondary metric surface, explicit `ImpactGraph`, and `StateRepairLedger` were implemented.

Integrity disposition:
- The seed and result files from that dry run were deleted locally and are not used as Candidate-v3 development, validation, selection, threshold, or tuning inputs.
- Candidate-v3 is a contract-completeness lineage: it adds explicit impact/state-repair records and predeclared secondary metrics; it is not tuned to the discarded cases.
- Formal confirmatory evaluation must use a fresh seed generated only after the Candidate-v3 source/protocol commit SHA is recorded in the freeze manifest.
- Any claim in this repository must cite only the fresh Candidate-v3 protected evaluation.

This note is preserved because invalid research-process evidence must not be silently erased.
