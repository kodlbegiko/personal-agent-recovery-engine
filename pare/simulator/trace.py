def event(world,event,**fields):world.ledger.append({'tick':world.tick,'event':event,**fields})
