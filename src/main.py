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

from core.memory import setup_memory, apply_memhack
from core.cache import setup_cache
from core.cleanup import cleanup_memory
from rooms.owned_rooms import catalog_owned_rooms
from creeps.runner import run_creeps
from spawning.spawner import run_spawning
from utils.body import generate_pixels

def main():
    setup_memory()
    apply_memhack()

    setup_cache()
    catalog_owned_rooms()

    cleanup_memory()
    run_creeps()
    run_spawning()

    generate_pixels()

module.exports.loop = main
