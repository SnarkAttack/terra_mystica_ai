from .mcts import MCTS
from .network import TerraMysticaAINetwork

class Agent(object):

    def __init__(self):
        self._network = TerraMysticaAINetwork()
        self._mcts = None

    def play_game(self, game):
        if self._mcts is None:
            self._mcts = MCTS(self._network, game)

    def determine_next_action(self, game, player):
        best_move = self._mcts.determine_next_action(game, player)
        return best_move