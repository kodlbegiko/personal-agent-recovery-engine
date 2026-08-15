from dataclasses import replace
from .generator import generate
ADVERSARIAL={'timeout-after-success':'POST_COMMIT_TIMEOUT','false-negative-verification':'DELAYED_VISIBILITY','false-positive-observation':'OUT_OF_ORDER_OBSERVATION','two-consecutive-faults':'RECOVERY_FAILURE','recovery-timeout':'RECOVERY_FAILURE','crash-during-recovery':'CRASH_AFTER_COMMIT','stale-verifier':'STALE_READ','concurrent-external-actor':'CONCURRENT_MUTATION','duplicate-response':'DUPLICATE_DELIVERY','partial-rollback':'ROLLBACK_FAILURE','dependency-cycle':'STATE_WRITE_CORRUPTION','missing-provenance':'STATE_WRITE_CORRUPTION','corrupted-state-reference':'STATE_WRITE_CORRUPTION','wrong-idempotency-key':'DUPLICATE_DELIVERY'}
def generate_adversarial():
    base=generate('adversarial',len(ADVERSARIAL)*2,4404);labels=list(ADVERSARIAL);out=[]
    for i,s in enumerate(base):
        label=labels[i%len(labels)];out.append(replace(s,scenario_id=f'adversarial-{i:03d}-{label}',fault=ADVERSARIAL[label]))
    return out
