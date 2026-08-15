# Limitations

- The world and fault injector are synthetic and deliberately small enough for CPU-only exhaustive replay.
- Recovery policy uses structured observations rather than a language model; this isolates recovery semantics but does not test natural-language interpretation.
- Compensation and rollback are modeled deterministically and do not capture every provider-specific irreversible side effect.
- Concurrency is represented as controlled external mutation, not a distributed-system model checker.
- Protected evidence is benchmark-specific and should not be generalized to real accounts or high-risk actions.
