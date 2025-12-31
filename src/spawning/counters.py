from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')
__pragma__('noalias', 'Object')
from core.cache import Cache


def count_parts():
    #This catalogues how many active work parts our workers have and how many active carry parts our haulers have.
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        room_cache = Cache.rooms.get(creep.memory.target_room)

        if room_cache == None:
            continue

        if creep.memory.role == 'worker':
            room_cache.current_work_parts += creep.getActiveBodyparts(WORK)

        if creep.memory.role == 'hauler' and (creep.ticksToLive > 150 or creep.spawning):
            room_cache.current_carry_parts += creep.getActiveBodyparts(CARRY)
