from defs import *
from core.cache import Cache

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')
__pragma__('noalias', 'Object')
# Cache setup
if not hasattr(Cache, 'rooms'):
    Cache.rooms = {}
if not hasattr(Cache, 'owned_rooms'):
    Cache.owned_rooms = []

def catalog_owned_rooms():
    # Reset owned rooms list
    Cache.owned_rooms = []

    # Iterate over Game.rooms safely using Object.keys()
    for room_name in Object.keys(Game.rooms):
        room = Game.rooms[room_name]

        # Only keep rooms that have a controller owned by you
        if room.controller is not None and room.controller.my:
            if room_name not in Cache.rooms:
                Cache.rooms[room_name] = {}
            
            Cache.owned_rooms.append(room_name)
            Cache.rooms[room_name]['current_work_parts'] = 0
            Cache.rooms[room_name]['current_carry_parts'] = 0
