from dataclasses import dataclass
@dataclass(frozen=True)
class Outcome: result:str; observation:dict; committed:bool; duplicate_count:int=0
def execute(world,scenario,idempotency_key,recovery=False):
    world.tick+=1;f=scenario.fault;item={'id':scenario.resource_id,'value':scenario.target_value,'target':scenario.target}
    if recovery and f in {'RECOVERY_FAILURE','ROLLBACK_FAILURE','COMPENSATION_FAILURE'}:return Outcome('ERROR',{'error':'recovery_operation_failed','side_effect':'unknown'},False)
    if f in {'PRE_DISPATCH_FAILURE','CRASH_BEFORE_COMMIT'}:return Outcome('ERROR',{'error':f,'side_effect':'none'},False)
    if f=='WRONG_TARGET':
        wrong=dict(item);wrong['target']='wrong-target';world.add(scenario.domain,wrong,idempotency_key);return Outcome('SUCCESS',{'status':'ok','target':'wrong-target'},True)
    if f=='DUPLICATE_DELIVERY':world.add(scenario.domain,item,idempotency_key);world.add(scenario.domain,item,'');return Outcome('SUCCESS',{'status':'ok','duplicate_possible':True},True,2)
    if f=='PARTIAL_MUTATION':
        partial=dict(item);partial['value']='PARTIAL';world.add(scenario.domain,partial,idempotency_key);return Outcome('ERROR',{'error':'partial_mutation','side_effect':'partial'},True)
    if f=='STATE_WRITE_CORRUPTION':world.add(scenario.domain,item,idempotency_key);world.set_assertion(scenario.assertion_key,'CORRUPT',scenario.action_id);return Outcome('SUCCESS',{'status':'ok','state_write':'failed'},True)
    if f=='CONCURRENT_MUTATION':world.add(scenario.domain,item,idempotency_key);world.resources[scenario.domain][-1]['value']='EXTERNAL';return Outcome('SUCCESS',{'status':'ok'},True)
    world.add(scenario.domain,item,idempotency_key)
    if f=='POST_COMMIT_TIMEOUT':return Outcome('TIMEOUT',{'error':'timeout','side_effect':'unknown'},True)
    if f=='CRASH_AFTER_COMMIT':return Outcome('CRASH',{'error':'crash','side_effect':'unknown'},True)
    if f=='OUT_OF_ORDER_OBSERVATION':return Outcome('SUCCESS',{'status':'old_ack','side_effect':'unknown'},True)
    if f=='DELAYED_VISIBILITY':return Outcome('SUCCESS',{'status':'ok','visibility':'delayed'},True)
    if f=='STALE_READ':return Outcome('SUCCESS',{'status':'ok','read':'stale'},True)
    if f=='VERIFIER_UNAVAILABLE':return Outcome('SUCCESS',{'status':'ok'},True)
    if f in {'RECOVERY_FAILURE','ROLLBACK_FAILURE','COMPENSATION_FAILURE'}:return Outcome('ERROR',{'error':f,'side_effect':'unknown'},True)
    return Outcome('SUCCESS',{'status':'ok'},True)
