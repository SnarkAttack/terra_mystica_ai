from .resources import ResourceRequirements, ResourceGroup
from ..mappings import Factions
from ..components.faction_board import WitchesFactionBoard, NomadsFactionBoard
from ..utilities import MAX_TRADING_POSTS, MAX_TEMPLES, MAX_STRONGHOLDS, MAX_SANCTUARIES, MAX_DWELLINGS

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

        self._power1 = 5
        self._power2 = 7
        self._power3 = 0

        self._available_dwellings = MAX_DWELLINGS
        self._available_trading_posts = MAX_TRADING_POSTS
        self._available_strongholds = MAX_STRONGHOLDS
        self._available_temples = MAX_TEMPLES
        self._available_sanctuaries = MAX_SANCTUARIES

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

    def get_power(self):
        return (self._power1, self._power2, self._power3)

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

    def add_power(self, power_to_add):
        power_1_to_move = min(self._power1, power_to_add)
        self._power1 -= power_1_to_move
        self._power2 += power_1_to_move
        power_to_add -= power_1_to_move
        power_2_to_add = min(self._power2, power_to_add)
        self._power2 -= power_2_to_add
        self._power3 += power_2_to_add

    def spend_power(self, power_to_lose):
        self._power3 -= power_to_lose
        self._power1 += power_to_lose

    def gain_resources(self, resource_income):
        self._coins += resource_income.get_coins()
        self._workers += resource_income.get_workers()
        self._priests += resource_income.get_priests()
        self._vp += resource_income.get_vp()
        self.add_power(resource_income.get_power())

    def spend_resources(self, resource_cost):
        self._coins -= resource_cost.get_coins()
        self._workers -= resource_cost.get_workers()
        self._priests -= resource_cost.get_priests()
        self._power3 -= resource_cost.get_power()
        self._power1 += resource_cost.get_power()
        self._vp -= resource_cost.get_vp()

    def take_income(self):
        pass

    def select_move(self):
        raise NotImplementedError()