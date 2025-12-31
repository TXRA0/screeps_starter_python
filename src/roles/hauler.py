from defs import *
import math
import random

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')
__pragma__('noalias', 'Object')


def run_hauler(creep):
    if creep.memory.target_room == None:
        print('Hauler ' + creep.name + ' is lacking target_room.')
        return
    if creep.room.name != creep.memory.target_room:
        exitpos = creep.pos.findClosestByPath(Game.map.findRoute(creep.room.name, creep.memory.target_room)[0].exit, {'ignoreCreeps': True})
        creep.moveTo(exitpos)
        return
    if creep.memory.task == None or ((creep.memory.task == "sucking" or creep.memory.task == "picking") and creep.store.getFreeCapacity() == 0) or (creep.memory.task == 'filling' and creep.store[RESOURCE_ENERGY] == 0):
        creep.memory.task = "idle"
    target = None
    if creep.memory.task != "idle":
        target = Game.getObjectById(creep.memory.target)
        if target == None or (creep.memory.task == 'filling' and target.store.getFreeCapacity(RESOURCE_ENERGY) == 0) or (creep.memory.task == 'sucking' and target.store[RESOURCE_ENERGY] < 20):
            creep.memory.task = "idle"
    if creep.memory.task == "idle" and creep.store[RESOURCE_ENERGY] > 0:
        fill_structs = filter(lambda s: [STRUCTURE_EXTENSION, STRUCTURE_SPAWN].includes(s.structureType) and s.store.getFreeCapacity(RESOURCE_ENERGY) > 0, creep.room.find(FIND_MY_STRUCTURES))
        if len(fill_structs) > 0:
            target = creep.pos.findClosestByPath(fill_structs, {'ignoreCreeps': True})
            if target != None:
                creep.memory.target = target.id
                creep.memory.task = 'filling'
            else:
                print('No path to fill structures for hauler ' + creep.name)
        else:
            fill_creeps = filter(lambda c: c.memory.role == 'worker' and c.store.getFreeCapacity(RESOURCE_ENERGY) > c.store.getUsedCapacity(RESOURCE_ENERGY), creep.room.find(FIND_MY_CREEPS))
            if len(fill_creeps) > 0:
                target = creep.pos.findClosestByPath(fill_creeps, {'ignoreCreeps': True})
                if target != None:
                    creep.memory.target = target.id
                    creep.memory.task = 'filling'
                else:
                    print('No path to fill creeps for hauler ' + creep.name)
    if creep.memory.task == "idle" and creep.store.getFreeCapacity() > 0:
        grab_piles = filter(lambda r: r.resourceType == RESOURCE_ENERGY and r.amount > 100, creep.room.find(FIND_DROPPED_RESOURCES))
        if len(grab_piles) > 0:
            target = creep.pos.findClosestByPath(grab_piles, {'ignoreCreeps': True})
            if target != None:
                creep.memory.target = target.id
                creep.memory.task = 'picking'
            else:
                print('No path to grab piles for hauler ' + creep.name)
        else:
            grab_containers = filter(lambda s: s.structureType == STRUCTURE_CONTAINER and s.store[RESOURCE_ENERGY] > 100, creep.room.find(FIND_STRUCTURES))
            if len(grab_containers) > 0:
                target = creep.pos.findClosestByPath(grab_containers, {'ignoreCreeps': True})
                if target != None:
                    creep.memory.target = target.id
                    creep.memory.task = 'sucking'
                else:
                    print('No path to grab containers for hauler ' + creep.name)
    if creep.memory.task == "picking" and target != None:
        if creep.pos.isNearTo(target):
            creep.pickup(target)
            creep.memory.task = "idle"
        else:
            creep.moveTo(target)
    if creep.memory.task == "sucking" and target != None:
        if creep.pos.isNearTo(target):
            creep.withdraw(target, RESOURCE_ENERGY)
            creep.memory.task = "idle"
        else:
            creep.moveTo(target)
    if creep.memory.task == "filling" and target != None:
        if creep.pos.isNearTo(target):
            creep.transfer(target, RESOURCE_ENERGY)
            creep.memory.task = "idle"
        else:
            creep.moveTo(target)
    if creep.memory.task == "idle" and ([0, 1, 48, 49].includes(creep.pos.x) or [0, 1, 48, 49].includes(creep.pos.y)):
        creep.moveTo(creep.room.controller)