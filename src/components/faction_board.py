from ..mappings import Terrain, Cults

class FactionBoard(object):

    def __init__(self):
        self._uncovered_dwellings = 0
        self._uncovered_trading_posts = 0
        self._uncovered_stronghold = 0
        self._uncovered_temples = 0
        self._uncovered_sanctuary = 0
        self._exchange_track_upgrades = 0
        self._shipping_track_upgrades = 0
        self._starting_coins = 0
        self._starting_workers = 0
        self._starting_cult_1 = Cults.NONE
        self._starting_cult_2 = Cults.NONE

    def get_starting_workers(self):
        return self._starting_workers

    def get_starting_coins(self):
        return self._starting_coins

class WitchesFactionBoard(FactionBoard):

    def __init__(self):
        super().__init__()
        self.home_terrain = Terrain.FOREST
        self._starting_workers = 3
        self._starting_coins = 15
        self._starting_cult_1 = Cults.AIR
        self._starting_cult_2 = Cults.AIR
        self._dwelling_upgrade_cost_workers = 1
        self._dwelling_upgrade_cost_coins = 2
        self._trading_post_upgrade_cost_workers = 2
        self._trading_post_upgrade_cost_coins_adjacent = 3
        self._trading_post_upgrade_cost_coins_non_adjacent = 6
        self._stronghold_upgrade_cost_workers = 4
        self._stronghold_upgrade_cost_coins = 6
        self._temple_upgrade_cost_workers = 2
        self._temple_upgrade_cost_coins = 5
        self._sanctuary_upgrade_cost_workers = 4
        self._sanctuary_upgrade_cost_coins = 6
        self._exchange_upgrade_cost_workers = 2
        self._exchange_upgrade_cost_coins = 5
        self._exchange_upgrade_cost_priests = 1
        self._shipping_upgrade_cost_coins = 4
        self._shipping_upgrade_cost_priests = 1
        self._bowl_1 = 5
        self._bowl_2 = 7
        self._bowl_3 = 0

class NomadsFactionBoard(FactionBoard):
    def __init__(self):
        super().__init__()
        self.home_terrain = Terrain.FOREST
        self._starting_workers = 2
        self._starting_coins = 15
        self._starting_cult_1 = Cults.EARTH
        self._starting_cult_2 = Cults.FIRE
        self._dwelling_upgrade_cost_workers = 1
        self._dwelling_upgrade_cost_coins = 2
        self._trading_post_upgrade_cost_workers = 2
        self._trading_post_upgrade_cost_coins_adjacent = 3
        self._trading_post_upgrade_cost_coins_non_adjacent = 6
        self._stronghold_upgrade_cost_workers = 4
        self._stronghold_upgrade_cost_coins = 8
        self._temple_upgrade_cost_workers = 2
        self._temple_upgrade_cost_coins = 5
        self._sanctuary_upgrade_cost_workers = 4
        self._sanctuary_upgrade_cost_coins = 6
        self._exchange_upgrade_cost_workers = 2
        self._exchange_upgrade_cost_coins = 5
        self._exchange_upgrade_cost_priests = 1
        self._shipping_upgrade_cost_coins = 4
        self._shipping_upgrade_cost_priests = 1
        self._bowl_1 = 5
        self._bowl_2 = 7
        self._bowl_3 = 0