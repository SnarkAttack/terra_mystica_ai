import pickle
import os
import sys


class Memory(object):

    def __init__(self, lt_memory_path, max_moves):
        self._short_term_memory = []
        self._long_term_memory_path = lt_memory_path
        self._file_count = 1
        self._file_name = 'mem'
        self._max_moves = max_moves

        memory_path = os.path.join(sys.path[0], self._long_term_memory_path)

        if not os.path.isdir(memory_path):
            os.mkdir(memory_path)

    def add_to_st_memory(self, game_state):
        self._short_term_memory.append(game_state)

    def add_to_lt_memory(self):
        file_name = os.path.join(self._long_term_memory_path, f'{self._file_name}_{self._file_count}')
        with open(file_name, 'wb') as f:
            pickle.dump(self._short_term_memory, f)
        self._file_count += 1
        self._short_term_memory = []

    def check_st_memory_stored(self):
        return len(self._short_term_memory) >= self._max_moves
