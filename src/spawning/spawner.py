from defs import *
from core.cache import Cache
from spawning.naming import generate_timecode
from spawning.counters import count_parts

from managers.miner_manager import run_miner_manager
from managers.hauler_manager import run_hauler_manager
from managers.worker_manager import run_worker_manager


def run_spawning():
    #All spawning related code runs every 3 ticks, because creep spawning duration is always a mutliple of 3 ticks.
    if Game.time % 3 != 0:
        return

    #This catalogues how many active work parts our workers have and how many active carry parts our haulers have.
    count_parts()

    #This number tracks how many total creeps have been spawned so far on this tick.
    num_spawns = 0

    for room_name in Cache.owned_rooms:
        room = Game.rooms[room_name]

        #This finds all of your spawns in the room.
        spawns = room.find(FIND_MY_SPAWNS)

        #This keeps track of how much energy we've used on spawning creeps so far this tick.
        used_energy = 0

        for spawn in spawns:
            if not spawn.isActive():
                continue

            if spawn.spawning:
                if spawn.spawning.remainingTime <= 1:
                    creeps = spawn.pos.findInRange(FIND_MY_CREEPS, 1)
                    for creep in creeps:
                        creep.moveTo(room.controller)
                continue

            #This constructs a creep name from the timecode we made earlier.
            name = generate_timecode(num_spawns)

            #Run managers in priority order
            if run_miner_manager(room, spawn, name, used_energy):
                num_spawns += 1
                continue

            if run_hauler_manager(room, spawn, name, used_energy):
                num_spawns += 1
                continue

            if run_worker_manager(room, spawn, name, used_energy):
                num_spawns += 1
                continue

            #If we got here without trying to spawn anything, skip the remaining spawns.
            break
