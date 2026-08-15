from dataclasses import dataclass
from pare.contracts.models import RecoveryMode
POLICY_VERSION='pare-v3-policy-1.0'
@dataclass(frozen=True)
class CandidateConfig:
    name:str='Candidate-v3';idempotency:bool=True;verify_before_retry:bool=True;risk_layer:bool=True;dependency_graph:bool=True;minimal_rollback:bool=True;state_repair:bool=True;reverification:bool=True
def decide(outcome,verification,scenario,cfg=CandidateConfig()):
    if verification.verdict.value=='VERIFIED_SUCCESS':return RecoveryMode.NO_ACTION
    if cfg.risk_layer and scenario.risk_class=='high' and scenario.reversibility_class=='irreversible':return RecoveryMode.FAIL_CLOSED
    if verification.verdict.value=='INCONCLUSIVE':return RecoveryMode.WAIT_AND_REVERIFY if cfg.verify_before_retry else RecoveryMode.FAIL_CLOSED
    obs=verification.observations
    if obs.get('duplicates',0)>1 or obs.get('wrong',0)>0:return RecoveryMode.COMPENSATE if cfg.minimal_rollback else RecoveryMode.ROLLBACK
    if scenario.requires_assertion and not obs.get('state_ok',True):return RecoveryMode.ROLLBACK if cfg.state_repair else RecoveryMode.FAIL_CLOSED
    if outcome.observation.get('side_effect')=='none':return RecoveryMode.IDEMPOTENT_RETRY
    if scenario.reversibility_class=='reversible':return RecoveryMode.ROLLBACK
    return RecoveryMode.FAIL_CLOSED
