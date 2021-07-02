import tensorflow as tf

from ..game.exceptions import InvalidActionException
from ..mappings import Factions, Terrain, Structures
from ..components.structures import Structure, Dwelling, TradingPost, Stronghold, Temple, Sanctuary

class GameBoard(object):

    def __init__(self):
         self._locations = []
         self._structures = []

    def get_valid_location_codes(self):
        all_valid_locations = []
        for i, row in enumerate(self._locations):
            row_letter = chr(i+ord('A'))
            valid_locations = [f"{row_letter}{j+1}" for j in range(len(row))]
            all_valid_locations += valid_locations
        return all_valid_locations

    def get_valid_location_codes_terrain_type(self, terrain_type):
        all_valid_locations = []
        for i, row in enumerate(self._locations):
            row_letter = chr(i+ord('A'))
            match_row = [i for i, terrain in enumerate(row) if terrain == terrain_type]
            valid_locations = [f"{row_letter}{j+1}" for j in match_row]
            all_valid_locations += valid_locations
        return all_valid_locations

    def _get_location_row_col(self, location_code):
        return ord(location_code[:1].upper())-ord('A'), int(location_code[1:])-1

    def place_dwelling(self, location_code, faction):
        row_val, col_val = self._get_location_row_col(location_code)
        if row_val >= len(self._structures):
            return None
        row = self._structures[row_val]
        if col_val >= len(row):
            return None
        row[col_val] = Dwelling(location_code, faction)

    def get_structure(self, location_code):
        row_val, col_val = self._get_location_row_col(location_code)
        if row_val >= len(self._structures):
            return Terrain.NONE
        row = self._structures[row_val]
        if col_val >= len(row):
            return Terrain.NONE
        return row[col_val]

    def _get_all_faction_structures(self, faction):
        all_structures = []
        for row in self._structures:
            for struct in row:
                if struct.get_faction() == faction:
                    all_structures.append(struct)
        return all_structures

    def get_all_player_structures(self, player):
        return self._get_all_faction_structures(player.get_faction())

    def get_terrain(self, location_code):
        row_val, col_val = self._get_location_row_col(location_code)
        if row_val >= len(self._locations):
            return Terrain.NONE
        row = self._locations[row_val]
        if col_val >= len(row):
            return Terrain.NONE
        return row[col_val]

    def terraform_location(self, location_code, terraform_to):
        row_val, col_val = self._get_location_row_col(location_code)
        if row_val >= len(self._locations):
            raise InvalidActionException
        row = self._locations[row_val]
        cols = [terrain for terrain in row if terrain != Terrain.RIVER]
        if col_val >= len(cols):
            raise InvalidActionException
        row[col_val] = terraform_to
        return

    def _extend_row(self, row, extend_value, is_outer):
        extended_row = []
        if is_outer:
            for col in row[:-1]:
                extended_row.append(col)
                extended_row.append(extend_value)
            extended_row.append(row[-1])
        else:
            for col in row:
                extended_row.append(extend_value)
                extended_row.append(col)
            extended_row.append(extend_value)
        return extended_row

    def _extend_short_row(self, row, extend_value):
        return self._extend_row(row, extend_value, False)

    def _extend_long_row(self, row, extend_value):
        return self._extend_row(row, extend_value, True)

    def _extend_map(self, map, extend_value):
        extended_map = []
        for i, row in enumerate(map):
            if i % 2 == 1:
                extended_map.append(self._extend_short_row(row, extend_value))
            else:
                extended_map.append(self._extend_long_row(row, extend_value))
        return extended_map

    def _extend_terrain_map(self, map):
        return self._extend_map(map, int(Terrain.NONE))
    
    def _extend_structure_map(self, map):
        return self._extend_map(map, int(Structures.NONE))

    def _convert_map_to_tensor(self, map, axis=0):
        tensor_rows = []
        for row in map:
            tensor_row = tf.convert_to_tensor(row)
            tensor_rows.append(tensor_row)
        return tf.stack(tensor_rows, axis=axis)

    def _get_only_terrain(self, terrain):
        terrain_only_locations = []
        for row in self._locations:
            terrain_only_row = [1 if row_terrain == terrain else 0 for row_terrain in row]
            terrain_only_locations.append(terrain_only_row)
        return terrain_only_locations

    def _get_only_faction_struct_type(self, faction, struct_type):
        faction_struct_type_only_locations = []
        for row in self._structures:
            faction_struct_only_row = [1 if struct.get_faction() == faction and struct.get_type() == struct_type else 0 for struct in row]
            faction_struct_type_only_locations.append(faction_struct_only_row)
        return faction_struct_type_only_locations

    def _convert_faction_struct_type_map_to_tensor(self, faction, struct_type):
        faction_struct_type_map = self._get_only_faction_struct_type(faction, struct_type)
        extended_map = self._extend_structure_map(faction_struct_type_map)
        return self._convert_map_to_tensor(extended_map, axis=0)

    def _generate_terrain_board_state(self):
        terrain_maps = []
        for terrain in Terrain:
            if terrain == Terrain.NONE:
                continue
            else:
                terrain_only_map = self._get_only_terrain(terrain)
                extended_map = self._extend_terrain_map(terrain_only_map)
                tensor_terrain_map = self._convert_map_to_tensor(extended_map, axis=0)
                terrain_maps.append(tensor_terrain_map)
        return tf.stack(terrain_maps, axis=0)

    def _generate_structures_board_state(self):
        structure_map_layers = []
        for faction in Factions:
            if faction == Factions.NONE:
                continue
            else:
                for structure_type in Structures:
                    if structure_type is Structures.NONE:
                        continue
                    else:
                        # TODO: Iterating structure map (faction_count x structure_count) times, try and make it
                        # just one iteration
                        structure_map_layer = self._convert_faction_struct_type_map_to_tensor(faction, structure_type)
                        structure_map_layers.append(structure_map_layer)
        return tf.stack(structure_map_layers, axis=0)

    def generate_board_state(self):
        #print(self._generate_terrain_board_state())
        terrain_tensors = self._generate_terrain_board_state()
        structure_tensors = self._generate_structures_board_state()
        flat_tensor = tf.reshape(structure_tensors, [-1])
        total_game_board_tensor = tf.concat([terrain_tensors, structure_tensors], axis=0)
        return tf.reshape(total_game_board_tensor, (1, 78, 9, 25))

    def get_board_state_str(self):
        board_state = self.generate_board_state()
        flat_tensor = tf.reshape(board_state, [-1])
        bs_str = tf.strings.as_string(flat_tensor).numpy().tolist()
        return b','.join(bs_str)




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

        self._structures = [
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
        ]
