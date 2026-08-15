from pare.simulator.world import World
from pare.simulator.actions import execute
from pare.simulator.observations import verify
from pare.simulator.oracle import oracle_success,collateral
from pare.baselines.policies import BASELINES,decide_baseline
from pare.candidates.policy import CandidateConfig,decide
from pare.candidates.impact import ImpactGraph
from pare.candidates.state_repair import StateRepairLedger
from pare.contracts.models import RecoveryMode,VerificationVerdict

def _repair(world,scenario,mode,cfg,attempt_key):
    ops=[];attempts=0;ledger=StateRepairLedger();impact=ImpactGraph().analyze(scenario,world)
    if mode==RecoveryMode.WAIT_AND_REVERIFY:return ops,attempts,ledger,impact
    if mode==RecoveryMode.IDEMPOTENT_RETRY:
        attempts=1;execute(world,scenario,attempt_key,recovery=True);ops.append('retry')
    elif mode in {RecoveryMode.COMPENSATE,RecoveryMode.ROLLBACK}:
        attempts=1;world.remove_matching(scenario.domain,scenario.resource_id);ops.append(mode.value.lower())
        if scenario.fault not in {'PRE_DISPATCH_FAILURE','CRASH_BEFORE_COMMIT','RECOVERY_FAILURE','ROLLBACK_FAILURE','COMPENSATION_FAILURE'}:
            world.add(scenario.domain,{'id':scenario.resource_id,'value':scenario.target_value,'target':scenario.target},attempt_key+'-repair');ops.append('restore_expected')
    if cfg and cfg.state_repair and scenario.requires_assertion:ledger.repair(world,scenario,f'{mode.value}:dependency_repair');ops.append('repair_assertion')
    return ops,attempts,ledger,impact

def run_case(scenario,method='Candidate-v3',cfg=None):
    world=World();world.set_assertion('benign_anchor','preserve','fixture');pre=world.hash();key=f'idem:{scenario.action_id}';idem=method in {'B4','Candidate-v2','Candidate-v3'};outcome=execute(world,scenario,key if idem else '')
    if scenario.requires_assertion and scenario.fault not in {'STATE_WRITE_CORRUPTION','PRE_DISPATCH_FAILURE','CRASH_BEFORE_COMMIT'}:world.set_assertion(scenario.assertion_key,scenario.target_value,scenario.action_id)
    v1=verify(world,scenario,1);pre_ok=oracle_success(world,scenario)
    if method.startswith('B'):
        bc=BASELINES[method];mode=decide_baseline(bc,outcome,v1,scenario);local=CandidateConfig(name=method,idempotency=bc.idempotency,state_repair=False,minimal_rollback=False,reverification=True)
    else:local=cfg or CandidateConfig(name=method);mode=decide(outcome,v1,scenario,local)
    ops=[];retry=0;entries=[];affected=()
    if mode==RecoveryMode.WAIT_AND_REVERIFY:
        v2=verify(world,scenario,2)
        if v2.verdict==VerificationVerdict.VERIFIED_SUCCESS:final=v2
        else:
            mode2=RecoveryMode.IDEMPOTENT_RETRY if method.startswith('B') and BASELINES[method].retry_budget>0 else (decide(outcome,v2,scenario,local) if not method.startswith('B') else RecoveryMode.FAIL_CLOSED)
            if mode2 not in {RecoveryMode.FAIL_CLOSED,RecoveryMode.NO_ACTION,RecoveryMode.WAIT_AND_REVERIFY}:
                x,a,l,i=_repair(world,scenario,mode2,local,key);ops+=x;retry+=a;entries+=l.entries;affected=i.affected_assertions
            final=verify(world,scenario,3) if local.reverification else v2
    elif mode not in {RecoveryMode.NO_ACTION,RecoveryMode.FAIL_CLOSED,RecoveryMode.ESCALATE}:
        x,a,l,i=_repair(world,scenario,mode,local,key);ops+=x;retry+=a;entries+=l.entries;affected=i.affected_assertions;final=verify(world,scenario,2) if local.reverification else v1
    else:final=v1
    ok=oracle_success(world,scenario);ben=collateral(world,scenario);xs=[x for x in world.resources.get(scenario.domain,[]) if x.get('id')==scenario.resource_id];dup=max(0,len(xs)-1);destructive=1 if any(x.get('target')!=scenario.target for x in xs) else 0;false_completion=1 if final.verdict==VerificationVerdict.VERIFIED_SUCCESS and not ok else 0;inc=1 if v1.verdict==VerificationVerdict.INCONCLUSIVE and final.verdict==VerificationVerdict.VERIFIED_SUCCESS and not ok else 0;post_cov=1 if local.reverification or mode in {RecoveryMode.NO_ACTION,RecoveryMode.FAIL_CLOSED,RecoveryMode.WAIT_AND_REVERIFY} else 0;state_required=int(scenario.requires_assertion and not pre_ok);state_correct=int((not state_required) or bool(world.assertions.get(scenario.assertion_key,{}).get('valid') and world.assertions.get(scenario.assertion_key,{}).get('value')==scenario.target_value));repaired=int(bool(entries));invalidated=int(any(e.assertion in affected for e in entries))
    return {'scenario_id':scenario.scenario_id,'domain':scenario.domain,'fault':scenario.fault,'method':method,'oracle_success':int(ok),'pre_recovery_oracle_success':int(pre_ok),'false_completion':false_completion,'duplicate_side_effects':dup,'destructive_side_effects':destructive,'benign_preserved':int(ben),'unnecessary_recovery':int(bool(ops) and pre_ok),'recovery_actions':len(ops),'verification_actions':1+(final.verification_id!=v1.verification_id),'recovery_latency':len(ops)+1+(final.verification_id!=v1.verification_id),'recovery_cost_proxy':len(ops)*2+1+(final.verification_id!=v1.verification_id),'fail_closed_correct':int(mode==RecoveryMode.FAIL_CLOSED and not ok),'retry_budget_violations':int(retry>2),'inconclusive_to_completed_violations':inc,'post_recovery_verification':post_cov,'final_verdict':final.verdict.value,'mode':mode.value,'state_repair_required':state_required,'state_repair_attempted':repaired,'state_repair_correct':state_correct,'affected_state_invalidated':invalidated,'pre_hash':pre,'post_hash':world.hash(),'ops':ops,'observation':outcome.observation}
def run_suite(scenarios,method='Candidate-v3',cfg=None):return [run_case(s,method,cfg) for s in scenarios]
