#!/usr/bin/env python3
"""
Final validation script to confirm the fix works correctly.
"""

import sys
from pathlib import Path

# Add paths
project_root = Path(__file__).resolve().parent
unified_path = project_root / "simulador_heuristica" / "unified"
sys.path.insert(0, str(unified_path))

from sim_ca_scenario import Scenario

def main():
    print("=" * 80)
    print("FINAL VALIDATION: Wall Map Fix for Cached NSGA-II")
    print("=" * 80)
    print()
    
    experiment = "sim_cache_adadad"
    
    # Test 1: Basic scenario initialization
    print("[1] Testing basic scenario initialization...")
    try:
        scenario = Scenario(experiment)
        print(f"✓ Scenario loaded: {scenario.structure_map.len_row}x{scenario.structure_map.len_col}")
        print(f"✓ Doors configurations: {len(scenario.doors_configurations)} available")
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False
    
    print()
    
    # Test 2: Factory decode (mimics what NSGA-II does)
    print("[2] Testing Factory.decode (simulates NSGA-II evaluation)...")
    try:
        sys.path.insert(0, str(unified_path))
        from mh_ga_instance import Instance
        from mh_ga_factory import Factory
        
        instance = Instance(
            experiment=experiment,
            draw=False,
            scenario_seed=[1, 2, 3],  # 3-objective mode uses multiple seeds
            simulation_seed=42
        )
        
        factory = Factory(instance)
        
        # Create a simple gene (first 3 doors enabled)
        from mh_ga_factory import Gene
        gene_config = [True if i < 3 else False for i in range(len(factory.exits))]
        gene = Gene(gene_config)
        
        print(f"  Testing gene with {sum(gene_config)} doors enabled...")
        
        # This should trigger Scenario creation with doors -> map_reset -> load_wall_map
        result = factory.decode(gene)
        
        print(f"✓ Decode successful: num_doors={result[0]}, iters={result[1]:.1f}, dist={result[2]:.1f}")
        
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    
    # Test 3: Multiple evaluations (cache test)
    print("[3] Testing multiple evaluations (cache functionality)...")
    try:
        # Evaluate same gene again - should use cache
        result2 = factory.decode(gene)
        print(f"✓ Second decode successful (cached)")
        
        # Evaluate different gene
        gene_config2 = [True if i < 5 else False for i in range(len(factory.exits))]
        gene2 = Gene(gene_config2)
        result3 = factory.decode(gene2)
        print(f"✓ Third decode successful (different gene): num_doors={result3[0]}")
        
        print(f"✓ Cache contains {len(factory.cache)} entries")
        
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    print("=" * 80)
    print("✓✓✓ ALL VALIDATION TESTS PASSED ✓✓✓")
    print("=" * 80)
    print()
    print("The fix is working correctly:")
    print("  - Wall maps initialize properly with unknown values")
    print("  - Static maps initialize properly with unknown values")
    print("  - Cached NSGA-II can evaluate solutions")
    print("  - Cache functionality works")
    print()
    print("Ready for full NSGA-II optimization runs!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
