from src.game.action import *
from src.game.game import TerraMysticaGame
from src.game.player import Player
from src.game.move import Move
from src.utilities.mappings import Factions, Terrains, BoardType
from src.game.action import TerraformNoBuildAction

def test_terraform_no_build():

    game = TerraMysticaGame(BoardType.ORIGINAL)
    player = Player(game, Factions.WITCHES)

    action = TerraformNoBuildAction("A1", Terrains.FOREST)
    move = Move(player, action)
    game.perform_move(move)
    assert game.get_game_board().get_terrain("A1") == Terrains.PLAINS

    action = TerraformNoBuildAction("A4", Terrains.SWAMP)
    move = Move(player, action)
    game.perform_move(move)
    assert game.get_game_board().get_terrain("A4") == Terrains.SWAMP
    assert player.get_workers() == 0
    assert player.get_coins() == 15

def test_terraform_build():

    game = TerraMysticaGame(BoardType.ORIGINAL)
    player = Player(game, Factions.WITCHES)
    player._workers += 2

    action = TerraformBuildAction("A1", Terrains.FOREST)
    move = Move(player, action)
    game.perform_move(move)
    assert game.get_game_board().get_terrain("A1") == Terrains.PLAINS

    action = TerraformBuildAction("A4", Terrains.SWAMP)
    move = Move(player, action)
    game.perform_move(move)
    assert game.get_game_board().get_terrain("A4") == Terrains.SWAMP
    assert player.get_workers() == 1
    assert player.get_coins() == 13

def test_place_dwelling():

    game = TerraMysticaGame(BoardType.ORIGINAL)
    player = Player(game, Factions.WITCHES)
    action = PlaceDwellingAction("A3")
    move = Move(player, action)
    game.perform_move(move)
    assert game.get_game_board().get_structure("A3").get_faction() == Factions.WITCHES
    assert game.get_game_board().get_structure("A3").get_type() == Structures.DWELLING
    assert game.get_game_board().get_structure("A2").get_type() == Structures.NONE
