import json
import os
from pathlib import Path
import tempfile
import pytest
import sys
import types

# insert fake constants module to avoid heavy simulator import
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
import sys
if str(proj_root) not in sys.path:
    sys.path.insert(0, str(proj_root))

from interface.services.simulator_integration import SimulatorIntegration
from interface.services.nsga_integration import NSGAIntegration


def make_fake_metrics(out_dir: Path, name: str, iterations: int = 10, distance: float = 5.5):
    d = out_dir / name
    d.mkdir(parents=True, exist_ok=True)
    m = {'iterations': iterations, 'distance': distance, 'tempo_total': 0.123}
    (d / 'metrics.json').write_text(json.dumps(m))
    return d


def test_simulator_read_and_atomic_write(tmp_path):
    sim = SimulatorIntegration(base_path=str(tmp_path))
    # Simulate an output experiment
    exp_name = 'exp_test_01'
    out_dir = Path(sim.base_path) / 'output' / exp_name
    out_dir.mkdir(parents=True, exist_ok=True)
    # Write a metrics file
    metrics = {'iterations': 7, 'distance': 3.14}
    metrics_file = out_dir / 'metrics.json'
    # emulate atomic write: write .tmp then replace
    tmp_metrics = metrics_file.with_suffix('.tmp')
    tmp_metrics.write_text(json.dumps(metrics))
    tmp_metrics.replace(metrics_file)

    res = sim.read_results(exp_name)
    assert 'metrics' in res
    mf = res['metrics'][0]
    assert mf.exists()

    # Test NSGAIntegration.save_results writes results and consolidated metrics
    nsga = NSGAIntegration(sim)
    # provide a minimal problem object expected by save_results
    import types
    nsga.problem = types.SimpleNamespace(door_positions=[(0,0),(1,0),(2,0)])
    # Build synthetic pymoo-like result with X and F arrays
    import numpy as _np
    class DummyRes:
        def __init__(self):
            self.X = _np.array([[0,1],[1,0]])
            self.F = _np.array([[1, 10, 2.5],[2, 20, 5.5]])
    res_obj = DummyRes()

    out_file = tmp_path / 'results_exp_test_01.json'
    ok = nsga.save_results(res_obj, out_file)
    assert ok is True
    assert out_file.exists()
    data = json.loads(out_file.read_text())
    assert isinstance(data, list)
    # Check objectives shape and types
    for entry in data:
        objs = entry.get('objectives')
        assert isinstance(objs, list)
        assert len(objs) == 2
        # types: first is num_doors (int/float), second is distance (float)
        assert isinstance(objs[0], (int, float))
        assert isinstance(objs[1], (int, float))
