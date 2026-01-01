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

def get_miner_spawn_data(room, current_creeps):
    """
    Decide if a miner should be spawned in the room.
    Returns None if no miner needed.
    Otherwise returns (body, target_source_id)
    """
    sources = room.find(FIND_SOURCES)

    for source in sources:
        current_miners = [
            c for c in current_creeps
            if c.memory.role == "miner"
            and c.memory.target == source.id
            and (c.spawning or c.ticksToLive > 50)
        ]

        if len(current_miners) == 0:
            energy_to_use = room.energyCapacityAvailable
            if getattr(room.memory, "no_miner_ticks", 0) > 20:
                energy_to_use = room.energyAvailable

            miner_multiple = max(1, math.floor(energy_to_use / 250))

            body = []
            for _ in range(miner_multiple):
                body.append(WORK)
                body.append(WORK)
                body.append(MOVE)

            if body:
                return body, source.id

    return None
