from src.utilities.mappings import Terrains
from src.utilities.functions import get_shovel_cost

def test_get_shovel_cost():
    assert get_shovel_cost(Terrains.PLAINS, Terrains.PLAINS) == 0

    assert get_shovel_cost(Terrains.WASTELAND, Terrains.MOUNTAINS) == 1

    assert get_shovel_cost(Terrains.SWAMP, Terrains.DESERT) == 2