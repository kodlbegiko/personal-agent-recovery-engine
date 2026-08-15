import pytest
from dataclasses import replace
from pare.contracts.models import ActionAttempt,validate_contract
from pare.evaluation.state_machine import transition
from pare.benchmark.generator import generate,manifest,DOMAINS
from pare.simulator.faults import FAULTS
from pare.evaluation.runner import run_suite
from pare.simulator.world import World
from pare.simulator.actions import execute
from pare.simulator.resume import crash_resume
from pare.candidates.impact import ImpactGraph
from pare.candidates.state_repair import StateRepairLedger

def test_contract_validation():validate_contract(ActionAttempt('a','p','sim','create',{},'auth','low','reversible',1,2,'SUCCESS',(),'k'))
def test_inconclusive_completed_illegal():
    with pytest.raises(ValueError):transition('INCONCLUSIVE','COMPLETED')
def test_happy_transition():assert transition('ACTION_STARTED','ACTION_RETURNED')=='ACTION_RETURNED'
def test_scale_and_coverage():
    xs=generate('development',180,1101)+generate('validation',120,2202);assert len(xs)>=300;assert {x.domain for x in xs}==set(DOMAINS);assert {x.fault for x in xs}==set(FAULTS)
def test_determinism():assert manifest(generate('x',60,7))==manifest(generate('x',60,7))
def test_no_unbounded_retry():assert sum(r['retry_budget_violations'] for r in run_suite(generate('t',96,12)))==0
def test_hash_stable_for_clones():
    w=World();w.add('files',{'id':'x'},'k');assert w.hash()==w.clone().hash()
def test_candidates_do_not_import_oracle():
    from pathlib import Path
    for p in Path('pare/candidates').glob('*.py'):assert 'simulator.oracle' not in p.read_text() and 'oracle_success' not in p.read_text()
def test_minimal_state_repair_preserves_benign():
    s=next(x for x in generate('x',20,3) if x.requires_assertion);w=World();w.set_assertion('benign_anchor','preserve','fixture');w.set_assertion(s.assertion_key,'bad','old');impact=ImpactGraph().analyze(s,w);assert 'benign_anchor' in impact.preserved_assertions;l=StateRepairLedger();l.repair(w,s,'test');assert w.assertions[s.assertion_key]['value']==s.target_value and w.assertions['benign_anchor']['value']=='preserve'
def test_crash_after_commit_resume_verifies_without_duplicate():
    s=replace(generate('x',1,1)[0],fault='CRASH_AFTER_COMMIT');w=World();execute(w,s,'k');r,v=crash_resume(w,s);assert v.verdict.value=='VERIFIED_SUCCESS';assert len(r.resources[s.domain])==1
def test_no_absolute_user_file_access():
    from pathlib import Path
    for p in Path('pare').rglob('*.py'):assert "open('/" not in p.read_text()
