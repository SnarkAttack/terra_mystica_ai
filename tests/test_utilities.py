from src.mappings import Terrain
from src.utilities import get_shovel_cost

def test_get_shovel_cost():
    assert get_shovel_cost(Terrain.PLAINS, Terrain.PLAINS) == 0

    assert get_shovel_cost(Terrain.WASTELAND, Terrain.MOUNTAINS) == 1

    assert get_shovel_cost(Terrain.SWAMP, Terrain.DESERT) == 2