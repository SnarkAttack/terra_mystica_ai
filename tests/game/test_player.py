from src.game.player import Player
from src.game.game import TerraMysticaGame
from src.mappings import Factions, BoardType

def test_power():
    player = Player(None, Factions.WITCHES)

    assert player.get_power() == (5, 7, 0)
    player.add_power(2)
    assert player.get_power() == (3, 9, 0)
    player.add_power(6)
    assert player.get_power() == (0, 9, 3)
    player.spend_power(2)
    assert player.get_power() == (2, 9, 1)

def test_get_home_terrain_type_codes():
   game = TerraMysticaGame(BoardType.ORIGINAL)
   player = Player(game, Factions.WITCHES)

   assert player.get_home_terrain_tile_codes() == ["A3", "A10", "C3", "C4", "D1", "E9", "F2", "F4", "G3", "I6", "I11"]