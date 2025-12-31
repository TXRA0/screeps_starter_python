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

def generate_timecode(num_spawns):
    #This prepares for unique creep names.
    timestamp = Game.time.toString().split("")
    timecode = 'snek '

    for i in range(4):
        char = timestamp[i + len(timestamp) - 4]

        if char == '0':
            timecode += '--'
        if char == '1':
            timecode += '-~'
        if char == '2':
            timecode += '~-'
        if char == '3':
            timecode += '~~'
        if char == '4':
            timecode += '=-'
        if char == '5':
            timecode += '-='
        if char == '6':
            timecode += '=='
        if char == '7':
            timecode += '=~'
        if char == '8':
            timecode += '~='
        if char == '9':
            timecode += '<>'

    timecode += ':3'

    name = ''
    for i in range(num_spawns):
        name += 's'

    name += timecode
    return name
