import tensorflow as tf

from ..game.exceptions import InvalidActionException
from ..mappings import Terrain, Buildings

class GameBoard(object):

    def __init__(self):
         self._locations = []
         self._components = []

    def get_valid_location_codes(self):
        all_valid_locations = []
        for i, row in enumerate(self._locations):
            row_letter = chr(i+ord('A'))
            trim_row = [terrain for terrain in row if terrain != Terrain.RIVER]
            valid_locations = [f"{row_letter}{j+1}" for j in range(len(trim_row))]
            all_valid_locations += valid_locations
        return all_valid_locations

    def _get_location_row_col(self, location_code):
        return ord(location_code[:1].upper())-ord('A'), int(location_code[1:])-1

    def get_terrain(self, code):
        row_val, col_val = self._get_location_row_col(code)
        if row_val >= len(self._locations):
            return Terrain.NONE
        row = self._locations[row_val]
        cols = [terrain for terrain in row if Terrain.RIVER]
        if col_val >= len(row):
            return Terrain.NONE
        return cols[col_val]

    def terraform_location(self, location_code, terraform_to):
        row_val, col_val = self._get_location_row_col(location_code)
        if row_val >= len(self._locations):
            raise InvalidActionException
        row = self._locations[row_val]
        cols = [terrain for terrain in row if Terrain.RIVER]
        if col_val >= len(row):
            raise InvalidActionException
        row[col_val] = terraform_to
        return

    def _extend_terrain_row(self, row, is_outer):
        extended_row = []
        if is_outer:
            for col in row[:-1]:
                extended_row.append(col)
                extended_row.append(Terrain.NONE)
            extended_row.append(row[-1])
        else:
            for col in row:
                extended_row.append(Terrain.NONE)
                extended_row.append(col)
            extended_row.append(Terrain.NONE)
        return extended_row

    def _extend_terrain_inner_row(self, row):
        return self._extend_terrain_row(row, False)

    def _extend_terrain_outer_row(self, row):
        return self._extend_terrain_row(row, True)

    def _extend_terrain_map(self, map):
        extended_map = []
        for i, row in enumerate(map):
            if i % 2 == 1:
                extended_map.append(self._extend_terrain_inner_row(row))
            else:
                extended_map.append(self._extend_terrain_outer_row(row))
        return extended_map

    def _get_only_terrain(self, terrain):
        terrain_only_locations = []
        for row in self._locations:
            terrain_only_row = [1 if row_terrain == terrain else 0 for row_terrain in row]
            terrain_only_locations.append(terrain_only_row)
        return terrain_only_locations

    def _convert_terrain_map_to_tensor(self, map):
        tensor_rows = []
        for row in map:
            tensor_row = tf.convert_to_tensor(row)
            tensor_rows.append(tensor_row)
        return tf.stack(tensor_rows, axis=0)

    def _generate_terrain_board_state(self):
        terrain_maps = []
        for terrain in Terrain:
            if terrain == Terrain.NONE:
                continue
            else:
                terrain_only_map = self._get_only_terrain(terrain)
                extended_map = self._extend_terrain_map(terrain_only_map)
                tensor_terrain_map = self._convert_terrain_map_to_tensor(extended_map)
                terrain_maps.append(tensor_terrain_map)
        return tf.stack(terrain_maps, axis=0)

    def generate_board_state(self):
        return self._generate_terrain_board_state()


class OriginalGameBoard(GameBoard):
    def __init__(self):
        self._locations = [
            [Terrain.PLAINS, Terrain.MOUNTAINS, Terrain.FOREST, Terrain.LAKES, Terrain.DESERT, Terrain.WASTELAND, Terrain.PLAINS, Terrain.SWAMP, Terrain.WASTELAND, Terrain.FOREST, Terrain.LAKES, Terrain.WASTELAND, Terrain.SWAMP],
            [Terrain.DESERT, Terrain.RIVER, Terrain.RIVER, Terrain.PLAINS, Terrain.SWAMP, Terrain.RIVER, Terrain.RIVER, Terrain.DESERT, Terrain.SWAMP, Terrain.RIVER, Terrain.RIVER, Terrain.DESERT],
            [Terrain.RIVER, Terrain.RIVER, Terrain.SWAMP, Terrain.RIVER, Terrain.MOUNTAINS, Terrain.RIVER, Terrain.FOREST, Terrain.RIVER, Terrain.FOREST, Terrain.RIVER, Terrain.MOUNTAINS, Terrain.RIVER, Terrain.RIVER],
            [Terrain.FOREST, Terrain.LAKES, Terrain.DESERT, Terrain.RIVER, Terrain.RIVER, Terrain.WASTELAND, Terrain.LAKES, Terrain.RIVER, Terrain.WASTELAND, Terrain.RIVER, Terrain.WASTELAND, Terrain.PLAINS],
            [Terrain.SWAMP, Terrain.PLAINS, Terrain.WASTELAND, Terrain.LAKES, Terrain.SWAMP, Terrain.PLAINS, Terrain.MOUNTAINS, Terrain.DESERT, Terrain.RIVER, Terrain.RIVER, Terrain.FOREST, Terrain.SWAMP, Terrain.LAKES],
            [Terrain.MOUNTAINS, Terrain.FOREST, Terrain.RIVER, Terrain.RIVER, Terrain.DESERT, Terrain.FOREST, Terrain.RIVER, Terrain.RIVER, Terrain.RIVER, Terrain.PLAINS, Terrain.MOUNTAINS, Terrain.PLAINS],
            [Terrain.RIVER, Terrain.RIVER, Terrain.RIVER, Terrain.MOUNTAINS, Terrain.RIVER, Terrain.WASTELAND, Terrain.RIVER, Terrain.FOREST, Terrain.RIVER, Terrain.DESERT, Terrain.SWAMP, Terrain.LAKES, Terrain.DESERT],
            [Terrain.DESERT, Terrain.LAKES, Terrain.PLAINS, Terrain.RIVER, Terrain.RIVER, Terrain.RIVER, Terrain.LAKES, Terrain.SWAMP, Terrain.RIVER, Terrain.MOUNTAINS, Terrain.PLAINS, Terrain.MOUNTAINS],
            [Terrain.WASTELAND, Terrain.SWAMP, Terrain.MOUNTAINS, Terrain.LAKES, Terrain.WASTELAND, Terrain.FOREST, Terrain.DESERT, Terrain.PLAINS, Terrain.MOUNTAINS, Terrain.RIVER, Terrain.LAKES, Terrain.FOREST, Terrain.WASTELAND]
        ]

        self._components = [
            [Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE],
            [Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE],
            [Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE],
            [Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE],
            [Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE],
            [Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE],
            [Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE],
            [Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE],
            [Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE, Buildings.NONE],
        ]
