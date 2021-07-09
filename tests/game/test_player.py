from src.game.player import Player
from src.game.game import PendingMove, TerraMysticaGame
from src.utilities.mappings import Factions, BoardType, Actions
from src.game.move import Move

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

   assert player.get_home_terrain_tile_codes() == ["A3", "A10", "C7", "C9", "D1", "E11", "F2", "F6", "G8", "I6", "I12"]

def test_take_income():
    game = TerraMysticaGame(BoardType.ORIGINAL)

    player = Player(game, Factions.WITCHES)
    pm1 = PendingMove(player, Actions.PLACE_DWELLING)
    pm2 = PendingMove(player, Actions.PLACE_DWELLING)
    game.add_pending_move_end(pm1)
    game.add_pending_move_end(pm2)
    move = Move(player, player.determine_valid_next_actions(pm1)[0])
    game.perform_move(move)
    move2 = Move(player, player.determine_valid_next_actions(pm2)[0])
    game.perform_move(move2)

    player.take_income()

    assert player.get_workers() == 6
    assert player.get_coins() == 15

def test_get_adjacent_locations():
    game = TerraMysticaGame(BoardType.ORIGINAL)
    faction = Factions.WITCHES
    player = Player(game, faction)

    game.get_game_board().place_dwelling("F6", faction)

    assert player.get_all_adjacent_locations() == ['E6', 'E7', 'F5', 'G6']

def test_valid_terraform_build_locations():

    game = TerraMysticaGame(BoardType.ORIGINAL)
    faction = Factions.WITCHES
    player = Player(game, faction)

    game.get_game_board().place_dwelling("C7", faction)

    terraform_actions = player.determine_valid_terraform_build_actions()
    terra_action_locs = [a.get_location() for a in terraform_actions]

    assert terra_action_locs == ['D7']



