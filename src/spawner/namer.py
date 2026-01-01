# defs is a package which claims to export all constants and some JavaScript objects, but in reality does
#  nothing. This is useful mainly when using an editor like PyCharm, so that it 'knows' that things like Object, Creep,
#  Game, etc. do exist.
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

def make_timecode():
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
    return timecode


def make_creep_name():
    timecode = make_timecode()

    count = Math.floor(Math.random() * 5) + 1

    creep_name = ''
    for i in range(count):
        creep_name += 's'

    creep_name += timecode
    return creep_name

