from ..mappings import Terrain

def get_shovel_cost(terrain_from, terrain_to):
    terrain_diff = abs(int(terrain_from)-int(terrain_to))
    return terrain_diff if terrain_diff <=3 else abs(terrain_diff-7)