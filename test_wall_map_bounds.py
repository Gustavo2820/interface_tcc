#!/usr/bin/env python3
"""
Test script to validate wall_map bounds checking fix.
"""

import sys
import os
from pathlib import Path

# Add simulador_heuristica/unified to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "simulador_heuristica" / "unified"))
os.chdir(project_root / "simulador_heuristica")

from sim_ca_scenario import Scenario

def test_wall_map_bounds():
    """Test that wall map doesn't crash with IndexError on boundary conditions."""
    print("=" * 60)
    print("Testing Wall Map Bounds Fix")
    print("=" * 60)
    
    # Check if experiment directory exists
    experiment = "sim_cache_adadad"
    input_path = Path("simulador_heuristica/input") / experiment / "map.txt"
    
    if not input_path.exists():
        print(f"\n⚠️  Experiment directory not found: {input_path}")
        print("   Looking for any available experiment...")
        
        input_dir = Path("simulador_heuristica/input")
        available = [d.name for d in input_dir.iterdir() if d.is_dir() and (d / "map.txt").exists()]
        
        if not available:
            print("   ❌ No valid experiments found in simulador_heuristica/input/")
            return False
        
        experiment = available[0]
        print(f"   ✓ Using experiment: {experiment}")
    
    try:
        print(f"\n1. Loading scenario: {experiment}")
        scenario = Scenario(experiment)
        
        print(f"   ✓ Structure map loaded: {scenario.structure_map.len_row}x{scenario.structure_map.len_col}")
        print(f"   ✓ Doors found: {len(scenario.doors_configurations)}")
        
        print("\n2. Testing map_reset with existing doors configuration")
        doors = scenario.doors_configurations
        
        print(f"   Doors to test: {len(doors)} doors")
        for i, door in enumerate(doors):
            print(f"     Door {i}: row={door['row']}, col={door['col']}, "
                  f"size={door['size']}, direction={door['direction']}")
        
        print("\n3. Executing map_reset (this previously caused IndexError)...")
        scenario.map_reset(doors)
        
        print("   ✓ map_reset completed successfully!")
        print(f"   ✓ Wall map dimensions: {scenario.wall_map.len_row}x{scenario.wall_map.len_col}")
        
        # Verify map integrity
        print("\n4. Verifying wall map integrity...")
        non_empty_count = 0
        for i in range(scenario.wall_map.len_row):
            for j in range(scenario.wall_map.len_col):
                if scenario.wall_map.map[i][j] != 0:
                    non_empty_count += 1
        
        print(f"   ✓ Non-empty cells in wall map: {non_empty_count}")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED - Wall map bounds fix is working!")
        print("=" * 60)
        return True
        
    except IndexError as e:
        print(f"\n❌ IndexError still occurs: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_wall_map_bounds()
    sys.exit(0 if success else 1)
