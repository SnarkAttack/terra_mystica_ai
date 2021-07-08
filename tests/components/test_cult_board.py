from src.components.cult_board import CultBoard
from src.utilities.mappings import Factions, Cults

def test_cult_board_increase():
    cult_board = CultBoard()
    faction = Factions.WITCHES
    cult = Cults.FIRE

    cult_board.add_faction_to_cult_board(faction)

    assert cult_board.get_faction_location_on_cult_track(cult, faction) == 0

    cult_board.increase_cult_track(cult, faction, 2)

    assert cult_board.get_faction_location_on_cult_track(cult, faction) == 2

def test_cult_board_add_priest():
    cult_board = CultBoard()
    faction = Factions.WITCHES
    cult = Cults.FIRE

    cult_board.add_faction_to_cult_board(faction)

    assert cult_board.get_faction_location_on_cult_track(cult, faction) == 0

    cult_board.play_priest(cult, faction)

    assert cult_board.get_faction_location_on_cult_track(cult, faction) == 3

    cult_board.play_priest(cult, faction)

    assert cult_board.get_faction_location_on_cult_track(cult, faction) == 5