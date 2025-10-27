"""
Módulo de integração com algoritmo Brute Force.

Este módulo implementa a integração específica para o algoritmo de Força Bruta,
permitindo a enumeração completa do espaço de busca para problemas pequenos
de otimização de evacuação.

IMPORTANTE: Brute Force é viável apenas para problemas pequenos (≤15 portas)
devido à explosão combinatória (2^n combinações).
"""
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import streamlit as st
from .logger import default_log as logger

# Adiciona o caminho do simulador ao sys.path
project_root = Path(__file__).resolve().parents[2]
unified_path = project_root / "simulador_heuristica" / "unified"
simulator_path = project_root / "simulador_heuristica" / "simulator"

if str(unified_path) not in sys.path:
    sys.path.insert(0, str(unified_path))
if str(simulator_path) not in sys.path:
    sys.path.insert(0, str(simulator_path))

# Import necessários da pasta unified
try:
    from mh_ga_instance import Instance
    from h_brute_force import BruteForce as BruteForceAlgorithm
    logger.info("Successfully imported Brute Force from unified folder")
    BRUTEFORCE_AVAILABLE = True
except ImportError as e:
    logger.error(f"Failed to import Brute Force: {e}")
    BruteForceAlgorithm = None
    Instance = None
    BRUTEFORCE_AVAILABLE = False

# Import integration_api for door extraction (from simulator folder)
try:
    import integration_api
    logger.info("Successfully imported integration_api")
except ImportError as e:
    logger.warning(f"integration_api not available: {e}")
    integration_api = None


class BruteForceIntegration:
    """
    Classe de integração para o algoritmo Brute Force.
    
    Esta classe adapta o algoritmo de Força Bruta da pasta unified
    para trabalhar com a interface e formatos padronizados.
    """
    
    def __init__(self, simulator_integration):
        """
        Inicializa a integração com Brute Force.
        
        Args:
            simulator_integration: Instância da integração com o simulador
        """
        self.simulator_integration = simulator_integration
        self.config = {
            'max_doors': 15,  # Limite de segurança para evitar explosão combinatória
            'algorithm': 'BruteForce'
        }
        self.simulation_params = {}
    
    def load_configuration(self, config_file: Path = None) -> bool:
        """
        Carrega configuração do Brute Force a partir de arquivo (opcional).
        
        Brute Force não requer muitos parâmetros, apenas um limite de segurança
        para o número máximo de portas.
        
        Args:
            config_file: Path to configuration file (optional)
            
        Returns:
            True if loaded successfully or using defaults
        """
        try:
            if config_file and config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                # Detecta formato
                if 'bruteforce_config' in config:
                    bf_config = config['bruteforce_config']
                    self.simulation_params = config.get('simulation_params', {})
                else:
                    bf_config = config
                    self.simulation_params = {}
                
                # Atualiza limite máximo se fornecido
                if 'max_doors' in bf_config:
                    self.config['max_doors'] = int(bf_config['max_doors'])
                
                logger.info(f"Brute Force configuration loaded: max_doors={self.config['max_doors']}")
            else:
                # Usa configuração padrão
                logger.info(f"Using default Brute Force configuration: max_doors={self.config['max_doors']}")
            
            return True
            
        except Exception as e:
            logger.exception(f"Error loading Brute Force configuration: {e}")
            # Ainda assim retorna True pois pode usar defaults
            return True
    
    def validate_problem_size(self, num_doors: int) -> Tuple[bool, str]:
        """
        Valida se o problema é viável para Brute Force.
        
        Args:
            num_doors: Número total de portas/posições possíveis
            
        Returns:
            Tuple (is_valid, message)
        """
        max_allowed = self.config['max_doors']
        
        if num_doors > max_allowed:
            total_combinations = 2 ** num_doors
            msg = (f"⚠️ PROBLEMA MUITO GRANDE para Brute Force!\n"
                   f"Número de portas: {num_doors}\n"
                   f"Combinações necessárias: {total_combinations:,}\n"
                   f"Limite configurado: {max_allowed} portas\n"
                   f"Recomendação: Use NSGA-II para problemas grandes.")
            return False, msg
        
        total_combinations = 2 ** num_doors
        estimated_time = total_combinations * 0.1  # Estimativa grosseira: 0.1s por avaliação
        
        if num_doors >= 12:
            msg = (f"⚠️ AVISO: Problema grande para Brute Force\n"
                   f"Número de portas: {num_doors}\n"
                   f"Combinações: {total_combinations:,}\n"
                   f"Tempo estimado: ~{estimated_time/60:.1f} minutos\n"
                   f"Continuar mesmo assim?")
            return True, msg
        
        msg = (f"✓ Problema viável para Brute Force\n"
               f"Número de portas: {num_doors}\n"
               f"Combinações: {total_combinations:,}")
        return True, msg
    
    def prepare_instance(
        self,
        experiment_name: str,
        draw: bool = False,
        scenario_seed: Optional[List[int]] = None,
        simulation_seed: int = 0
    ) -> Any:
        """
        Prepara um objeto Instance para Brute Force.
        
        Args:
            experiment_name: Nome do experimento
            draw: Se deve desenhar frames de simulação
            scenario_seed: Lista de seeds de cenário (para múltiplas execuções)
            simulation_seed: Seed de simulação
            
        Returns:
            Instance object para Brute Force
        """
        if Instance is None:
            raise RuntimeError("Brute Force not available (import failed)")
        
        # Default to single scenario seed if not provided
        if scenario_seed is None:
            scenario_seed = [self.simulation_params.get('scenario_seed', 0)]
        elif not isinstance(scenario_seed, list):
            scenario_seed = [scenario_seed]
        
        if simulation_seed is None:
            simulation_seed = self.simulation_params.get('simulation_seed', 0)
        
        max_iterations = self.simulation_params.get('max_iterations')
        
        return Instance(
            experiment=experiment_name,
            draw=draw,
            scenario_seed=scenario_seed,
            simulation_seed=simulation_seed,
            max_iterations=max_iterations
        )
    
    def run_optimization(
        self,
        experiment_name: str,
        draw: bool = False
    ) -> Optional[Tuple[List, List]]:
        """
        Executa o algoritmo Brute Force.
        
        Args:
            experiment_name: Nome do experimento
            draw: Se deve desenhar frames
            
        Returns:
            Tuple (pareto_combinations, pareto_objectives) ou None em caso de erro
        """
        if BruteForceAlgorithm is None or Instance is None:
            logger.error("Brute Force not available - imports failed")
            st.error("Brute Force não disponível - falha na importação dos módulos")
            return None
        
        logger.info(f"Starting Brute Force optimization: {experiment_name}")
        st.info(f"🔍 Iniciando Brute Force: {experiment_name}")
        
        try:
            # Stage input files (similar to NSGA-II)
            import os
            import shutil
            root_path = os.path.dirname(os.path.dirname(os.path.abspath("simulator"))) + os.path.sep
            input_dir = Path(root_path) / "input" / experiment_name
            input_dir.mkdir(parents=True, exist_ok=True)
            
            # Source files are in simulador_heuristica/input/<experiment>/
            source_dir = project_root / "simulador_heuristica" / "input" / experiment_name
            
            logger.info(f"Staging files from {source_dir} to {input_dir}")
            
            if not (source_dir / "map.txt").exists():
                raise FileNotFoundError(f"map.txt not found in {source_dir}")
            if not (source_dir / "individuals.json").exists():
                raise FileNotFoundError(f"individuals.json not found in {source_dir}")
            
            shutil.copy2(source_dir / "map.txt", input_dir / "map.txt")
            shutil.copy2(source_dir / "individuals.json", input_dir / "individuals.json")
            logger.info("✓ Files staged successfully")
            
            # Create instance
            scenario_seed = self.simulation_params.get('scenario_seed', [0])
            if not isinstance(scenario_seed, list):
                scenario_seed = [scenario_seed]
            
            simulation_seed = self.simulation_params.get('simulation_seed', 0)
            max_iterations = self.simulation_params.get('max_iterations')
            
            instance = Instance(
                experiment=experiment_name,
                draw=draw,
                scenario_seed=scenario_seed,
                simulation_seed=simulation_seed,
                max_iterations=max_iterations
            )
            
            # Create Brute Force algorithm
            logger.info("Creating Brute Force algorithm...")
            brute_force = BruteForceAlgorithm(instance)
            
            # Validate problem size before running
            num_doors = len(brute_force.exits)
            total_combinations = 2 ** num_doors
            is_valid, msg = self.validate_problem_size(num_doors)
            
            if not is_valid:
                st.error(msg)
                logger.error(msg)
                return None
            
            # Aviso com modal (dialog) se problema for muito grande
            if num_doors >= 12:
                st.warning(msg)
                # Cria um modal de confirmação
                with st.expander("⚠️ ATENÇÃO: Problema Grande", expanded=True):
                    st.warning(f"**Este problema possui {num_doors} portas agrupadas**")
                    st.warning(f"**Total de combinações a avaliar: {total_combinations:,}**")
                    st.warning("**Isso pode demorar vários minutos!**")
                    st.info("💡 **Dica:** Para problemas grandes, considere usar NSGA-II ao invés de Brute Force.")
            else:
                st.success(msg)
            
            # Run Brute Force (modifica o método pareto para retornar os resultados)
            logger.info(f"Running Brute Force for {num_doors} doors...")
            
            # Captura resultado do pareto (precisamos modificar ligeiramente)
            pareto_combinations, pareto_objectives = self._run_pareto_with_results(brute_force)
            
            logger.info(f"Brute Force completed: {len(pareto_combinations)} solutions in Pareto front")
            st.success(f"✓ Brute Force concluído: {len(pareto_combinations)} soluções na fronteira de Pareto")
            
            # Retorna combinações, objetivos e informação das portas
            return pareto_combinations, pareto_objectives, brute_force.exits
            
        except Exception as e:
            import traceback
            logger.exception(f"Error running Brute Force: {e}")
            st.error(f"Erro ao executar Brute Force: {e}")
            st.code(traceback.format_exc())
            return None
    
    def _run_pareto_with_results(self, brute_force: Any) -> Tuple[List, List]:
        """
        Executa o algoritmo Pareto e retorna os resultados.
        
        Esta é uma versão modificada do método pareto() que retorna os resultados
        em vez de apenas imprimi-los.
        
        Args:
            brute_force: Instância do BruteForce
            
        Returns:
            Tuple (combinations, objectives) da fronteira de Pareto
        """
        from itertools import product
        from copy import copy
        
        n = len(brute_force.exits)
        combinations = list(product([True, False], repeat=n))
        
        # Inicializa com primeira combinação (se válida)
        combs = []
        objs = []
        
        # Avalia primeira combinação e adiciona se tiver pelo menos 1 porta
        first_obj = brute_force.decode(combinations[0])
        if first_obj[0] > 0:  # Se num_doors > 0
            combs = [combinations[0]]
            objs = [first_obj]
        
        # Barra de progresso
        progress_bar = st.progress(0.0)
        status_text = st.empty()
        
        total = len(combinations)
        
        for idx, combination in enumerate(combinations[1:], 1):
            # Atualiza progresso
            if idx % max(1, total // 100) == 0:
                progress = idx / total
                progress_bar.progress(progress)
                status_text.text(f"Avaliando combinação {idx}/{total} ({progress*100:.1f}%)")
            
            obj = brute_force.decode(combination)
            
            # ===== PENALIZAÇÃO: Rejeita soluções com 0 portas =====
            # Solução inválida (nenhuma porta selecionada) - não adiciona ao Pareto
            num_doors = obj[0] if len(obj) >= 1 else 0
            if num_doors == 0:
                continue  # Pula para próxima combinação
            
            # Lógica de dominância de Pareto (copiada do original)
            i = 0
            menor = True
            while i < len(combs):
                menor = menor and ((obj[0] < objs[i][0] or obj[1] < objs[i][1] or obj[2] < objs[i][2])
                                   or (obj[0] == objs[i][0] and obj[1] == objs[i][1] and obj[2] == objs[i][2]))
                
                if (obj[0] < objs[i][0] and obj[1] < objs[i][1] and obj[2] < objs[i][2]
                    or obj[0] == objs[i][0] and obj[1] < objs[i][1] and obj[2] < objs[i][2]
                    or obj[0] < objs[i][0] and obj[1] == objs[i][1] and obj[2] < objs[i][2]
                    or obj[0] < objs[i][0] and obj[1] < objs[i][1] and obj[2] == objs[i][2]
                    or obj[0] == objs[i][0] and obj[1] == objs[i][1] and obj[2] < objs[i][2]
                    or obj[0] == objs[i][0] and obj[1] < objs[i][1] and obj[2] == objs[i][2]
                    or obj[0] < objs[i][0] and obj[1] == objs[i][1] and obj[2] == objs[i][2]
                ):
                    combs.pop(i)
                    objs.pop(i)
                    i -= 1
                
                i += 1
            
            if menor:
                combs.append(combination)
                objs.append(obj)
        
        progress_bar.progress(1.0)
        status_text.text(f"✓ Avaliação completa: {total} combinações")
        
        logger.info(f"Pareto front size: {len(combs)} out of {total} combinations")
        
        return combs, objs
    
    def convert_results_to_standard_format(
        self,
        pareto_combinations: List,
        pareto_objectives: List,
        exits_info: List
    ) -> List[Dict[str, Any]]:
        """
        Converte resultados do Brute Force para o formato padrão da interface.
        
        Args:
            pareto_combinations: Lista de combinações (genes) da fronteira de Pareto
            pareto_objectives: Lista de objetivos correspondentes
            exits_info: Informação sobre as portas/saídas disponíveis
            
        Returns:
            Lista de dicionários de soluções
        """
        from simulador_heuristica.simulator import integration_api
        
        converted = []

        for i, (combination, objectives) in enumerate(zip(pareto_combinations, pareto_objectives)):
            # Decodifica combinação para portas selecionadas
            selected_doors = []
            for j, bit in enumerate(combination):
                if bit and j < len(exits_info):
                    selected_doors.append(exits_info[j])

            # Expande portas agrupadas para coordenadas individuais
            try:
                doors_expanded = integration_api.expand_grouped_doors(selected_doors)
            except Exception as e:
                logger.warning(f"Failed to expand doors for solution {i}: {e}")
                doors_expanded = []

            # Objetivos: [num_doors, iterations, distance]
            num_doors, iterations, distance = objectives
            
            # POST-PARETO FILTER: Remove solutions with 0 doors (they don't make sense)
            if num_doors is not None and int(num_doors) == 0:
                logger.debug(f"Filtering out 0-door BruteForce solution {i} from Pareto front")
                continue

            # Objetivos: [num_doors, iterations, distance]
            num_doors, iterations, distance = objectives

            # Use original solution id (preserve indexing)
            solution_id = i

            result_obj = {
                "solution_id": solution_id,
                "gene": list(combination),
                "door_positions": doors_expanded,
                "door_positions_grouped": selected_doors,
                "objectives": [int(num_doors), float(iterations), float(distance)],
                "num_doors": int(num_doors),
                "iterations": float(iterations),
                "distance": float(distance),
                "algorithm": "BruteForce"
            }

            converted.append(result_obj)
        
        logger.info(f"Converted {len(converted)} Brute Force results to standard format")
        return converted
    
    def save_results(
        self,
        pareto_combinations: List,
        pareto_objectives: List,
        exits_info: List,
        output_file: Path
    ) -> bool:
        """
        Salva resultados do Brute Force em arquivo.
        
        Args:
            pareto_combinations: Combinações da fronteira de Pareto
            pareto_objectives: Objetivos correspondentes
            exits_info: Informação sobre portas
            output_file: Path para arquivo de saída
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            # Converte para formato padrão
            converted = self.convert_results_to_standard_format(
                pareto_combinations, pareto_objectives, exits_info
            )
            
            # Atomic write
            tmp_path = output_file.with_suffix('.tmp')
            try:
                with open(tmp_path, 'w') as f:
                    json.dump(converted, f, indent=2)
                tmp_path.replace(output_file)
                logger.info(f"Saved Brute Force results to {output_file}")
                return True
            finally:
                if tmp_path.exists():
                    tmp_path.unlink(missing_ok=True)
                    
        except Exception as e:
            logger.exception(f"Error saving Brute Force results: {e}")
            return False
    
    def extract_door_positions_from_map(self, map_template: str) -> List[dict]:
        """
        Extrai posições das portas existentes no mapa.
        
        This method delegates to the official integration_api module.
        Returns grouped door dictionaries for consistency with simulator.
        
        Args:
            map_template: Template do mapa como string
            
        Returns:
            Lista de dicionários com portas agrupadas {'row','col','size','direction'}
        """
        # OFFICIAL INTEGRATION: Delegate to the unified API (single source of truth)
        if integration_api is not None:
            try:
                doors_info = integration_api.extract_doors_from_map_text(map_template)
                logger.info(f"integration_api.extract_doors_from_map_text returned {len(doors_info)} grouped doors")
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
                    door_positions.append({'row': y, 'col': x, 'size': 1, 'direction': 'h'})
        return door_positions


# Singleton instance
_bruteforce_integration_singleton = None

def get_bruteforce_integration(simulator_integration):
    """
    Get or create the Brute Force integration singleton.
    
    Args:
        simulator_integration: SimulatorIntegration instance
        
    Returns:
        BruteForceIntegration instance
    """
    global _bruteforce_integration_singleton
    if _bruteforce_integration_singleton is None:
        _bruteforce_integration_singleton = BruteForceIntegration(simulator_integration)
    return _bruteforce_integration_singleton
