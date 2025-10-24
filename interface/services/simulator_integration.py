"""
Módulo de integração com o simulador de heurística.

Este módulo implementa as funções necessárias para integrar a interface Streamlit
com o simulador de evacuação, seguindo as diretrizes da documentação de integração.

NOTE: This module now delegates to simulador_heuristica.simulator.integration_api
for all map/door/individuals logic. No simulation logic is duplicated here.
"""
import subprocess
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import sqlite3

# ======= SIMULATOR IMPORTS =======
# Import the official integration API and simulator modules
try:
    from simulador_heuristica.simulator.constants import Constants
    from simulador_heuristica.simulator import integration_api
    from simulador_heuristica.simulator.structure_map import StructureMap
except Exception:
    current_file = Path(__file__).resolve()
    project_root = current_file.parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from simulador_heuristica.simulator.constants import Constants
    from simulador_heuristica.simulator import integration_api
    from simulador_heuristica.simulator.structure_map import StructureMap


# ======= REMOVED: Duplicated StructureMap class =======
# This class previously duplicated logic from simulador_heuristica.simulator.structure_map
# Integration code should now use the official StructureMap from the simulator package.
# See: simulador_heuristica/simulator/structure_map.py for the canonical implementation.


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
        # Ensure DB schema exists (useful when DB file is present but empty)
        try:
            self._ensure_schema()
        except Exception as e:
            print(f"Warning: failed to ensure DB schema: {e}")

    def _ensure_schema(self):
        """Create required tables if they don't exist. Idempotent."""
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        # enable foreign keys
        cur.execute('PRAGMA foreign_keys = ON')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Mapa (
            id_mapa INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            arquivo_map TEXT NOT NULL
        )
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Simulacao (
            id_simulacao INTEGER PRIMARY KEY,
            id_mapa INTEGER NOT NULL,
            nome TEXT NOT NULL,
            algoritmo TEXT NOT NULL,
            config_pedestres_json TEXT NOT NULL,
            pos_pedestres_json TEXT,
            config_simulacao_json TEXT NOT NULL,
            cli_config_json TEXT NOT NULL,
            nsga_config_json TEXT,
            executada INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (id_mapa) REFERENCES Mapa(id_mapa) ON DELETE CASCADE
        )
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Resultado (
            id_resultado INTEGER PRIMARY KEY,
            id_simulacao INTEGER NOT NULL,
            frente_pareto_json TEXT NOT NULL,
            FOREIGN KEY (id_simulacao) REFERENCES Simulacao(id_simulacao) ON DELETE CASCADE
        )
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Preset (
            id_preset INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL,
            parametros_json TEXT NOT NULL
        )
        ''')
        con.commit()
        con.close()
    
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
            # ensure foreign key constraints are enabled
            con.execute('PRAGMA foreign_keys = ON')
            cur = con.cursor()
            # If an id_simulacao is provided, try to insert using it.
            if id_simulacao and int(id_simulacao) > 0:
                try:
                    cur.execute("""
                        INSERT OR REPLACE INTO Simulacao 
                        (id_simulacao, id_mapa, nome, algoritmo, config_pedestres_json, 
                         pos_pedestres_json, config_simulacao_json, cli_config_json, 
                         nsga_config_json, executada)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (int(id_simulacao), id_mapa, nome, algoritmo, config_pedestres_json,
                          pos_pedestres_json, config_simulacao_json, cli_config_json,
                          nsga_config_json, int(executada)))
                except Exception as e:
                    # fallback: insert without id (let DB assign primary key)
                    print(f"Warning: failed to insert with provided id_simulacao={id_simulacao}: {e}. Falling back to autoinsert.")
                    cur.execute("""
                        INSERT INTO Simulacao 
                        (id_mapa, nome, algoritmo, config_pedestres_json, 
                         pos_pedestres_json, config_simulacao_json, cli_config_json, 
                         nsga_config_json, executada)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (id_mapa, nome, algoritmo, config_pedestres_json,
                          pos_pedestres_json, config_simulacao_json, cli_config_json,
                          nsga_config_json, int(executada)))
            else:
                # No id provided: let the DB assign one
                cur.execute("""
                    INSERT INTO Simulacao 
                    (id_mapa, nome, algoritmo, config_pedestres_json, 
                     pos_pedestres_json, config_simulacao_json, cli_config_json, 
                     nsga_config_json, executada)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (id_mapa, nome, algoritmo, config_pedestres_json,
                      pos_pedestres_json, config_simulacao_json, cli_config_json,
                      nsga_config_json, int(executada)))
            con.commit()
            con.close()
            return True
        except Exception as e:
            # log detailed error for debugging
            print(f"Erro ao salvar simulação (id_simulacao={id_simulacao}, id_mapa={id_mapa}, nome={nome}): {e}")
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

    def get_simulations_by_map(self, mapa_nome: str) -> List[Dict]:
        """Retorna todas as simulações associadas a um mapa (pelo nome do mapa)."""
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            cur.execute("""
                SELECT s.id_simulacao, s.nome, m.nome as mapa_nome, s.algoritmo, s.executada
                FROM Simulacao s
                JOIN Mapa m ON s.id_mapa = m.id_mapa
                WHERE m.nome = ?
                ORDER BY s.id_simulacao DESC
            """, (mapa_nome,))
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
            print(f"Erro ao recuperar simulações por mapa: {e}")
            return []

    def get_simulation(self, id_simulacao: int) -> Optional[Dict]:
        """Retorna os detalhes de uma simulação pelo seu id_simulacao."""
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            cur.execute("""
                SELECT s.id_simulacao, s.nome, s.id_mapa, m.nome as mapa_nome, s.algoritmo,
                       s.config_pedestres_json, s.pos_pedestres_json, s.config_simulacao_json,
                       s.cli_config_json, s.nsga_config_json, s.executada
                FROM Simulacao s
                JOIN Mapa m ON s.id_mapa = m.id_mapa
                WHERE s.id_simulacao = ?
            """, (id_simulacao,))
            row = cur.fetchone()
            con.close()
            if not row:
                return None
            return {
                "id": row[0],
                "nome": row[1],
                "id_mapa": row[2],
                "mapa": row[3],
                "algoritmo": row[4],
                "config_pedestres_json": row[5],
                "pos_pedestres_json": row[6],
                "config_simulacao_json": row[7],
                "cli_config_json": row[8],
                "nsga_config_json": row[9],
                "executada": row[10]
            }
        except Exception as e:
            print(f"Erro ao recuperar simulação: {e}")
            return None
    
    def save_map(self, nome: str, arquivo_map: str) -> int:
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            # Try to insert, but if the name already exists (unique), retrieve the existing id
            try:
                cur.execute("INSERT INTO Mapa (nome, arquivo_map) VALUES (?, ?)", (nome, arquivo_map))
                map_id = cur.lastrowid
            except sqlite3.IntegrityError:
                # nome is unique - retrieve existing id
                cur.execute("SELECT id_mapa FROM Mapa WHERE nome = ?", (nome,))
                row = cur.fetchone()
                map_id = row[0] if row else -1
            con.commit()
            con.close()
            return map_id
        except Exception as e:
            print(f"Erro ao salvar mapa: {e}")
            return -1
    def save_result(self, id_simulacao: int, result_json: str) -> bool:
        """Generic saver for any simulation result JSON into Resultado."""
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            import time
            id_resultado = int(time.time())
            cur.execute(
                """
                INSERT OR REPLACE INTO Resultado (id_resultado, id_simulacao, frente_pareto_json)
                VALUES (?, ?, ?)
                """,
                (id_resultado, id_simulacao, result_json)
            )
            con.commit()
            con.close()
            return True
        except Exception as e:
            print(f"Erro ao salvar resultado: {e}")
            return False

    def save_nsga_results(self, id_simulacao: int, frente_pareto_json: str) -> bool:
        """Backward-compatible wrapper for saving NSGA results."""
        return self.save_result(id_simulacao, frente_pareto_json)

    def create_simulation_return_id(
        self,
        id_mapa: int,
        nome: str,
        algoritmo: str,
        config_pedestres_json: str,
        pos_pedestres_json: str,
        config_simulacao_json: str,
        cli_config_json: str,
        nsga_config_json: Optional[str] = None,
        executada: int = 0
    ) -> Optional[int]:
        """Insert a simulation without requiring an id_simulacao and return the new id on success."""
        try:
            con = sqlite3.connect(self.db_path)
            con.execute('PRAGMA foreign_keys = ON')
            cur = con.cursor()
            cur.execute("""
                INSERT INTO Simulacao 
                (id_mapa, nome, algoritmo, config_pedestres_json, 
                 pos_pedestres_json, config_simulacao_json, cli_config_json, 
                 nsga_config_json, executada)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (id_mapa, nome, algoritmo, config_pedestres_json,
                  pos_pedestres_json, config_simulacao_json, cli_config_json,
                  nsga_config_json, int(executada)))
            con.commit()
            # get the last inserted id
            cur.execute('SELECT last_insert_rowid()')
            row = cur.fetchone()
            con.close()
            return row[0] if row else None
        except Exception as e:
            print(f"Erro ao criar simulação sem id: {e}")
            return None
