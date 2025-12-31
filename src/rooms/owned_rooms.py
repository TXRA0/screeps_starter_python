from defs import *
from core.cache import Cache


def catalog_owned_rooms():
    #This catalogues your owned rooms.
    Cache.owned_rooms = []

    for room_name in Object.keys(Game.rooms):
        room = Game.rooms[room_name]

        if room.controller != None and room.controller.my:
            if Cache.rooms.get(room_name) == None:
                Cache.rooms[room_name] = {}

            Cache.owned_rooms.append(room_name)
            Cache.rooms[room_name].current_work_parts = 0
            Cache.rooms[room_name].current_carry_parts = 0
