from .mcts import MCTS
from .network import TerraMysticaAINetwork

class Agent(object):

    def __init__(self):
        self._network = TerraMysticaAINetwork()
        self._mcts = MCTS(self._network)

    def determine_next_action(self, game, player):
        if self._mcts is None:
            self._mcts = MCTS(self._network, game)
        best_move = self._mcts.determine_next_action(game, player)
        return best_move

    def get_state_tree(self, game):
        return self._mtcs.get_state_tree(game)