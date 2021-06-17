from ..mappings import Factions
from ..components.faction_board import WitchesFactionBoard, NomadsFactionBoard

class Player(object):

    def __init__(self, game, faction):
        if faction == Factions.NOMADS:
            self._player_board = NomadsFactionBoard()
        elif faction == Factions.WITCHES:
            self._player_board = WitchesFactionBoard()
        else:
            raise NotImplementedError()

        self._coins = self._player_board.get_starting_coins()
        self._workers = self._player_board.get_starting_workers()
        self._points = 20

        game.add_player(self)