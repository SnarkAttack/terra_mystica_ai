from src.game.action import *
from src.game.game import TerraMysticaGame, PendingMove
from src.game.player import Player
from src.game.move import Move
from src.utilities.mappings import Factions, Terrains, BoardType, Actions, Cults
from src.game.action import TerraformNoBuildAction
import pytest

def test_terraform_no_build():

    game = TerraMysticaGame(BoardType.ORIGINAL)
    player = Player(game, Factions.WITCHES)

    game.add_pending_move_end(PendingMove(player, Actions.TERRAFORM_NO_BUILD))
    move = Move(player, TerraformNoBuildAction("A4", Terrains.SWAMP, ResourceRequirements(workers=3)))
    game.perform_move(move)
    assert game.get_game_board().get_terrain("A4") == Terrains.SWAMP
    assert player.get_workers() == 0
    assert player.get_coins() == 15

def test_terraform_build():

    game = TerraMysticaGame(BoardType.ORIGINAL)
    player = Player(game, Factions.WITCHES)
    player._workers += 2

    game.add_pending_move_end(PendingMove(player, Actions.TERRAFORM_BUILD))

    action = TerraformBuildAction("A4", Terrains.SWAMP, ResourceRequirements(workers=4, coins=2))
    move = Move(player, action)
    game.perform_move(move)
    assert game.get_game_board().get_terrain("A4") == Terrains.SWAMP
    assert player.get_workers() == 1
    assert player.get_coins() == 13

def test_place_dwelling():

    game = TerraMysticaGame(BoardType.ORIGINAL)
    player = Player(game, Factions.WITCHES)
    game.add_pending_move_end(PendingMove(player, Actions.PLACE_DWELLING))
    action = PlaceDwellingAction("A3")
    move = Move(player, action)
    game.perform_move(move)
    assert game.get_game_board().get_structure_at_location("A3").get_faction() == Factions.WITCHES
    assert game.get_game_board().get_structure_at_location("A3").get_type() == Structures.DWELLING
    assert game.get_game_board().get_structure_at_location("A2").get_type() == Structures.NONE

# def test_add_priest():

#     faction = Factions.WITCHES
#     cult = Cults.FIRE

#     game = TerraMysticaGame(BoardType.ORIGINAL)
#     player = Player(game, faction)
#     game.add_pending_move_end(PendingMove(player, Actions.PLAY_PRIEST_TO_CULT_TRACK))
#     action = PlayPriestToCultTrackAction(cult)
#     move = Move(player, action)
#     with pytest.raises(InvalidActionException):
#         game.perform_move(move)
#     player._priests += 1
#     assert player.get_priests() == 1
#     game.perform_move(move)
#     assert game.get_player_by_faction(faction)._available_priests == 6
#     assert player.get_priests() == 0
#     cult_board = game.get_cult_board()
#     assert cult_board.get_faction_on_cult_track(cult, faction) == 3
