from .action import PlaceDwellingAction
from .move import Move
from .resources import ResourceRequirements, ResourceGroup
from ..mappings import Factions, MoveType, Structures
from ..components.faction_board import FactionBoard, WitchesFactionBoard, NomadsFactionBoard, FactionBoard
from ..utilities import MAX_TRADING_POSTS, MAX_TEMPLES, MAX_STRONGHOLDS, MAX_SANCTUARIES, MAX_DWELLINGS
import copy

class Player(object):

    def __init__(self, game=None, faction=None, agent=None):
        if faction == Factions.NOMADS:
            self._player_board = NomadsFactionBoard()
        elif faction == Factions.WITCHES:
            self._player_board = WitchesFactionBoard()
        elif faction == None:
            # TODO: This is just to cheat deepcopy, figure out a better way
            self._player_board = FactionBoard()
        else:
            raise NotImplementedError()

        self._game = game

        self._faction = faction
        self._agent = agent

        self._coins = self._player_board.get_starting_coins()
        self._workers = self._player_board.get_starting_workers()
        self._priests = 0
        self._vps = 20

        self._exchange_level = 0

        self._power1 = 5
        self._power2 = 7
        self._power3 = 0

        self._available_dwellings = MAX_DWELLINGS
        self._available_trading_posts = MAX_TRADING_POSTS
        self._available_strongholds = MAX_STRONGHOLDS
        self._available_temples = MAX_TEMPLES
        self._available_sanctuaries = MAX_SANCTUARIES

    # This is a mess, I think I need to decouple some of this
    def __deepcopy__(self, memo):
        player_copy = Player(self._game)
        for k, v in self.__dict__.items():
            if k in ['_agent']:
                player_copy.__dict__[k] = v
            else:
                player_copy.__dict__[k] = copy.deepcopy(v, memo)
        return player_copy

    def get_vps(self):
        return self._vps

    def _get_spade_exchange_cost(self):
        return 3-self._exchange_level

    def get_faction(self):
        return self._player_board.get_faction()

    def get_home_terrain(self):
        return self._player_board.get_home_terrain()

    def get_resources(self):
        return ResourceGroup(
            coins=self._coins,
            workers=self._workers,
            priests=self._priests,
            power=self._power_3
        )

    def get_player_board(self):
        return self._player_board

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
        self._vp -= resource_cost.get_vp()
        self.spend_power(resource_cost.get_power())

    def take_income(self):
        self.gain_resources(self._player_board.get_income_from_dwellings())
        self.gain_resources(self._player_board.get_income_from_trading_posts())
        self.gain_resources(self._player_board.get_income_from_stronghold())
        self.gain_resources(self._player_board.get_income_from_temples())
        self.gain_resources(self._player_board.get_income_from_sanctuary())

    def get_home_terrain_tile_codes(self):
        return self._game.get_game_board().get_valid_location_codes_terrain_type(self.get_home_terrain())

    def select_move(self):
        next_action = self._agent.determine_next_action(self._game, self)
        move = Move(self, next_action)
        return move

    def determine_valid_next_actions(self, move_type):
        if move_type == MoveType.PLACE_DWELLING:
            terrain_codes = self.get_home_terrain_tile_codes()
            valid_building_locations = [location_code for location_code in terrain_codes if self._game.get_game_board().get_structure(location_code).get_type() == Structures.NONE]
            return [PlaceDwellingAction(location_code) for location_code in valid_building_locations]

    def generate_player_state(self):
        return None