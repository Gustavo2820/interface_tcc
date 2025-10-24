#!/usr/bin/env python3
"""
Quick test to verify cached NSGA-II imports are working.
"""
import sys
from pathlib import Path

# Add unified path
project_root = Path(__file__).resolve().parent
unified_path = project_root / "simulador_heuristica" / "unified"
sys.path.insert(0, str(unified_path))

print(f"Testing imports from: {unified_path}")
print(f"Path exists: {unified_path.exists()}")

try:
    from mh_ga_instance import Instance
    print("✓ Instance imported")
except ImportError as e:
    print(f"✗ Failed to import Instance: {e}")
    Instance = None

try:
    from mh_ga_factory import Factory, selector
    print("✓ Factory and selector imported")
except ImportError as e:
    print(f"✗ Failed to import Factory/selector: {e}")
    Factory = None
    selector = None

try:
    from mh_ga_nsgaii import nsgaii as cached_nsgaii
    print("✓ cached_nsgaii imported")
except ImportError as e:
    print(f"✗ Failed to import cached_nsgaii: {e}")
    cached_nsgaii = None

if all([Instance, Factory, selector, cached_nsgaii]):
    print("\n✓ All imports successful!")
else:
    print("\n✗ Some imports failed")
    
# List files in unified folder
print(f"\nFiles in {unified_path}:")
if unified_path.exists():
    for f in sorted(unified_path.glob("*.py")):
        print(f"  - {f.name}")
