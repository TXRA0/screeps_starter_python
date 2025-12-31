import creep_roles
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
#This sets up Cache, which is lost on global reset, but takes no Memory space.
Cache = {}


def setup_cache():
    creep_roles.init_cache()
    Cache.rooms = {}
    Cache.owned_rooms = []
