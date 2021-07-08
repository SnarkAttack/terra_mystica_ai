from .game import PendingMove
from ..utilities.functions import get_shovel_cost
from ..utilities.locations import all_locations
from .exceptions import InvalidActionException
from ..utilities.mappings import Structures, Terrains, Actions
from .resources import ResourceRequirements, ResourceGroup

class Action(object):

    def __init__(self, resource_cost=None):
        self._resource_cost = resource_cost

    def take_action(self, game, player):
        pass

    def _raw_take_action(self, game, player):
        raise NotImplementedError()

    def get_text_str(self):
        return ""

    def __eq__(self, other):
        return type(self) == type(other)

class TerraformNoBuildAction(Action):

    def __init__(self, location, terraform_to, resource_cost=None):
        super().__init__(resource_cost)
        self._location = location
        self._terraform_to = terraform_to

    def __eq__(self, other):
        if super().__eq__(other):
            return self._location == other._location and self._terraform_to == other._terraform_to
        return False

    def take_action(self, game, player):

        game_board = game.get_game_board()

        game_board.terraform_location(self._location, self._terraform_to)
        player.spend_resources(self._resource_cost)

        game.add_pending_move_end(PendingMove(player, Actions.STANDARD_ACTION))

    def get_text_str(self):
        return f"TerraformNoBuildAction at {self._location} to {self._terraform_to}"

class TerraformBuildAction(Action):

    def __init__(self, location, terraform_to, resource_cost=None):
        super().__init__(resource_cost)
        self._location = location
        self._terraform_to = terraform_to

    def __eq__(self, other):
        if super().__eq__(other):
            return self._location == other._location and self._terraform_to == other._terraform_to
        return False

    def take_action(self, game, player):

        game_board = game.get_game_board()

        game_board.terraform_location(self._location, self._terraform_to)
        game_board.place_dwelling(self._location, player.get_faction())
        player.spend_resources(self._resource_cost)
        player._available_dwellings -= 1

        game.add_pending_move_end(PendingMove(player, Actions.STANDARD_ACTION))

    def get_text_str(self):
        return f"TerraformBuildAction at {self._location} to {self._terraform_to}"

class PlaceDwellingAction(Action):

    def __init__(self, location, resource_cost=None):
        super().__init__(resource_cost)
        self._location = location

    def __eq__(self, other):
        if super().__eq__(other):
            return self._location == other._location
        return False

    def get_location(self):
        return self._location

    def take_action(self, game, player):

        game_board = game.get_game_board()
        game_board.place_dwelling(self._location, player.get_faction())
        player._available_dwellings -= 1

    def get_text_str(self):
        return f"PlaceDwelling at location {self._location}"

class IncreaseShippingTrackAction(Action):

    def __init__(self, resource_cost=None):
        super().__init__(resource_cost)

    def __eq__(self, other):
        return type(self) == type(other)

    def take_action(self, game, player):

        player.spend_resources(self._resource_cost)
        player.increase_shipping_track()

        game.add_pending_move_end(PendingMove(player, Actions.STANDARD_ACTION))

class IncreaseExchangeTrackAction(Action):

    def __init__(self, resource_cost=None):
        super().__init__(resource_cost)

    def __eq__(self, other):
        return type(self) == type(other)

    def take_action(self, game, player):

        player.spend_resources(self._resource_cost)
        player.increase_exchange_track()

        game.add_pending_move_end(PendingMove(player, Actions.STANDARD_ACTION))

class UpgradeBuildingAction(Action):

    # TODO: Dislike this special flag for upgrading to stronghold, but there's a
    # decision point when upgrading the trasding post and I don't know a better
    # way to represent that
    def __init__(self, location_code, upgrade_to_stronghold, resource_cost=None):
        super().__init__(resource_cost)
        self._location_code = location_code
        self._upgrade_to_stronghold = upgrade_to_stronghold

    def __eq__(self, other):
        if type(self) == type(other):
            return self._location_code == other._location_code and \
                self._upgrade_to_stronghold == other._upgrade_to_stronghold

    def take_action(self, game, player):

        game_board = game.get_game_board()

        structure = game_board.get_structure_at_location(self._location_code)
        orig_struct_type = structure.get_type()

        if orig_struct_type == Structures.DWELLING:
            struct_to = Structures.TRADING_POST
        elif orig_struct_type == Structures.TRADING_POST:
            if self._upgrade_to_stronghold:
                struct_to = Structures.STRONGHOLD
            else:
                struct_to = Structures.TEMPLE
        elif orig_struct_type == Structures.TEMPLE:
            struct_to = Structures.SANCTUARY

        player.spend_resources(self._resource_cost)
        player.upgrade_building(self._location_code, orig_struct_type, struct_to)

        game.add_pending_move_end(PendingMove(player, Actions.STANDARD_ACTION))

class SiphonPowerAction(Action):

    def __init__(self, power_val, resource_cost=None):
        super().__init__(resource_cost)
        self._power_val = power_val

    def __eq__(self, other):
        return type(self) == type(other)

    def take_action(self, game, player):

        # Hacky, expecting the vps passed in to be negative
        player.gain_resources(self._resource_cost)

class DeclineSiphonPowerAction(Action):

    def __init__(self, power_val, resource_cost=None):
        super().__init__(resource_cost)
        self._power_val = power_val

    def __eq__(self, other):
        return type(self) == type(other)

    def take_action(self, game, player):
        pass

class PlayPriestToCultTrackAction(Action):

    def __init__(self, cult, resource_cost=None):
        super().__init__(resource_cost)
        self._cult = cult

    def __eq__(self, other):
        if super().__eq__(other):
            return self._cult == other._cult
        return False

    def get_cult(self):
        return self.get_cult

    def take_action(self, game, player):

        cult_board = game.get_cult_board()
        action_cost = ResourceRequirements(priests=1)

        if player.get_priests() < action_cost.get_priests():
            raise InvalidActionException("Not enough priests")

        cult_board.play_priest(self._cult, player.get_faction())

        player._available_priests -= 1
        player.spend_resources(action_cost)

        game.add_pending_move_end(PendingMove(player, Actions.STANDARD_ACTION))

class PassAction(Action):

    def __init__(self):
        super().__init__(ResourceRequirements())

    def __eq__(self, other):
        return super().__eq__(other)

    def take_action(self, game, player):
        game.add_player_pass(player)

    def get_text_str(self):
        return f"Pass"


# Will be final list of all available actions
all_actions = []

no_build_actions = []
build_actions = []
place_dwelling_actions = []
upgrade_structure_actions = []

for location in all_locations:
    for terrain in Terrains:
        no_build_actions.append(TerraformNoBuildAction(location, terrain))
        build_actions.append(TerraformBuildAction(location, terrain))
    place_dwelling_actions.append(PlaceDwellingAction(location))
    for val in [True, False]:
        upgrade_structure_actions.append(UpgradeBuildingAction(location, val))

all_actions += no_build_actions
all_actions += build_actions
all_actions += place_dwelling_actions
all_actions += upgrade_structure_actions
all_actions.append(IncreaseShippingTrackAction())
all_actions.append(IncreaseExchangeTrackAction())
all_actions.append(SiphonPowerAction())
all_actions.append(DeclineSiphonPowerAction())
all_actions.append(PassAction())

action_space = len(all_actions)

def get_actions_mask(valid_actions):
    return [1 if all_actions[i] in valid_actions else 0 for i in range(action_space)]
