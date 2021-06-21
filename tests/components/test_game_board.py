from src.components.game_board import OriginalGameBoard
from src.mappings import Terrain

def count_terrain_spaces(board, terrain):
    count = 0
    for row in board._locations:
        count += sum([1 if loc == terrain else 0 for loc in row])
    return count

def test_original_board_setup():
    board = OriginalGameBoard()

    row_lens = [len(row) for row in board._locations]
    assert row_lens == [13, 12, 13, 12, 13, 12, 13, 12, 13]

    row_lens = [len(row) for row in board._components]
    assert row_lens == [13, 12, 13, 12, 13, 12, 13, 12, 13]

    terrain_counts = [count_terrain_spaces(board, terrain) for terrain in Terrain]

    assert terrain_counts == [0, 11, 11, 11, 11, 11, 11, 11, 36]

# def test_original_board_valid_location():
#     board = OriginalGameBoard()
#     valid_locations = board.get_valid_location_codes()
#     print(valid_locations)
#     assert False

def test_board_location():
    board = OriginalGameBoard()
    assert board.get_terrain("A1") == Terrain.PLAINS