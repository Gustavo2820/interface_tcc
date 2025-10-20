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
        n_var = len(door_positions)
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
        except Exception as e:
            logger.exception("Failed to convert evaluation results to array")
            # do not invent values; fail safe by assigning large penalty but log as ERROR
            results = np.full((len(x), 2), 1e6, dtype=float)

        # Normalize shape to (pop_size, 2)
        if results.ndim == 1 and results.size == 2:
            results = np.tile(results, (len(x), 1))
        elif results.ndim == 1 and results.size != 2:
            # Unexpected shape, set penalties
            print(f"DEBUG: Unexpected evaluation shape {results.shape}, applying penalties")
            results = np.full((len(x), 2), 1e6, dtype=float)
        elif results.ndim == 2 and results.shape[1] != 2:
            # If more/less objectives returned, try to truncate or pad
            print(f"DEBUG: Evaluation returned {results.shape[1]} objectives per individual; adjusting to 2")
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
            if results[i, 0] == results[i, 1]:
                results[i, 1] = results[i, 1] + 1e-6

        out["F"] = results
    
     
    def _evaluate_single(self, gene):
        """
        Avalia uma única solução.
        
        Args:
            gene: Vetor binário representando quais portas usar
            
        Returns:
            Lista com os valores dos objetivos
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

            # Extract numeric objectives safely
            objectives = self._extract_objectives(results, stdout=stdout, stderr=stderr)

            # Validate extracted objectives strictly
            try:
                t0 = float(objectives[0])
                d0 = float(objectives[1])
            except Exception:
                logger.exception("Invalid objectives extracted for %s: %s", experiment_name, objectives)
                # Return penalty but avoid inventing values
                return [1e6, 1e6]

            if not np.isfinite(t0) or not np.isfinite(d0):
                logger.error("Non-finite objectives for %s: %s", experiment_name, (t0, d0))
                return [1e6, 1e6]

            # keep values as-is (do not invent or perturb)
            return [t0, d0]

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
        door_positions = []
        for i, bit in enumerate(gene):
            if bit == 1 and i < len(self.door_positions):
                door_positions.append(self.door_positions[i])
        return door_positions
    
    def _generate_map_with_doors(self, door_positions: List[tuple]) -> str:
        """
        Gera o conteúdo do mapa com as portas posicionadas.
        
        Args:
            door_positions: Lista de posições das portas a serem ativadas
            
        Returns:
            Conteúdo do mapa como string
        """
        lines = self.map_template.split('\n')
        
        # Primeiro, desativa todas as portas existentes (converte '2' para '0')
        for y, line in enumerate(lines):
            lines[y] = line.replace('2', '0')
        
        # Depois, ativa apenas as portas selecionadas (converte '0' para '2' nas posições escolhidas)
        for x, y in door_positions:
            if 0 <= y < len(lines) and 0 <= x < len(lines[y]):
                line = list(lines[y])
                line[x] = '2'  # 2 representa porta ativa no formato do simulador
                lines[y] = ''.join(line)
        
        return '\n'.join(lines)
    
    def _extract_objectives(self, results: Dict, stdout: Optional[str] = None, stderr: Optional[str] = None) -> List[float]:
        """
        Extrai as métricas de interesse a partir do dicionário retornado por `read_results`.

        Aceita diferentes formatos de `results`:
        - Um dicionário contendo chaves 'tempo_total' e 'distancia_total'.
        - Um dicionário onde 'metrics' é uma lista de caminhos de arquivos JSON/TXT que contém as métricas.
        - Um dicionário com 'directory' apontando para a pasta de saída (procura por metrics*.json).

        Retorna uma lista com dois floats: [tempo_total, distancia_total]. Em caso de falha,
        retorna penalidades controladas [1e6, 1e6].
        """
        try:
            # Fast path: results already contain metrics
            if isinstance(results, dict):
                # If metrics already present as top-level numeric keys
                if 'tempo_total' in results and 'distancia_total' in results:
                    return [float(results['tempo_total']), float(results['distancia_total'])]
                # Fallbacks for alternative names produced by GUI or simulator
                if 'iterations' in results and 'distance' in results:
                    return [float(results['iterations']), float(results['distance'])]
                if 'iterations' in results and 'distancia_total' in results:
                    return [float(results['iterations']), float(results['distancia_total'])]
                if 'tempo_total' in results and 'distance' in results:
                    return [float(results['tempo_total']), float(results['distance'])]

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

                # Try to parse candidate files
                for candidate in metrics_candidates:
                    try:
                        candidate_path = Path(candidate)
                        if not candidate_path.exists():
                            # candidate may already be a Path-like object
                            continue
                        with open(candidate_path, 'r') as fh:
                            data = json.load(fh)
                        # Accept nested structures: try common key names
                        for t_key in ('tempo_total', 'total_time', 'time_total'):
                            for d_key in ('distancia_total', 'total_distance', 'distance_total'):
                                if t_key in data and d_key in data:
                                    return [float(data[t_key]), float(data[d_key])]
                                # also check under a 'metrics' object
                                if 'metrics' in data and isinstance(data['metrics'], dict) and t_key in data['metrics'] and d_key in data['metrics']:
                                    return [float(data['metrics'][t_key]), float(data['metrics'][d_key])]
                    except Exception as e:
                        print(f"DEBUG: Failed to parse metrics candidate {candidate}: {e}")

                # If nothing found in metrics files, try parsing raw stdout/stderr for printed metrics
                if stdout:
                    try:
                        s_iters = None
                        s_dist = None
                        for line in str(stdout).splitlines():
                            line = line.strip()
                            if line.startswith('qtd iteracoes'):
                                try:
                                    s_iters = int(line.split()[-1])
                                except Exception:
                                    pass
                            if line.startswith('qtd distancia'):
                                try:
                                    s_dist = float(line.split()[-1])
                                except Exception:
                                    pass
                        if s_iters is not None and s_dist is not None:
                            return [float(s_iters), float(s_dist)]
                    except Exception as e:
                        print(f"DEBUG: Failed to parse stdout for metrics: {e}")

            # If nothing found, log context and return penalties
            print("DEBUG: Unable to extract tempo_total and distancia_total from simulator results. Returning penalties.")
            # Optionally print stdout/stderr snippets to help debugging
            if stdout:
                print(f"DEBUG: Simulator stdout snippet: {str(stdout)[:1000]}")
            if stderr:
                print(f"DEBUG: Simulator stderr snippet: {str(stderr)[:1000]}")
            return [1e6, 1e6]

        except Exception as e:
            print(f"ERROR: Exception while extracting objectives: {e}")
            import traceback
            print(traceback.format_exc())
            return [1e6, 1e6]




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
    
    def extract_door_positions_from_map(self, map_template: str) -> List[tuple]:
        """
        Extrai posições das portas existentes no mapa.
        
        Args:
            map_template: Template do mapa como string
            
        Returns:
            Lista de tuplas (x, y) com posições das portas existentes
        """
        door_positions = []
        lines = map_template.strip().split('\n')
        
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                # Procura por portas existentes (valor 2 = M_DOOR)
                if char == '2':
                    door_positions.append((x, y))
        
        print(f"DEBUG: Encontradas {len(door_positions)} portas existentes no mapa")
        if door_positions:
            print(f"DEBUG: Posições das portas: {door_positions}")
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
    
    def run_optimization(self) -> Optional[Dict]:
        """
        Executa a otimização NSGA-II com pymoo.
        
        Returns:
            Resultado da otimização do pymoo, ou None em caso de erro
        """
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
        Salva os resultados da otimização pymoo.
        
        Args:
            result: Resultado da otimização do pymoo
            output_file: Arquivo de saída
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
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
                        door_positions.append(dp)

                res_obj = {
                    "solution_id": int(i),
                    "gene": _to_native(solution.tolist()),
                    "door_positions": _to_native(door_positions),
                    "objectives": _to_native(objectives.tolist()),
                    "num_doors": int(int(sum(solution)))
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

                    # Collect nsga_eval_* subdirs
                    evals = []
                    eval_base = base_output
                    for p in sorted(eval_base.glob('nsga_eval_*')):
                        metrics_file = p / 'metrics.json'
                        if metrics_file.exists():
                            try:
                                data = json.loads(metrics_file.read_text())
                                # normalize keys and types
                                t = data.get('tempo_total') or data.get('iterations') or data.get('qtd_iteracoes')
                                d = data.get('distancia_total') or data.get('distance') or data.get('qtd_distancia')
                                evals.append({
                                    'eval': p.name,
                                    'tempo_total': float(t) if t is not None else None,
                                    'distancia_total': float(d) if d is not None else None,
                                })
                            except Exception as e:
                                print(f"DEBUG: failed to read/parse {metrics_file}: {e}")

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

            except Exception as e:
                print(f"DEBUG: failed to aggregate per-eval metrics: {e}")

            return True

        except Exception as e:
            print(f"Erro ao salvar resultados: {e}")
            import traceback
            print(traceback.format_exc())
            return False
