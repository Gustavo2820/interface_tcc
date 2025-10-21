import ast
from pathlib import Path
import pytest


def _read_source(path: Path) -> str:
    return path.read_text()


def test_resultados_contains_expected_sections():
    p = Path('interface/pages/Resultados.py')
    src = _read_source(p)
    # check some key UI labels and CSS classes
    assert 'Mini-mapa' in src or 'mini-mapa' in src
    assert 'metric-card' in src
    assert 'section-title' in src


def test_criacao_mapas_page_exists_and_has_title():
    p = Path('interface/pages/Criacao_Mapas.py')
    assert p.exists()
    src = _read_source(p)
    assert 'Criação de Mapas' in src or 'Cria' in src
