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

# Adiciona o caminho do simulador ao sys.path para importar módulos
sys.path.append(str(Path(__file__).parent.parent.parent / "simulador_heuristica"))

try:
    from unified.mh_ga_nsgaii import NSGAII, Chromosome
    from unified.mh_ga_factory import ChromosomeFactory
    from unified.mh_ga_selectors import TournamentSelector
except ImportError as e:
    print(f"Erro ao importar módulos do NSGA-II: {e}")
    # Fallback para quando os módulos não estão disponíveis
    NSGAII = None
    Chromosome = None
    ChromosomeFactory = None
    TournamentSelector = None

# Define uma classe base ChromosomeFactory se a importação falhou
if ChromosomeFactory is None:
    class ChromosomeFactory:
        """Classe base para ChromosomeFactory quando os módulos não estão disponíveis."""
        def __init__(self, instance):
            self.instance = instance
        
        def decode(self, gene):
            raise NotImplementedError
        
        def new(self):
            raise NotImplementedError
        
        def crossover(self, parent_a, parent_b):
            raise NotImplementedError
        
        def mutate(self, gene):
            raise NotImplementedError
        
        def build(self, generation, gene):
            raise NotImplementedError

# Define uma classe base Chromosome se a importação falhou
if Chromosome is None:
    class Chromosome:
        """Classe base para Chromosome quando os módulos não estão disponíveis."""
        def __init__(self, generation, gene, obj):
            self.generation = generation
            self.gene = gene
            self.obj = obj
            self.rank = 0
            self.dist = 0.0


class EvacuationChromosomeFactory(ChromosomeFactory):
    """
    Fábrica de cromossomos para problemas de evacuação.
    
    Esta classe implementa a interface necessária para o NSGA-II,
    adaptando o problema de evacuação para o formato genético.
    """
    
    def __init__(self, simulator_integration, map_template: str, individuals_template: Dict):
        """
        Inicializa a fábrica de cromossomos.
        
        Args:
            simulator_integration: Instância da integração com o simulador
            map_template: Template do mapa base
            individuals_template: Template dos indivíduos base
        """
        self.simulator_integration = simulator_integration
        self.map_template = map_template
        self.individuals_template = individuals_template
        self.evaluation_count = 0
    
    def build(self, generation: int, gene: Any) -> Chromosome:
        """
        Constrói um cromossomo a partir de um gene.
        
        Args:
            generation: Geração do cromossomo
            gene: Gene que representa a solução
            
        Returns:
            Cromossomo com os objetivos avaliados
        """
        if Chromosome is None:
            raise ImportError("Módulos do NSGA-II não disponíveis")
        
        # Decodifica o gene para posições de portas
        door_positions = self._decode_gene(gene)
        
        # Gera arquivos de entrada para o simulador
        experiment_name = f"nsga_eval_{self.evaluation_count}_{generation}"
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
            
            return Chromosome(generation, gene, objectives)
            
        except Exception as e:
            print(f"Erro na avaliação do cromossomo: {e}")
            # Retorna valores padrão em caso de erro
            return Chromosome(generation, gene, [float('inf'), float('inf')])
        
        finally:
            # Limpa arquivos temporários
            import shutil
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
    
    def _decode_gene(self, gene: Any) -> List[tuple]:
        """
        Decodifica um gene para posições de portas.
        
        Args:
            gene: Gene a ser decodificado
            
        Returns:
            Lista de tuplas (x, y) com posições das portas
        """
        # Implementação simplificada - assume que o gene é uma lista de posições
        if isinstance(gene, list):
            return [(int(x), int(y)) for x, y in gene if len(gene) >= 2]
        return []
    
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
        initial_population: Optional[List] = None
    ) -> bool:
        """
        Configura a otimização NSGA-II.
        
        Args:
            map_template: Template do mapa base
            individuals_template: Template dos indivíduos base
            initial_population: População inicial (opcional)
            
        Returns:
            True se configurou com sucesso, False caso contrário
        """
        if NSGAII is None:
            print("NSGA-II não disponível")
            return False
        
        try:
            # Cria a fábrica de cromossomos
            self.factory = EvacuationChromosomeFactory(
                self.simulator_integration, 
                map_template, 
                individuals_template
            )
            
            # Cria o seletor
            selector = TournamentSelector(tournament_size=2)
            
            # Cria o NSGA-II
            self.nsga = NSGAII(
                population_size=self.config['population_size'],
                generations=self.config['generations'],
                factory=self.factory,
                selector=selector,
                crossover_rate=self.config['crossover_rate'],
                mutation_rate=self.config['mutation_rate']
            )
            
            return True
            
        except Exception as e:
            print(f"Erro ao configurar otimização: {e}")
            return False
    
    def run_optimization(self) -> Optional[List[Chromosome]]:
        """
        Executa a otimização NSGA-II.
        
        Returns:
            Lista de cromossomos da frente de Pareto, ou None em caso de erro
        """
        if self.nsga is None:
            print("NSGA-II não configurado")
            return None
        
        try:
            # Executa a otimização
            pareto_front = self.nsga.run()
            return pareto_front
            
        except Exception as e:
            print(f"Erro na execução da otimização: {e}")
            return None
    
    def save_results(self, pareto_front: List[Chromosome], output_file: Path) -> bool:
        """
        Salva os resultados da otimização.
        
        Args:
            pareto_front: Frente de Pareto resultante
            output_file: Arquivo de saída
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            results = []
            for chromosome in pareto_front:
                results.append({
                    "generation": chromosome.generation,
                    "gene": chromosome.gene,
                    "objectives": chromosome.obj,
                    "rank": chromosome.rank,
                    "distance": chromosome.dist
                })
            
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Erro ao salvar resultados: {e}")
            return False
