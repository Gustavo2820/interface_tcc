"""
Módulo de integração com NSGA-II.

Este módulo implementa a integração específica para o algoritmo NSGA-II,
permitindo a execução de otimização multiobjetivo usando o simulador.
"""
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
import streamlit as st
from .logger import default_log as logger
import types
import warnings

# Adiciona o caminho do simulador ao sys.path para importar módulos
# Usa caminho absoluto baseado na raiz do projeto (duas pastas acima de `services`)
project_root = Path(__file__).resolve().parents[2]
simulador_path = project_root / "simulador_heuristica"
unified_path = simulador_path / "unified"
simulator_path = simulador_path / "simulator"

# Adiciona os caminhos necessários ao sys.path
if str(simulador_path) not in sys.path:
    sys.path.append(str(simulador_path))
if str(unified_path) not in sys.path:
    sys.path.append(str(unified_path))
if str(simulator_path) not in sys.path:
    sys.path.append(str(simulator_path))

print("DEBUG: Tentando importar módulos NSGA-II...")
print(f"DEBUG: simulador_path: {simulador_path}")
print(f"DEBUG: unified_path: {unified_path}")
print(f"DEBUG: sys.path entries: {[p for p in sys.path if 'simulador' in p]}")

# Import the unified integration API (single source of truth for simulator logic)
try:
    from simulador_heuristica.simulator import integration_api
    print("DEBUG: integration_api imported successfully")
except ImportError as e:
    print(f"WARNING: Could not import integration_api: {e}")
    integration_api = None

# Import cached NSGA-II integration (optional)
try:
    from .nsga_cached_integration import get_cached_nsga_integration
    print("DEBUG: Cached NSGA-II integration available")
    CACHED_NSGA_AVAILABLE = True
except ImportError as e:
    print(f"DEBUG: Cached NSGA-II not available: {e}")
    get_cached_nsga_integration = None
    CACHED_NSGA_AVAILABLE = False

try:
    print("DEBUG: Importando pymoo...")
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.core.problem import Problem
    from pymoo.optimize import minimize
    from pymoo.operators.sampling.rnd import BinaryRandomSampling
    from pymoo.operators.crossover.hux import HalfUniformCrossover
    from pymoo.operators.mutation.bitflip import BitflipMutation
    print("DEBUG: Módulos pymoo importados com sucesso")
    print("DEBUG: NSGA2 =", NSGA2)
    print("DEBUG: Problem =", Problem)
    print("DEBUG: minimize =", minimize)
    st.success("Módulos pymoo importados com sucesso")
except ImportError as e:
    print(f"DEBUG: Erro ao importar módulos do pymoo: {e}")
    import traceback
    print(f"DEBUG: Traceback completo: {traceback.format_exc()}")
    st.error(f"Erro ao importar módulos do pymoo: {e}")
    # Fallback para quando os módulos não estão disponíveis
    NSGA2 = None
    Problem = None
    minimize = None
    BinaryRandomSampling = None
    HalfUniformCrossover = None
    BitflipMutation = None
except Exception as e:
    print(f"DEBUG: Erro inesperado ao importar módulos: {e}")
    import traceback
    print(f"DEBUG: Traceback completo: {traceback.format_exc()}")
    st.error(f"Erro inesperado ao importar módulos: {e}")
    # Fallback para quando os módulos não estão disponíveis
    NSGA2 = None
    Problem = None
    minimize = None
    BinaryRandomSampling = None
    HalfUniformCrossover = None
    BitflipMutation = None

# Define uma classe base Problem se a importação falhou
if Problem is None:
    class Problem:
        """Classe base para Problem quando os módulos não estão disponíveis."""
        def __init__(self, n_var, n_obj, n_constr=0, xl=0, xu=1, type_var=bool):
            self.n_var = n_var
            self.n_obj = n_obj
            self.n_constr = n_constr
            self.xl = xl
            self.xu = xu
            self.type_var = type_var
        
        def _evaluate(self, x, out, *args, **kwargs):
            raise NotImplementedError


class EvacuationProblem(Problem):
    """
    Problema de evacuação para pymoo NSGA-II.
    
    Esta classe implementa a interface necessária para o pymoo,
    adaptando o problema de evacuação para otimização multiobjetivo.
    """
    
    def __init__(self, simulator_integration, map_template: str, individuals_template: Dict, door_positions: List[tuple], simulation_params: Dict = None):
        """
        Inicializa o problema de evacuação.
        
        Args:
            simulator_integration: Instância da integração com o simulador
            map_template: Template do mapa base
            individuals_template: Template dos indivíduos base
            door_positions: Lista de posições possíveis para portas
            simulation_params: Parâmetros de simulação (opcional)
        """
        self.simulator_integration = simulator_integration
        self.map_template = map_template
        self.individuals_template = individuals_template
        self.door_positions = door_positions
        self.simulation_params = simulation_params or {}
        self.evaluation_count = 0
    # Define um problema com 2 objetivos e n variáveis binárias (uma para cada posição de porta)
    # Objetivos (legacy adjusted): [num_doors, distance]
        # initialize base Problem now that self.door_positions is set
        n_var = len(self.door_positions)
        super().__init__(n_var=n_var, n_obj=2, n_constr=0, xl=0, xu=1, type_var=bool)
    
    def _evaluate(self, x, out, *args, **kwargs):
        """
        Avalia uma população de soluções.

        Args:
            x: Matriz de soluções (pop_size x n_var)
            out: Dicionário de saída onde 'F' contém os objetivos
        """
        # Evaluate each individual and ensure returned array is numeric and finite.
        raw = np.apply_along_axis(self._evaluate_single, 1, x)

        try:
            results = np.asarray(raw, dtype=float)
        except Exception:
            logger.exception("Failed to convert evaluation results to array")
            # do not invent values; fail safe by assigning large penalty but log as ERROR
            results = np.full((len(x), 2), 1e6, dtype=float)

        # Normalize shape to (pop_size, 2)
        if results.ndim == 1 and results.size == 2:
            results = np.tile(results, (len(x), 1))
        elif results.ndim == 1 and results.size != 2:
            # Unexpected shape, set penalties
            logger.debug(f"Unexpected evaluation shape {results.shape}, applying penalties")
            results = np.full((len(x), 2), 1e6, dtype=float)
        elif results.ndim == 2 and results.shape[1] != 2:
            # If more/less objectives returned, try to truncate or pad
            logger.debug(f"Evaluation returned {results.shape[1]} objectives per individual; adjusting to 2")
            if results.shape[1] > 2:
                results = results[:, :2]
            else:
                # pad with penalty
                pad = np.full((results.shape[0], 2 - results.shape[1]), 1e6, dtype=float)
                results = np.hstack([results, pad])

        # Sanitize non-finite values
        nonfinite_mask = ~np.isfinite(results)
        if nonfinite_mask.any():
            logger.warning("Non-finite objective values detected; replacing with penalty 1e6")
            results[nonfinite_mask] = 1e6

        # Ensure slight difference between objectives to avoid degenerate equal objectives
        for i in range(results.shape[0]):
            for a in range(results.shape[1]-1):
                if results[i, a] == results[i, a+1]:
                    results[i, a+1] = results[i, a+1] + 1e-6

        out["F"] = results
    
     
    def _evaluate_single(self, gene):
        """
        Avalia uma única solução.
        
        Args:
            gene: Vetor binário representando quais portas usar
            
            Returns:
            Lista com os valores dos 3 objetivos na ordem [num_doors, iterations, distance]
        """
        # Decode gene and prepare experiment directory and files
        door_positions = self._decode_gene(gene)

        experiment_name = f"nsga_eval_{self.evaluation_count}"
        self.evaluation_count += 1

        map_content = self._generate_map_with_doors(door_positions)

        temp_dir = Path("temp_nsga") / experiment_name
        temp_dir.mkdir(parents=True, exist_ok=True)

        map_file = temp_dir / "map.txt"
        individuals_file = temp_dir / "individuals.json"

        try:
            with open(map_file, 'w') as f:
                f.write(map_content)

            with open(individuals_file, 'w') as f:
                json.dump(self.individuals_template, f, indent=2)

            # Prepare experiment using the integration helper (copies files to simulator input)
            self.simulator_integration.prepare_experiment_from_uploads(
                experiment_name, map_file, individuals_file
            )

            scenario_seed = self.simulation_params.get('scenario_seed')
            simulation_seed = self.simulation_params.get('simulation_seed')
            draw_mode = self.simulation_params.get('draw_mode', False)

            # Execute simulator CLI and capture output for debugging
            proc = self.simulator_integration.run_simulator_cli(
                experiment_name,
                draw=draw_mode,
                scenario_seed=scenario_seed,
                simulation_seed=simulation_seed
            )

            # Log subprocess result when available
            try:
                rc = getattr(proc, 'returncode', None)
                stdout = getattr(proc, 'stdout', None)
                stderr = getattr(proc, 'stderr', None)
                logger.debug("Simulator returncode=%s for experiment %s", rc, experiment_name)
                if stdout:
                    logger.debug("Simulator stdout (truncated): %s", str(stdout)[:1000])
                if stderr:
                    logger.debug("Simulator stderr (truncated): %s", str(stderr)[:1000])
            except Exception:
                rc = None
                stdout = None
                stderr = None

            # Read results produced by the simulator (files in output/<experiment>)
            results = self.simulator_integration.read_results(experiment_name)

            if results.get("error"):
                logger.error("read_results returned error for %s: %s", experiment_name, results.get('error'))
                # No invented values: return explicit penalty but log for audit
                return [1e6, 1e6]

            # num_doors should reflect number of selected door *configurations* (grouped doors)
            # If door_positions contains door dicts (from extract_doors_info), count them; otherwise count tuples
            if door_positions and isinstance(door_positions[0], dict):
                num_doors = len(door_positions)
            else:
                num_doors = len(door_positions)

            # Extract numeric objective distance (and optionally num_doors) from results
            obj = self._extract_objectives(results, stdout=stdout, stderr=stderr, num_doors=num_doors)

            # _extract_objectives returns [num_doors, distance]
            try:
                num_doors_val = float(obj[0]) if obj and obj[0] is not None else float(num_doors)
            except Exception:
                num_doors_val = float(num_doors)
            try:
                distance_val = float(obj[1]) if obj and obj[1] is not None else None
            except Exception:
                distance_val = None

            # Do not penalize iterations (auxiliary metric). Only penalize distance if missing
            if distance_val is None or not np.isfinite(distance_val):
                logger.warning("Missing or non-finite distance for %s, applying penalty", experiment_name)
                distance_val = 1e6

            # Return objectives as floats: [num_doors, distance]
            return [float(num_doors_val), float(distance_val)]

        except Exception as e:
            logger.exception("Exception during evaluation of experiment %s", experiment_name)
            return [1e6, 1e6]

        finally:
            # Clean up temporary staging directory
            import shutil
            try:
                if temp_dir.exists():
                    shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception as e:
                print(f"DEBUG: Failed to remove temp_dir {temp_dir}: {e}")

    
    def _decode_gene(self, gene: Any) -> List[tuple]:
        """
        Decodifica um gene binário para posições de portas.
        
        Args:
            gene: Vetor binário onde 1 indica que a porta deve ser usada
            
        Returns:
            Lista de tuplas (x, y) com posições das portas
        """
        # Converte gene binário para posições de portas
        # Decode gene to selected door configurations or tuples.
        # The self.door_positions may contain either tuples (x,y) or dicts produced by
        # simulador_heuristica.simulator.sim_ca_scenario.extract_doors_info (grouped doors).
        selected = []
        for i, bit in enumerate(gene):
            if int(bit) == 1 and i < len(self.door_positions):
                selected.append(self.door_positions[i])
        return selected
    
    def _generate_map_with_doors(self, door_positions: List[tuple]) -> str:
        """
        Gera o conteúdo do mapa com as portas posicionadas.
        
        Now delegates to integration_api for consistent door placement logic.
        
        Args:
            door_positions: Lista de posições das portas a serem ativadas
            
        Returns:
            Conteúdo do mapa como string
        """
        # OFFICIAL INTEGRATION: Use the unified API for map generation
        if integration_api is not None:
            try:
                # Filter to only dict entries (grouped doors)
                grouped_doors = [d for d in door_positions if isinstance(d, dict)]
                return integration_api.generate_map_text_with_grouped_doors(
                    self.map_template, 
                    grouped_doors
                )
            except Exception as e:
                logger.error(f"Failed to call integration_api.generate_map_text_with_grouped_doors: {e}")
                # Fall through to legacy fallback
        
        # DEPRECATED FALLBACK: manual string manipulation
        logger.warning("integration_api not available, using deprecated fallback for map generation")
        lines = self.map_template.split('\n')
        
        # Primeiro, desativa todas as portas existentes (converte '2' para '0')
        for y, line in enumerate(lines):
            lines[y] = line.replace('2', '0')
        
        # Depois, ativa apenas as portas selecionadas.
        # door_positions entries may be tuples (x,y) or dicts describing grouped doors
        for entry in door_positions:
            if isinstance(entry, dict):
                # grouped door: has 'row','col','size','direction'
                r = int(entry.get('row', 0))
                c = int(entry.get('col', 0))
                size = int(entry.get('size', 1))
                direction = entry.get('direction', '')
                if direction == 'H':
                    for offset in range(size):
                        x = c + offset
                        y = r
                        if 0 <= y < len(lines) and 0 <= x < len(lines[y]):
                            line = list(lines[y])
                            line[x] = '2'
                            lines[y] = ''.join(line)
                elif direction == 'V':
                    for offset in range(size):
                        x = c
                        y = r + offset
                        if 0 <= y < len(lines) and 0 <= x < len(lines[y]):
                            line = list(lines[y])
                            line[x] = '2'
                            lines[y] = ''.join(line)
                else:
                    # fallback: treat as single coordinate if present
                    x = int(entry.get('col', 0))
                    y = int(entry.get('row', 0))
                    if 0 <= y < len(lines) and 0 <= x < len(lines[y]):
                        line = list(lines[y])
                        line[x] = '2'
                        lines[y] = ''.join(line)
            else:
                # legacy tuple (x,y)
                try:
                    x, y = entry
                    if 0 <= y < len(lines) and 0 <= x < len(lines[y]):
                        line = list(lines[y])
                        line[x] = '2'  # 2 representa porta ativa no formato do simulador
                        lines[y] = ''.join(line)
                except Exception:
                    continue
        
        return '\n'.join(lines)
    
    def _extract_objectives(self, results: Dict, stdout: Optional[str] = None, stderr: Optional[str] = None, num_doors: Optional[int] = None) -> List[Optional[float]]:
        """
        Extrai as métricas de interesse a partir do dicionário retornado por `read_results`.
        Para compatibilidade com os experiments legacy, procura preferencialmente por:
        - 'distancia' / 'distance' / 'qtdDistance' / 'distancia_total' -> distance objective

        Nota: 'iterations' é considerada uma métrica auxiliar e NÃO é tratada como objetivo.

        Retorna uma lista com dois elementos: [num_doors, distance]. num_doors pode ser fornecido
        pelo chamador (a partir do gene) e será usado por preferência; caso contrário, retornará None
        no primeiro elemento.
        """
        try:
            # Fast path: results already contain metrics
            if isinstance(results, dict):
                # If explicit metrics already present as top-level numeric keys, prefer distance keys
                distance_keys = ['distance', 'avg_distance', 'qtdDistance', 'qtd_distancia', 'qtd_distance', 'distancia', 'total_distance', 'distancia_total']
                d_key = next((k for k in distance_keys if k in results), None)
                d_val = None
                if d_key:
                    try:
                        d_val = float(results[d_key])
                    except Exception:
                        d_val = None
                    # num_doors preference: take provided num_doors if available
                    nd = float(num_doors) if num_doors is not None else None
                    return [nd, d_val]

                # If a metrics file list is provided, try to open the first JSON containing keys
                metrics_candidates = results.get('metrics') or []
                # If directory is provided, scan for metrics*.json
                out_dir = results.get('directory')
                if out_dir and not metrics_candidates:
                    try:
                        p = Path(out_dir)
                        metrics_candidates = [str(p / f.name) for f in p.glob('metrics*.json')]
                    except Exception:
                        metrics_candidates = []

                # Try to parse candidate files (prefer explicit iteration and distance keys)
                for candidate in metrics_candidates:
                    try:
                        candidate_path = Path(candidate)
                        if not candidate_path.exists():
                            # candidate may already be a Path-like object
                            continue
                        with open(candidate_path, 'r') as fh:
                            data = json.load(fh)
                        # Accept nested structures: try explicit distance key names (including legacy keys)
                        d_key = next((k for k in ('distance','avg_distance','qtdDistance','qtd_distancia','qtd_distance','distancia','total_distance','distancia_total') if k in data), None)
                        if d_key:
                            try:
                                d_val = float(data[d_key])
                            except Exception:
                                d_val = None
                            nd = float(num_doors) if num_doors is not None else None
                            return [nd, d_val]
                        # also check under a 'metrics' object
                        # also check under a 'metrics' object for distance
                        if 'metrics' in data and isinstance(data['metrics'], dict):
                            d_key = next((k for k in ('distance','avg_distance','qtdDistance','qtd_distancia','qtd_distance','distancia','total_distance','distancia_total') if k in data['metrics']), None)
                            if d_key:
                                try:
                                    d_val = float(data['metrics'][d_key])
                                except Exception:
                                    d_val = None
                                nd = float(num_doors) if num_doors is not None else None
                                return [nd, d_val]
                    except Exception as e:
                        logger.debug(f"Failed to parse metrics candidate {candidate}: {e}")

                # If nothing found in metrics files, try parsing raw stdout/stderr for explicit printed time/distance
                if stdout:
                    try:
                        s_time = None
                        s_dist = None
                        for line in str(stdout).splitlines():
                            line = line.strip().lower()
                            # Look for explicit time lines
                            if 'tempo' in line and any(tok in line for tok in ('tempo','time')):
                                # attempt to parse a float from the line
                                parts = line.replace(',', '.').split()
                                for p in reversed(parts):
                                    try:
                                        s_time = float(p)
                                        break
                                    except Exception:
                                        continue
                            # Look for explicit distance lines
                            # also capture legacy printed tokens like 'qtdDistance' or 'qtd distancia'
                            if 'dist' in line or 'distância' in line or 'distance' in line or 'qtd' in line:
                                parts = line.replace(',', '.').split()
                                for p in reversed(parts):
                                    try:
                                        s_dist = float(p)
                                        break
                                    except Exception:
                                        continue
                        # prefer distance parsing from stdout
                        if s_dist is not None:
                            nd = float(num_doors) if num_doors is not None else None
                            return [nd, float(s_dist)]
                    except Exception as e:
                        logger.debug(f"Failed to parse stdout for metrics: {e}")

            # If nothing found (for iterations and distance), log context and return Nones
            logger.debug("Unable to extract iterations and distance from simulator results. Returning Nones.")
            # Optionally print stdout/stderr snippets to help debugging
            if stdout:
                logger.debug(f"Simulator stdout snippet: {str(stdout)[:1000]}")
            if stderr:
                logger.debug(f"Simulator stderr snippet: {str(stderr)[:1000]}")
            return [None, None]

        except Exception as e:
            logger.exception(f"Exception while extracting objectives: {e}")
            return [None, None]




class NSGAIntegration:
    """
    Classe principal para integração com NSGA-II.
    
    Esta classe coordena a execução do algoritmo NSGA-II para problemas
    de otimização de evacuação.
    """
    
    def __init__(self, simulator_integration):
        """
        Inicializa a integração com NSGA-II.
        
        Args:
            simulator_integration: Instância da integração com o simulador
        """
        self.simulator_integration = simulator_integration
        self.nsga = None
        self.factory = None
        self.use_cached = False  # Flag to select between standard/cached NSGA-II
    
    def load_configuration(self, config_file: Path) -> bool:
        """
        Carrega configuração do NSGA-II a partir de arquivo.
        Suporta tanto formato legado quanto formato unificado.
        
        Args:
            config_file: Caminho para o arquivo de configuração
            
        Returns:
            True se carregou com sucesso, False caso contrário
        """
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Detecta se é formato unificado ou legado
            if 'nsga_config' in config:
                # Formato unificado
                print("DEBUG: Detectado formato unificado")
                nsga_config = config['nsga_config']
                simulation_params = config.get('simulation_params', {})
                
                # Valida configuração NSGA-II necessária
                required_keys = ['population_size', 'generations', 'crossover_rate', 'mutation_rate']
                if not all(key in nsga_config for key in required_keys):
                    print("Configuração unificada inválida: chaves NSGA-II obrigatórias ausentes")
                    return False
                
                # Armazena configurações separadamente
                self.config = nsga_config
                self.simulation_params = simulation_params
                self.is_unified_format = True
                
            else:
                # Formato legado (compatibilidade)
                print("DEBUG: Detectado formato legado")
                required_keys = ['population_size', 'generations', 'crossover_rate', 'mutation_rate']
                if not all(key in config for key in required_keys):
                    print("Configuração legada inválida: chaves obrigatórias ausentes")
                    return False
                
                self.config = config
                self.simulation_params = {}
                self.is_unified_format = False
            
            print(f"DEBUG: Configuração carregada - NSGA: {self.config}")
            print(f"DEBUG: Parâmetros de simulação: {self.simulation_params}")
            return True
            
        except Exception as e:
            print(f"Erro ao carregar configuração: {e}")
            return False
    
    def get_simulation_params(self) -> Dict:
        """
        Retorna os parâmetros de simulação carregados.
        
        Returns:
            Dicionário com parâmetros de simulação
        """
        return getattr(self, 'simulation_params', {})
    
    def is_unified_config(self) -> bool:
        """
        Verifica se a configuração carregada é do formato unificado.
        
        Returns:
            True se é formato unificado, False se é legado
        """
        return getattr(self, 'is_unified_format', False)
    
    def set_use_cached(self, use_cached: bool) -> bool:
        """
        Set whether to use cached NSGA-II or standard pymoo NSGA-II.
        
        Args:
            use_cached: True to use cached NSGA-II, False for standard
            
        Returns:
            True if the selected mode is available, False otherwise
        """
        if use_cached and not CACHED_NSGA_AVAILABLE:
            logger.warning("Cached NSGA-II requested but not available")
            return False
        
        self.use_cached = use_cached
        logger.info(f"NSGA-II mode set to: {'CACHED' if use_cached else 'STANDARD (pymoo)'}")
        return True
    
    def run_cached_nsga(
        self,
        experiment_name: str,
        draw: bool = False
    ) -> Optional[Dict]:
        """
        Run optimization using cached NSGA-II from unified folder.
        
        Args:
            experiment_name: Name of the experiment
            draw: Whether to draw simulation frames
            
        Returns:
            Results dict or None on error
        """
        if not CACHED_NSGA_AVAILABLE:
            logger.error("Cached NSGA-II not available")
            return None
        
        try:
            # Get cached NSGA integration
            cached_nsga = get_cached_nsga_integration(self.simulator_integration)
            
            # Use the same configuration
            if not hasattr(self, 'config') or not self.config:
                logger.error("Configuration not loaded")
                return None
            
            # Transfer config to cached NSGA (it reads same format)
            cached_nsga.config = self.config
            cached_nsga.simulation_params = self.get_simulation_params()
            
            # Run optimization
            logger.info("Running CACHED NSGA-II optimization...")
            result = cached_nsga.run_optimization(
                experiment_name=experiment_name,
                draw=draw
            )
            
            if result is None:
                logger.error("Cached NSGA-II optimization failed")
                return None
            
            results_list, factory = result
            
            # Return results in a format compatible with save_results
            return {
                'results': results_list,
                'factory': factory,
                'algorithm': 'NSGA-II-Cached'
            }
            
        except Exception as e:
            logger.exception(f"Error in cached NSGA-II: {e}")
            return None
    
    def extract_door_positions_from_map(self, map_template: str) -> List[tuple]:
        """
        Extrai posições das portas existentes no mapa.
        
        This method now delegates to the official integration_api module.
        Returns grouped door dictionaries (not tuples) for consistency with simulator.
        
        Args:
            map_template: Template do mapa como string
            
        Returns:
            Lista de dicionários com portas agrupadas {'row','col','size','direction'}
        """
        # OFFICIAL INTEGRATION: Delegate to the unified API (single source of truth)
        if integration_api is not None:
            try:
                doors_info = integration_api.extract_doors_from_map_text(map_template)
                print(f"DEBUG: integration_api.extract_doors_from_map_text returned {len(doors_info)} grouped doors")
                return doors_info
            except Exception as e:
                logger.error(f"Failed to call integration_api.extract_doors_from_map_text: {e}")
                # Fall through to legacy fallback
        
        # DEPRECATED FALLBACK: only used if integration_api is unavailable
        logger.warning("integration_api not available, using deprecated fallback logic")
        door_positions = []
        lines = map_template.strip().split('\n')
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == '2':
                    door_positions.append((x, y))
        
        print(f"DEBUG: Fallback found {len(door_positions)} door cells (legacy per-cell format)")
        return door_positions
    
    def setup_optimization(
        self, 
        map_template: str, 
        individuals_template: Dict,
        door_positions: List[tuple],
        initial_population: Optional[List] = None
    ) -> bool:
        """
        Configura a otimização NSGA-II com pymoo.
        
        Args:
            map_template: Template do mapa base
            individuals_template: Template dos indivíduos base
            door_positions: Lista de posições possíveis para portas
            initial_population: População inicial (opcional)
            
        Returns:
            True se configurou com sucesso, False caso contrário
        """
        try:
            print("DEBUG: Iniciando setup_optimization...")
            st.info("Iniciando setup_optimization...")
            
            # Check if pymoo modules are available
            print("DEBUG: Verificando módulos pymoo...")
            if NSGA2 is None or Problem is None or minimize is None:
                print("DEBUG: Módulos pymoo não disponíveis")
                st.error("Módulos pymoo não disponíveis")
                return False
            
            print(f"DEBUG: hasattr config: {hasattr(self, 'config')}")
            if not hasattr(self, 'config'):
                print("DEBUG: Configuração NSGA-II não carregada")
                st.error("Configuração NSGA-II não carregada")
                return False
            
            st.info(f"Configuração NSGA-II: {self.config}")
            st.info(f"Map template length: {len(map_template)}")
            st.info(f"Individuals template keys: {list(individuals_template.keys()) if isinstance(individuals_template, dict) else 'Not a dict'}")
            st.info(f"Door positions: {len(door_positions)}")
            
            print("DEBUG: Criando EvacuationProblem...")
            st.info("Criando EvacuationProblem...")
            # Cria o problema de evacuação
            self.problem = EvacuationProblem(
                self.simulator_integration, 
                map_template, 
                individuals_template,
                door_positions,
                self.get_simulation_params()
            )
            print("DEBUG: Problem criado com sucesso")
            st.success("Problem criado com sucesso")
            
            st.info("Configurando algoritmo NSGA-II...")
            # Cria o algoritmo NSGA-II
            self.algorithm = NSGA2(
                pop_size=self.config['population_size'],
                sampling=BinaryRandomSampling(),
                crossover=HalfUniformCrossover(),
                mutation=BitflipMutation(prob=self.config['mutation_rate']),
                eliminate_duplicates=True
            )
            st.success("Algoritmo NSGA-II configurado com sucesso")
            
            st.success("setup_optimization concluído com sucesso!")
            return True
            
        except Exception as e:
            import traceback
            st.error(f"Erro ao configurar otimização: {e}")
            st.text("Traceback completo:")
            st.code(traceback.format_exc())
            return False
    
    def run_optimization(self, experiment_name: Optional[str] = None) -> Optional[Dict]:
        """
        Executa a otimização NSGA-II (pymoo ou cached).
        
        Args:
            experiment_name: Nome do experimento (required for cached NSGA-II)
        
        Returns:
            Resultado da otimização, ou None em caso de erro
        """
        # Check if using cached NSGA-II
        if self.use_cached:
            logger.info("Using CACHED NSGA-II workflow")
            if not experiment_name:
                logger.error("experiment_name required for cached NSGA-II")
                return None
            
            draw_mode = self.get_simulation_params().get('draw_mode', False)
            return self.run_cached_nsga(experiment_name=experiment_name, draw=draw_mode)
        
        # Standard pymoo workflow
        logger.info("Using STANDARD (pymoo) NSGA-II workflow")
        
        if not hasattr(self, 'problem') or not hasattr(self, 'algorithm'):
            print("NSGA-II não configurado")
            return None
        
        try:
            print(f"DEBUG: Iniciando otimização pymoo...")
            print(f"  - population_size: {self.config['population_size']}")
            print(f"  - generations: {self.config['generations']}")
            print(f"  - mutation_rate: {self.config['mutation_rate']}")
            
            # Executa a otimização usando pymoo
            res = minimize(
                self.problem,
                self.algorithm,
                termination=('n_gen', self.config['generations']),
                seed=1,
                verbose=True
            )
            
            print(f"DEBUG: Otimização concluída")
            print(f"  - Soluções encontradas: {len(res.X)}")
            print(f"  - Objetivos: {len(res.F)}")
            
            return res
            
        except Exception as e:
            import traceback
            print(f"Erro na execução da otimização: {e}")
            print(f"Traceback completo: {traceback.format_exc()}")
            return None
    
    def save_results(self, result: Dict, output_file: Path) -> bool:
        """
        Salva os resultados da otimização (pymoo ou cached NSGA-II).
        
        Args:
            result: Resultado da otimização (pymoo ou cached dict)
            output_file: Arquivo de saída
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        # Check if this is cached NSGA-II results (matches "NSGA-II-Cached" or "NSGA-II-Cached-2obj" or "NSGA-II-Cached-3obj")
        if isinstance(result, dict) and 'algorithm' in result and 'NSGA-II-Cached' in result['algorithm']:
            logger.info(f"Saving cached NSGA-II results (algorithm: {result['algorithm']})...")
            
            if not CACHED_NSGA_AVAILABLE:
                logger.error("Cannot save cached results: cached NSGA not available")
                return False
            
            try:
                cached_nsga = get_cached_nsga_integration(self.simulator_integration)
                return cached_nsga.save_results(
                    results=result['results'],
                    factory=result['factory'],
                    output_file=output_file
                )
            except Exception as e:
                logger.exception(f"Error saving cached NSGA-II results: {e}")
                return False
        
        # Standard pymoo results - use existing logic
        def _to_native(o):
            """Recursively convert numpy types to native Python types for JSON serialization."""
            try:
                # numpy scalars
                import numpy as _np
                if isinstance(o, (_np.integer,)):
                    return int(o)
                if isinstance(o, (_np.floating,)):
                    return float(o)
                if isinstance(o, (_np.ndarray,)):
                    return _to_native(o.tolist())
            except Exception:
                pass

            if isinstance(o, list):
                return [_to_native(x) for x in o]
            if isinstance(o, tuple):
                return tuple(_to_native(x) for x in o)
            if isinstance(o, dict):
                return {str(k): _to_native(v) for k, v in o.items()}
            # Fallback: try to coerce numeric-like objects
            try:
                if hasattr(o, 'item'):
                    return _to_native(o.item())
                # try int/float conversions
                try:
                    return int(o)
                except Exception:
                    pass
                try:
                    return float(o)
                except Exception:
                    pass
            except Exception:
                pass
            # builtin types (int, float, str, bool, None) are fine
            return o

        try:
            results = []
            for i, (solution, objectives) in enumerate(zip(result.X, result.F)):
                # Decodifica a solução para posições de portas
                door_positions = []
                for j, bit in enumerate(solution):
                    if int(bit) == 1 and j < len(self.problem.door_positions):
                        # ensure native ints
                        dp = self.problem.door_positions[j]
                        if isinstance(dp, (list, tuple)):
                            dp = (int(dp[0]), int(dp[1]))
                        elif isinstance(dp, dict):
                            # preserve grouped-door structure but ensure native types
                            dp = {
                                'row': int(dp.get('row', 0)),
                                'col': int(dp.get('col', 0)),
                                'size': int(dp.get('size', 1)),
                                'direction': str(dp.get('direction', ''))
                            }
                        door_positions.append(dp)

                # Objectives expected to be [num_doors, distance] (2 elements)
                # Convert numpy arrays to native lists if necessary
                try:
                    obj_list = objectives.tolist()
                except Exception:
                    # if objectives is a list/tuple
                    obj_list = list(objectives)

                # Ensure the objectives array length is 2
                if len(obj_list) > 2:
                    obj_list = obj_list[:2]
                elif len(obj_list) < 2:
                    # pad missing distance with None (caller/consumer may apply penalties)
                    obj_list = obj_list + [None] * (2 - len(obj_list))

                # attempt to get auxiliary iterations value from per-eval metrics if available
                aux_iterations = None
                try:
                    # some result objects embed auxiliary info; otherwise will be filled during aggregation
                    aux_iterations = getattr(objectives, 'iterations', None)
                except Exception:
                    aux_iterations = None

                # If no auxiliary iterations found on the objectives object, try reading
                # the per-eval metrics file produced by the simulator for this evaluation.
                # The simulator writes metrics to simulador_heuristica/output/nsga_eval_<id>/metrics.json
                if aux_iterations is None:
                    try:
                        base_output = Path(self.simulator_integration.output_path)
                        eval_dir = base_output / f'nsga_eval_{i}'
                        metrics_file = eval_dir / 'metrics.json'
                        if metrics_file.exists():
                            try:
                                md = json.loads(metrics_file.read_text())
                                aux_iterations = md.get('iterations') or md.get('qtd_iteracoes') or md.get('iters') or md.get('tempo_total')
                            except Exception:
                                aux_iterations = None
                    except Exception:
                        aux_iterations = None

                # Build expanded per-cell door coordinates from grouped/tuple representations.
                # OFFICIAL INTEGRATION: Use integration_api.expand_grouped_doors
                expanded_positions = []
                if integration_api is not None:
                    try:
                        expanded_positions = integration_api.expand_grouped_doors(door_positions)
                    except Exception as e:
                        logger.error(f"Failed to call integration_api.expand_grouped_doors: {e}")
                        # Fall through to manual expansion
                
                # DEPRECATED FALLBACK: manual expansion logic
                if not expanded_positions:
                    try:
                        for dp in door_positions:
                            if isinstance(dp, (list, tuple)):
                                # dp is (x,y)
                                expanded_positions.append([int(dp[0]), int(dp[1])])
                            elif isinstance(dp, dict):
                                # grouped door: expand according to direction and size
                                r = int(dp.get('row', 0))
                                c = int(dp.get('col', 0))
                                size = int(dp.get('size', 1))
                                direction = str(dp.get('direction', ''))
                                if direction == 'H':
                                    for offset in range(size if size>0 else 1):
                                        expanded_positions.append([c + offset, r])
                                elif direction == 'V':
                                    for offset in range(size if size>0 else 1):
                                        expanded_positions.append([c, r + offset])
                                else:
                                    # fallback: single cell
                                    expanded_positions.append([c, r])
                            else:
                                # unknown type, attempt to coerce
                                try:
                                    x, y = dp
                                    expanded_positions.append([int(x), int(y)])
                                except Exception:
                                    continue
                    except Exception:
                        expanded_positions = []

                # Preserve the original/grouped descriptor under a separate key,
                # but keep `door_positions` as the expanded per-cell coordinates
                # because downstream UI (pages/Resultados.py) expects a list of [x,y].
                res_obj = {
                    "solution_id": int(i),
                    "gene": _to_native(solution.tolist()),
                    # Provide expanded per-cell positions as the primary key for compatibility
                    "door_positions": _to_native(expanded_positions),
                    # Keep grouped/native representation for traceability
                    "door_positions_grouped": _to_native(door_positions),
                    "objectives": _to_native(obj_list),
                    "num_doors": int(int(sum(solution))),
                    "iterations": int(aux_iterations) if aux_iterations is not None else None
                }
                results.append(res_obj)

            # Atomic write: write to temp file then replace
            tmp_path = output_file.with_suffix('.tmp')
            try:
                with open(tmp_path, 'w') as f:
                    json.dump(results, f, indent=2)
                # replace atomically
                tmp_path.replace(output_file)
            finally:
                if tmp_path.exists():
                    try:
                        tmp_path.unlink()
                    except Exception:
                        pass

            # Aggregate per-eval metrics into consolidated metrics.json for the main experiment
            try:
                # Attempt to infer simulation_name from output_file name: results_<simname>_timestamp.json
                sim_name = None
                parts = output_file.stem.split('_')
                if len(parts) >= 2 and parts[0] == 'results':
                    sim_name = parts[1]
                if sim_name:
                    base_output = Path(self.simulator_integration.output_path)
                    consolidated_dir = base_output / sim_name
                    consolidated_dir.mkdir(parents=True, exist_ok=True)

                    # Collect any metrics.json files under the simulator output tree (recursive)
                    evals = []
                    for metrics_file in sorted(base_output.rglob('metrics.json')):
                        try:
                            # ignore consolidated per-simulation metrics.json (those live under base_output/<sim_name>/metrics.json)
                            # but accept any per-eval metrics.json produced by simulator runs
                            data = json.loads(metrics_file.read_text())
                            d = data.get('distancia_total') or data.get('total_distance') or data.get('distance') or data.get('qtdDistance')
                            it = (
                                data.get('iterations') or
                                data.get('tempo_total') or
                                data.get('total_time') or
                                data.get('qtd_iteracoes') or
                                data.get('iters')
                            )
                            nd = data.get('num_doors') or data.get('qtd_doors') or None
                            evals.append({
                                'eval': metrics_file.parent.name,
                                'path': str(metrics_file),
                                'distancia_total': float(d) if d is not None else None,
                                'num_doors': int(nd) if nd is not None else None,
                                'iterations': int(it) if it is not None else None
                            })
                        except Exception as e:
                            logger.debug(f"failed to read/parse {metrics_file}: {e}")

                    consolidated = {
                        'algorithm': 'NSGA-II',
                        'simulation_name': sim_name,
                        'num_evals': len(evals),
                        'evaluations': evals
                    }
                    consolidated_path = consolidated_dir / 'metrics.json'
                    # atomic write
                    tmp_c = consolidated_path.with_suffix('.tmp')
                    with open(tmp_c, 'w') as f:
                        json.dump(consolidated, f, indent=2)
                    tmp_c.replace(consolidated_path)

                    # Backfill iterations into the per-solution results file by matching evaluations
                    try:
                        # load previously written results file (output_file)
                        if output_file.exists():
                            try:
                                raw_results = json.loads(output_file.read_text())
                            except Exception:
                                raw_results = results
                        else:
                            raw_results = results

                        # Helper to extract numeric distance from eval entry
                        def _eval_distance(e):
                            for k in ('distancia_total','distancia','distance','dist'):
                                if k in e and e.get(k) is not None:
                                    try:
                                        return float(e.get(k))
                                    except Exception:
                                        try:
                                            return float(str(e.get(k)).replace(',','.'))
                                        except Exception:
                                            return None
                            return None

                        # Try to match each saved result to an evaluation and set iterations when found
                        for r in raw_results:
                            if r.get('iterations') is None:
                                r_num = r.get('num_doors')
                                r_dist = None
                                try:
                                    if isinstance(r.get('objectives'), (list,tuple)) and len(r.get('objectives')) >= 2:
                                        r_dist = float(r.get('objectives')[1])
                                except Exception:
                                    r_dist = None

                                matched_iter = None
                                for e in evals:
                                    try:
                                        ev_num = e.get('num_doors')
                                        ev_dist = _eval_distance(e)
                                        if ev_num is not None and r_num is not None and int(ev_num) == int(r_num):
                                            # If both distances available, require approximate match; otherwise accept num match
                                            if r_dist is not None and ev_dist is not None:
                                                try:
                                                    if abs(float(ev_dist) - float(r_dist)) <= max(1e-6, 0.001 * abs(float(r_dist))):
                                                        matched_iter = e.get('iterations') or e.get('qtd_iteracoes') or e.get('iters') or e.get('tempo_total')
                                                        break
                                                except Exception:
                                                    continue
                                            else:
                                                matched_iter = e.get('iterations') or e.get('qtd_iteracoes') or e.get('iters') or e.get('tempo_total')
                                                break
                                    except Exception:
                                        continue

                                if matched_iter is not None:
                                    try:
                                        # coerce to int if possible
                                        r['iterations'] = int(matched_iter)
                                    except Exception:
                                        r['iterations'] = matched_iter

                        # rewrite updated results atomically
                        tmp_r = output_file.with_suffix('.tmp')
                        with open(tmp_r, 'w') as f:
                            json.dump(raw_results, f, indent=2)
                        tmp_r.replace(output_file)
                    except Exception as e:
                        logger.debug(f"failed to backfill iterations into results file: {e}")

            except Exception as e:
                print(f"DEBUG: failed to aggregate per-eval metrics: {e}")

            return True

        except Exception as e:
            print(f"Erro ao salvar resultados: {e}")
            import traceback
            print(traceback.format_exc())
            return False
