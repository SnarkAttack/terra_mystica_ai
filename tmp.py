from src.components.game_board import OriginalGameBoard
from src.game.game import TerraMysticaGame
from src.game.player import Player
from src.mappings import BoardType, Factions
from src.neural_network.network import TerraMysticaAINetwork
from src.neural_network.mcts import id_hash
from src.neural_network.agent import Agent

setup_game = TerraMysticaGame(BoardType.ORIGINAL)
agent1 = Agent()
agent2 = Agent()
player1 = Player(setup_game, Factions.WITCHES, agent=agent1)
player2 = Player(setup_game, Factions.NOMADS, agent=agent2)
# Figure out a better way to do this
agent1.play_game(setup_game)
agent2.play_game(setup_game)

for i in range(5):
    game = TerraMysticaGame(BoardType.ORIGINAL)
    game2 = TerraMysticaGame(BoardType.ORIGINAL)
    assert id_hash(game) == id_hash(game2)
    player1 = Player(game, Factions.WITCHES, agent=agent1)
    player2 = Player(game, Factions.NOMADS, agent=agent2)
    game.add_player(player1)
    game.add_player(player2)
    game.play_game()