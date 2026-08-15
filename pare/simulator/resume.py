from pare.simulator.observations import verify
def crash_resume(world,scenario):
    restarted=world.clone();return restarted,verify(restarted,scenario,2)
