from defs import *


def run_miner(creep):
    if creep.memory.target_room == None:
        print('Miner ' + creep.name + ' is lacking target_room.')
        return
    if creep.room.name != creep.memory.target_room:
        exitpos = creep.pos.findClosestByPath(Game.map.findRoute(creep.room.name, creep.memory.target_room)[0].exit, {'ignoreCreeps': True})
        creep.moveTo(exitpos)
        return
    target = Game.getObjectById(creep.memory.target)
    if target == None:
        print('Miner ' + creep.name + ' is lacking target source.')
        return
    if creep.memory.container == None:
        creep.memory.container = ''
        containers = filter(lambda s: s.structureType == STRUCTURE_CONTAINER, target.pos.findInRange(FIND_STRUCTURES, 1))
        if containers != '':
            creep.memory.container = _.sample(containers).id
    container = None
    if creep.memory.container != None and creep.memory.container != '':
        container = Game.getObjectById(creep.memory.container)
    if container:
        if creep.pos.isEqualTo(container):
            creep.harvest(target)
        else:
            creep.moveTo(container)
    else:
        if creep.pos.isNearTo(target):
            creep.harvest(target)
        else:
            creep.moveTo(target)

