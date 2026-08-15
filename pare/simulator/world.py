from __future__ import annotations
from dataclasses import dataclass, field
import copy, hashlib, json
@dataclass
class World:
    resources: dict[str,list[dict]]=field(default_factory=dict); assertions:dict[str,dict]=field(default_factory=dict); ledger:list[dict]=field(default_factory=list); tick:int=0; seen_keys:set[str]=field(default_factory=set)
    def clone(self): return copy.deepcopy(self)
    def canonical(self): return {'resources':self.resources,'assertions':self.assertions,'ledger':self.ledger,'tick':self.tick,'seen_keys':sorted(self.seen_keys)}
    def hash(self): return hashlib.sha256(json.dumps(self.canonical(),sort_keys=True,separators=(',',':')).encode()).hexdigest()
    def add(self,domain,item,idempotency_key=''):
        if idempotency_key and idempotency_key in self.seen_keys:
            self.ledger.append({'tick':self.tick,'event':'idempotent_noop','key':idempotency_key}); return False
        self.resources.setdefault(domain,[]).append(copy.deepcopy(item))
        if idempotency_key:self.seen_keys.add(idempotency_key)
        self.ledger.append({'tick':self.tick,'event':'add','domain':domain,'item':copy.deepcopy(item)});return True
    def remove_matching(self,domain,rid):
        xs=self.resources.get(domain,[]);before=len(xs);self.resources[domain]=[x for x in xs if x.get('id')!=rid]
        if len(self.resources[domain])!=before:self.ledger.append({'tick':self.tick,'event':'remove','domain':domain,'id':rid})
    def set_assertion(self,key,value,source): self.assertions[key]={'value':value,'source':source,'valid':True};self.ledger.append({'tick':self.tick,'event':'assert','key':key,'value':value,'source':source})
    def invalidate(self,key,reason):
        if key in self.assertions:self.assertions[key]['valid']=False;self.assertions[key]['invalid_reason']=reason
