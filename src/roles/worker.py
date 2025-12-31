from defs import *


def run_worker(creep):
    if creep.memory.target_room == None:
        print('Worker ' + creep.name + ' is lacking target_room.')
        return
    if creep.room.name != creep.memory.target_room:
        exitpos = creep.pos.findClosestByPath(Game.map.findRoute(creep.room.name, creep.memory.target_room)[0].exit, {'ignoreCreeps': True})
        creep.moveTo(exitpos)
        return
    if creep.memory.task != "idle":
        if creep.memory.check_delay == None:
            creep.memory.check_delay = 0
        else:
            creep.memory.check_delay += 1
            if creep.memory.check_delay > 100 and creep.store[RESOURCE_ENERGY] == 0:
                creep.memory.task = "idle"
    target = None
    if creep.memory.task != "idle":
        target = Game.getObjectById(creep.memory.target)
        if target == None or creep.memory.task == 'repairing' and target.hits >= target.hitsMax:
            creep.memory.task = "idle"
    if creep.memory.task == "idle":
        if creep.room.controller.ticksToDowngrade < CONTROLLER_DOWNGRADE[creep.room.controller.level] - 3000:
            creep.memory.target = creep.room.controller.id
            creep.memory.task = 'upgrading'
            target = creep.room.controller
            creep.memory.check_delay = 0
        else:
            repair_structs = filter(lambda s: s.my and s.hits < s.hitsMax or [STRUCTURE_ROAD, STRUCTURE_CONTAINER].includes(s.structureType) and s.hits * 2 < s.hitsMax, creep.room.find(FIND_STRUCTURES))
            if len(repair_structs) > 0:
                target = creep.pos.findClosestByPath(repair_structs, {'ignoreCreeps': True, 'range': 3})
                if target != None:
                    creep.memory.target = target.id
                    creep.memory.task = 'repairing'
                    creep.memory.check_delay = 0
                else:
                    print('No path to repair structures for worker ' + creep.name)
            else:
                sites = creep.room.find(FIND_MY_CONSTRUCTION_SITES)
                if len(sites) > 0:
                    target = creep.pos.findClosestByPath(sites, {'ignoreCreeps': True, 'range': 3})
                    if target != None:
                        creep.memory.target = target.id
                        creep.memory.task = 'building'
                        creep.memory.check_delay = 0
                    else:
                        print('No path to construction sites for worker ' + creep.name)
                else:
                    creep.memory.target = creep.room.controller.id
                    creep.memory.task = 'upgrading'
                    target = creep.room.controller
                    creep.memory.check_delay = 0
    if creep.memory.task == 'upgrading' and target != None:
        if creep.pos.inRangeTo(target, 3):
            creep.upgradeController(target)
        else:
            creep.moveTo(target)
    if creep.memory.task == 'repairing' and target != None:
        if creep.pos.inRangeTo(target, 3):
            creep.repair(target)
        else:
            creep.moveTo(target)
    if creep.memory.task == 'building' and target != None:
        if creep.pos.inRangeTo(target, 3):
            creep.build(target)
        else:
            creep.moveTo(target)