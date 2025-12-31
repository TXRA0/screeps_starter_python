from defs import *


def cleanup_memory():
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
