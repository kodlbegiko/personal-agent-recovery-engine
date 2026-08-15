from dataclasses import dataclass,field
@dataclass
class RepairEntry:assertion:str;action:str;reason:str;prior_valid:bool;restored_value:str
@dataclass
class StateRepairLedger:
    entries:list[RepairEntry]=field(default_factory=list)
    def repair(self,world,scenario,reason):
        if not scenario.requires_assertion:return
        prior=world.assertions.get(scenario.assertion_key,{});prior_valid=bool(prior.get('valid'));world.invalidate(scenario.assertion_key,reason);world.set_assertion(scenario.assertion_key,scenario.target_value,scenario.action_id);self.entries.append(RepairEntry(scenario.assertion_key,scenario.action_id,reason,prior_valid,scenario.target_value))
