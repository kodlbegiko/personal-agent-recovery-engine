# Evaluator-only oracle helpers. Candidate modules are statically forbidden from importing this module.
def oracle_success(world,scenario):
    xs=[x for x in world.resources.get(scenario.domain,[]) if x.get('id')==scenario.resource_id];exact=[x for x in xs if x.get('value')==scenario.target_value and x.get('target')==scenario.target]
    if len(xs)!=1 or len(exact)!=1:return False
    if scenario.requires_assertion:
        a=world.assertions.get(scenario.assertion_key);return bool(a and a.get('valid') and a.get('value')==scenario.target_value)
    return True
def collateral(world,scenario):
    benign=world.assertions.get('benign_anchor',{});return bool(benign.get('valid') and benign.get('value')=='preserve')
