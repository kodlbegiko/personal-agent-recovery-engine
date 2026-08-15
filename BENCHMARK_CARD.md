# Benchmark Card

PARE-Bench is a deterministic synthetic state-transition benchmark for recovery after ambiguous and non-atomic tool execution. It covers six personal-agent domains and sixteen fault classes. Candidate-visible observations are separated from evaluator-only oracle truth.

## Scale
The frozen generator produces 180 development + 120 validation cases before protected evaluation, then 72 fresh protected cases after candidate freeze. A separate 96-case robustness set supports ablations.

## What it measures
Recovery efficacy, false completion, duplicate/destructive effects, benign-state preservation, bounded recovery effort, post-recovery verification and failure-class behavior.

## What it does not establish
Human preference, production safety, real-provider API semantics, universal agent reliability, or cross-benchmark SOTA.
