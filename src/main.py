from defs import *
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
