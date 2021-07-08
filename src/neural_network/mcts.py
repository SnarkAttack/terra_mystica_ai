import numpy as np
from copy import deepcopy, copy
import hashlib

from ..game.move import Move
from ..utilities.locations import all_locations
from ..utilities.loggers import log_timing_info
from datetime import datetime
from ..game.action import get_actions_mask, action_space, all_actions

C = 1

class MCTSNode(object):

    def __init__(self, game, current_player=None, parent=None, probability=0, action=None):
        self._parent = parent
        self._children = []
        self._child_probs = []
        self._visits = 0
        self._value = 0
        self._probability = probability
        self._action = action

        self._game = game
        self._current_player = current_player

        # Don't want to propogate value of game_ending node we have already found,
        # so this is flipped if node contains a finished game and we have processed it
        self._is_found_leaf_node = False

    def _ucb(self):
        # Visits + 1e-5 is to make sure we aren't dividing by 0, while not actually effecting the
        # final result significantly
        return self._value + C * np.sqrt(np.log(self._parent.get_visits())/(self._visits+1e-5))

    # tau = 0 is pure exploration, tau = 1 is pure exploitation
    def _uci(self, tau):
        return tau*self._value + (1-tau)*(C * self._probability*(np.sqrt(self._parent.get_visits())/(self._visits+1e-5)))

    def get_current_player(self):
        return self._current_player

    def get_action(self):
        return self._action

    def get_num_children(self):
        return len(self._children)

    def get_children(self):
        return self._children

    def get_action(self):
        return self._action

    def get_visits(self):
        return self._visits

    def get_game(self):
        return self._game

    def get_parent(self):
        return self._parent

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def is_found_leaf_node(self):
        return self._is_found_leaf_node

    def set_is_found_leaf_node(self):
        self._is_found_leaf_node = True

    def increment_visits(self):
        self._visits += 1

    def increase_visits(self, visit_count):
        self._visits += visit_count

    def is_leaf(self):
        return len(self._children) == 0

    def select_next_node(self, tau):
        start_time = datetime.now()
        best_node = max(self._children, key=lambda x: x._uci(tau))
        end_time = datetime.now()
        log_timing_info(f"select_next_node time: {end_time-start_time}")
        return best_node

    def backprop_value(self, v):
        self._value += v
        return self._value

    def get_game_state(self):
        return self._game.get_game_state()

    def generate_all_valid_next_states(self, player, valid_next_actions, probs, add_noise=True):
        start_time = datetime.now()
        valid_probs = [probs[i] for i in range(action_space) if all_actions[i] in valid_next_actions]
        for action, prob in zip(valid_next_actions, valid_probs):
            game_copy = deepcopy(self._game)
            game_copy._log = False
            move = Move(player, action)
            game_copy.perform_move(move)
            child_node = MCTSNode(
                game=game_copy,
                current_player=player,
                parent=self,
                probability=prob,
                action=action
            )
            self._children.append(child_node)
            self._child_probs.append(prob)
        end_time = datetime.now()
        log_timing_info(f"generate_all_valid_next_states time: {end_time-start_time}")

    def is_game_done(self):
        return self._game.is_done()

    def get_highest_value_visited_child(self):
        value_children = sorted(self._children, key=lambda x: x._value, reverse=True)
        for child in value_children:
            if child.get_visits() > 0:
                return child

    def expand(self, tree):
        player, valid_next_actions = self.get_game().get_all_valid_next_actions()
        action_mask = get_actions_mask(valid_next_actions)
        probs = tree._network.predict_actions(self.get_game_state(), action_mask)
        self.generate_all_valid_next_states(player, valid_next_actions, probs, tree.add_noise())

    def determine_value(self, network):
        is_done = self.is_game_done()
        if is_done:
            self._game.score_game()
            high_score = self._game.get_high_score()
            player_score = self._game.get_player_by_faction(self._current_player.get_faction()).get_vps()
            if player_score == high_score:
                #value = high_score
                value = 1
            else:
                #value = player_score - high_score
                value = -1
        else:
            value = network.predict_value(self.get_game_state())
        return value, is_done


class MCTS(object):

    def __init__(self, network, num_steps=10, add_noise=True):
        self._network = network
        self._num_steps = num_steps
        self._add_noise = add_noise

    def get_add_noise(self):
        return self._add_noise

    def _linear_tau_step(self, current_step):
        return current_step/(self._num_steps*2)

    def _flip_tau_step(self, current_step):
        if current_step < self._num_steps/2:
            return 0
        else:
            return 1

    def _mid_tau_step(self, current_step):
        return 0.5

    def determine_next_action(self, game, our_player):
        curr_root = MCTSNode(
            game=game,
            current_player=our_player,
        )

        if curr_root.get_num_children() == 0:
            curr_root.expand(self)

        for i in range(self._num_steps):
            tau = self._mid_tau_step(i)
            self.step(curr_root, our_player, 0)

        best_child = curr_root.get_highest_value_visited_child()
        best_action = best_child.get_action()
        return curr_root, best_action

    def step(self, start_node, our_player, tau):
        start_time_step = datetime.now()
        node = start_node
        while not node.is_leaf():
            node = node.select_next_node(tau)

        value, is_done = node.determine_value(self._network)
        # If the player this MCTS belongs to takes the action, add the
        # raw output, if another player takes the action, add the negative
        if our_player.get_faction() == node.get_current_player().get_faction():
            v = value
        else:
            v = -1*value

        if is_done:
            if node.is_found_leaf_node():
                v = 0
            else:
                node.set_is_found_leaf_node()
        else:
            if node.get_num_children() == 0 and not node.is_game_done():
                node.expand(self)

        start_time_backprop = datetime.now()
        while node is not None:
            node.increment_visits()
            v = node.backprop_value(v)
            node = node.get_parent()
        end_time_backprop = datetime.now()
        log_timing_info(f"backprop time: {end_time_backprop-start_time_backprop}")
        log_timing_info(f"step time: {end_time_backprop-start_time_step}")