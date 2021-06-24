from ..mappings import BoardType, GamePhase, MoveType
from ..components.game_board import OriginalGameBoard

class PendingMove(object):

    def __init__(self, player, move_type):
        self._player = player
        self._move_type = move_type

    def get_player(self):
        return self._player

    def get_move_type(self):
        return self._move_type

class TerraMysticaGame(object):

    def __init__(self, board_type):
        if board_type == BoardType.ORIGINAL:
            self._game_board = OriginalGameBoard()
        else:
            raise NotImplementedError()

        self._ready = False

        self._players = []
        self._pending_moves = []
        self._current_phase = GamePhase.SETUP
        self._player_order = []
        self._round = 0
        self._is_done = False

        self._current_move = None

    def add_player(self, player):
        if player not in self._players:
            self._players.append(player)
            self._player_order.append(player)
        else:
            raise ValueError("Player already exists")

    def get_game_board(self):
        return self._game_board

    def get_cult_board(self):
        pass

    def get_players(self):
        return self._players

    def play_game(self):
        for player in self._players:
            self._pending_moves.append(PendingMove(player, MoveType.PLACE_DWELLING))
        for player in self._players[::-1]:
            self._pending_moves.append(PendingMove(player, MoveType.PLACE_DWELLING))

        while not self._is_done:
            self.perform_next_move()

    def perform_next_move(self):
        self._current_move = self._pending_moves.pop(0)
        # Set conditional flags signalling change to next game stage, etc:
        if len(self._pending_moves) == 0:
            self._is_done = True
        selected_move = self._current_move.get_player().select_move()
        self.perform_move(selected_move)
        self._current_move = None

    def perform_move(self, move):
        action = move.get_action()
        action.take_action(self, move.get_player())

    def get_all_valid_next_actions(self):
        current_move = self._current_move
        actions = current_move.get_player().determine_valid_next_actions(current_move.get_move_type())
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
        row, col = self._get_location_row_col(location_code)
        return row+col

    def get_player_by_faction(self, faction):
        return [player for player in self._players if player.get_faction() == faction][0]

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

