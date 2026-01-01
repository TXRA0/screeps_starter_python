from defs import *
from spawner.namer import make_creep_name
from managers.miner_manager import get_miner_spawn_data
from managers.hauler_manager import get_hauler_spawn_data
from managers.worker_manager import get_worker_spawn_data
import math

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

def count_part(body, part):
    count = 0
    for p in body:
        if p == part:
            count += 1
    return count

def run_room_spawning(room):
    print('--- Spawning tick for room', room.name, '---')

    # Gather creeps targeting this room
    creep_names = [
        n for n in Object.keys(Game.creeps)
        if Game.creeps[n].memory.target_room == room.name
    ]
    current_creeps = [Game.creeps[n] for n in creep_names]

    # Room stats
    sources = room.find(FIND_SOURCES)
    miner_multiple = min(3, math.floor(room.energyCapacityAvailable / 250))
    income = len(sources) * min(10, 4 * miner_multiple)

    current_carry_parts = getattr(Cache.rooms[room.name], 'current_carry_parts', 0)
    current_work_parts = getattr(Cache.rooms[room.name], 'current_work_parts', 0)

    print(
        'Income:', income,
        '| Carry:', current_carry_parts,
        '| Work:', current_work_parts
    )

    for spawn in room.find(FIND_MY_SPAWNS):
        if not spawn.isActive() or spawn.spawning:
            continue

        creep_name = make_creep_name()

        miner_data = get_miner_spawn_data(room, current_creeps)
        if miner_data:
            body, source_id = miner_data
            if spawn.spawnCreep(
                body,
                creep_name,
                {'memory': {
                    'role': 'miner',
                    'target': source_id,
                    'target_room': room.name
                }}
            ) == OK:
                print('Spawned miner:', creep_name)
                return  # one spawn per tick

        hauler_body = get_hauler_spawn_data(
            room,
            current_creeps,
            current_carry_parts,
            income
        )

        if hauler_body:
            if spawn.spawnCreep(
                hauler_body,
                creep_name,
                {'memory': {
                    'role': 'hauler',
                    'target_room': room.name
                }}
            ) == OK:
                print('Spawned hauler:', creep_name)
                Cache.rooms[room.name].current_carry_parts += count_part(hauler_body, CARRY)
                return

        worker_body = get_worker_spawn_data(
            room,
            current_creeps,
            current_work_parts,
            income
        )

        if worker_body:
            if spawn.spawnCreep(
                worker_body,
                creep_name,
                {'memory': {
                    'role': 'worker',
                    'target_room': room.name
                }}
            ) == OK:
                print('Spawned worker:', creep_name)
                Cache.rooms[room.name].current_work_parts += count_part(worker_body, WORK)
                return

        print('No spawn needed for spawn', spawn.name)
