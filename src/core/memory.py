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

# Initialize memory safely
my_memory = RawMemory._parsed
if my_memory == None:
    my_memory = {}
    RawMemory._parsed = my_memory

def setup_memory():
    # Initialize fields if missing
    if not hasattr(my_memory, 'reset_log') or my_memory.reset_log == None:
        my_memory.reset_log = []

    if hasattr(my_memory, 'last_reset') and my_memory.last_reset != None:
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

    # Initialize sub-objects
    if my_memory.creeps == None:
        my_memory.creeps = {}

    if my_memory.rooms == None:
        my_memory.rooms = {}

    if my_memory.spawns == None:
        my_memory.spawns = {}

def apply_memhack():
    __pragma__('js', '{}', 'delete global.Memory;')
    __pragma__('js', '{}', 'global.Memory = my_memory;')
    __pragma__('js', '{}', 'RawMemory._parsed = my_memory;')