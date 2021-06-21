from .resources import ResourceRequirements, ResourceGroup
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
        self._priests = 0
        self._points = 20

        self._exchange_level = 0

        self._power_1 = 5
        self._power_2 = 7
        self._power_3 = 0

        self._available_dwellings = 8
        self._available_trading_posts = 5
        self._available_strongholds = 1
        self._available_temples = 3
        self._available_sanctuaries = 1

        self._game = game

    def _get_spade_exchange_cost(self):
        return 3-self._exchange_level

    def get_resources(self):
        return ResourceGroup(
            coins=self._coins,
            workers=self._workers,
            priests=self._priests,
            power=self._power_3
        )

    def get_coins(self):
        return self._coins

    def get_workers(self):
        return self._workers

    def get_priests(self):
        return self._priests

    def get_terraform_worker_cost(self, terrain_diff_val):
        worker_per_spade = self._get_spade_exchange_cost()
        return ResourceRequirements(workers=worker_per_spade*terrain_diff_val)

    # TODO: Might have to change this to account for instant power conversion to a coin
    def get_available_coins(self):
        return self._coins

    # TODO: Same as above
    def get_available_workers(self):
        return self._workers

    def get_build_dwelling_cost(self):
        return self._player_board.get_dwelling_build_cost()

    def spend_resources(self, resource_cost):
        self._coins -= resource_cost.get_coins()
        self._workers -= resource_cost.get_workers()
        self._priests -= resource_cost.get_priests()
        self._power_3 -= resource_cost.get_power()

    def select_move(self):
        raise NotImplementedError()