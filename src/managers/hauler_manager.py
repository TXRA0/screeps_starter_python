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

def get_hauler_spawn_data(room, current_creeps, current_carry_parts, income):
    """
    Returns None if no hauler is needed, otherwise returns body list.
    """
    print(f"Checking hauler spawn for room {room.name}")
    print(f"Current carry parts: {current_carry_parts}, Income: {income}")

    if current_carry_parts >= income * 3:
        print("No hauler needed (carry parts sufficient).")
        return None

    energy_to_use = room.energyCapacityAvailable
    if current_carry_parts == 0:
        energy_to_use = room.energyAvailable
    print(f"Energy to use for hauler: {energy_to_use}")

    hauler_multiple = min(16, math.floor(energy_to_use / 150))
    print(f"Hauler multiple: {hauler_multiple}")

    body = []
    for _ in range(hauler_multiple):
        body.append(CARRY)
        body.append(CARRY)
        body.append(MOVE)

    if body:
        print(f"Hauler body generated: {body}")
    else:
        print("Error: No valid hauler body generated!")

    return body
