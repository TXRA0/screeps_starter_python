from defs import *

#This sets up "memhack", which saves CPU by remembering the contents of Memory between ticks.
my_memory = RawMemory._parsed


def setup_memory():
    #This keeps track of every time your script experiences a global reset.
    if my_memory.reset_log == None:
        my_memory.reset_log = []

    if my_memory.last_reset != None:
        print(
            ' ======= Global reset! Time of reset: ' +
            Game.time +
            ' Time since last reset: ' +
            (Game.time - my_memory.last_reset) +
            ' ======= '
        )
        my_memory.reset_log.append(Game.time - my_memory.last_reset)

        while len(my_memory.reset_log) > 10:
            my_memory.reset_log.pop(0)

    my_memory.last_reset = Game.time

    #This sets up some parts of Memory if they're not set yet.
    if my_memory.creeps == None:
        my_memory.creeps = {}

    if my_memory.rooms == None:
        my_memory.rooms = {}

    if my_memory.spawns == None:
        my_memory.spawns = {}


def apply_memhack():
    #This is the in-loop part of memhack.
    __pragma__('js', '{}', 'delete global.Memory;')
    __pragma__('js', '{}', 'global.Memory = my_memory;')
    __pragma__('js', '{}', 'RawMemory._parsed = my_memory;')
