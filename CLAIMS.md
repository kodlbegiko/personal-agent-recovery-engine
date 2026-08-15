# Claims Registry

| claim_id | claim_text | scope | evidence | status | limitations |
|---|---|---|---|---|---|
| PARE-001 | Simulator replay and benchmark generation are deterministic for fixed seeds. | PARE-Bench | tests + manifests | UNTESTED | Excludes CSPRNG protected seed generation itself. |
| PARE-002 | Candidate code is isolated from evaluator oracle imports. | repository | static test | UNTESTED | Static guard does not prove absence of every conceivable covert channel. |
| PARE-003 | Selected candidate improves protected recovery efficacy over strongest eligible baseline. | fresh protected PARE-Bench | protected paired comparison | UNTESTED | Benchmark-specific only. |
| PARE-004 | Selected candidate passes mandatory recovery safety gates. | fresh protected PARE-Bench | protected safety metrics | UNTESTED | Synthetic environment. |
| PARE-005 | PARE is universally superior / production-safe. | universal | none | NOT_SUPPORTED | Outside study scope. |
