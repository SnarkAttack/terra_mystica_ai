from src.game.player import Player
from src.mappings import Factions

def test_power():
    player = Player(None, Factions.WITCHES)

    assert player.get_power() == (5, 7, 0)
    player.add_power(2)
    assert player.get_power() == (3, 9, 0)
    player.add_power(6)
    assert player.get_power() == (0, 9, 3)
    player.spend_power(2)
    assert player.get_power() == (2, 9, 1)