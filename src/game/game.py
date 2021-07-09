from ..utilities.mappings import BoardType, GamePhase, Actions
from ..components.game_board import OriginalGameBoard, TinyGameBoard
from ..components.cult_board import CultBoard
from ..utilities.loggers import game_logger
from ..utilities.functions import convert_location_code_to_row_col
from .player import Player
from copy import deepcopy
from .action import PendingMove

MAX_ROUNDS = 6

class GameState(object):

    def __init__(self, game):

        self._game_board_state = game.get_game_board().generate_board_state()
        self._player_states = [player.generate_player_state() for player in game.get_players()]
        self._cult_board_state = game.get_cult_board()

    def get_game_board_state(self):
        return self._game_board_state

def get_default_game(board_type):
    return TerraMysticaGame(board_type)

class TerraMysticaGame(object):

    def __init__(self, board_type):
        if board_type == BoardType.ORIGINAL:
            self._game_board = OriginalGameBoard()
        elif board_type == BoardType.TINY:
            self._game_board = TinyGameBoard()
        else:
            raise NotImplementedError()

        self._cult_board = CultBoard()

        self._ready = False

        self._players = []
        self._pending_moves = []
        self._current_phase = GamePhase.SETUP
        self._player_order = []
        self._round = 0
        self._is_done = False

        self._passed_players = []

        self._current_move = None

        self._log = True

    def add_player(self, player):
        if player not in self._players:
            self._players.append(player)
            self._player_order.append(player)
        else:
            raise ValueError("Player already exists")

    def get_game_board(self):
        return self._game_board

    def get_cult_board(self):
        return self._cult_board

    def get_players(self):
        return self._players

    def get_next_player(self):
        return self._pending_moves[0].get_player()

    def get_player_of_faction(self, faction):
        return [player for player in self._players if player._faction == faction][0]

    def play_game(self):

        game_logger.info("Starting game")
        game_logger.info(f"Factions: {', '.join([str(int(player.get_faction())) for player in self._players])}")

        game_logger.info("***** Placing starting dwellings *****")
        for player in self._players:
            self._pending_moves.append(PendingMove(player, Actions.PLACE_DWELLING))
        for player in self._players[::-1]:
            self._pending_moves.append(PendingMove(player, Actions.PLACE_DWELLING))

        while not self._is_done:
            self.determine_next_move()

        self.score_game()

        players_by_score = sorted(self._players, key=lambda x: x._vps, reverse=True)

        game_logger.info(f"Final scores:")
        for player in players_by_score:
            game_logger.info(f"\t{str(int(player.get_faction()))}: {player.get_vps()}")
        game_logger.info(f"{str(int(players_by_score[0].get_faction()))} wins\n")

    def determine_next_move(self):
        self._log = True
        current_move = self._pending_moves[0]
        # Set conditional flags signalling change to next game stage, etc:
        selected_move = current_move.get_player().select_move()
        game_logger.info(f"Faction {selected_move.get_player().get_faction()} "
            f"selects action {selected_move.get_action().get_text_str()}")
        round_change = self.perform_move(selected_move)
        game_logger.debug([str(a) for a in self._pending_moves])
        if round_change:
            game_logger.info(f"***** Round {self._round} *****")
            for player in self._players:
                game_logger.info(player.get_player_resource_str())
        self._log = False

    def perform_move(self, move):
        round_change = False
        self._pending_moves.pop(0)
        action = move.get_action()
        action.take_action(self, move.get_player())
        if len(self._pending_moves) == 0:
            if self._log:
                game_logger.debug("No pending moves left")
            self.setup_next_round()
            round_change = True
        return round_change

    def setup_next_round(self):
        if self._round == MAX_ROUNDS:
            self._is_done = True
        elif self._round < MAX_ROUNDS:
            for player in self._players:
                player.take_income()
                self._pending_moves.append(PendingMove(player, Actions.STANDARD_ACTION))
            self._round += 1

    def get_all_valid_next_actions(self):
        current_move = self._pending_moves[0]
        actions = current_move.get_player().determine_valid_next_actions(current_move)
        return current_move.get_player(), actions

    def get_high_score(self):
        return max([player.get_vps() for player in self._players])

    def is_done(self):
        return self._is_done

    def get_game_state(self):
        return self._game_board.generate_board_state()

    def _get_location_row_col(self, location_code):
        return ord(location_code[:1].upper())-ord('A'), int(location_code[1:])-1

    def _sum_row_col(self, location_code):
        row, col = convert_location_code_to_row_col(location_code)
        return (row+1)+(col+1)

    def get_player_by_faction(self, faction):
        return [player for player in self._players if player.get_faction() == faction][0]

    def replace_player_by_faction(self, faction):
        for i, player in enumerate(self._players):
            if player.get_faction() == faction:
                break
        new_player = Player(game=self, other=player)
        print(f"{player},{new_player}")
        self._players[i] = new_player
        return new_player

    # Made up scoring system where the score is base score of
    # 20 + sum of row/column for each placed dwelling. Just to check
    # if we learn things, would expect dwellings to end up in bottom right
    def score_game(self):
        for player in self._players:
            player_structs = self._game_board.get_all_player_structures(player)
            locations = [struct.get_location() for struct in player_structs]
            add_score = sum([self._sum_row_col(location) for location in locations])
            player._vps += add_score

    def get_cult_board(self):
        return None

    def get_game_state(self):
        return GameState(self)

    def add_pending_move_end(self, pending_move):
        self._pending_moves.append(pending_move)

    def add_pending_move_start(self, pending_move):
        self._pending_moves.insert(0, pending_move)

    def add_player_pass(self, player):
        self._passed_players.append(player)
