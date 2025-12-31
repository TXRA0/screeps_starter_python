import creep_roles

#This sets up Cache, which is lost on global reset, but takes no Memory space.
Cache = {}


def setup_cache():
    creep_roles.init_cache()
    Cache.rooms = {}
    Cache.owned_rooms = []
