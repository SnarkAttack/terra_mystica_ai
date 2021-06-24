from ..mappings import Terrain, Cults, Factions
from ..game.resources import ResourceGroup, ResourceRequirements
from ..utilities import MAX_DWELLINGS, MAX_SANCTUARIES, MAX_STRONGHOLDS, MAX_TEMPLES, MAX_TRADING_POSTS

class FactionBoard(object):

    def __init__(self):
        self._faction = Factions.NONE
        self._home_terrain = Terrain.NONE
        self._starting_coins = 0
        self._starting_workers = 0
        self._starting_cult_1 = Cults.NONE
        self._starting_cult_2 = Cults.NONE
        self._dwelling_build_cost = ResourceRequirements(
            coins=2,
            workers=1
        )
        self._trading_post_adj_build_cost = ResourceRequirements(
            coins=3,
            workers=2
        )
        self._trading_post_non_adj_build_cost = ResourceRequirements(
            coins=6,
            workers=2
        )
        self._stronghold_build_cost = ResourceRequirements(
            coins=6,
            workers=4
        )
        self._temple_build_cost = ResourceRequirements(
            coins=5,
            workers=2
        )
        self._sanctuary_build_cost = ResourceRequirements(
            coins=6,
            workers=4
        )
        self._exchange_cost = ResourceRequirements(
            coins=5,
            workers=2,
            priests=1
        )
        self._shipping_upgrade_cost_coins = ResourceRequirements(
            coins=4,
            priests=1
        )
        self._bowl_1 = 5
        self._bowl_2 = 7
        self._bowl_3 = 0
        self._dwelling_income = [
            ResourceGroup(workers=1),
            ResourceGroup(workers=1),
            ResourceGroup(workers=1),
            ResourceGroup(workers=1),
            ResourceGroup(workers=1),
            ResourceGroup(workers=1),
            ResourceGroup(workers=1),
            ResourceGroup(),
        ]
        self._trading_post_income = [
            ResourceGroup(coins=2, power=1),
            ResourceGroup(coins=2, power=1),
            ResourceGroup(coins=2, power=2),
            ResourceGroup(coins=2, power=2),
        ]
        self._stronghold_income = [
            ResourceGroup(power=2),
        ]
        self._temple_income = [
            ResourceGroup(priests=1),
            ResourceGroup(priests=1),
            ResourceGroup(priests=1),
        ]
        self._sanctuary_income = [
            ResourceGroup(priests=1)
        ]

    def get_faction(self):
        return self._faction

    def get_home_terrain(self):
        return self._home_terrain

    def get_starting_workers(self):
        return self._starting_workers

    def get_starting_coins(self):
        return self._starting_coins

    def get_dwelling_build_cost(self):
        return self._dwelling_build_cost

    def get_income_from_dwellings(self, dwellings_on_board):
        return sum(self._dwelling_income[:dwellings_on_board])

    def get_income_from_trading_posts(self, trading_posts_on_board):
        return sum(self._trading_post_income[:trading_posts_on_board])

    def get_income_from_stronghold(self, strongholds_on_board):
        return sum(self._stronghold_income[:strongholds_on_board])

    def get_income_from_temples(self, temples_on_board):
        return sum(self._temple_income[:temples_on_board])

    def get_income_from_sanctuary(self, sanctuaries_on_board):
        return sum(self._sanctuary_income[:sanctuaries_on_board])


class WitchesFactionBoard(FactionBoard):

    def __init__(self):
        super().__init__()
        self._faction = Factions.WITCHES
        self._home_terrain = Terrain.FOREST
        self._starting_workers = 3
        self._starting_coins = 15
        self._starting_cult_1 = Cults.AIR
        self._starting_cult_2 = Cults.AIR
        self._dwelling_build_cost = ResourceRequirements(
            coins=2,
            workers=1
        )
        self._trading_post_adj_build_cost = ResourceRequirements(
            coins=3,
            workers=2
        )
        self._trading_post_non_adj_build_cost = ResourceRequirements(
            coins=6,
            workers=2
        )
        self._stronghold_build_cost = ResourceRequirements(
            coins=6,
            workers=4
        )
        self._temple_build_cost = ResourceRequirements(
            coins=5,
            workers=2
        )
        self._sanctuary_build_cost = ResourceRequirements(
            coins=6,
            workers=4
        )
        self._exchange_cost = ResourceRequirements(
            coins=5,
            workers=2,
            priests=1
        )
        self._shipping_upgrade_cost_coins = ResourceRequirements(
            coins=4,
            priests=1
        )
        self._bowl_1 = 5
        self._bowl_2 = 7
        self._bowl_3 = 0
        self._dwelling_income = [
            ResourceGroup(workers=1),
            ResourceGroup(workers=1),
            ResourceGroup(workers=1),
            ResourceGroup(workers=1),
            ResourceGroup(workers=1),
            ResourceGroup(workers=1),
            ResourceGroup(workers=1),
            ResourceGroup(),
        ]
        self._trading_post_income = [
            ResourceGroup(coins=2, power=1),
            ResourceGroup(coins=2, power=1),
            ResourceGroup(coins=2, power=2),
            ResourceGroup(coins=2, power=2),
        ]
        self._stronghold_income = [
            ResourceGroup(power=2),
        ]
        self._temple_income = [
            ResourceGroup(priests=1),
            ResourceGroup(priests=1),
            ResourceGroup(priests=1),
        ]
        self._sanctuary_income = [
            ResourceGroup(priests=1)
        ]

class NomadsFactionBoard(FactionBoard):
    def __init__(self):
        super().__init__()
        self._faction = Factions.NOMADS
        self._home_terrain = Terrain.DESERT
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