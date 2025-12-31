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
