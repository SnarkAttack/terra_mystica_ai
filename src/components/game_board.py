import tensorflow as tf

from ..game.exceptions import InvalidActionException
from ..utilities.mappings import Factions, Terrains, Structures
from ..components.structures import Structure, Dwelling, TradingPost, Stronghold, Temple, Sanctuary

from ..utilities.loggers import game_logger
from ..utilities.functions import convert_row_col_to_location_code, convert_location_code_to_row_col

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

    # TODO: Have to add bridges
    def get_directly_adjacent_locations(self, location_code):
        directly_adjacent_locations = []
        row_val, col_val = convert_location_code_to_row_col(location_code)
        long_row = False if self._locations[row_val][-1] == Terrains.NONE else True
        row_above, row_below = row_val-1, row_val+1
        if long_row:
            left_shift = col_val-1
            right_shift = col_val
        else:
            left_shift = col_val
            right_shift = col_val+1

        if row_above >= 0:
            if left_shift >= 0:
                up_left = convert_row_col_to_location_code(row_above, left_shift)
                directly_adjacent_locations.append(up_left)
            if right_shift < len(self._locations[0]):
                up_right = convert_row_col_to_location_code(row_above, right_shift)
                directly_adjacent_locations.append(up_right)
        if col_val != 0:
            center_left = convert_row_col_to_location_code(row_val, col_val-1)
            directly_adjacent_locations.append(center_left)
        if col_val < len(self._locations[0])-1:
            center_right = convert_row_col_to_location_code(row_val, col_val+1)
            directly_adjacent_locations.append(center_right)
        if row_below < len(self._locations):
            if left_shift >= 0:
                down_left = convert_row_col_to_location_code(row_below, left_shift)
                directly_adjacent_locations.append(down_left)
            if right_shift < len(self._locations[0]):
                down_right = convert_row_col_to_location_code(row_below, right_shift)
                directly_adjacent_locations.append(down_right)

        return directly_adjacent_locations

    def get_indrectly_adjacent_locations(self, location_code):
        return []

    def get_adjacent_locations(self, faction):
        adj_locs = []
        faction_structures = self._get_all_faction_structures(faction)
        struct_locations = [struct.get_location() for struct in faction_structures]
        for location in struct_locations:
            adj_locs += self.get_directly_adjacent_locations(location)
            adj_locs += self.get_indrectly_adjacent_locations(location)
        adj_locs = list(set(adj_locs))
        return adj_locs

    def get_adjacent_modifiable_locations(self, faction):
        adj_locs = self.get_adjacent_locations(faction)
        adj_locs = [loc for loc in adj_locs if self.get_terrain(loc) != Terrains.RIVER and self.get_terrain(loc) != Terrains.NONE]
        return adj_locs

    # This calculating all possible locations based on directly and indirecly adjacent tiles
    def get_valid_terraform_locations(self, terrain_type):
        all_valid_locations = []
        for i, row in enumerate(self._locations):
            row_letter = chr(i+ord('A'))
            match_row = [i for i, terrain in enumerate(row) if terrain != terrain_type and terrain != Terrains.RIVER and terrain != Terrains.NONE]
            valid_locations = [f"{row_letter}{j+1}" for j in match_row]
            all_valid_locations += valid_locations
        return all_valid_locations

    def place_structure(self, struct_type, location_code, faction):
        row_val, col_val = convert_location_code_to_row_col(location_code)
        if row_val >= len(self._structures):
            return None
        row = self._structures[row_val]
        if col_val >= len(row):
            return None
        row[col_val] = Structure.create_structure(struct_type, location_code, faction)

    def place_dwelling(self, location_code, faction):
        self.place_structure(Structures.DWELLING, location_code, faction)

    def get_valid_building_locations(self, terrain, structure_type):
        terrain_codes = self.get_valid_location_codes_terrain_type(terrain)
        if structure_type == Structures.DWELLING:
            struct_needed = Structures.NONE
        else:
            game_logger.error(f"Structure type {structure_type} has no defined structure requirements")
        valid_building_locations = [location_code for location_code in terrain_codes if self.get_structure_at_location(location_code).get_type() == struct_needed]
        return valid_building_locations

    def get_structure_at_location(self, location_code):
        row_val, col_val = convert_location_code_to_row_col(location_code)
        if row_val >= len(self._structures):
            game_logger.error(f"Location {location_code} is not a valid code; row value too large")
            return Terrains.NONE
        row = self._structures[row_val]
        if col_val >= len(row):
            game_logger.error(f"Location {location_code} is not a valid code; column value too large")
            return Terrains.NONE
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

    def is_opponent_adjacent(self, location_code, faction):
        adj_locs = self.get_directly_adjacent_locations(location_code)
        for loc in adj_locs:
            struct = self.get_structure_at_location(loc)
            if struct.get_faction() != Factions.NONE and struct.get_faction() != faction:
                return True
        return False

    def is_opponent_adjacent_to_struct(self, location_code):
        struct = self.get_structure_at_location(location_code)
        return self.is_opponent_adjacent(location_code, struct.get_faction())

    # TODO: DO some refactoring to better combine is_opponent_adjacent and this
    def get_adjacent_opponents_power(self, location_code):
        opp_power_levels = {}
        orig_struct = self.get_structure_at_location(location_code)
        adj_locs = self.get_directly_adjacent_locations()
        for loc in adj_locs:
            struct = self.get_structure_at_location(loc)
            opp_faction = struct.get_faction()
            if opp_faction != Factions.NONE and struct.get_faction() != orig_struct.get_faction():
                prev_val = opp_power_levels.get(opp_faction, 0)
                opp_power_levels[opp_faction] = prev_val + struct.get_value()

    def get_terrain(self, location_code):
        row_val, col_val = convert_location_code_to_row_col(location_code)
        if row_val >= len(self._locations):
            game_logger.error(f"Row val: {row_val}")
        row = self._locations[row_val]
        if col_val >= len(row):
            game_logger.error(f"Col val: {col_val}")
        return row[col_val]

    def terraform_location(self, location_code, terraform_to):
        row_val, col_val = convert_location_code_to_row_col(location_code)
        if row_val >= len(self._locations):
            game_logger.error(f"Row val: {row_val}")
        row = self._locations[row_val]
        if col_val >= len(row):
            game_logger.error(f"Col val: {col_val}")
        row[col_val] = terraform_to
        return

    def _extend_row(self, row, extend_value, is_outer):
        extended_row = []
        if is_outer:
            for col in row:
                extended_row.append(col)
                extended_row.append(extend_value)
        else:
            for col in row:
                extended_row.append(extend_value)
                extended_row.append(col)
            #extended_row.append(extend_value)
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
        return self._extend_map(map, int(Terrains.NONE))

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
        for terrain in Terrains:
            if terrain == Terrains.NONE:
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
        terrain_tensors = self._generate_terrain_board_state()
        structure_tensors = self._generate_structures_board_state()
        total_game_board_tensor = tf.concat([terrain_tensors, structure_tensors], axis=0)
        return tf.reshape(total_game_board_tensor, (1, 78, 9, 26))

    def get_board_state_str(self):
        board_state = self.generate_board_state()
        flat_tensor = tf.reshape(board_state, [-1])
        bs_str = tf.strings.as_string(flat_tensor).numpy().tolist()
        return b','.join(bs_str)

class OriginalGameBoard(GameBoard):
    def __init__(self):
        self._locations = [
            [Terrains.PLAINS, Terrains.MOUNTAINS, Terrains.FOREST, Terrains.LAKES, Terrains.DESERT, Terrains.WASTELAND, Terrains.PLAINS, Terrains.SWAMP, Terrains.WASTELAND, Terrains.FOREST, Terrains.LAKES, Terrains.WASTELAND, Terrains.SWAMP],
            [Terrains.DESERT, Terrains.RIVER, Terrains.RIVER, Terrains.PLAINS, Terrains.SWAMP, Terrains.RIVER, Terrains.RIVER, Terrains.DESERT, Terrains.SWAMP, Terrains.RIVER, Terrains.RIVER, Terrains.DESERT, Terrains.NONE],
            [Terrains.RIVER, Terrains.RIVER, Terrains.SWAMP, Terrains.RIVER, Terrains.MOUNTAINS, Terrains.RIVER, Terrains.FOREST, Terrains.RIVER, Terrains.FOREST, Terrains.RIVER, Terrains.MOUNTAINS, Terrains.RIVER, Terrains.RIVER],
            [Terrains.FOREST, Terrains.LAKES, Terrains.DESERT, Terrains.RIVER, Terrains.RIVER, Terrains.WASTELAND, Terrains.LAKES, Terrains.RIVER, Terrains.WASTELAND, Terrains.RIVER, Terrains.WASTELAND, Terrains.PLAINS, Terrains.NONE],
            [Terrains.SWAMP, Terrains.PLAINS, Terrains.WASTELAND, Terrains.LAKES, Terrains.SWAMP, Terrains.PLAINS, Terrains.MOUNTAINS, Terrains.DESERT, Terrains.RIVER, Terrains.RIVER, Terrains.FOREST, Terrains.SWAMP, Terrains.LAKES],
            [Terrains.MOUNTAINS, Terrains.FOREST, Terrains.RIVER, Terrains.RIVER, Terrains.DESERT, Terrains.FOREST, Terrains.RIVER, Terrains.RIVER, Terrains.RIVER, Terrains.PLAINS, Terrains.MOUNTAINS, Terrains.PLAINS, Terrains.NONE],
            [Terrains.RIVER, Terrains.RIVER, Terrains.RIVER, Terrains.MOUNTAINS, Terrains.RIVER, Terrains.WASTELAND, Terrains.RIVER, Terrains.FOREST, Terrains.RIVER, Terrains.DESERT, Terrains.SWAMP, Terrains.LAKES, Terrains.DESERT],
            [Terrains.DESERT, Terrains.LAKES, Terrains.PLAINS, Terrains.RIVER, Terrains.RIVER, Terrains.RIVER, Terrains.LAKES, Terrains.SWAMP, Terrains.RIVER, Terrains.MOUNTAINS, Terrains.PLAINS, Terrains.MOUNTAINS, Terrains.NONE],
            [Terrains.WASTELAND, Terrains.SWAMP, Terrains.MOUNTAINS, Terrains.LAKES, Terrains.WASTELAND, Terrains.FOREST, Terrains.DESERT, Terrains.PLAINS, Terrains.MOUNTAINS, Terrains.RIVER, Terrains.LAKES, Terrains.FOREST, Terrains.WASTELAND]
        ]

        self._structures = [
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
        ]

class TinyGameBoard(GameBoard):
    def __init__(self):
        self._locations = [
            [Terrains.DESERT, Terrains.DESERT, Terrains.FOREST, Terrains.DESERT, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE],
            [Terrains.FOREST, Terrains.DESERT, Terrains.FOREST, Terrains.FOREST, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE],
            [Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE],
            [Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE],
            [Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE],
            [Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE],
            [Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE],
            [Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE],
            [Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE, Terrains.NONE],
        ]

        self._structures = [
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
            [Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure(), Structure()],
        ]