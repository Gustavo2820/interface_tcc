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

# Import the unified integration API (single source of truth for simulator logic)
try:
    from simulador_heuristica.simulator import integration_api
except ImportError as e:
    logger.warning(f"Could not import integration_api: {e}")
    integration_api = None

# Import cached NSGA-II integration (optional)
try:
    from .nsga_cached_integration import get_cached_nsga_integration
    CACHED_NSGA_AVAILABLE = True
except ImportError as e:
    logger.debug(f"Cached NSGA-II not available: {e}")
    get_cached_nsga_integration = None
    CACHED_NSGA_AVAILABLE = False

try:
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.core.problem import Problem
    from pymoo.core.callback import Callback
    from pymoo.optimize import minimize
    from pymoo.operators.sampling.rnd import BinaryRandomSampling
    from pymoo.operators.crossover.hux import HalfUniformCrossover
    from pymoo.operators.mutation.bitflip import BitflipMutation
    st.success("✓ Algoritmo NSGA-II carregado com sucesso")
except ImportError as e:
    logger.error(f"Erro ao importar módulos do pymoo: {e}")
    st.error(f"⚠ Erro ao carregar NSGA-II: {e}")
    # Fallback para quando os módulos não estão disponíveis
    NSGA2 = None
    Problem = None
    minimize = None
    BinaryRandomSampling = None
    HalfUniformCrossover = None
    BitflipMutation = None
except Exception as e:
    logger.exception(f"Erro inesperado ao importar módulos: {e}")
    st.error(f"⚠ Erro inesperado ao carregar NSGA-II: {e}")
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


class StreamlitProgressCallback(Callback):
    """
    Callback do pymoo para atualizar barra de progresso no Streamlit.
    
    Monitora o progresso da otimização NSGA-II e atualiza a interface
    do Streamlit com informações sobre a geração atual.
    """
    
    def __init__(self, max_generations: int, progress_bar, status_text):
        """
        Inicializa o callback.
        
        Args:
            max_generations: Número total de gerações
            progress_bar: Componente st.progress já criado
            status_text: Componente st.empty já criado
        """
        super().__init__()
        self.max_generations = max_generations
        self.progress_bar = progress_bar
        self.status_text = status_text
    
    def notify(self, algorithm):
        """
        Chamado a cada geração pela otimização do pymoo.
        
        Args:
            algorithm: Instância do algoritmo NSGA-II
        """
        try:
            current_gen = algorithm.n_gen
            progress = current_gen / self.max_generations
            
            # Atualiza barra de progresso
            self.progress_bar.progress(min(progress, 1.0))
            
            # Atualiza texto de status
            pop_size = len(algorithm.pop) if hasattr(algorithm, 'pop') and algorithm.pop is not None else 0
            self.status_text.text(
                f"Geração {current_gen}/{self.max_generations} "
                f"({progress*100:.1f}%) - População: {pop_size}"
            )
        except Exception as e:
            # Silenciosamente ignora erros de UI para não interromper a otimização
            logger.debug(f"Erro ao atualizar progresso: {e}")


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
        # Define um problema com 3 objetivos e n variáveis binárias (uma para cada posição de porta)
        # Objetivos: [num_doors, iterations, distance] (alinhado com z_experiment1_audition.py)
        # initialize base Problem now that self.door_positions is set
        n_var = len(self.door_positions)
        super().__init__(n_var=n_var, n_obj=3, n_constr=0, xl=0, xu=1, type_var=bool)
    
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
            results = np.full((len(x), 3), 1e6, dtype=float)

        # Normalize shape to (pop_size, 3)
        if results.ndim == 1 and results.size == 3:
            results = np.tile(results, (len(x), 1))
        elif results.ndim == 1 and results.size != 3:
            # Unexpected shape, set penalties
            logger.debug(f"Unexpected evaluation shape {results.shape}, applying penalties")
            results = np.full((len(x), 3), 1e6, dtype=float)
        elif results.ndim == 2 and results.shape[1] != 3:
            # If more/less objectives returned, try to truncate or pad
            logger.debug(f"Evaluation returned {results.shape[1]} objectives per individual; adjusting to 3")
            if results.shape[1] > 3:
                results = results[:, :3]
            else:
                # pad with penalty
                pad = np.full((results.shape[0], 3 - results.shape[1]), 1e6, dtype=float)
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
        
        # CRITICAL: Penalize solutions with zero doors (invalid/nonsensical)
        # Zero doors means no evacuation paths, leading to artificially low distance (0)
        # which pollutes the Pareto front with invalid solutions.
        if not door_positions or len(door_positions) == 0:
            logger.warning("Gene selected 0 doors - applying heavy penalty to prevent invalid Pareto solutions")
            # Return maximum penalty for all objectives
            # Use a recognizable large value that clearly marks this as invalid
            return [0.0, 1e6, 1e6]

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
            max_iterations = self.simulation_params.get('max_iterations')

            # NOTA: NSGA-II usa apenas um scenario_seed por avaliação (não faz média de múltiplos seeds)
            # Se scenario_seed for uma lista, usamos apenas o primeiro valor
            # A estratégia de múltiplos seeds é mais apropriada para algoritmos que fazem média interna
            if isinstance(scenario_seed, list):
                scenario_seed_value = scenario_seed[0] if scenario_seed else 0
            else:
                scenario_seed_value = scenario_seed

            # Execute simulator CLI and capture output for debugging
            proc = self.simulator_integration.run_simulator_cli(
                experiment_name,
                draw=draw_mode,
                scenario_seed=scenario_seed_value,
                simulation_seed=simulation_seed,
                max_iterations=max_iterations
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
                return [1e6, 1e6, 1e6]

            # num_doors should reflect number of selected door *configurations* (grouped doors)
            # If door_positions contains door dicts (from extract_doors_info), count them; otherwise count tuples
            if door_positions and isinstance(door_positions[0], dict):
                num_doors = len(door_positions)
            else:
                num_doors = len(door_positions)

            # Extract numeric objectives [num_doors, iterations, distance] from results
            obj = self._extract_objectives(results, stdout=stdout, stderr=stderr, num_doors=num_doors)

            # _extract_objectives returns [num_doors, iterations, distance]
            try:
                num_doors_val = float(obj[0]) if obj and obj[0] is not None else float(num_doors)
            except Exception:
                num_doors_val = float(num_doors)
            try:
                iterations_val = float(obj[1]) if obj and len(obj) > 1 and obj[1] is not None else None
            except Exception:
                iterations_val = None
            try:
                distance_val = float(obj[2]) if obj and len(obj) > 2 and obj[2] is not None else None
            except Exception:
                distance_val = None

            # Penalize missing metrics
            if iterations_val is None or not np.isfinite(iterations_val):
                logger.warning("Missing or non-finite iterations for %s, applying penalty", experiment_name)
                iterations_val = 1e6
            if distance_val is None or not np.isfinite(distance_val):
                logger.warning("Missing or non-finite distance for %s, applying penalty", experiment_name)
                distance_val = 1e6

            # Return objectives as floats: [num_doors, iterations, distance]
            return [float(num_doors_val), float(iterations_val), float(distance_val)]

        except Exception as e:
            logger.exception("Exception during evaluation of experiment %s", experiment_name)
            return [1e6, 1e6, 1e6]

        finally:
            # Clean up temporary staging directory
            import shutil
            try:
                if temp_dir.exists():
                    shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception as e:
                logger.debug(f"Failed to remove temp_dir {temp_dir}: {e}")

    
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
        
        Procura por:
        - 'iterations' / 'tempo_total' / 'qtd_iteracoes' -> iterations objective
        - 'distance' / 'distancia' / 'qtdDistance' / 'distancia_total' -> distance objective

        Retorna uma lista com três elementos: [num_doors, iterations, distance].
        num_doors pode ser fornecido pelo chamador (a partir do gene).
        """
        try:
            # Fast path: results already contain metrics at top level
            if isinstance(results, dict):
                # Try to find iterations and distance at top level
                iterations_keys = ['iterations', 'tempo_total', 'qtd_iteracoes', 'iters', 'total_time']
                distance_keys = ['distance', 'avg_distance', 'qtdDistance', 'qtd_distancia', 'qtd_distance', 'distancia', 'total_distance', 'distancia_total']
                
                i_key = next((k for k in iterations_keys if k in results), None)
                d_key = next((k for k in distance_keys if k in results), None)
                
                i_val = None
                d_val = None
                
                if i_key:
                    try:
                        i_val = float(results[i_key])
                    except Exception:
                        i_val = None
                
                if d_key:
                    try:
                        d_val = float(results[d_key])
                    except Exception:
                        d_val = None
                
                # If we found both at top level, return early
                if i_val is not None and d_val is not None:
                    nd = float(num_doors) if num_doors is not None else None
                    return [nd, i_val, d_val]

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
                        
                        # Try to find iterations
                        i_key = next((k for k in ('iterations','tempo_total','qtd_iteracoes','iters','total_time') if k in data), None)
                        i_val = None
                        if i_key:
                            try:
                                i_val = float(data[i_key])
                            except Exception:
                                i_val = None
                        
                        # Try to find distance
                        d_key = next((k for k in ('distance','avg_distance','qtdDistance','qtd_distancia','qtd_distance','distancia','total_distance','distancia_total') if k in data), None)
                        d_val = None
                        if d_key:
                            try:
                                d_val = float(data[d_key])
                            except Exception:
                                d_val = None
                        
                        # If both found, return
                        if i_val is not None and d_val is not None:
                            nd = float(num_doors) if num_doors is not None else None
                            return [nd, i_val, d_val]
                        
                        # Also check under a nested 'metrics' object
                        if 'metrics' in data and isinstance(data['metrics'], dict):
                            if i_val is None:
                                i_key = next((k for k in ('iterations','tempo_total','qtd_iteracoes','iters','total_time') if k in data['metrics']), None)
                                if i_key:
                                    try:
                                        i_val = float(data['metrics'][i_key])
                                    except Exception:
                                        i_val = None
                            
                            if d_val is None:
                                d_key = next((k for k in ('distance','avg_distance','qtdDistance','qtd_distancia','qtd_distance','distancia','total_distance','distancia_total') if k in data['metrics']), None)
                                if d_key:
                                    try:
                                        d_val = float(data['metrics'][d_key])
                                    except Exception:
                                        d_val = None
                            
                            if i_val is not None and d_val is not None:
                                nd = float(num_doors) if num_doors is not None else None
                                return [nd, i_val, d_val]
                    except Exception as e:
                        logger.debug(f"Failed to parse metrics candidate {candidate}: {e}")

                # If nothing found in metrics files, try parsing raw stdout/stderr
                if stdout:
                    try:
                        s_iters = None
                        s_dist = None
                        for line in str(stdout).splitlines():
                            line_lower = line.strip().lower()
                            # Look for iterations/tempo lines
                            if any(tok in line_lower for tok in ('tempo','time','iteracoes','iterations','iters')):
                                parts = line.replace(',', '.').split()
                                for p in reversed(parts):
                                    try:
                                        s_iters = float(p)
                                        break
                                    except Exception:
                                        continue
                            # Look for distance lines
                            if any(tok in line_lower for tok in ('dist','distância','distance','qtd')):
                                parts = line.replace(',', '.').split()
                                for p in reversed(parts):
                                    try:
                                        s_dist = float(p)
                                        break
                                    except Exception:
                                        continue
                        
                        if s_iters is not None and s_dist is not None:
                            nd = float(num_doors) if num_doors is not None else None
                            return [nd, float(s_iters), float(s_dist)]
                    except Exception as e:
                        logger.debug(f"Failed to parse stdout for metrics: {e}")

            # If nothing found (for iterations and distance), log context and return Nones
            logger.debug("Unable to extract iterations and distance from simulator results. Returning Nones.")
            # Optionally print stdout/stderr snippets to help debugging
            if stdout:
                logger.debug(f"Simulator stdout snippet: {str(stdout)[:1000]}")
            if stderr:
                logger.debug(f"Simulator stderr snippet: {str(stderr)[:1000]}")
            nd = float(num_doors) if num_doors is not None else None
            return [nd, None, None]

        except Exception as e:
            logger.exception(f"Exception while extracting objectives: {e}")
            nd = float(num_doors) if num_doors is not None else None
            return [nd, None, None]




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
                nsga_config = config['nsga_config']
                simulation_params = config.get('simulation_params', {})
                
                # Valida configuração NSGA-II necessária
                required_keys = ['population_size', 'generations', 'crossover_rate', 'mutation_rate']
                if not all(key in nsga_config for key in required_keys):
                    logger.error("Unified config missing required NSGA-II keys")
                    st.error("⚠ Configuração incompleta")
                    return False
                
                # Armazena configurações separadamente
                self.config = nsga_config
                self.simulation_params = simulation_params
                self.is_unified_format = True
                
            else:
                # Formato legado (compatibilidade)
                required_keys = ['population_size', 'generations', 'crossover_rate', 'mutation_rate']
                if not all(key in config for key in required_keys):
                    logger.error("Legacy config missing required keys")
                    st.error("⚠ Configuração incompleta")
                    return False
                
                self.config = config
                self.simulation_params = {}
                self.is_unified_format = False
            
            logger.info(f"✓ Configuração carregada: pop={self.config['population_size']}, gen={self.config['generations']}")
            return True
            
        except Exception as e:
            logger.exception(f"Error loading configuration: {e}")
            st.error(f"⚠ Erro ao carregar configuração: {e}")
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
            
            logger.info(f"DEBUG: Config transferred: {cached_nsga.config}")
            logger.info(f"DEBUG: Simulation params: {cached_nsga.simulation_params}")
            print(f"[NSGA-INTEGRATION] Config transferred: {cached_nsga.config}")
            print(f"[NSGA-INTEGRATION] Simulation params: {cached_nsga.simulation_params}")
            
            # Run optimization
            logger.info("Running CACHED NSGA-II optimization...")
            print("[NSGA-INTEGRATION] Calling cached_nsga.run_optimization...")
            result = cached_nsga.run_optimization(
                experiment_name=experiment_name,
                draw=draw
            )
            
            logger.info(f"DEBUG: result type: {type(result)}")
            logger.info(f"DEBUG: result value: {result}")
            print(f"[NSGA-INTEGRATION] Result type: {type(result)}")
            print(f"[NSGA-INTEGRATION] Result is None: {result is None}")
            
            if result is None:
                logger.error("Cached NSGA-II optimization failed - returned None")
                print("[NSGA-INTEGRATION] ERROR: Result is None!")
                return None
            
            try:
                results_list, factory = result
                logger.info(f"DEBUG: Unpacked successfully - results_list has {len(results_list) if results_list else 0} items")
                print(f"[NSGA-INTEGRATION] Unpacked: {len(results_list) if results_list else 0} results")
            except Exception as unpack_error:
                logger.error(f"Failed to unpack result: {unpack_error}")
                logger.error(f"Result was: {result}")
                print(f"[NSGA-INTEGRATION] ERROR unpacking: {unpack_error}")
                return None
            
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
                logger.debug(f"Extracted {len(doors_info)} grouped doors from map")
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
        
        logger.debug(f"Fallback found {len(door_positions)} door cells (legacy per-cell format)")
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
            # Check if pymoo modules are available
            if NSGA2 is None or Problem is None or minimize is None:
                st.error("⚠ Módulos de otimização não disponíveis")
                logger.error("Pymoo modules not available")
                return False
            
            if not hasattr(self, 'config'):
                st.error("⚠ Configuração não carregada")
                logger.error("NSGA-II configuration not loaded")
                return False
            
            # Cria o problema de evacuação
            self.problem = EvacuationProblem(
                self.simulator_integration, 
                map_template, 
                individuals_template,
                door_positions,
                self.get_simulation_params()
            )
            
            # Cria o algoritmo NSGA-II
            self.algorithm = NSGA2(
                pop_size=self.config['population_size'],
                sampling=BinaryRandomSampling(),
                crossover=HalfUniformCrossover(),
                mutation=BitflipMutation(prob=self.config['mutation_rate']),
                eliminate_duplicates=True
            )
            
            logger.info(f"NSGA-II configurado: pop={self.config['population_size']}, gen={self.config['generations']}")
            return True
            
        except Exception as e:
            st.error(f"⚠ Erro ao configurar otimização: {e}")
            logger.exception(f"Error in setup_optimization: {e}")
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
            st.error("⚠ NSGA-II não configurado corretamente")
            logger.error("NSGA-II not properly configured")
            return None
        
        try:
            # Cria componentes de progresso
            progress_bar = st.progress(0.0)
            status_text = st.empty()
            
            # Cria callback para atualizar progresso no Streamlit
            progress_callback = StreamlitProgressCallback(
                self.config['generations'],
                progress_bar,
                status_text
            )
            
            # Executa a otimização usando pymoo
            res = minimize(
                self.problem,
                self.algorithm,
                termination=('n_gen', self.config['generations']),
                seed=1,
                callback=progress_callback,
                verbose=False
            )
            
            # Limpa a barra de progresso ao finalizar
            progress_bar.empty()
            status_text.empty()
            
            logger.info(f"Otimização concluída: {len(res.X)} soluções encontradas")
            return res
            
        except Exception as e:
            logger.exception(f"Erro na execução da otimização: {e}")
            st.error(f"⚠ Erro durante a otimização: {e}")
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

                # Objectives expected to be [num_doors, iterations, distance] (3 elements)
                # Convert numpy arrays to native lists if necessary
                try:
                    obj_list = objectives.tolist()
                except Exception:
                    # if objectives is a list/tuple
                    obj_list = list(objectives)

                # Ensure the objectives array length is 3
                if len(obj_list) > 3:
                    obj_list = obj_list[:3]
                elif len(obj_list) < 3:
                    # Pad with None if we somehow got fewer objectives
                    obj_list = obj_list + [None] * (3 - len(obj_list))

                # Extract num_doors, iterations, distance from the 3-objective array
                num_doors = obj_list[0]
                iterations = obj_list[1]
                distance = obj_list[2]
                
                # POST-PARETO FILTER: Remove invalid solutions
                if num_doors is not None and int(num_doors) == 0:
                    logger.debug(f"Filtering out 0-door solution {i} from Pareto front")
                    continue
                
                # Filter out solutions with invalid distance (0 or negative)
                if distance is not None and float(distance) <= 0:
                    logger.debug(f"Filtering out solution {i} with invalid distance={distance} from Pareto front")
                    continue
                
                # Filter out solutions with suspicious iterations (0 when there are doors)
                if iterations is not None and num_doors is not None:
                    if float(iterations) == 0 and int(num_doors) > 0:
                        logger.debug(f"Filtering out solution {i} with suspicious iterations=0 and doors={num_doors}")
                        continue

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
                    "iterations": int(iterations) if iterations is not None else None,
                    "distance": float(distance) if distance is not None else None
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
                logger.debug(f"failed to aggregate per-eval metrics: {e}")

            return True

        except Exception as e:
            logger.exception(f"Error saving results: {e}")
            st.error(f"⚠ Erro ao salvar resultados: {e}")
            import traceback
            print(traceback.format_exc())
            return False
