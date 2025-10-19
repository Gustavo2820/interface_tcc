"""
Módulo de integração com o simulador de heurística.

Este módulo implementa as funções necessárias para integrar a interface Streamlit
com o simulador de evacuação, seguindo as diretrizes da documentação de integração.
"""
import subprocess
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import sqlite3

# ======= STRUCTURE MAP =======
from simulador_heuristica.simulator.constants import Constants

class StructureMap(object):
    """Responsável por armazenar informações físicas do mapa: portas, paredes, etc."""

    def __init__(self, label, path: Optional[str] = None):
        self.label = label
        # Se path não for fornecido, monta caminho relativo: simulador_heuristica/input/<label>/map.txt
        if path is None:
            self.path = Path(__file__).parent.parent / "input" / label / "map.txt"
        else:
            self.path = Path(path)
        self.map = []
        self.len_row = 0
        self.len_col = 0
        self.exits = []

    def load_map(self):
        """Lê o arquivo de mapa e constrói o mapa da estrutura."""
        if not self.path.exists():
            raise FileNotFoundError(f"Mapa não encontrado em {self.path}")
        with open(self.path, 'r') as file:
            for line in file:
                line = line.strip('\n')
                self.map.append([])
                for col in line:
                    self.map[self.len_row].append(int(col))
                self.len_row += 1
        self.len_col = len(self.map[0])
        self.exits = self.get_exits()

    def get_empty_positions(self) -> List[Tuple[int, int]]:
        """Retorna uma lista com posições vazias do mapa."""
        empty_positions = []
        for i in range(self.len_row):
            for j in range(self.len_col):
                if self.map[i][j] == Constants.M_EMPTY:
                    empty_positions.append((i, j))
        return empty_positions

    def isSaida(self, row: int, col: int) -> bool:
        """Retorna se a posição é uma saída."""
        return self.map[row][col] == Constants.M_DOOR

    def get_exits(self) -> List[Tuple[int, int]]:
        """Retorna uma lista com as saídas do mapa."""
        exits = []
        for i in range(self.len_row):
            for j in range(self.len_col):
                if self.map[i][j] == Constants.M_DOOR:
                    exits.append((i, j))
        return exits

    def rewrite_doors(self, new_doors):
        """Substitui portas existentes por novas portas."""
        for exit in self.exits:
            self.map[exit[0]][exit[1]] = Constants.M_WALL
        for new_door in new_doors:
            if new_door['direction'] == 'V':
                for i in range(new_door['size']):
                    self.map[new_door['row'] + i][new_door['col']] = Constants.M_DOOR
            else:
                for i in range(new_door['size']):
                    self.map[new_door['row']][new_door['col'] + i] = Constants.M_DOOR
        self.exits = self.get_exits()


# ======= SIMULATOR INTEGRATION =======
class SimulatorIntegration:
    """Classe responsável pela integração entre interface e simulador."""
    
    def __init__(self, base_path: str = "simulador_heuristica"):
        # Derive project root from this file's location to avoid dependence on CWD
        current_file = Path(__file__).resolve()
        project_root = current_file.parents[2]
        self.base_path = (project_root / base_path).resolve()
        self.input_path = self.base_path / "input"
        self.output_path = self.base_path / "output"
        
    def prepare_experiment_from_uploads(
        self, 
        experiment_name: str, 
        map_file_path: Path, 
        individuals_file_path: Path
    ) -> Path:
        in_dir = self.input_path / experiment_name
        in_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(map_file_path, in_dir / "map.txt")
        shutil.copy2(individuals_file_path, in_dir / "individuals.json")
        return in_dir
    
    def run_simulator_cli(
        self, 
        experiment_name: str, 
        draw: bool = False, 
        scenario_seed: Optional[int] = None, 
        simulation_seed: Optional[int] = None
    ) -> subprocess.CompletedProcess:
        cmd = [sys.executable, "-m", "simulador_heuristica.simulator.main", "-e", experiment_name]
        if draw:
            cmd.append("-d")
        if scenario_seed is not None:
            cmd += ["-m", str(scenario_seed)]
        if simulation_seed is not None:
            cmd += ["-s", str(simulation_seed)]
        # Execute from project root so 'simulador_heuristica' package is importable with -m
        project_root = self.base_path.parent
        return subprocess.run(cmd, cwd=project_root, capture_output=True, text=True, check=False)
    
    def read_results(self, experiment_name: str) -> Dict:
        out_dir = self.output_path / experiment_name
        if not out_dir.exists():
            return {"error": "Diretório de saída não encontrado"}
        report_html = next(out_dir.glob("*.html"), None)
        frames = sorted(out_dir.glob("*.png"))
        metrics_files = list(out_dir.glob("*.json")) + list(out_dir.glob("*.txt"))
        return {"report": report_html, "frames": frames, "metrics": metrics_files, "directory": out_dir}
    
    def create_experiment_name(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"exp_{timestamp}"
    
    def validate_upload_files(self, map_file: Path, individuals_file: Path) -> Tuple[bool, str]:
        if not map_file.exists():
            return False, "Arquivo de mapa não encontrado"
        if not individuals_file.exists():
            return False, "Arquivo de indivíduos não encontrado"
        try:
            with open(individuals_file, 'r') as f:
                data = json.load(f)
                if 'caracterizations' not in data:
                    return False, "Arquivo de indivíduos deve conter 'caracterizations'"
        except json.JSONDecodeError:
            return False, "Arquivo de indivíduos deve ser um JSON válido"
        return True, "Arquivos válidos"


# ======= DATABASE INTEGRATION =======
class DatabaseIntegration:
    """Classe responsável pela integração com o banco de dados."""
    
    def __init__(self, db_path: str = "simulador.db"):
        self.db_path = db_path
    
    def save_simulation(
        self,
        id_simulacao: int,
        id_mapa: int,
        nome: str,
        algoritmo: str,
        config_pedestres_json: str,
        pos_pedestres_json: str,
        config_simulacao_json: str,
        cli_config_json: str,
        nsga_config_json: Optional[str] = None,
        executada: int = 0
    ) -> bool:
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            cur.execute("""
                INSERT OR REPLACE INTO Simulacao 
                (id_simulacao, id_mapa, nome, algoritmo, config_pedestres_json, 
                 pos_pedestres_json, config_simulacao_json, cli_config_json, 
                 nsga_config_json, executada)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (id_simulacao, id_mapa, nome, algoritmo, config_pedestres_json,
                  pos_pedestres_json, config_simulacao_json, cli_config_json,
                  nsga_config_json, executada))
            con.commit()
            con.close()
            return True
        except Exception as e:
            print(f"Erro ao salvar simulação: {e}")
            return False
    
    def get_simulations(self) -> List[Dict]:
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            cur.execute("""
                SELECT s.id_simulacao, s.nome, m.nome as mapa_nome, s.algoritmo, s.executada
                FROM Simulacao s
                JOIN Mapa m ON s.id_mapa = m.id_mapa
                ORDER BY s.id_simulacao DESC
            """)
            results = []
            for row in cur.fetchall():
                results.append({
                    "id": row[0],
                    "nome": row[1],
                    "mapa": row[2],
                    "algoritmo": row[3],
                    "simulado": "SIM" if row[4] == 1 else "NÃO"
                })
            con.close()
            return results
        except Exception as e:
            print(f"Erro ao recuperar simulações: {e}")
            return []
    
    def save_map(self, nome: str, arquivo_map: str) -> int:
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            cur.execute("INSERT INTO Mapa (nome, arquivo_map) VALUES (?, ?)", (nome, arquivo_map))
            map_id = cur.lastrowid
            con.commit()
            con.close()
            return map_id
        except Exception as e:
            print(f"Erro ao salvar mapa: {e}")
            return -1

    def save_nsga_results(self, id_simulacao: int, frente_pareto_json: str) -> bool:
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            # usa timestamp como id_resultado simples
            import time
            id_resultado = int(time.time())
            cur.execute(
                """
                INSERT OR REPLACE INTO Resultado (id_resultado, id_simulacao, frente_pareto_json)
                VALUES (?, ?, ?)
                """,
                (id_resultado, id_simulacao, frente_pareto_json)
            )
            con.commit()
            con.close()
            return True
        except Exception as e:
            print(f"Erro ao salvar resultados NSGA: {e}")
            return False
