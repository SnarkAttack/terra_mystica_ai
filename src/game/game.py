from ..mappings import BoardType
from ..components.game_board import OriginalGameBoard

class TerraMysticaGame(object):

    def __init__(self, board_type):
        if board_type == BoardType.ORIGINAL:
            self._board = OriginalGameBoard()
        else:
            raise NotImplementedError()

        self._ready = False

        self._players = []

    def add_player(self, player):
        if player not in self._players:
            self._players.append(player)
        else:
            raise ValueError("Player already exists")

    def get_game_board(self):
        return self._board

    def perform_move(self, move):
        action = move.get_action()
        action.take_action(self, move.get_player())
