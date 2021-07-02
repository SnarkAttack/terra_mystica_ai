import numpy as np
from copy import deepcopy, copy
import hashlib

from numpy.core.numeric import indices
from ..game.move import Move
from ..junk import all_locations
from ..utilities.loggers import log_timing_info
from datetime import datetime

C = 5

def id_hash(game):
    return GameState(game).get_id()

class GameState(object):

    def __init__(self, game):

        self._game_board_state = game.get_game_board().generate_board_state()
        self._player_states = [player.generate_player_state() for player in game.get_players()]
        self._cult_board_state = game.get_cult_board()

        gb_string = game.get_game_board().get_board_state_str()
        res = hashlib.md5(gb_string)

        self._id = res.digest()

    def get_id(self):
        return self._id

    def get_game_board_state(self):
        return self._game_board_state

class MCTSNode(object):

    def __init__(self, game, player=None, parent=None, probability=0, action=None):
        self._parent = parent
        self._children = []
        self._child_probs = []
        self._visits = 0
        self._value = 0
        self._probability = probability
        self._action = action

        self._game = game
        self._player = player
        self._id = id_hash(game)

        # Don't want to propogate value of game_ending node we have already found,
        # so this is flipped if node contains a finished game and we have processed it
        self._is_found_leaf_node = False

    def _ucb(self):
        # Visits + 1e-5 is to make sure we aren't dividing by 0, while not actually effecting the
        # final result significantly
        return self._value + C * np.sqrt(np.log(self._parent.get_visits())/(self._visits+1e-5))

    # tau = 0 is pure exploration, tau = 1 is pure exploitation
    def _uci(self, tau):
        # print(self._parent.get_visits())
        # print(self._visits)
        # print(self._parent.get_visits()/(self._visits+1e-5))
        # print(self._probability)
        # print(tau)
        # print()
        return tau*self._value + (1-tau)*(C * self._probability*(np.sqrt(self._parent.get_visits())/(self._visits+1e-5)))

    def get_id(self):
        return self._id

    def get_player(self):
        return self._player

    def replace_child(self, node):
        for i, child in enumerate(self._children):
            if child.get_id() == node.get_id():
                self._children[i] = node

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
        #return max(self._children, key=lambda x: x._ucb())
        # print([x._uci(tau) for x in self._children])
        # print(max(self._children, key=lambda x: x._uci(tau)).get_action().get_location())
        best_node = max(self._children, key=lambda x: x._uci(tau))
        end_time = datetime.now()
        log_timing_info(f"select_next_node time: {end_time-start_time}")
        return best_node

    def backprop_value(self, v):
        self._value += v
        return self._value

    def get_game_state(self):
        return GameState(self._game)

    # TODO: Burn this to the ground
    def _cheaty_thing(self, valid_next_actions, probs):
        locations = [action.get_location() for action in valid_next_actions]
        indices = [all_locations.index(location) for location in locations]
        needed_probs = [probs[i] for i in indices]
        s = sum(needed_probs)
        softmax_probs = [prob/s for prob in needed_probs]
        return softmax_probs

    def generate_all_valid_next_states(self, player, valid_next_actions, probs, tree):
        start_time = datetime.now()
        softmax_probs = self._cheaty_thing(valid_next_actions, probs)
        for action, prob in zip(valid_next_actions, softmax_probs):
            game_copy = deepcopy(self._game)
            move = Move(player, action)
            game_copy.perform_move(move)
            if tree.get_ids().get(GameState(game_copy).get_id()) is None:
                child_node = MCTSNode(game=game_copy, player=player, parent=self, probability=prob, action=action)
                #print("Making new node")
            else:
                child_node = tree.get_ids()[id_hash(game_copy)]
                #print("Node already exists")
            self._children.append(child_node)
            self._child_probs.append(prob)
            tree.add_node_to_tree(child_node)
        end_time = datetime.now()
        log_timing_info(f"generate_all_valid_next_states time: {end_time-start_time}")

    def is_game_done(self):
        return self._game.is_done()

    def get_highest_value_child(self):
        return max(self._children, key=lambda x: x._value)

    def expand(self, tree):
        player, valid_next_actions = self.get_game().get_all_valid_next_actions()
        probs = tree._network.predict_actions(self.get_game_state())
        self.generate_all_valid_next_states(player, valid_next_actions, probs, tree)

    def get_child_node_prob(self, child_node):
        for child, prob in zip(self._children, self._child_probs):
            if child.get_id() == child_node.get_id():
                return prob
        print("Did not find child")
        return 0

    def determine_value(self, network):
        is_done = self.is_game_done()
        if is_done:
            self._game.score_game()
            high_score = self._game.get_high_score()
            player_score = self._game.get_player_by_faction(self._player.get_faction()).get_vps()
            if player_score == high_score:
                value = high_score
                #value = 1
            else:
                value = player_score - high_score
                #value = -1
        else:
            value = network.predict_value(self.get_game_state())
        return value, is_done



class MCTS(object):

    def __init__(self, network, num_steps=100):
        self._network = network
        self._num_steps = num_steps
        self._ids = {
        }

    def _linear_tau_step(self, current_step):
        return current_step/(self._num_steps*2)

    def _flip_tau_step(self, current_step):
        if current_step < self._num_steps/2:
            return 0
        else:
            return 1

    def _mid_tau_step(self, current_step):
        return 0.5

    def add_node_to_tree(self, node):
        self._ids[node.get_id()] = node

    def add_ids(self, nodes):
        for node in nodes:
            self.add_node_to_tree(node)

    def get_ids(self):
        return self._ids

    def determine_next_action(self, game, our_player):
        if self._ids.get(id_hash(game)) is None:
            curr_root = MCTSNode(
                game=game,
                player=our_player)
            self.add_node_to_tree(curr_root)
            #print("Making new root for this action")
        else:
            curr_root = self._ids[id_hash(game)]

        if curr_root.get_num_children() == 0:
            #print("Expanding current root")
            curr_root.expand(self)

        for i in range(self._num_steps):
            tau = self._mid_tau_step(i)
            self.step(curr_root, our_player, tau)

        best_child = curr_root.get_highest_value_child()
        best_action = best_child.get_action()
        #print(f"Children values: {[child.get_value() for child in curr_root._children]}")
        #print(f"Best action location: {best_action.get_location()}")
        #print(f"Best action value: {best_child.get_value()}")
        return best_action

    def get_state_tree(self, game):
        node = self._ids.get(id_hash(game))
        #print([child.get_visits() for child in node.get_children()])
        for i, child in enumerate(self._root._children):
            print(f"{i}: {[gchild.get_visits() for gchild in child.get_children()]}")

    def step(self, start_node, our_player, tau):
        start_time_step = datetime.now()
        node = start_node
        while not node.is_leaf():
            node = node.select_next_node(tau)

        value, is_done = node.determine_value(self._network)
        # If the player this MCTS belongs to takes the action, add the
        # raw output, if another player takes the action, add the negative
        if our_player.get_faction() == node.get_player().get_faction():
            v = value
        else:
            v = -1*value

        # If game is done save off memory, else check if node needs expanding
        if is_done:
            if node.is_found_leaf_node():
                v = 0
            else:
                node.set_is_found_leaf_node()
        else:
            if node.get_num_children() == 0:
                node.expand(self)

        start_time_backprop = datetime.now()
        while node is not None:
            node.increment_visits()
            v = node.backprop_value(v)
            node = node.get_parent()
        end_time_backprop = datetime.now()
        log_timing_info(f"backprop time: {end_time_backprop-start_time_backprop}")
        log_timing_info(f"step time: {end_time_backprop-start_time_step}")

    def reverse_build_tree(self, node):
        """
        Using a node taken from another MCTS, confirm that the node is currently in
        our tree. If not, add to tree and build backwards until we meet a portion of
        the tree we already have. This is necessary because unlike chess/go/shogi, a single
        player can concievably take multiple turns in a row, so we are not guaranteed to have
        a connection from the last move in one tree to the root of the other.
        """
        prev_node = None
        while self._ids.get(node.get_id()) is None:
            new_node = MCTSNode(
                game=node.get_game(),
                player=node.get_player(),
                parent=None,
                probability=None,
                action=node.get_action(),
            )
            new_node.set_value(new_node.determine_value(self._network))
            # Want to rebuild our own list of children using this network's weights
            new_node.expand()
            if prev_node is not None:
                prob = new_node.get_child_node_prob(prev_node)
                new_node.replace_child(prev_node)
                prev_node._parent = new_node
                prev_node._probability = prob
            prev_node = new_node
            node = node.parent

        value = node.get_value()
        visits = node.get_visits()

        if prev_node is not None:
            old_node = self._ids.get(node.get_id())
            prob = old_node.get_child_node_prob(prev_node)
            old_node.replace_child(prev_node)
            prev_node._parent = old_node
            prev_node._probabilty = prob

        self._curr_root = self._ids.get(node.get_id())


