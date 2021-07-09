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
    assert row_lens == [13, 13, 13, 13, 13, 13, 13, 13, 13]

    row_lens = [len(row) for row in board._structures]
    assert row_lens == [13, 13, 13, 13, 13, 13, 13, 13, 13]

    terrain_counts = [count_terrain_spaces(board, terrain) for terrain in Terrains]

    assert terrain_counts == [4, 11, 11, 11, 11, 11, 11, 11, 36]

def test_board_location():
    board = OriginalGameBoard()
    assert board.get_terrain("A1") == Terrains.PLAINS

def test_valid_dwelling_placements():
    board = OriginalGameBoard()
    faction = Factions.GIANTS

    valid_building_locations = board.get_valid_dwelling_placement_locations(faction, Structures.DWELLING)
    assert valid_building_locations == ['A6', 'A9', 'A12', 'D6', 'D9', 'D11', 'E3', 'G6', 'I1', 'I5', 'I13']

    board.place_dwelling('A9', faction)
    board.place_dwelling('I5', faction)

    updated_valid_building_locations = board.get_valid_dwelling_placement_locations(faction, Structures.DWELLING)
    assert updated_valid_building_locations == ['A6', 'A12', 'D6', 'D9', 'D11', 'E3', 'G6', 'I1', 'I13']

def test_direct_adjacency():
    board = OriginalGameBoard()

    # Check central location where everything should be fetched
    assert board.get_directly_adjacent_locations("E7") == ['D6', 'D7', 'E6', 'E8', 'F6', 'F7']

    # Check when on top row
    assert board.get_directly_adjacent_locations("A5") == ['A4', 'A6', 'B4', 'B5']

    # Check when on bottom row
    assert board.get_directly_adjacent_locations("I8") == ['H7', 'H8', 'I7', 'I9']

    # Check left side
    assert board.get_directly_adjacent_locations("D1") == ['C1', 'C2', 'D2', 'E1', 'E2']

    # Check right side
    assert board.get_directly_adjacent_locations("C13") == ['B12', 'B13', 'C12', 'D12', 'D13']