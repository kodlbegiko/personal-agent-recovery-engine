from dataclasses import dataclass,asdict
import hashlib,json,random
from pare.simulator.faults import FAULTS
DOMAINS=('messaging','calendar','files','tasks','personal_state','composite')
@dataclass(frozen=True)
class Scenario:
    scenario_id:str;split:str;domain:str;fault:str;risk_class:str;reversibility_class:str;resource_id:str;target_value:str;target:str;action_id:str;assertion_key:str;requires_assertion:bool;postcondition:dict;seed:int
def generate(split,count,seed):
    rng=random.Random(seed);out=[]
    for i in range(count):
        domain=DOMAINS[i%len(DOMAINS)];fault=FAULTS[(i*5+seed)%len(FAULTS)];risk='high' if fault in {'WRONG_TARGET','DUPLICATE_DELIVERY','COMPENSATION_FAILURE'} else ('medium' if i%3==0 else 'low');reversible='irreversible' if domain=='messaging' and i%4==0 else 'reversible';rid=f'{domain}-{i:04d}';val=f'v-{(i*7)%23}';target=f'{domain}-target-{i%9}';aid=f'a-{split}-{i:04d}';req=domain in {'personal_state','composite'}
        out.append(Scenario(f'{split}-{i:04d}',split,domain,fault,risk,reversible,rid,val,target,aid,f'state:{rid}',req,{'resource_id':rid,'value':val,'target':target,'assertion_required':req},rng.getrandbits(32)))
    return out
def manifest(scenarios):return hashlib.sha256(json.dumps([asdict(s) for s in scenarios],sort_keys=True,separators=(',',':')).encode()).hexdigest()
