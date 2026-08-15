# Integration Contract v1 — Conditional

This contract becomes umbrella-eligible only if protected capability success is established.

`StateSnapshot -> InterventionDecision -> ActionAttempt -> VerificationRecord -> RecoveryDecision -> RecoveryRecord -> StateSnapshot'`

The umbrella architecture consumes versioned records, never PARE implementation internals. High-risk irreversible recovery remains fail-closed unless independently authorized.
