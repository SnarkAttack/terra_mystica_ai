from ..utilities.functions import get_shovel_cost
from ..utilities.locations import all_locations
from .exceptions import InvalidActionException
from ..utilities.mappings import Structures, Terrains

class Action(object):

    def __init__(self):
        pass

    def take_action(self, game, player):
        try:
            self._raw_take_action(game, player)
        except NotImplementedError as e:
            raise e
        except Exception as e:
            print(e)

    def _raw_take_action(self, game, player):
        raise NotImplementedError()

    def get_text_str(self):
        return ""

class TerraformNoBuildAction(Action):

    def __init__(self, location, terraform_to):
        self._location = location
        self._terraform_to = terraform_to

    def __eq__(self, other):
        return self._location == other._location and self._terraform_to == other._terraform_to

    def _raw_take_action(self, game, player):

        game_board = game.get_game_board()

        if game_board.get_terrain(self._location) == self._terraform_to:
            raise InvalidActionException("Cannot terraform to current terrain type")

        terrain_diff_cost = get_shovel_cost(game_board.get_terrain(self._location), self._terraform_to)
        action_cost = player.get_terraform_worker_cost(terrain_diff_cost)

        if player.get_workers() < action_cost.get_workers():
            raise InvalidActionException("Not enough workers to terraform")

        game_board.terraform_location(self._location, self._terraform_to)

        player.spend_resources(action_cost)

    def get_text_str(self):
        return f"TerraformNoBuildAction at {self._location} to {self._terraform_to}"

class TerraformBuildAction(Action):

    def __init__(self, location, terraform_to):
        self._location = location
        self._terraform_to = terraform_to

    def __eq__(self, other):
        return self._location == other._location and self._terraform_to == other._terraform_to

    def _raw_take_action(self, game, player):

        game_board = game.get_game_board()

        terrain_diff_cost = get_shovel_cost(game_board.get_terrain(self._location), self._terraform_to)
        terraforming_cost = player.get_terraform_worker_cost(terrain_diff_cost)
        build_cost = player.get_build_dwelling_cost()
        action_cost = terraforming_cost + build_cost

        if player.get_workers() < action_cost.get_workers():
            raise InvalidActionException("Not enough workers to terraform")

        game_board.terraform_location(self._location, self._terraform_to)
        #game_board.modify_building()

        player.spend_resources(action_cost)

    def get_text_str(self):
        return f"TerraformBuildAction at {self._location} to {self._terraform_to}"

class PlaceDwellingAction(Action):

    def __init__(self, location):
        super().__init__()
        self._location = location

    def __eq__(self, other):
        return self._location == other._location

    def get_location(self):
        return self._location

    def _raw_take_action(self, game, player):

        game_board = game.get_game_board()

        if game_board.get_structure(self._location).get_type() != Structures.NONE:
            raise InvalidActionException("Building already located in this place")

        if game_board.get_terrain(self._location) != player.get_home_terrain():
            raise InvalidActionException("Terrains location does not match faction")

        game_board.place_dwelling(self._location, player.get_faction())
        player._available_dwellings -= 1

    def get_text_str(self):
        return f"PlaceDwelling at location {self._location}"


# Will be final list of all available actions
all_actions = []


no_build_actions = []
build_actions = []
place_dwelling_actions = []

for location in all_locations:
    for terrain in Terrains:
        no_build_actions.append(TerraformNoBuildAction(location, terrain))
        build_actions.append(TerraformBuildAction(location, terrain))
    place_dwelling_actions.append(PlaceDwellingAction(location))

all_actions += no_build_actions
all_actions += build_actions

print(len(all_actions))

def get_actions_mask(valid_actions):
    return [1 if action in all_actions else 0 for action in valid_actions]
