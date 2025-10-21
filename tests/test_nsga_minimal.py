import os
import json
import numpy as np
import tempfile
import pytest
import sys
import types

# Insert a lightweight fake constants module to avoid importing the heavy simulator package during test collection
fake_mod = types.ModuleType('simulador_heuristica.simulator.constants')
class _C:
    M_EMPTY = 0
    M_WALL = 1
    M_DOOR = 2
fake_mod.Constants = _C
sys.modules['simulador_heuristica.simulator.constants'] = fake_mod

from pathlib import Path
# ensure project root is on sys.path so 'interface' package can be imported
proj_root = Path(__file__).resolve().parents[1]
if str(proj_root) not in sys.path:
    sys.path.insert(0, str(proj_root))

from interface.services.nsga_integration import NSGAIntegration, EvacuationProblem
from interface.services.simulator_integration import SimulatorIntegration


@pytest.mark.skipif(NSGAIntegration is None, reason="pymoo or integration not available")
def test_minimal_nsga_run(monkeypatch, tmp_path):
    # Build a trivial map template and door positions
    map_template = "000\n020\n000"
    door_positions = [(1,1)]

    # Create a dummy simulator integration that doesn't actually call external processes
    sim = SimulatorIntegration(base_path=str(tmp_path))

    # Create individuals template minimal shape
    individuals_template = {"caracterizations": []}

    # Create EvacuationProblem but monkeypatch _evaluate_single to deterministic values
    prob = EvacuationProblem(sim, map_template, individuals_template, door_positions, simulation_params={})

    def fake_evaluate_single(gene):
        # return [num_doors, iterations, distance]
        return [float(sum(int(bool(x)) for x in gene)), 10.0, 5.0]

    monkeypatch.setattr(prob, '_evaluate_single', fake_evaluate_single)

    # Create a small population of binary genes
    pop = np.array([[0], [1], [1], [0]], dtype=bool)

    out = {}
    prob._evaluate(pop, out)
    F = out.get('F')
    assert F is not None
    assert F.shape[0] == pop.shape[0]
    assert F.shape[1] == 2
    assert np.isfinite(F).all()
