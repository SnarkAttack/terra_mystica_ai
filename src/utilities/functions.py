from ..utilities.mappings import Terrains

def get_shovel_cost(terrain_from, terrain_to):
    terrain_diff = abs(int(terrain_from)-int(terrain_to))
    return terrain_diff if terrain_diff <=3 else abs(terrain_diff-7)

def convert_row_col_to_location_code(row, col):
    row_letter = chr(row+ord('A'))
    col_number = col+1
    return f"{row_letter}{col_number}"

def convert_location_code_to_row_col(location_code):
    return ord(location_code[:1].upper())-ord('A'), int(location_code[1:])-1

def sort_location_codes(location_code):
    row_val, col_val = convert_location_code_to_row_col(location_code)
    return (row_val, col_val)