from src.components.game_board import OriginalGameBoard
from src.game.game import TerraMysticaGame
from src.game.player import Player
from src.mappings import BoardType, Factions
from src.neural_network.network import TerraMysticaAINetwork
from src.neural_network.mcts import id_hash
from src.neural_network.agent import Agent
import tensorflow as tf

agent1 = Agent()
agent2 = Agent()

for i in range(5):
    game = TerraMysticaGame(BoardType.ORIGINAL)
    game2 = TerraMysticaGame(BoardType.ORIGINAL)
    player1 = Player(game, Factions.WITCHES, agent=agent1)
    player2 = Player(game, Factions.NOMADS, agent=agent2)
    game.add_player(player1)
    game.add_player(player2)
    game.play_game()

game = TerraMysticaGame(BoardType.ORIGINAL)

agent1.get_state_tree(game)

# old_game = TerraMysticaGame(BoardType.ORIGINAL)
# game_state = old_game.get_game_board().generate_board_state()

# for i in range(2):
#     game = TerraMysticaGame(BoardType.ORIGINAL)
#     game2 = TerraMysticaGame(BoardType.ORIGINAL)
#     #assert id_hash(game) == id_hash(game2)
#     player1 = Player(game, Factions.WITCHES, agent=agent1)
#     player2 = Player(game, Factions.NOMADS, agent=agent2)
#     print(tf.reduce_all(tf.equal(game_state, game.get_game_board().generate_board_state())))
#     game.add_player(player1)
#     game.add_player(player2)
#     print(f"Iter {i}")
#     print(id_hash(game))
#     #game.play_game()