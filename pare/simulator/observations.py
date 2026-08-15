from pare.contracts.models import VerificationRecord,VerificationVerdict
def verify(world,scenario,round_no=1):
    if scenario.fault=='VERIFIER_UNAVAILABLE':return VerificationRecord(f'v-{scenario.action_id}-{round_no}',scenario.action_id,scenario.postcondition,{'available':False},VerificationVerdict.INCONCLUSIVE,True,{})
    if scenario.fault=='DELAYED_VISIBILITY' and round_no==1:return VerificationRecord(f'v-{scenario.action_id}-{round_no}',scenario.action_id,scenario.postcondition,{'visible':False,'reason':'delayed'},VerificationVerdict.INCONCLUSIVE,True,{})
    xs=world.resources.get(scenario.domain,[]);exact=[x for x in xs if x.get('id')==scenario.resource_id and x.get('value')==scenario.target_value and x.get('target')==scenario.target];wrong=[x for x in xs if x.get('id')==scenario.resource_id and (x.get('value')!=scenario.target_value or x.get('target')!=scenario.target)];duplicates=sum(1 for x in xs if x.get('id')==scenario.resource_id);state_ok=True
    if scenario.requires_assertion:
        a=world.assertions.get(scenario.assertion_key);state_ok=bool(a and a.get('valid') and a.get('value')==scenario.target_value)
    verdict=VerificationVerdict.VERIFIED_SUCCESS if exact and duplicates==1 and state_ok else VerificationVerdict.VERIFIED_FAILURE
    return VerificationRecord(f'v-{scenario.action_id}-{round_no}',scenario.action_id,scenario.postcondition,{'exact':len(exact),'duplicates':duplicates,'wrong':len(wrong),'state_ok':state_ok},verdict,verdict!=VerificationVerdict.VERIFIED_SUCCESS,{})
