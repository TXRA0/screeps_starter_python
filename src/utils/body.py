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


#This function turns the long creep body array into a shorter form for readability in the console
def body_shorthand(body):
    body_count = {}

    for part in body:
        if body_count.get(part) == None:
            body_count[part] = 1
        else:
            body_count[part] += 1

    outstring = ''
    for part_type in Object.keys(body_count):
        outstring += body_count[part_type] + part_type + ' '

    return outstring


def generate_pixels():
    #It's likely that you won't fully utilize your CPU when starting out.
    if (
        Game.cpu.generatePixel and
        Game.cpu.bucket == 10000 and
        Game.cpu.getUsed() < Game.cpu.limit and
        ['shard0', 'shard1', 'shard2', 'shard3'].includes(Game.shard.name)
    ):
        if Game.cpu.generatePixel() == OK:
            print(' ======= Generating pixel! Press F to pay respects to your bucket! ======= ')
