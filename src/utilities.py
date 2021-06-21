from .mappings import Terrain

MAX_DWELLINGS = 8
MAX_TRADING_POSTS = 4
MAX_STRONGHOLDS = 1
MAX_TEMPLES = 3
MAX_SANCTUARIES = 1

def get_shovel_cost(terrain_from, terrain_to):
    terrain_diff = abs(int(terrain_from)-int(terrain_to))
    return terrain_diff if terrain_diff <=3 else abs(terrain_diff-7)