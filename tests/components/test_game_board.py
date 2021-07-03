from src.components.game_board import OriginalGameBoard
from src.utilities.mappings import Structures, Terrains, Factions

def count_terrain_spaces(board, terrain):
    count = 0
    for row in board._locations:
        count += sum([1 if loc == terrain else 0 for loc in row])
    return count

def test_original_board_setup():
    board = OriginalGameBoard()

    row_lens = [len(row) for row in board._locations]
    assert row_lens == [13, 12, 13, 12, 13, 12, 13, 12, 13]

    row_lens = [len(row) for row in board._structures]
    assert row_lens == [13, 12, 13, 12, 13, 12, 13, 12, 13]

    terrain_counts = [count_terrain_spaces(board, terrain) for terrain in Terrains]

    assert terrain_counts == [0, 11, 11, 11, 11, 11, 11, 11, 36]

def test_board_location():
    board = OriginalGameBoard()
    assert board.get_terrain("A1") == Terrains.PLAINS

def test_valid_dwelling_placements():
    board = OriginalGameBoard()
    terrain = Terrains.WASTELAND
    faction = Factions.GIANTS


    valid_building_locations = board.get_valid_building_locations(terrain, Structures.DWELLING)
    assert valid_building_locations == ['A6', 'A9', 'A12', 'D6', 'D9', 'D11', 'E3', 'G6', 'I1', 'I5', 'I13']

    board.place_dwelling('A9', faction)
    board.place_dwelling('I5', faction)

    updated_valid_building_locations = board.get_valid_building_locations(terrain, Structures.DWELLING)
    assert updated_valid_building_locations == ['A6', 'A12', 'D6', 'D9', 'D11', 'E3', 'G6', 'I1', 'I13']