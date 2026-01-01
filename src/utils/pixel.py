from defs import *
import math
import random

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

def make_pixel():
    if (
        Game.cpu.generatePixel and
        Game.cpu.bucket == 10000 and
        Game.cpu.getUsed() < Game.cpu.limit and
        Game.shard.name in ['shard0', 'shard1', 'shard2', 'shard3']
    ):
        if Game.cpu.generatePixel() == OK:
            print('======= Generating pixel! Press F to pay respects to your bucket! =======')