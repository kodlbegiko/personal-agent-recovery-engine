from dataclasses import dataclass
@dataclass(frozen=True)
class ImpactSet:affected_resources:tuple[str,...];affected_assertions:tuple[str,...];preserved_assertions:tuple[str,...]
class ImpactGraph:
    def analyze(self,scenario,world):
        affected=(scenario.assertion_key,) if scenario.requires_assertion else ();preserved=tuple(sorted(k for k in world.assertions if k not in affected));return ImpactSet((scenario.resource_id,),affected,preserved)
