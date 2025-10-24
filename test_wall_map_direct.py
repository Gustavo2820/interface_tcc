#!/usr/bin/env python3
"""
Direct test of wall_map calculation with the actual map that's failing.
"""

import sys
from pathlib import Path

# Add paths
project_root = Path(__file__).resolve().parent
unified_path = project_root / "simulador_heuristica" / "unified"
sys.path.insert(0, str(unified_path))

import logging
logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

from sim_ca_structure_map import StructureMap
from sim_ca_wall_map import WallMap

def test_wall_map_load(experiment_name):
    """Test wall_map.load_map() with actual experiment."""
    
    root_path = str(project_root) + "/"
    map_path = root_path + "simulador_heuristica/input/" + experiment_name + "/map.txt"
    
    print(f"=== TESTING WALL MAP LOAD ===")
    print(f"Experiment: {experiment_name}")
    print(f"Map path: {map_path}")
    print()
    
    # Load structure map
    structure_map = StructureMap(experiment_name, map_path)
    structure_map.load_map()
    
    print(f"✓ Structure map loaded: {structure_map.len_row}x{structure_map.len_col}")
    print()
    
    # Create wall map
    wall_map = WallMap(experiment_name, structure_map)
    
    print("Calling wall_map.load_map()...")
    try:
        wall_map.load_map()
        print("✓ SUCCESS! Wall map loaded without errors")
        print(f"Wall map dimensions: {wall_map.len_row}x{wall_map.len_col}")
        print(f"Wall map structure: {len(wall_map.map)} rows")
        if wall_map.map:
            print(f"First row length: {len(wall_map.map[0])}")
            print(f"Last row length: {len(wall_map.map[-1])}")
        return True
    except IndexError as e:
        print(f"✗ FAILED with IndexError: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"✗ FAILED with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_wall_map_load("sim_cache_adadad")
    sys.exit(0 if success else 1)
