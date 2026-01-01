import creep_roles
import utils.pixel
import math
import random
from spawner.counter import count_room_parts
from spawner.namer import make_timecode
from spawner.spawner import run_room_spawning

# defs is a package which claims to export all constants and some JavaScript objects, but in reality does
#  nothing. This is useful mainly when using an editor like PyCharm, so that it 'knows' that things like Object, Creep,
#  Game, etc. do exist.
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


#This sets up "memhack", which saves CPU by remembering the contents of Memory between ticks.
my_memory = Memory
my_memory = RawMemory._parsed


#This keeps track of every time your script experiences a global reset, which means that the server reloaded it fresh. It happens every time you push your code, and also happens occasionally without your input.
if my_memory.reset_log == None:
    my_memory.reset_log = []
if my_memory.last_reset != None:
    print(' ======= Global reset! Time of reset: ' + Game.time + ' Time since last reset: ' + (Game.time - my_memory.last_reset) + ' ======= ')
    my_memory.reset_log.append(Game.time - my_memory.last_reset)
    while len(my_memory.reset_log) > 10:
        my_memory.reset_log.pop(0)
my_memory.last_reset = Game.time


#This sets up Cache, which is lost on global reset, but takes no Memory space and is cheaper on CPU than Memory. If it doesn't matter for something to be forgotten sometimes, it's better to put it in Cache than Memory.
Cache = {}
creep_roles.init_cache()
Cache.rooms = {}


#This sets up some parts of Memory if they're not set yet.
if my_memory.creeps == None:
    my_memory.creeps = {}
if my_memory.rooms == None:
    my_memory.rooms = {}
if my_memory.spawns == None:
    my_memory.spawns = {}


#This function turns the long creep body array into a shorter form for readability in the console
def body_shorthand(body):
    body_count = {}
    for part in body:
        if body_count[part] == None:
            body_count[part] = 1
        else:
            body_count[part] += 1
    outstring = ''
    for part_type in Object.keys(body_count):
        outstring += '' + body_count[part_type] + part_type + ' '
    return outstring

        
def main():
    """
    Main game logic loop.
    """

    #This is the in-loop part of memhack.
    __pragma__ ('js', '{}', 'delete global.Memory;')
    __pragma__ ('js', '{}', 'global.Memory = my_memory;')
    __pragma__ ('js', '{}', 'RawMemory._parsed = my_memory;')

    #This catalogues your owned rooms.
    Cache.owned_rooms = []
    for room_name in Object.keys(Game.rooms):
        room = Game.rooms[room_name]
        if room.controller != None and room.controller.my:
            if Cache.rooms[room_name] == None:
                Cache.rooms[room_name] = {}
            Cache.owned_rooms.append(room_name)
            Cache.rooms[room_name].current_work_parts = 0
            Cache.rooms[room_name].current_carry_parts = 0

    #This clears out memory of creeps, rooms, and spawns that no longer exist.
    for name in Object.keys(Memory.creeps):
        if Game.creeps[name] == None:
            print('RIP ' + name)
            del Memory.creeps[name]
    for name in Object.keys(Memory.rooms):
        if Game.rooms[name] == None:
            del Memory.rooms[name]
    for name in Object.keys(Memory.spawns):
        if Game.spawns[name] == None:
            del Memory.spawns[name]

    #This runs the action function for each creep, as defined in the creep_roles.py module.
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        if not creep.spawning:
            creep_roles.do_action(creep)

    #This tries to activate safe mode if your spawn gets damaged.
    for spawn_name in Object.keys(Game.spawns):
        spawn = Game.spawns[spawn_name]
        if spawn.hits < spawn.hitsMax and spawn.room.controller.my:
            spawn.room.controller.activateSafeMode()

    # All spawning related code runs every 3 ticks,
    # because creep spawning duration is always a multiple of 3 ticks.
    if Game.time % 3 == 0:

        # Generate the shared name seed for this tick
        timecode = make_timecode()

        # Count worker / hauler parts (mutates Cache.rooms exactly like before)
        count_room_parts()

        # Run spawning per owned room
        for room_name in Cache.owned_rooms:
            room = Game.rooms[room_name]
            run_room_spawning(room, timecode)

    utils.pixel.make_pixel()
module.exports.loop = main