from defs import *

from roles.miner import run_miner
from roles.hauler import run_hauler
from roles.worker import run_worker


def run_creeps():
    #This runs the action function for each creep, based on its role.
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]

        if creep.spawning:
            continue

        role = creep.memory.role

        if role == 'miner':
            run_miner(creep)

        elif role == 'hauler':
            run_hauler(creep)

        elif role == 'worker':
            run_worker(creep)

        else:
            print('No role function for creep ' + creep.name + ' with role ' + role + '!')
