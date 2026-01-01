import math
from defs import *

# These are currently required for Transcrypt in order to use the following names in JavaScript.
# Without the 'noalias' pragma, each of the following would be translated into something like 'py_Infinity' or
#  'py_keys' in the output file.
__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')
def get_worker_spawn_data(room, current_creeps, current_work_parts, income):
    """
    Returns None if no worker is needed, otherwise returns body list.
    """
    if current_work_parts >= income:
        return None
    worker_multiple = min(16, math.floor(room.energyCapacityAvailable / 200))
    body = []
    for i in range(worker_multiple):
        body.append(WORK)
    for i in range(worker_multiple):
        body.append(CARRY)
    for i in range(worker_multiple):
        body.append(MOVE)
    return body
