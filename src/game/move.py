from enum import Enum

class Actions(Enum):
    pass

class Move(object):
    def __init__(self, player, action):
        self._player = player
        self._action = action

    def get_player(self):
        return self._player

    def get_action(self):
        return self._action