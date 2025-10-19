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
    
    def __init__(self, simulator_integration, map_template: str, individuals_template: Dict, door_positions: List[tuple]):
        """
        Inicializa o problema de evacuação.
        
        Args:
            simulator_integration: Instância da integração com o simulador
            map_template: Template do mapa base
            individuals_template: Template dos indivíduos base
            door_positions: Lista de posições possíveis para portas
        """
        self.simulator_integration = simulator_integration
        self.map_template = map_template
        self.individuals_template = individuals_template
        self.door_positions = door_positions
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
        results = np.apply_along_axis(self._evaluate_single, 1, x)
        out["F"] = results
    
    def _evaluate_single(self, gene):
        """
        Avalia uma única solução.
        
        Args:
            gene: Vetor binário representando quais portas usar
            
        Returns:
            Lista com os valores dos objetivos
        """
        # Decodifica o gene para posições de portas
        door_positions = self._decode_gene(gene)
        
        # Gera arquivos de entrada para o simulador
        experiment_name = f"nsga_eval_{self.evaluation_count}"
        self.evaluation_count += 1
        
        # Cria o mapa com as portas posicionadas
        map_content = self._generate_map_with_doors(door_positions)
        
        # Salva arquivos temporários
        temp_dir = Path("temp_nsga") / experiment_name
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        map_file = temp_dir / "map.txt"
        individuals_file = temp_dir / "individuals.json"
        
        with open(map_file, 'w') as f:
            f.write(map_content)
        
        with open(individuals_file, 'w') as f:
            json.dump(self.individuals_template, f, indent=2)
        
        try:
            # Prepara o experimento
            self.simulator_integration.prepare_experiment_from_uploads(
                experiment_name, map_file, individuals_file
            )
            
            # Executa a simulação
            result = self.simulator_integration.run_simulator_cli(experiment_name)
            
            # Lê os resultados
            results = self.simulator_integration.read_results(experiment_name)
            
            # Extrai métricas dos objetivos
            objectives = self._extract_objectives(results)
            
            return objectives
            
        except Exception as e:
            print(f"Erro na avaliação do cromossomo: {e}")
            # Retorna valores padrão em caso de erro
            return [float('inf'), float('inf')]
        
        finally:
            # Limpa arquivos temporários
            import shutil
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
    
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
            door_positions: Lista de posições das portas
            
        Returns:
            Conteúdo do mapa como string
        """
        # Implementação simplificada - substitui '0' por '3' nas posições das portas
        lines = self.map_template.split('\n')
        
        for x, y in door_positions:
            if 0 <= y < len(lines) and 0 <= x < len(lines[y]):
                line = list(lines[y])
                line[x] = '3'  # 3 representa porta no formato do simulador
                lines[y] = ''.join(line)
        
        return '\n'.join(lines)
    
    def _extract_objectives(self, results: Dict) -> List[float]:
        """
        Extrai os objetivos dos resultados da simulação.
        
        Args:
            results: Resultados da simulação
            
        Returns:
            Lista com os valores dos objetivos
        """
        # Implementação simplificada - retorna tempo e distância
        # Em uma implementação real, estes valores seriam extraídos dos logs
        return [100.0, 50.0]  # [tempo, distância]


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
        
        Args:
            config_file: Caminho para o arquivo de configuração
            
        Returns:
            True se carregou com sucesso, False caso contrário
        """
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Valida configuração necessária
            required_keys = ['population_size', 'generations', 'crossover_rate', 'mutation_rate']
            if not all(key in config for key in required_keys):
                print("Configuração inválida: chaves obrigatórias ausentes")
                return False
            
            self.config = config
            return True
            
        except Exception as e:
            print(f"Erro ao carregar configuração: {e}")
            return False
    
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
                door_positions
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
        try:
            results = []
            for i, (solution, objectives) in enumerate(zip(result.X, result.F)):
                # Decodifica a solução para posições de portas
                door_positions = []
                for j, bit in enumerate(solution):
                    if bit == 1 and j < len(self.problem.door_positions):
                        door_positions.append(self.problem.door_positions[j])
                
                results.append({
                    "solution_id": i,
                    "gene": solution.tolist(),
                    "door_positions": door_positions,
                    "objectives": objectives.tolist(),
                    "num_doors": sum(solution)
                })
            
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Erro ao salvar resultados: {e}")
            return False
