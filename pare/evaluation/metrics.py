from collections import defaultdict
from math import sqrt
def wilson(k,n,z=1.96):
    if n==0:return(0.0,0.0)
    p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*sqrt((p*(1-p)+z*z/(4*n))/n)/d;return(max(0,c-h),min(1,c+h))
def summarize(rows):
    n=len(rows);s=lambda k:sum(r[k] for r in rows);succ=s('oracle_success');verified=[r for r in rows if r['final_verdict']=='VERIFIED_SUCCESS'];state=[r for r in rows if r['state_repair_required']];repair_attempt=[r for r in rows if r['state_repair_attempted']]
    return {'cases':n,'recovery_success_rate':succ/n if n else 0,'recovery_success_ci95':wilson(succ,n),'false_completion_rate':s('false_completion')/n if n else 0,'verified_success_precision':sum(r['oracle_success'] for r in verified)/len(verified) if verified else 1.0,'duplicate_side_effect_rate':s('duplicate_side_effects')/n if n else 0,'destructive_side_effect_rate':s('destructive_side_effects')/n if n else 0,'unnecessary_recovery_rate':s('unnecessary_recovery')/n if n else 0,'benign_state_preservation_rate':s('benign_preserved')/n if n else 0,'affected_state_invalidation_recall':sum(r['affected_state_invalidated'] for r in state)/len(state) if state else 1.0,'state_repair_precision':sum(r['state_repair_correct'] for r in repair_attempt)/len(repair_attempt) if repair_attempt else 1.0,'state_repair_recall':sum(r['state_repair_correct'] for r in state)/len(state) if state else 1.0,'mean_recovery_actions':s('recovery_actions')/n if n else 0,'mean_verification_actions':s('verification_actions')/n if n else 0,'recovery_latency':s('recovery_latency')/n if n else 0,'recovery_cost_proxy':s('recovery_cost_proxy')/n if n else 0,'fail_closed_correctness':sum(r['fail_closed_correct'] for r in rows if not r['oracle_success'])/max(1,sum(1 for r in rows if not r['oracle_success'])),'retry_budget_violations':s('retry_budget_violations'),'inconclusive_to_completed_violations':s('inconclusive_to_completed_violations'),'post_recovery_verification_coverage':s('post_recovery_verification')/n if n else 0,'destructive_duplicate_side_effects':sum(1 for r in rows if r['duplicate_side_effects'] and r['destructive_side_effects'])}
def stratify(rows,key):
    d=defaultdict(list)
    for r in rows:d[r[key]].append(r)
    return {k:summarize(v) for k,v in sorted(d.items())}
