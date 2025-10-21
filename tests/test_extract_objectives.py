import json
from pathlib import Path
import tempfile
import pytest
import sys
import types

# lightweight fake constants module for simulator during tests
fake_mod = types.ModuleType('simulador_heuristica.simulator.constants')
class _C:
    M_EMPTY = 0
    M_WALL = 1
    M_DOOR = 2
fake_mod.Constants = _C
sys.modules['simulador_heuristica.simulator.constants'] = fake_mod
from pathlib import Path
import sys
# ensure project root is on sys.path so 'interface' package can be imported
proj_root = Path(__file__).resolve().parents[1]
if str(proj_root) not in sys.path:
    sys.path.insert(0, str(proj_root))

from interface.services.nsga_integration import EvacuationProblem
from interface.services.simulator_integration import SimulatorIntegration


def test_extract_from_dict(tmp_path):
    sim = SimulatorIntegration(base_path=str(tmp_path))
    prob = EvacuationProblem(sim, "0", {"caracterizations": []}, [], {})
    res = {'iterations': 12, 'distance': 2.5}
    nd, dist = prob._extract_objectives(res, num_doors=4)
    # now _extract_objectives returns [num_doors, distance]
    assert nd == 4
    assert dist == 2.5


def test_extract_from_metrics_file(tmp_path):
    sim = SimulatorIntegration(base_path=str(tmp_path))
    # build a fake output dir and metrics.json
    outdir = tmp_path / 'some_exp'
    outdir.mkdir()
    m = {'iterations': 3, 'distance': 1.1}
    (outdir / 'metrics.json').write_text(json.dumps(m))
    prob = EvacuationProblem(sim, "0", {"caracterizations": []}, [], {})
    res = {'metrics': [str(outdir / 'metrics.json')], 'directory': str(outdir)}
    nd, dist = prob._extract_objectives(res, num_doors=2)
    assert nd == 2
    assert dist == 1.1


def test_extract_from_stdout(tmp_path):
    sim = SimulatorIntegration(base_path=str(tmp_path))
    prob = EvacuationProblem(sim, "0", {"caracterizations": []}, [], {})
    stdout = "Some log\ntempo total 2.0\ndistancia 0.5\n"
    nd, dist = prob._extract_objectives({}, stdout=stdout, num_doors=3)
    # num_doors should be reflected and distance parsed
    assert nd == 3
    assert dist == pytest.approx(0.5)
