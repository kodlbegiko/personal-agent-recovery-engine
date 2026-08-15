import hashlib,json
from pathlib import Path
r=Path(__file__).resolve().parents[1];p=r/'artifacts'/'freeze-manifest.json'
if not p.exists():print('freeze manifest unavailable before protected freeze');raise SystemExit(2)
m=json.loads(p.read_text());checks={'protocol_sha256':'RESEARCH_PROTOCOL.md','benchmark_generator_sha256':'pare/benchmark/generator.py','metric_definition_sha256':'pare/evaluation/metrics.py','candidate_source_sha256':'pare/candidates/policy.py'}
for k,f in checks.items():assert hashlib.sha256((r/f).read_bytes()).hexdigest()==m[k],f'{k} mismatch'
assert m.get('candidate_commit_sha') and m['candidate_commit_sha']!='UNCOMMITTED','candidate commit not frozen'
print('freeze verified')
