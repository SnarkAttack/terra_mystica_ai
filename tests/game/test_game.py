from src.game.game import TerraMysticaGame
from src.utilities.mappings import BoardType

def test_game_creation():
    game = TerraMysticaGame(BoardType.ORIGINAL)