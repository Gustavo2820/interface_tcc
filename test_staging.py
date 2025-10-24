#!/usr/bin/env python3
"""
Test file staging for cached NSGA-II.
"""
import os
import shutil
from pathlib import Path

# Simulate what the code does
experiment_name = "sim_cache1_3obj"

# Calculate paths
root_path = os.path.dirname(os.path.dirname(os.path.abspath("simulator"))) + os.path.sep
input_dir = Path(root_path) / "input" / experiment_name
input_dir.mkdir(parents=True, exist_ok=True)

project_root = Path.cwd()
source_dir = project_root / "simulador_heuristica" / "input" / experiment_name

print(f"Source dir: {source_dir}")
print(f"  exists: {source_dir.exists()}")
if source_dir.exists():
    print(f"  map.txt: {(source_dir / 'map.txt').exists()}")
    print(f"  individuals.json: {(source_dir / 'individuals.json').exists()}")

print(f"\nTarget dir: {input_dir}")
print(f"  exists: {input_dir.exists()}")

if (source_dir / "map.txt").exists():
    shutil.copy2(source_dir / "map.txt", input_dir / "map.txt")
    print("\n✓ map.txt copied")
else:
    print("\n✗ map.txt NOT FOUND in source")

if (source_dir / "individuals.json").exists():
    shutil.copy2(source_dir / "individuals.json", input_dir / "individuals.json")
    print("✓ individuals.json copied")
else:
    print("✗ individuals.json NOT FOUND in source")

print(f"\nTarget dir after copy:")
if input_dir.exists():
    print(f"  map.txt: {(input_dir / 'map.txt').exists()}")
    print(f"  individuals.json: {(input_dir / 'individuals.json').exists()}")
