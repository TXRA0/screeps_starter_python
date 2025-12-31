import math
from defs import *
from core.cache import Cache
from utils.body import body_shorthand


def run_hauler_manager(room, spawn, name, used_energy):
    #This calculates the income based on the number of sources and the size of our miners.
    sources = room.find(FIND_SOURCES)
    miner_multiple = min(3, math.floor(room.energyCapacityAvailable / 250))
    income = len(sources) * min(10, 4 * miner_multiple)

    #Spawn haulers if we have less carry parts than three times our income.
    if Cache.rooms[room.name].current_carry_parts >= income * 3:
        return False

    energy_to_use = room.energyCapacityAvailable
    if Cache.rooms[room.name].current_carry_parts == 0:
        energy_to_use = room.energyAvailable

    hauler_multiple = min(16, math.floor(energy_to_use / 150))
    body = []
    cost = 0
    part_change = 0

    for i in range(hauler_multiple):
        body.append(CARRY)
        body.append(CARRY)
        body.append(MOVE)
        part_change += 2
        cost += 150

    if room.energyAvailable - used_energy >= cost:
        result = spawn.spawnCreep(
            body,
            name,
            {'memory': {'target_room': room.name, 'role': 'hauler'}}
        )

        if result == OK:
            Cache.rooms[room.name].current_carry_parts += part_change
            print(room.name + ' spawned hauler ' + name + ' with body ' + body_shorthand(body))
            return True

    return False
