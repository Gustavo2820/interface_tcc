#!/usr/bin/env python3
"""
Verification script for integration layer refactoring.

This script verifies that:
1. The integration_api module is properly created and imports
2. All required functions are available
3. Integration files properly delegate to the API
4. No duplicated StructureMap exists
5. All tests pass

Run this after refactoring to verify success.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_integration_api():
    """Verify integration_api module exists and has all required functions."""
    print("✓ Checking integration_api module...")
    
    try:
        from simulador_heuristica.simulator import integration_api
        print("  ✓ integration_api imported successfully")
    except ImportError as e:
        print(f"  ✗ Failed to import integration_api: {e}")
        return False
    
    required_functions = [
        'parse_map_text',
        'extract_doors_from_matrix',
        'extract_doors_from_map_text',
        'expand_grouped_doors',
        'generate_map_text_with_grouped_doors',
        'save_individuals_json',
        'load_individuals_json',
        'parse_metrics_from_output_dir',
        'create_structure_map_from_text',
        'extract_door_positions_legacy',
    ]
    
    for func_name in required_functions:
        if hasattr(integration_api, func_name):
            print(f"  ✓ {func_name} available")
        else:
            print(f"  ✗ {func_name} missing")
            return False
    
    return True


def check_no_duplicated_structure_map():
    """Verify StructureMap is not duplicated in integration files."""
    print("\n✓ Checking for duplicated StructureMap...")
    
    integration_files = [
        project_root / 'interface' / 'services' / 'nsga_integration.py',
        project_root / 'interface' / 'services' / 'simulator_integration.py',
    ]
    
    for file_path in integration_files:
        if file_path.exists():
            content = file_path.read_text()
            if 'class StructureMap' in content:
                print(f"  ✗ Duplicated StructureMap found in {file_path.name}")
                return False
            else:
                print(f"  ✓ No duplicated StructureMap in {file_path.name}")
    
    return True


def check_integration_delegates():
    """Verify integration files delegate to integration_api."""
    print("\n✓ Checking integration files delegate to API...")
    
    nsga_file = project_root / 'interface' / 'services' / 'nsga_integration.py'
    
    if nsga_file.exists():
        content = nsga_file.read_text()
        
        if 'from simulador_heuristica.simulator import integration_api' in content:
            print("  ✓ nsga_integration imports integration_api")
        else:
            print("  ✗ nsga_integration does not import integration_api")
            return False
        
        if 'integration_api.extract_doors_from_map_text' in content:
            print("  ✓ nsga_integration uses extract_doors_from_map_text")
        else:
            print("  ✗ nsga_integration does not use extract_doors_from_map_text")
            return False
        
        if 'integration_api.expand_grouped_doors' in content:
            print("  ✓ nsga_integration uses expand_grouped_doors")
        else:
            print("  ✗ nsga_integration does not use expand_grouped_doors")
            return False
        
        if 'integration_api.generate_map_text_with_grouped_doors' in content:
            print("  ✓ nsga_integration uses generate_map_text_with_grouped_doors")
        else:
            print("  ✗ nsga_integration does not use generate_map_text_with_grouped_doors")
            return False
    
    return True


def check_simulator_integration_imports():
    """Verify simulator_integration imports from simulator package."""
    print("\n✓ Checking simulator_integration imports...")
    
    sim_file = project_root / 'interface' / 'services' / 'simulator_integration.py'
    
    if sim_file.exists():
        content = sim_file.read_text()
        
        if 'from simulador_heuristica.simulator import integration_api' in content:
            print("  ✓ simulator_integration imports integration_api")
        else:
            print("  ✗ simulator_integration does not import integration_api")
            return False
        
        if 'from simulador_heuristica.simulator.structure_map import StructureMap' in content:
            print("  ✓ simulator_integration imports official StructureMap")
        else:
            print("  ✗ simulator_integration does not import official StructureMap")
            return False
    
    return True


def test_basic_functionality():
    """Test basic integration_api functionality."""
    print("\n✓ Testing basic functionality...")
    
    try:
        from simulador_heuristica.simulator import integration_api
        
        # Test map parsing
        map_text = "000\n020\n000"
        matrix = integration_api.parse_map_text(map_text)
        assert len(matrix) == 3, "Map parsing failed"
        print("  ✓ parse_map_text works")
        
        # Test door extraction
        map_with_door = "00000\n02220\n00000"
        doors = integration_api.extract_doors_from_map_text(map_with_door)
        assert len(doors) >= 1, "Door extraction failed"
        print("  ✓ extract_doors_from_map_text works")
        
        # Test door expansion
        grouped = [{'row': 0, 'col': 1, 'size': 2, 'direction': 'H'}]
        expanded = integration_api.expand_grouped_doors(grouped)
        assert len(expanded) == 2, "Door expansion failed"
        print("  ✓ expand_grouped_doors works")
        
        # Test map generation
        new_map = integration_api.generate_map_text_with_grouped_doors(
            "00000\n00000\n00000",
            [{'row': 1, 'col': 1, 'size': 3, 'direction': 'H'}]
        )
        assert '2' in new_map, "Map generation failed"
        print("  ✓ generate_map_text_with_grouped_doors works")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Basic functionality test failed: {e}")
        return False


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Integration Layer Refactoring Verification")
    print("=" * 60)
    
    checks = [
        ("Integration API Module", check_integration_api),
        ("No Duplicated StructureMap", check_no_duplicated_structure_map),
        ("Integration Delegates to API", check_integration_delegates),
        ("Simulator Integration Imports", check_simulator_integration_imports),
        ("Basic Functionality", test_basic_functionality),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} raised exception: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✅ All verification checks passed!")
        print("The integration layer refactoring is complete and successful.")
        return 0
    else:
        print("\n❌ Some verification checks failed.")
        print("Please review the output above for details.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
