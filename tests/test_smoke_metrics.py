import pytest
from pathlib import Path
import json


def find_nsga_eval_dirs():
    base = Path('simulador_heuristica') / 'output'
    return sorted([p for p in base.glob('nsga_eval_*') if p.is_dir()])


def test_per_eval_metrics_exist_and_consolidated():
    dirs = find_nsga_eval_dirs()
    if not dirs:
        pytest.skip('No nsga_eval_* dirs present')

    # pick a sample directory
    sample = dirs[0]
    metrics = sample / 'metrics.json'
    assert metrics.exists(), f'metrics.json missing in {sample}'
    data = json.loads(metrics.read_text())
    assert 'tempo_total' in data and 'distancia_total' in data

    # consolidated file
    consolidated = Path('simulador_heuristica') / 'output' / 'agoravai' / 'metrics.json'
    assert consolidated.exists(), 'consolidated metrics.json missing'
    c = json.loads(consolidated.read_text())
    assert 'evaluations' in c and isinstance(c['evaluations'], list)
