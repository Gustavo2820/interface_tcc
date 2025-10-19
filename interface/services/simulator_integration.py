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


class SimulatorIntegration:
    """Classe responsável pela integração entre interface e simulador."""
    
    def __init__(self, base_path: str = "simulador_heuristica"):
        """
        Inicializa a integração com o simulador.
        
        Args:
            base_path: Caminho base para o simulador
        """
        self.base_path = Path(base_path)
        self.input_path = self.base_path / "input"
        self.output_path = self.base_path / "output"
        
    def prepare_experiment_from_uploads(
        self, 
        experiment_name: str, 
        map_file_path: Path, 
        individuals_file_path: Path
    ) -> Path:
        """
        Prepara um experimento copiando arquivos de upload para o diretório de entrada do simulador.
        
        Args:
            experiment_name: Nome único do experimento
            map_file_path: Caminho para o arquivo de mapa
            individuals_file_path: Caminho para o arquivo de indivíduos
            
        Returns:
            Caminho do diretório de entrada criado
        """
        in_dir = self.input_path / experiment_name
        in_dir.mkdir(parents=True, exist_ok=True)
        
        # Copia os arquivos preservando os nomes esperados pelo simulador
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
        """
        Executa o simulador via CLI.
        
        Args:
            experiment_name: Nome do experimento
            draw: Se deve gerar imagens
            scenario_seed: Seed para geração do cenário
            simulation_seed: Seed para a simulação
            
        Returns:
            Resultado da execução do subprocesso
        """
        cmd = [sys.executable, "-m", "simulador_heuristica.simulator.main", "-e", experiment_name]
        
        if draw:
            cmd.append("-d")
        if scenario_seed is not None:
            cmd += ["-m", str(scenario_seed)]
        if simulation_seed is not None:
            cmd += ["-s", str(simulation_seed)]
            
        return subprocess.run(cmd, check=True, capture_output=True, text=True)
    
    def read_results(self, experiment_name: str) -> Dict:
        """
        Lê os resultados gerados pelo simulador.
        
        Args:
            experiment_name: Nome do experimento
            
        Returns:
            Dicionário com os resultados encontrados
        """
        out_dir = self.output_path / experiment_name
        
        if not out_dir.exists():
            return {"error": "Diretório de saída não encontrado"}
            
        # Procura por arquivos de relatório HTML
        report_html = next(out_dir.glob("*.html"), None)
        
        # Procura por frames de imagem
        frames = sorted(out_dir.glob("*.png"))
        
        # Procura por arquivos de métricas
        metrics_files = list(out_dir.glob("*.json")) + list(out_dir.glob("*.txt"))
        
        return {
            "report": report_html,
            "frames": frames,
            "metrics": metrics_files,
            "directory": out_dir
        }
    
    def create_experiment_name(self) -> str:
        """
        Cria um nome único para o experimento baseado em timestamp.
        
        Returns:
            Nome único do experimento
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"exp_{timestamp}"
    
    def validate_upload_files(self, map_file: Path, individuals_file: Path) -> Tuple[bool, str]:
        """
        Valida se os arquivos de upload estão no formato correto.
        
        Args:
            map_file: Arquivo de mapa
            individuals_file: Arquivo de indivíduos
            
        Returns:
            Tupla (é_válido, mensagem_de_erro)
        """
        if not map_file.exists():
            return False, "Arquivo de mapa não encontrado"
            
        if not individuals_file.exists():
            return False, "Arquivo de indivíduos não encontrado"
        
        # Valida formato do arquivo de indivíduos
        try:
            with open(individuals_file, 'r') as f:
                data = json.load(f)
                if 'caracterizations' not in data:
                    return False, "Arquivo de indivíduos deve conter 'caracterizations'"
        except json.JSONDecodeError:
            return False, "Arquivo de indivíduos deve ser um JSON válido"
        
        return True, "Arquivos válidos"


class DatabaseIntegration:
    """Classe responsável pela integração com o banco de dados."""
    
    def __init__(self, db_path: str = "simulador.db"):
        """
        Inicializa a integração com o banco de dados.
        
        Args:
            db_path: Caminho para o arquivo do banco de dados
        """
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
        """
        Salva uma simulação no banco de dados.
        
        Args:
            id_simulacao: ID da simulação
            id_mapa: ID do mapa
            nome: Nome da simulação
            algoritmo: Algoritmo utilizado
            config_pedestres_json: Configuração dos pedestres (JSON)
            pos_pedestres_json: Posições dos pedestres (JSON)
            config_simulacao_json: Configuração da simulação (JSON)
            cli_config_json: Configuração CLI (JSON)
            nsga_config_json: Configuração NSGA-II (JSON, opcional)
            executada: Se foi executada (0 ou 1)
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
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
        """
        Recupera todas as simulações do banco de dados.
        
        Returns:
            Lista de dicionários com as simulações
        """
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
        """
        Salva um mapa no banco de dados.
        
        Args:
            nome: Nome do mapa
            arquivo_map: Caminho para o arquivo do mapa
            
        Returns:
            ID do mapa salvo
        """
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            
            cur.execute("""
                INSERT INTO Mapa (nome, arquivo_map) VALUES (?, ?)
            """, (nome, arquivo_map))
            
            map_id = cur.lastrowid
            con.commit()
            con.close()
            return map_id
            
        except Exception as e:
            print(f"Erro ao salvar mapa: {e}")
            return -1
