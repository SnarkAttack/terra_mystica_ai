from ..utilities import get_shovel_cost
from .exceptions import InvalidActionException

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


class TerraformNoBuildAction(Action):

    def __init__(self, location, terraform_to):
        self._location = location
        self._terraform_to = terraform_to

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

class TerraformBuildAction(Action):

    def __init__(self, location, terraform_to):
        self._location = location
        self._terraform_to = terraform_to

    def _raw_take_action(self, game, player):

        game_board = game.get_game_board()

        if game_board.get_terrain(self._location) == self._terraform_to:
            raise InvalidActionException("Cannot terraform to current terrain type")

        terrain_diff_cost = get_shovel_cost(game_board.get_terrain(self._location), self._terraform_to)
        terraforming_cost = player.get_terraform_worker_cost(terrain_diff_cost)
        build_cost = player.get_build_dwelling_cost()
        action_cost = terraforming_cost + build_cost
        print(action_cost)

        if player.get_workers() < action_cost.get_workers():
            raise InvalidActionException("Not enough workers to terraform")

        game_board.terraform_location(self._location, self._terraform_to)
        #game_board.modify_building()

        player.spend_resources(action_cost)
