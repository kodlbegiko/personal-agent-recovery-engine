from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any

class VerificationVerdict(str, Enum):
    VERIFIED_SUCCESS='VERIFIED_SUCCESS'; VERIFIED_FAILURE='VERIFIED_FAILURE'; INCONCLUSIVE='INCONCLUSIVE'
class RecoveryMode(str, Enum):
    NO_ACTION='NO_ACTION'; WAIT_AND_REVERIFY='WAIT_AND_REVERIFY'; IDEMPOTENT_RETRY='IDEMPOTENT_RETRY'; COMPENSATE='COMPENSATE'; ROLLBACK='ROLLBACK'; REPLAN='REPLAN'; FAIL_CLOSED='FAIL_CLOSED'; ESCALATE='ESCALATE'
class RecoveryVerdict(str, Enum):
    VERIFIED_RECOVERED='VERIFIED_RECOVERED'; VERIFIED_UNRECOVERED='VERIFIED_UNRECOVERED'; INCONCLUSIVE='INCONCLUSIVE'

@dataclass(frozen=True)
class ActionAttempt:
    action_id:str; plan_ref:str; tool:str; operation:str; request:dict[str,Any]; authorization_ref:str
    risk_class:str; reversibility_class:str; started_at:int; finished_at:int; execution_result:str
    observed_side_effects:tuple[str,...]=(); idempotency_key:str=''

@dataclass(frozen=True)
class VerificationRecord:
    verification_id:str; action_id:str; success_criteria:dict[str,Any]; observations:dict[str,Any]
    verdict:VerificationVerdict; recovery_required:bool; state_updates:dict[str,Any]=field(default_factory=dict)

@dataclass(frozen=True)
class RecoveryDecision:
    recovery_decision_id:str; action_id:str; verification_id:str; state_snapshot_ref:str; failure_class:str
    side_effect_state:str; affected_resources:tuple[str,...]; affected_state_assertions:tuple[str,...]
    recovery_mode:RecoveryMode; risk_class:str; reversibility_class:str; retry_budget:int; idempotency_key:str
    required_postconditions:dict[str,Any]; reason_trace:tuple[str,...]; policy_version:str; created_at:int

@dataclass(frozen=True)
class RecoveryRecord:
    recovery_id:str; recovery_decision_id:str; operations:tuple[str,...]; observations:dict[str,Any]
    pre_recovery_state:str; post_recovery_state:str; preserved_state:tuple[str,...]; invalidated_state:tuple[str,...]
    restored_state:tuple[str,...]; verification_record_ref:str; verdict:RecoveryVerdict; attempt_count:int; terminal_reason:str

def validate_contract(obj: Any) -> None:
    data=asdict(obj)
    for k,v in data.items():
        if v is None: raise ValueError(f'{k} may not be None')
    if isinstance(obj, RecoveryDecision) and obj.retry_budget < 0: raise ValueError('retry_budget < 0')
    if isinstance(obj, ActionAttempt) and obj.finished_at < obj.started_at: raise ValueError('negative duration')
