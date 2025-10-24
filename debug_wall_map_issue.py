#!/usr/bin/env python3
"""
Deep diagnostic script to identify the root cause of the IndexError in wall_map calculation.
"""

import sys
from pathlib import Path

# Add paths
project_root = Path(__file__).resolve().parent
unified_path = project_root / "simulador_heuristica" / "unified"
sys.path.insert(0, str(unified_path))

from sim_ca_structure_map import StructureMap
from sim_ca_constants import Constants

def analyze_wall_map_issue(experiment_name):
    """Analyze the wall map calculation to find out-of-bounds issues."""
    
    root_path = str(project_root) + "/"
    map_path = root_path + "simulador_heuristica/input/" + experiment_name + "/map.txt"
    
    print(f"=== ANALYZING WALL MAP ISSUE ===")
    print(f"Experiment: {experiment_name}")
    print(f"Map path: {map_path}")
    print()
    
    # Load structure map
    structure_map = StructureMap(experiment_name, map_path)
    structure_map.load_map()
    
    print(f"Map dimensions: {structure_map.len_row} rows x {structure_map.len_col} cols")
    print()
    
    # Find all walls and objects
    walls_list = []
    wall_positions = []
    
    for i in range(structure_map.len_row):
        for j in range(structure_map.len_col):
            if (structure_map.map[i][j] == Constants.M_WALL or 
                structure_map.map[i][j] == Constants.M_OBJECT):
                wall_positions.append((i, j))
    
    print(f"Found {len(wall_positions)} wall/object cells")
    print()
    
    # Simulate wall_direction logic to find problematic cells
    problematic_fields = []
    
    for i, j in wall_positions:
        # Check bounds for each direction check in wall_direction
        checks = []
        
        # TOP: structure_map.map[i - 1][j]
        if i - 1 < 0:
            checks.append(f"TOP access i-1={i-1} (NEGATIVE!)")
        elif i - 1 >= structure_map.len_row:
            checks.append(f"TOP access i-1={i-1} >= len_row={structure_map.len_row}")
        
        # TOP RIGHT: structure_map.map[i - 1][j] and structure_map.map[i][j + 1]
        if i - 1 < 0:
            checks.append(f"TOP_RIGHT access i-1={i-1} (NEGATIVE!)")
        if j + 1 >= structure_map.len_col:
            checks.append(f"TOP_RIGHT access j+1={j+1} >= len_col={structure_map.len_col}")
        
        # RIGHT: structure_map.map[i][j + 1]
        if j + 1 >= structure_map.len_col:
            checks.append(f"RIGHT access j+1={j+1} >= len_col={structure_map.len_col}")
        
        # BOTTOM RIGHT: structure_map.map[i + 1][j] and structure_map.map[i][j + 1]
        if i + 1 >= structure_map.len_row:
            checks.append(f"BOTTOM_RIGHT access i+1={i+1} >= len_row={structure_map.len_row}")
        if j + 1 >= structure_map.len_col:
            checks.append(f"BOTTOM_RIGHT access j+1={j+1} >= len_col={structure_map.len_col}")
        
        # BOTTOM: structure_map.map[i + 1][j]
        if i + 1 >= structure_map.len_row:
            checks.append(f"BOTTOM access i+1={i+1} >= len_row={structure_map.len_row}")
        
        # BOTTOM LEFT: structure_map.map[i + 1][j] and structure_map.map[i][j - 1]
        if i + 1 >= structure_map.len_row:
            checks.append(f"BOTTOM_LEFT access i+1={i+1} >= len_row={structure_map.len_row}")
        if j - 1 < 0:
            checks.append(f"BOTTOM_LEFT access j-1={j-1} (NEGATIVE!)")
        
        # LEFT: structure_map.map[i][j - 1]
        if j - 1 < 0:
            checks.append(f"LEFT access j-1={j-1} (NEGATIVE!)")
        
        # TOP LEFT: structure_map.map[i - 1][j] and structure_map.map[i][j - 1]
        if i - 1 < 0:
            checks.append(f"TOP_LEFT access i-1={i-1} (NEGATIVE!)")
        if j - 1 < 0:
            checks.append(f"TOP_LEFT access j-1={j-1} (NEGATIVE!)")
        
        if checks:
            problematic_fields.append({
                'position': (i, j),
                'issues': checks
            })
    
    print(f"=== PROBLEMATIC WALL POSITIONS ===")
    if problematic_fields:
        for prob in problematic_fields[:10]:  # Show first 10
            print(f"Position ({prob['position'][0]}, {prob['position'][1]}):")
            for issue in prob['issues']:
                print(f"  - {issue}")
        if len(problematic_fields) > 10:
            print(f"... and {len(problematic_fields) - 10} more")
    else:
        print("No problematic positions found in wall_direction checks!")
    
    print()
    
    # Now check what fields would be generated
    print(f"=== SIMULATING FIELD GENERATION ===")
    simulated_fields = []
    
    for i, j in wall_positions:
        # Simulate wall_direction safely
        try:
            # TOP
            if i > 0 and (structure_map.map[i - 1][j] == Constants.M_EMPTY or 
                          structure_map.map[i - 1][j] == Constants.M_DOOR):
                field = [i, j, 0, Constants.D_TOP]
                simulated_fields.append(field)
            
            # TOP RIGHT
            if (i > 0 and j < structure_map.len_col - 1 and
                (structure_map.map[i - 1][j] == Constants.M_EMPTY or 
                 structure_map.map[i - 1][j] == Constants.M_DOOR) and 
                (structure_map.map[i][j + 1] == Constants.M_EMPTY or 
                 structure_map.map[i][j + 1] == Constants.M_DOOR)):
                field = [i, j, 0, Constants.D_TOP_RIGHT]
                simulated_fields.append(field)
            
            # RIGHT
            if j < structure_map.len_col - 1 and (structure_map.map[i][j + 1] == Constants.M_EMPTY or 
                                                    structure_map.map[i][j + 1] == Constants.M_DOOR):
                field = [i, j, 0, Constants.D_RIGHT]
                simulated_fields.append(field)
            
            # BOTTOM RIGHT
            if (i < structure_map.len_row - 1 and j < structure_map.len_col - 1 and
                (structure_map.map[i + 1][j] == Constants.M_EMPTY or 
                 structure_map.map[i + 1][j] == Constants.M_DOOR) and 
                (structure_map.map[i][j + 1] == Constants.M_EMPTY or 
                 structure_map.map[i][j + 1] == Constants.M_DOOR)):
                field = [i, j, 0, Constants.D_BOTTOM_RIGHT]
                simulated_fields.append(field)
            
            # BOTTOM
            if i < structure_map.len_row - 1 and (structure_map.map[i + 1][j] == Constants.M_EMPTY or 
                                                    structure_map.map[i + 1][j] == Constants.M_DOOR):
                field = [i, j, 0, Constants.D_BOTTOM]
                simulated_fields.append(field)
            
            # BOTTOM LEFT
            if (i < structure_map.len_row - 1 and j > 0 and
                (structure_map.map[i + 1][j] == Constants.M_EMPTY or 
                 structure_map.map[i + 1][j] == Constants.M_DOOR) and 
                (structure_map.map[i][j - 1] == Constants.M_EMPTY or 
                 structure_map.map[i][j - 1] == Constants.M_DOOR)):
                field = [i, j, 0, Constants.D_BOTTOM_LEFT]
                simulated_fields.append(field)
            
            # LEFT
            if j > 0 and (structure_map.map[i][j - 1] == Constants.M_EMPTY or 
                          structure_map.map[i][j - 1] == Constants.M_DOOR):
                field = [i, j, 0, Constants.D_LEFT]
                simulated_fields.append(field)
            
            # TOP LEFT
            if (i > 0 and j > 0 and
                (structure_map.map[i - 1][j] == Constants.M_EMPTY or 
                 structure_map.map[i - 1][j] == Constants.M_DOOR) and 
                (structure_map.map[i][j - 1] == Constants.M_EMPTY or 
                 structure_map.map[i][j - 1] == Constants.M_DOOR)):
                field = [i, j, 0, Constants.D_TOP_LEFT]
                simulated_fields.append(field)
        
        except IndexError as e:
            print(f"ERROR at wall position ({i}, {j}): {e}")
    
    print(f"Generated {len(simulated_fields)} initial fields")
    print()
    
    # Check if any initial fields are out of bounds
    oob_initial = []
    for idx, field in enumerate(simulated_fields):
        if not (0 <= field[0] < structure_map.len_row and 0 <= field[1] < structure_map.len_col):
            oob_initial.append((idx, field))
    
    if oob_initial:
        print(f"WARNING: {len(oob_initial)} initial fields are OUT OF BOUNDS!")
        for idx, field in oob_initial[:5]:
            print(f"  Field {idx}: pos=({field[0]}, {field[1]}), bounds=[0-{structure_map.len_row}, 0-{structure_map.len_col}]")
    else:
        print("✓ All initial fields are within bounds")
    
    print()
    
    # Simulate field expansion to find where it goes wrong
    print(f"=== SIMULATING FIELD EXPANSION ===")
    
    # Check first 10 fields and their expansions
    for idx in range(min(10, len(simulated_fields))):
        field = simulated_fields[idx]
        new_field = (field[0] + field[3][0], field[1] + field[3][1], 
                     field[2] + field[3][2], field[3])
        
        in_bounds = (0 <= new_field[0] < structure_map.len_row and 
                     0 <= new_field[1] < structure_map.len_col)
        
        status = "✓" if in_bounds else "✗ OUT OF BOUNDS"
        print(f"Field {idx}: ({field[0]}, {field[1]}) + {field[3]} -> ({new_field[0]}, {new_field[1]}) {status}")
    
    # Find the problematic field
    print()
    print(f"=== CHECKING FIELD 105 (THE CRASH POINT) ===")
    if len(simulated_fields) > 105:
        field_105 = simulated_fields[105]
        print(f"Field 105: pos=({field_105[0]}, {field_105[1]}), direction={field_105[3]}")
        new_field_105 = (field_105[0] + field_105[3][0], field_105[1] + field_105[3][1], 
                         field_105[2] + field_105[3][2], field_105[3])
        print(f"Expansion: ({field_105[0]}, {field_105[1]}) + {field_105[3]} -> ({new_field_105[0]}, {new_field_105[1]})")
        print(f"Map bounds: [0-{structure_map.len_row}, 0-{structure_map.len_col}]")
        
        if not (0 <= new_field_105[0] < structure_map.len_row and 0 <= new_field_105[1] < structure_map.len_col):
            print(f"✗ EXPANSION IS OUT OF BOUNDS!")
        else:
            print(f"✓ Expansion is within bounds")
    else:
        print(f"Only {len(simulated_fields)} fields generated, cannot check field 105")

if __name__ == "__main__":
    analyze_wall_map_issue("sim_cache_adadad")
