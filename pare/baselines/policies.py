from dataclasses import dataclass
from pare.contracts.models import RecoveryMode
@dataclass(frozen=True)
class PolicyConfig:name:str;verify_before_retry:bool=False;idempotency:bool=False;conservative:bool=False;retry_budget:int=0
def decide_baseline(cfg,outcome,verification,scenario):
    if verification.verdict.value=='VERIFIED_SUCCESS':return RecoveryMode.NO_ACTION
    if cfg.conservative:return RecoveryMode.FAIL_CLOSED
    if cfg.verify_before_retry and verification.verdict.value=='INCONCLUSIVE':return RecoveryMode.WAIT_AND_REVERIFY
    if cfg.retry_budget>0:return RecoveryMode.IDEMPOTENT_RETRY
    return RecoveryMode.FAIL_CLOSED
BASELINES={'B0':PolicyConfig('B0-No-Recovery'),'B1':PolicyConfig('B1-Blind-Retry-Once',retry_budget=1),'B2':PolicyConfig('B2-Bounded-Retry',retry_budget=2),'B3':PolicyConfig('B3-Verify-Before-Retry',verify_before_retry=True,retry_budget=1),'B4':PolicyConfig('B4-Idempotency-Aware',verify_before_retry=True,idempotency=True,retry_budget=1),'B5':PolicyConfig('B5-Conservative-Fail-Closed',conservative=True)}
