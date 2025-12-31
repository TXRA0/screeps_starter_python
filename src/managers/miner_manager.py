import math
from defs import *
from core.cache import Cache


def run_miner_manager(room, spawn, name, used_energy):
    #Spawn miners if we have at least one hauler.
    if Cache.rooms[room.name].current_carry_parts <= 0:
        return False

    #This creates a list of all of our creeps with this room as their target room.
    creep_names = filter(
        lambda n: Game.creeps[n].memory.target_room == room.name,
        Object.keys(Game.creeps)
    )

    current_creeps = []
    for creep_name in creep_names:
        current_creeps.append(Game.creeps[creep_name])

    #Check how many miners we have.
    sources = room.find(FIND_SOURCES)

    for source in sources:
        current_miners = filter(
            lambda c:
                c.memory.role == 'miner'
                and c.memory.target == source.id
                and (c.spawning or (c.ticksToLive > 50)),
            current_creeps
        )

        if len(current_miners) > 0:
            continue

        energy_to_use = room.energyCapacityAvailable
        if room.memory.no_miner_ticks > 20:
            energy_to_use = room.energyAvailable

        miner_multiple = min(3, math.floor(energy_to_use / 250))
        body = []
        cost = 0

        for i in range(miner_multiple):
            body.append(WORK)
            body.append(WORK)
            cost += 200

        for i in range(miner_multiple):
            body.append(MOVE)
            cost += 50

        if room.energyAvailable - used_energy >= cost:
            result = spawn.spawnCreep(
                body,
                name,
                {'memory': {
                    'target_room': room.name,
                    'role': 'miner',
                    'target': source.id
                }}
            )

            if result == OK:
                room.memory.no_miner_ticks = 0
                return True

            elif result == ERR_NOT_ENOUGH_ENERGY:
                if room.memory.no_miner_ticks == None:
                    room.memory.no_miner_ticks = 0
                room.memory.no_miner_ticks += 1

    return False
