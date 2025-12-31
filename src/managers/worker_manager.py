import math
from defs import *
from core.cache import Cache
from utils.body import body_shorthand


def run_worker_manager(room, spawn, name, used_energy):
    #This calculates the income based on the number of sources and the size of our miners.
    sources = room.find(FIND_SOURCES)
    miner_multiple = min(3, math.floor(room.energyCapacityAvailable / 250))
    income = len(sources) * min(10, 4 * miner_multiple)

    #Spawn workers if we have less work parts than our income.
    if Cache.rooms[room.name].current_work_parts >= income:
        return False

    worker_multiple = min(16, math.floor(room.energyCapacityAvailable / 200))
    body = []
    cost = 0
    part_change = 0

    for i in range(worker_multiple):
        body.append(WORK)
        part_change += 1
        cost += 100

    for i in range(worker_multiple):
        body.append(CARRY)
        cost += 50

    for i in range(worker_multiple):
        body.append(MOVE)
        cost += 50

    if room.energyAvailable - used_energy >= cost:
        result = spawn.spawnCreep(
            body,
            name,
            {'memory': {'target_room': room.name, 'role': 'worker'}}
        )

        if result == OK:
            Cache.rooms[room.name].current_work_parts += part_change
            print(room.name + ' spawned worker ' + name + ' with body ' + body_shorthand(body))
            return True

    return False
