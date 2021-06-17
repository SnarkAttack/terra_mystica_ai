from src.tm_components.game_board import OriginalGameBoard
from src.mappings import Terrain

def count_terrain_spaces(board, terrain):
    count = 0
    for row in board._locations:
        count += sum([1 if loc == terrain else 0 for loc in row])
    return count

def test_original_board_setup():
    board = OriginalGameBoard()

    row_lens = [len(row) for row in board._locations]
    assert row_lens == [13, 6, 5, 8, 11, 7, 7, 8, 12]

    terrain_counts = [count_terrain_spaces(board, terrain) for terrain in Terrain]

    assert terrain_counts == [0, 11, 11, 11, 11, 11, 11, 11]