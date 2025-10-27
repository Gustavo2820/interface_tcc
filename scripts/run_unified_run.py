#!/usr/bin/env python3
"""
Run the unified simulator programmatically and write instrumented metrics to analysis_results.
Usage: python3 scripts/run_unified_run.py <experiment> <scenario_seed> <simulation_seed>
"""
import sys
from pathlib import Path
import json

if len(sys.argv) < 4:
    print("Usage: run_unified_run.py <experiment> <scenario_seed> <simulation_seed>")
    sys.exit(2)

experiment = sys.argv[1]
scenario_seed = int(sys.argv[2])
simulation_seed = int(sys.argv[3])

root = Path(__file__).resolve().parents[1]
unified_path = root / 'simulador_heuristica' / 'unified'
if str(unified_path) not in sys.path:
    sys.path.insert(0, str(unified_path))

# import unified modules
try:
    import sim_ca_scenario as scenario_mod
    import sim_ca_simulator as sim_mod
except Exception as e:
    print('Failed to import unified simulator modules:', e)
    raise

# prepare scenario and simulator
scen = scenario_mod.Scenario(experiment, draw=False, scenario_seed=scenario_seed, simulation_seed=simulation_seed)
simulator = sim_mod.Simulator(scen)

iters, _ = simulator.simulate()

# Collect metrics
metrics = {
    'tempo_total': float(iters),
    'distancia_total': float(simulator.log.calculateDistances()),
    'individuals_distances': list(getattr(simulator.log, 'individualsDistances', [])),
    'per_iteration_non_evacuated': list(getattr(simulator.log, 'per_iteration_non_evacuated', [])),
    'termination_reason': getattr(simulator.log, 'termination_reason', None),
    'algorithm': 'unified',
    'scenario_seed': int(scenario_seed),
    'simulation_seed': int(simulation_seed)
}

out_dir = root / 'analysis_results'
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / f'unified_seed_{simulation_seed}.json'
out_file.write_text(json.dumps(metrics, indent=2))
print('Wrote', out_file)
