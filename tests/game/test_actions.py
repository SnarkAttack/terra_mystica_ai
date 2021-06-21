from src.game.action import *
from src.game.game import TerraMysticaGame
from src.game.player import Player
from src.game.move import Move
from src.mappings import Factions, Terrain, BoardType
from src.game.action import TerraformNoBuildAction

def test_terraform_no_build():

    game = TerraMysticaGame(BoardType.ORIGINAL)
    player = Player(game, Factions.WITCHES)

    action = TerraformNoBuildAction("A1", Terrain.FOREST)
    move = Move(player, action)
    game.perform_move(move)
    assert game.get_game_board().get_terrain("A1") == Terrain.PLAINS

    action = TerraformNoBuildAction("A4", Terrain.SWAMP)
    move = Move(player, action)
    game.perform_move(move)
    assert game.get_game_board().get_terrain("A4") == Terrain.SWAMP
    assert player.get_workers() == 0
    assert player.get_coins() == 15

def test_terraform_build():

    game = TerraMysticaGame(BoardType.ORIGINAL)
    player = Player(game, Factions.WITCHES)
    player._workers += 2

    action = TerraformBuildAction("A1", Terrain.FOREST)
    move = Move(player, action)
    game.perform_move(move)
    assert game.get_game_board().get_terrain("A1") == Terrain.PLAINS

    action = TerraformBuildAction("A4", Terrain.SWAMP)
    move = Move(player, action)
    game.perform_move(move)
    assert game.get_game_board().get_terrain("A4") == Terrain.SWAMP
    assert player.get_workers() == 1
    assert player.get_coins() == 13
