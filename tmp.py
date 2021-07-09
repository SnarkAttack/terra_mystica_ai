from src.components.game_board import OriginalGameBoard
from src.game.game import TerraMysticaGame
from src.game.player import Player
from src.utilities.mappings import BoardType, Factions
from src.neural_network.network import TerraMysticaAINetwork
from src.neural_network.agent import Agent
from src.neural_network.memory import Memory
import tensorflow as tf
from src.game.action import all_actions, PlaceDwellingAction

memory = Memory('memory', max_moves=1000)

agent1 = Agent(memory=memory)
agent2 = Agent(memory=memory)

for i in range(1):
    game = TerraMysticaGame(BoardType.ORIGINAL)
    player1 = Player(game, Factions.WITCHES, agent=agent1)
    player2 = Player(game, Factions.NOMADS, agent=agent2)
    game.add_player(player1)
    game.add_player(player2)
    game.play_game()