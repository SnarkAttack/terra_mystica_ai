from .mcts import MCTS
from .network import TerraMysticaAINetwork

class Agent(object):

    def __init__(self, memory):
        self._network = TerraMysticaAINetwork()
        self._memory = memory

    def determine_next_action(self, game, player):
        mcts = MCTS(self._network)
        root, best_move = mcts.determine_next_action(game, player)
        self._memory.add_to_st_memory(root.get_game_state())
        if self._memory.check_st_memory_stored():
            print("Adding to long term memory")
            self._memory.add_to_lt_memory()
        return best_move

    def get_state_tree(self, game):
        return self._mcts.get_state_tree(game)