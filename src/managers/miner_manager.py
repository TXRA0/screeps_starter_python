import math
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
from core.cache import Cache


def run_miner_manager(room, spawn, name, used_energy):
    #Spawn miners if we have at least one hauler.
    room_cache = Cache['rooms'][room.name] if room.name in Cache['rooms'] else None
    if not room_cache or getattr(room_cache, 'current_carry_parts', 0) <= 0:
        return False

    #This creates a list of all of our creeps with this room as their target room.
    creep_names = filter(
        lambda n: Game.creeps[n].memory.target_room == room.name,
        Object.keys(Game.creeps)
    )

    current_creeps = [Game.creeps[n] for n in creep_names]

    #Check how many miners we have.
    sources = room.find(FIND_SOURCES)

    for source in sources:
        current_miners = [
            c for c in current_creeps
            if c.memory.role == 'miner'
            and c.memory.target == source.id
            and (c.spawning or (c.ticksToLive > 50))
        ]

        if len(current_miners) > 0:
            continue

        energy_to_use = room.energyCapacityAvailable
        if getattr(room.memory, 'no_miner_ticks', 0) > 20:
            energy_to_use = room.energyAvailable

        miner_multiple = min(3, math.floor(energy_to_use / 250))
        body = []
        cost = 0

        for _ in range(miner_multiple):
            body.append(WORK)
            body.append(WORK)
            cost += 200

        for _ in range(miner_multiple):
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
                if room.memory.no_miner_ticks is None:
                    room.memory.no_miner_ticks = 0
                room.memory.no_miner_ticks += 1

    return False
