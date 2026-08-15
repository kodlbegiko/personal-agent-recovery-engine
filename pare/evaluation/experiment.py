import csv,hashlib,json,os,secrets,sys
from datetime import datetime,timezone
from pathlib import Path
from pare.benchmark.generator import generate,manifest
from pare.benchmark.adversarial import generate_adversarial
from pare.evaluation.runner import run_suite
from pare.evaluation.metrics import summarize,stratify
from pare.evaluation.statistics import paired_delta
from pare.candidates.policy import CandidateConfig,POLICY_VERSION
ROOT=Path(__file__).resolve().parents[2]
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def dumpj(path,obj):p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,sort_keys=True),encoding='utf-8')
def writecsv(path,rows):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
    if not rows:return
    keys=[]
    for r in rows:
        for k in r:
            if k not in keys:keys.append(k)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows([{k:(json.dumps(v,sort_keys=True) if isinstance(v,(dict,list,tuple)) else v) for k,v in r.items()} for r in rows])
def qualifies(rows):
    m=summarize(rows);return m['inconclusive_to_completed_violations']==0 and m['retry_budget_violations']==0 and m['destructive_duplicate_side_effects']==0 and m['post_recovery_verification_coverage']==1.0 and m['false_completion_rate']<=0.05
def main():
    candidate_commit=os.environ.get('PARE_CANDIDATE_COMMIT_SHA','UNCOMMITTED');dev=generate('development',180,1101);val=generate('validation',120,2202);methods=['B0','B1','B2','B3','B4','B5','Candidate-v1','Candidate-v2','Candidate-v3'];configs={'Candidate-v1':CandidateConfig(name='Candidate-v1',dependency_graph=False,minimal_rollback=False,state_repair=False),'Candidate-v2':CandidateConfig(name='Candidate-v2'),'Candidate-v3':CandidateConfig(name='Candidate-v3')};val_results={};all_summary=[]
    for m in methods:
        dr=run_suite(dev,m,configs.get(m));vr=run_suite(val,m,configs.get(m));val_results[m]=vr;writecsv(f'results/development/{m}.csv',dr);writecsv(f'results/validation/{m}.csv',vr);all_summary += [{'split':'development','method':m,**summarize(dr)},{'split':'validation','method':m,**summarize(vr)}]
    cq=[m for m in methods[6:] if qualifies(val_results[m])]
    if not cq:selected='Candidate-v3'
    else:
        cq.sort(key=lambda m:(summarize(val_results[m])['recovery_success_rate'],summarize(val_results[m])['benign_state_preservation_rate'],-summarize(val_results[m])['duplicate_side_effect_rate'],-summarize(val_results[m])['mean_recovery_actions'],-methods.index(m)),reverse=True);selected=cq[0]
    bq=[m for m in methods[:6] if qualifies(val_results[m])];pool=bq or methods[:6];strongest=max(pool,key=lambda m:(summarize(val_results[m])['recovery_success_rate'],summarize(val_results[m])['benign_state_preservation_rate'],-summarize(val_results[m])['duplicate_side_effect_rate']));dumpj('artifacts/selection.json',{'selected_candidate':selected,'qualifying_candidates':cq,'strongest_baseline':strongest,'qualifying_baselines':bq})
    freeze={'protocol_sha256':sha('RESEARCH_PROTOCOL.md'),'benchmark_generator_sha256':sha('pare/benchmark/generator.py'),'metric_definition_sha256':sha('pare/evaluation/metrics.py'),'candidate_commit_sha':candidate_commit,'candidate_source_sha256':sha('pare/candidates/policy.py'),'policy_sha256':sha('pare/candidates/policy.py'),'candidate_version':selected,'policy_version':POLICY_VERSION,'baseline_versions':['B0','B1','B2','B3','B4','B5'],'environment':{'python':sys.version.split()[0]},'freeze_timestamp':datetime.now(timezone.utc).isoformat()};raw=json.dumps(freeze,sort_keys=True,separators=(',',':')).encode();freeze['freeze_manifest_sha256']=hashlib.sha256(raw).hexdigest();dumpj('artifacts/freeze-manifest.json',freeze)
    seed_path=ROOT/'evidence/protected/seed.json'
    if seed_path.exists():seed=json.loads(seed_path.read_text())['seed']
    else:seed=secrets.randbits(63);dumpj('evidence/protected/seed.json',{'seed':seed,'provenance':'Python secrets.randbits(63) after freeze manifest creation','generator_sha256':freeze['benchmark_generator_sha256'],'candidate_commit_sha':candidate_commit})
    protected=generate('protected',72,seed);dumpj('evidence/protected/scenario-manifest.json',{'count':len(protected),'manifest_sha256':manifest(protected)});scfg=configs.get(selected,CandidateConfig(name=selected));pr=run_suite(protected,selected,scfg);br=run_suite(protected,strongest);writecsv('results/protected/selected.csv',pr);writecsv('results/protected/strongest-baseline.csv',br);psm=summarize(pr);bsm=summarize(br);stats=paired_delta(pr,br);dumpj('results/protected/summary.json',{'selected':psm,'baseline':bsm,'paired':stats,'selected_candidate':selected,'strongest_baseline':strongest})
    robust=generate('robustness',96,3303);ablations={'full':CandidateConfig(name=selected),'no_idempotency':CandidateConfig(name=selected,idempotency=False),'no_verify_before_retry':CandidateConfig(name=selected,verify_before_retry=False),'no_risk_layer':CandidateConfig(name=selected,risk_layer=False),'no_dependency_graph':CandidateConfig(name=selected,dependency_graph=False),'no_minimal_rollback':CandidateConfig(name=selected,minimal_rollback=False),'no_state_repair':CandidateConfig(name=selected,state_repair=False),'no_reverification':CandidateConfig(name=selected,reverification=False)};abrows=[]
    for name,cfg in ablations.items():abrows.append({'ablation':name,**summarize(run_suite(robust,selected,cfg))})
    writecsv('results/ablation_results.csv',abrows);adv=run_suite(generate_adversarial(),selected,scfg);writecsv('results/adversarial_results.csv',adv);writecsv('results/overall_metrics.csv',all_summary+[{'split':'protected','method':selected,**psm},{'split':'protected','method':strongest,**bsm}]);writecsv('results/by_domain.csv',[{'method':selected,'domain':k,**v} for k,v in stratify(pr,'domain').items()]);writecsv('results/by_failure_class.csv',[{'method':selected,'fault':k,**v} for k,v in stratify(pr,'fault').items()]);writecsv('results/recovery_mode_distribution.csv',[{'mode':m,'count':sum(1 for r in pr if r['mode']==m)} for m in sorted({r['mode'] for r in pr})]);writecsv('results/state_repair_metrics.csv',[r for r in pr if r['state_repair_required'] or r['state_repair_attempted']]);cm=[]
    for verdict in sorted({r['final_verdict'] for r in pr}):
        for truth in (0,1):cm.append({'final_verdict':verdict,'oracle_success':truth,'count':sum(1 for r in pr if r['final_verdict']==verdict and r['oracle_success']==truth)})
    writecsv('results/confusion_matrix.csv',cm);writecsv('results/paired_comparison.csv',[stats]);dumpj('results/paired_comparison.json',stats);capability=(psm['false_completion_rate']<=.05 and psm['destructive_duplicate_side_effects']==0 and psm['retry_budget_violations']==0 and psm['inconclusive_to_completed_violations']==0 and psm['post_recovery_verification_coverage']==1.0 and stats['delta']>0 and stats['bootstrap_ci95'][0]>=0);terminal='READY_FOR_UMBRELLA_INTEGRATION' if capability else ('PROTECTED_RESULT_NEGATIVE' if psm['recovery_success_rate']<bsm['recovery_success_rate'] or psm['false_completion_rate']>.05 else 'PROTECTED_RESULT_INCONCLUSIVE');dumpj('artifacts/terminal.json',{'terminal_state':terminal,'scientific_success':True,'capability_success':capability,'selected_candidate':selected,'strongest_baseline':strongest});dumpj('artifacts/reproducibility-manifest.json',{'development_manifest':manifest(dev),'validation_manifest':manifest(val),'protected_manifest':manifest(protected),'generator_sha256':freeze['benchmark_generator_sha256'],'metrics_sha256':freeze['metric_definition_sha256'],'candidate_sha256':freeze['candidate_source_sha256'],'candidate_commit_sha':candidate_commit});print(json.dumps({'terminal':terminal,'selected':selected,'baseline':strongest,'protected':psm,'paired':stats,'adversarial':summarize(adv)},indent=2))
if __name__=='__main__':main()
