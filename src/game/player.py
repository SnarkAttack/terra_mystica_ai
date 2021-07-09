from .action import (
    PassAction,
    PlaceDwellingAction,
    TerraformNoBuildAction,
    TerraformBuildAction,
    IncreaseShippingTrackAction,
    IncreaseExchangeTrackAction,
    UpgradeBuildingAction,
    SiphonPowerAction,
    DeclineSiphonPowerAction,
    PlayPriestToCultTrackAction,
    UsePriestToIncreaseCultTrackAction,
)
from ..components.structures import Structure
from .move import Move
from .resources import ResourceRequirements, ResourceGroup
from ..utilities.mappings import Factions, Actions, Structures, Terrains, Cults
from ..utilities.functions import get_shovel_cost, sort_location_codes
from ..components.faction_board import FactionBoard, WitchesFactionBoard, NomadsFactionBoard, FactionBoard
from ..utilities import MAX_PRIESTS, MAX_TRADING_POSTS, MAX_TEMPLES, MAX_STRONGHOLDS, MAX_SANCTUARIES, MAX_DWELLINGS
import copy
from ..utilities.loggers import game_logger

class Player(object):

    def __init__(self, game=None, faction=None, agent=None, other=None):

        self._game = game

        if other is None:
            if faction == Factions.NOMADS:
                self._faction_board = NomadsFactionBoard()
            elif faction == Factions.WITCHES:
                self._faction_board = WitchesFactionBoard()
            elif faction == None:
                # TODO: This is just to cheat deepcopy, figure out a better way
                self._faction_board = FactionBoard()
            else:
                raise NotImplementedError()

            self._faction = faction
            self._terrain = self._faction_board.get_home_terrain()
            self._agent = agent

            self._coins = self._faction_board.get_starting_coins()
            self._workers = self._faction_board.get_starting_workers()
            self._priests = 0
            self._vps = 20

            self._exchange_level = 0
            self._shipping_level = 0

            self._power1 = 5
            self._power2 = 7
            self._power3 = 0

            self._available_dwellings = MAX_DWELLINGS
            self._available_trading_posts = MAX_TRADING_POSTS
            self._available_strongholds = MAX_STRONGHOLDS
            self._available_temples = MAX_TEMPLES
            self._available_sanctuaries = MAX_SANCTUARIES

            self._available_priests = MAX_PRIESTS

            self._unused_town_tokens = 0

        else:
            self._agent = other._agent
            self._faction_board = copy.deepcopy(other._faction_board)
            self._faction = self._faction_board.get_faction()

            self._terrain = self._faction_board.get_home_terrain()

            self._coins = other._coins
            self._workers = other._workers
            self._priests = other._priests
            self._vps = other._vps

            self._exchange_level = other._exchange_level
            self._shipping_level = other._shipping_level

            self._power1 = other._power1
            self._power2 = other._power2
            self._power3 = other._power3

            self._available_dwellings = other._available_dwellings
            self._available_trading_posts = other._available_trading_posts
            self._available_strongholds = other._available_strongholds
            self._available_temples = other._available_temples
            self._available_sanctuaries = other._available_sanctuaries

            self._available_priests = other._available_priests

    def get_player_resource_str(self):
        return f"Faction {self._faction}:\n\tCoins: {self._coins}\n\tWorkers: {self._workers}\n\t" \
               f"Priests: {self._priests}\n\tPower: ({self._power1},{self._power2},{self._power3})\n\t" \
               f"VPs: {self._vps}"

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
        return self._faction_board.get_faction()

    def get_home_terrain(self):
        return self._faction_board.get_home_terrain()

    def get_resources(self):
        return ResourceGroup(
            coins=self._coins,
            workers=self._workers,
            priests=self._priests,
            power=self._power_3
        )

    def get_faction_board(self):
        return self._faction_board

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
        return self._faction_board.get_dwelling_build_cost()

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

    def max_available_power(self):
        return self._power3 + int(self._power2/2)

    def gain_resources(self, resource_income):
        self._coins += resource_income.get_coins()
        self._workers += resource_income.get_workers()
        self._priests += resource_income.get_priests()
        self._vps += resource_income.get_vps()
        self.add_power(resource_income.get_power())

    def spend_resources(self, resource_cost):
        self._coins -= resource_cost.get_coins()
        self._workers -= resource_cost.get_workers()
        self._priests -= resource_cost.get_priests()
        self._vps -= resource_cost.get_vps()
        self.spend_power(resource_cost.get_power())

    def take_income(self):
        self.gain_resources(self._faction_board._default_income)
        self.gain_resources(self._faction_board.get_income_from_dwellings(MAX_DWELLINGS-self._available_dwellings))
        self.gain_resources(self._faction_board.get_income_from_trading_posts(MAX_TRADING_POSTS-self._available_trading_posts))
        self.gain_resources(self._faction_board.get_income_from_stronghold(MAX_STRONGHOLDS-self._available_strongholds))
        self.gain_resources(self._faction_board.get_income_from_temples(MAX_TEMPLES-self._available_temples))
        self.gain_resources(self._faction_board.get_income_from_sanctuary(MAX_SANCTUARIES-self._available_sanctuaries))

    def get_home_terrain_tile_codes(self):
        return self._game.get_game_board().get_valid_location_codes_terrain_type(self.get_home_terrain())

    def select_move(self):
        next_action = self._agent.determine_next_action(self._game, self)
        move = Move(self, next_action)
        return move

    def can_pay_cost(self, resource_cost):
        return self._coins >= resource_cost.get_coins() and \
               self._workers >= resource_cost.get_workers() and \
               self._priests >= resource_cost.get_priests() and \
               self._vps >= resource_cost.get_vps() and \
               self.max_available_power() >= resource_cost.get_power()


    def get_all_adjacent_locations(self):
        return sorted(self._game.get_game_board().get_adjacent_modifiable_locations(self._faction), key=sort_location_codes)

    def increase_shipping_track(self):
        self._shipping_level += 1
        self.gain_resources(self._faction_board._shipping_track_vps[self._shipping_level])

    def increase_exchange_track(self):
        self._exchange_level += 1
        self.gain_resources(self._faction_board._exchange_track_vps[self._exchange_level])

    def increase_structure_count(self, struct_type):
        if struct_type == Structures.DWELLING:
            self._available_dwellings += 1
        elif struct_type == Structures.TRADING_POST:
            self._available_trading_posts += 1
        elif struct_type == Structures.STRONGHOLD:
            self._available_strongholds += 1
        elif struct_type == Structures.TEMPLE:
            self._available_temples += 1
        elif struct_type == Structures.SANCTUARY:
            self._available_sanctuaries += 1

    def decrease_structure_count(self, struct_type):
        if struct_type == Structures.DWELLING:
            self._available_dwellings -= 1
        elif struct_type == Structures.TRADING_POST:
            self._available_trading_posts -= 1
        elif struct_type == Structures.STRONGHOLD:
            self._available_strongholds -= 1
        elif struct_type == Structures.TEMPLE:
            self._available_temples -= 1
        elif struct_type == Structures.SANCTUARY:
            self._available_sanctuaries -= 1

    def upgrade_building(self, location_code, struct_from, struct_to):
        game_board = self._game.get_game_board()
        self.increase_structure_count(struct_from)
        self.decrease_structure_count(struct_to)
        game_board.place_structure(struct_to, location_code, self._faction)

    def get_shipping_upgrade_cost(self):
        return self._faction_board.get_shipping_upgrade_cost()

    def get_exchange_upgrade_cost(self):
        return self._faction_board.get_exchange_upgrade_cost()

    def have_available_upgrade_structure(self, struct_type, upgrade_to_stronghold):
        if struct_type == Structures.DWELLING:
            return self._available_trading_posts > 0
        elif struct_type == Structures.TRADING_POST:
            if upgrade_to_stronghold:
                return self._available_strongholds > 0
            else:
                return self._available_temples > 0
        elif struct_type == Structures.TEMPLE:
            return self._available_sanctuaries > 0
        else:
            game_logger.error("Asking for upgrade count for struct that can't upgrade")
            raise ValueError("Asking for upgrade count for struct that can't upgrade")

    def get_siphon_power_gain(self, power_val):
        return ResourceGroup(power=power_val, vps=-1*(power_val-1))

    def determine_valid_terraform_no_build_actions(self):
        valid_actions = []
        game_board = self._game.get_game_board()
        valid_terraforming_locations = self.get_all_adjacent_locations()
        for location_code in valid_terraforming_locations:
            for terrain in [t for t in Terrains if t != Terrains.NONE and t != Terrains.RIVER]:
                location_terrain = game_board.get_terrain(location_code)
                if location_terrain != terrain:
                    terrain_diff_val = get_shovel_cost(location_terrain, terrain)
                    resource_cost = self.get_terraform_worker_cost(terrain_diff_val)
                    if self.can_pay_cost(resource_cost):
                        valid_actions.append(TerraformNoBuildAction(location_code, terrain, resource_cost))
        return valid_actions

    def determine_valid_terraform_build_actions(self):
        valid_actions = []
        if self._available_dwellings > 0:
                game_board = self._game.get_game_board()
                valid_terraforming_locations = self.get_all_adjacent_locations()
                build_cost = self._faction_board._dwelling_build_cost
                for location_code in valid_terraforming_locations:
                    terrain_diff_val = get_shovel_cost(game_board.get_terrain(location_code), self._terrain)
                    resource_cost = self.get_terraform_worker_cost(terrain_diff_val)
                    resource_cost += build_cost
                    if self.can_pay_cost(resource_cost):
                        valid_actions.append(TerraformBuildAction(location_code, self._terrain, resource_cost))
                valid_building_locations = self._game.get_game_board().get_valid_building_locations(self._faction, Structures.DWELLING)
                for location_code in valid_building_locations:
                    if self.can_pay_cost(build_cost):
                        valid_actions.append(TerraformBuildAction(location_code, self._terrain, resource_cost))
        return valid_actions

    def determine_valid_shipping_increase_action(self):
        resource_cost = self.get_shipping_upgrade_cost()
        if self.can_pay_cost(resource_cost) and self._shipping_level < len(self._faction_board._shipping_track_vps)-1:
            return [IncreaseShippingTrackAction(resource_cost)]
        return []

    def determine_valid_exchange_increase_action(self):
        resource_cost = self.get_exchange_upgrade_cost()
        if self.can_pay_cost(resource_cost) and self._exchange_level < len(self._faction_board._exchange_track_vps)-1:
            return [IncreaseExchangeTrackAction(resource_cost)]
        return []

    def determine_valid_upgrade_actions(self):
        valid_actions = []
        game_board = self._game.get_game_board()
        faction_structs = game_board.get_all_player_structures(self)
        for struct in faction_structs:
            struct_type = struct.get_type()
            if struct.get_type == Structures.TRADING_POST:
                upgrade_to_stronghold = True
                resource_cost = self._faction_board.get_upgrade_cost(struct_type, upgrade_to_stronghold, False)
                if self.can_pay_cost(resource_cost) and self.have_available_upgrade_structure(struct_type, upgrade_to_stronghold):
                    valid_actions.append(UpgradeBuildingAction(struct.get_location(), upgrade_to_stronghold, resource_cost))
            upgrade_to_stronghold = False
            adj_opp = game_board.is_opponent_adjacent(struct.get_location(), self._faction)
            resource_cost = self._faction_board.get_upgrade_cost(struct.get_type(), False, adj_opp)
            if self.can_pay_cost(resource_cost) and self.have_available_upgrade_structure(struct_type, upgrade_to_stronghold):
                valid_actions.append(UpgradeBuildingAction(struct.get_location(), upgrade_to_stronghold, resource_cost))
        return valid_actions

    def determine_valid_siphon_power_actions(self, power_val):
        valid_actions = []
        if self._vps >= power_val-1:
            valid_actions.append(SiphonPowerAction(self.get_siphon_power_gain(power_val)))
        valid_actions.append(DeclineSiphonPowerAction())
        return valid_actions

    def determine_valid_priest_to_cult_track_actions(self):
        valid_actions = []
        cult_board = self._game._cult_board
        for cult in [c for c in Cults if c != Cults.NONE]:
            cult_loc = cult_board.get_faction_location_on_cult_track(cult, self.get_faction())
            if (cult_loc < 10 and self._unused_town_tokens > 0 or \
                cult_loc < 9) and cult_board.find_cult_track_first_unused_priest_space(cult) and \
                self._priests >= 1:
                valid_actions.append(PlayPriestToCultTrackAction(cult))
        return valid_actions

    def determine_valid_use_priest_on_cult_track_actions(self):
        valid_actions = []
        cult_board = self._game._cult_board
        for cult in [c for c in Cults if c != Cults.NONE]:
            cult_loc = cult_board.get_faction_location_on_cult_track(cult, self.get_faction())
            if (cult_loc < 10 and self._unused_town_tokens > 0 or cult_loc < 9) and self._priests >= 1:
                valid_actions.append(UsePriestToIncreaseCultTrackAction(cult))
        return valid_actions


    def determine_valid_next_actions(self, pending_move):
        move_type = pending_move.get_move_type()
        possible_actions = []
        if move_type == Actions.PLACE_DWELLING:
            valid_building_locations = self._game.get_game_board().get_valid_dwelling_placement_locations(self._faction, Structures.DWELLING)
            possible_actions += [PlaceDwellingAction(location_code) for location_code in valid_building_locations]
        if move_type in [Actions.STANDARD_ACTION, Actions.TERRAFORM_NO_BUILD]:
            possible_actions += self.determine_valid_terraform_no_build_actions()
        if move_type in [Actions.STANDARD_ACTION, Actions.TERRAFORM_BUILD]:
            possible_actions += self.determine_valid_terraform_build_actions()
        if move_type in [Actions.STANDARD_ACTION, Actions.INCREASE_EXCHANGE_TRACK]:
            possible_actions += self.determine_valid_exchange_increase_action()
        if move_type in [Actions.STANDARD_ACTION, Actions.INCREASE_SHIPPING_TRACK]:
            possible_actions += self.determine_valid_shipping_increase_action()
        if move_type in [Actions.STANDARD_ACTION, Actions.UPGRADE_BUILDING_TRACK]:
            possible_actions += self.determine_valid_upgrade_actions()
        if move_type in [Actions.STANDARD_ACTION, Actions.PLAY_PRIEST_TO_CULT_TRACK]:
            possible_actions += self.determine_valid_priest_to_cult_track_actions()
        if move_type in [Actions.STANDARD_ACTION, Actions.USE_PRIEST_TO_INCREASE_CULT_TRACK]:
            possible_actions += self.determine_valid_use_priest_on_cult_track_actions()
        if move_type in [Actions.STANDARD_ACTION, Actions.PASS]:
            possible_actions.append(PassAction())
        if move_type in [Actions.SIPHON_POWER]:
            power_val = pending_move.get_power_val()
            possible_actions += self.determine_valid_siphon_power_actions(power_val)

        return possible_actions

    def generate_player_state(self):
        return None