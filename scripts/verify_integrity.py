from pathlib import Path
import sys
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from pare.benchmark.generator import generate,manifest,DOMAINS
from pare.simulator.faults import FAULTS
from pare.evaluation.state_machine import transition
xs=generate('development',180,1101)+generate('validation',120,2202)
assert len(xs)>=300 and {x.domain for x in xs}==set(DOMAINS) and {x.fault for x in xs}==set(FAULTS)
assert manifest(generate('x',60,7))==manifest(generate('x',60,7))
for p in (root/'pare'/'candidates').glob('*.py'):
    t=p.read_text();assert 'simulator.oracle' not in t and 'oracle_success' not in t
try:transition('INCONCLUSIVE','COMPLETED');raise AssertionError('illegal transition accepted')
except ValueError:pass
print('integrity checks passed')
