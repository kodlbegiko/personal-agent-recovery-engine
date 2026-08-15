import random
def paired_delta(rows_a,rows_b,metric='oracle_success',seed=20260815,reps=4000):
    a={r['scenario_id']:r for r in rows_a};b={r['scenario_id']:r for r in rows_b};ids=sorted(set(a)&set(b));diffs=[a[i][metric]-b[i][metric] for i in ids];obs=sum(diffs)/len(diffs) if diffs else 0.0;rng=random.Random(seed);boots=[]
    for _ in range(reps):
        sm=[rng.choice(diffs) for _ in diffs];boots.append(sum(sm)/len(sm) if sm else 0.0)
    boots.sort();lo=boots[int(.025*len(boots))] if boots else 0;hi=boots[int(.975*len(boots))-1] if boots else 0;return {'metric':metric,'n':len(diffs),'delta':obs,'bootstrap_ci95':[lo,hi]}
