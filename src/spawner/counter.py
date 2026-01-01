# defs is a package which claims to export all constants and some JavaScript objects, but in reality does
#  nothing. This is useful mainly when using an editor like PyCharm, so that it 'knows' that things like Object, Creep,
#  Game, etc. do exist.
from spawner.namer import make_timecode
from spawner.spawner import run_room_spawning
from defs import *

# These are currently required for Transcrypt in order to use the following names in JavaScript.
# Without the 'noalias' pragma, each of the following would be translated into something like 'py_Infinity' or
#  'py_keys' in the output file.
__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def count_room_parts():
    # This catalogues how many active work parts our workers have
    # and how many active carry parts our haulers have.
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        if creep.memory.role == 'worker' and Cache.rooms[creep.memory.target_room] != None:
            Cache.rooms[creep.memory.target_room].current_work_parts += creep.getActiveBodyparts(WORK)
        if (
            creep.memory.role == 'hauler'
            and (creep.ticksToLive > 150 or creep.spawning)
            and Cache.rooms[creep.memory.target_room] != None
        ):
            Cache.rooms[creep.memory.target_room].current_carry_parts += creep.getActiveBodyparts(CARRY)
