# Referência da API

## Visão Geral

Esta documentação descreve todas as funções e classes públicas do sistema de simulação de evacuação de multidões, incluindo assinaturas, parâmetros, retornos e exceções.

## Scripts de Execução

### sim_ca_main3.py

#### Função Principal
`python
def main():
    """Executa NSGA-II com cache para otimização multiobjetivo.
    
    Parâmetros de linha de comando:
        -e, --experiment: Nome do experimento (obrigatório)
        --pop_size: Tamanho da população (padrão: 10)
        --mut_prob: Probabilidade de mutação (padrão: 0.4)
        --max_gen: Número máximo de gerações (padrão: 300)
        --seed: Semente para gerador aleatório (padrão: 75)
        -o, --out: Pasta de saída (padrão: 'results')
    
    Saída:
        res.json: Arquivo com resultados da otimização
    
    Exceções:
        FileNotFoundError: Se experimento não for encontrado
        ValueError: Se parâmetros forem inválidos
    """
`

#### Funções Auxiliares
`python
def save_result(result, uncoded, filename):
    """Salva resultados da otimização em arquivo JSON.
    
    Args:
        result: Lista de objetos Chromosome com resultados
        uncoded: Lista de configurações decodificadas
        filename: Nome do arquivo de saída
    
    Returns:
        None
    
    Raises:
        IOError: Se não conseguir escrever arquivo
    """
`

### sim_ca_main4.py

#### Função Principal
`python
def main():
    """Executa força bruta para exploração exaustiva.
    
    Parâmetros de linha de comando:
        -e, --experiment: Nome do experimento (obrigatório)
        --seed: Semente para gerador aleatório (padrão: 75)
        -o, --out: Pasta de saída (padrão: 'results')
    
    Saída:
        res.json: Arquivo com resultados da otimização
    
    Exceções:
        FileNotFoundError: Se experimento não for encontrado
        MemoryError: Se houver explosão combinatória
    """
`

## Módulos Core - Meta-heurísticas

### mh_ga_nsgaii.py

#### Classe Chromosome
`python
class Chromosome:
    """Representa um indivíduo no algoritmo genético.
    
    Attributes:
        generation (int): Geração de nascimento do indivíduo
        gene (object): Representação genética da solução
        obj (list): Valores dos objetivos [doors, iterations, distance]
        rank (int): Frente de dominância (0 = melhor)
        dist (float): Distância de crowding
    
    Methods:
        __init__(generation, gene, obj): Inicializa cromossomo
        __lt__(other): Comparação para ordenação
        __eq__(other): Verifica igualdade
    """
    
    def __init__(self, generation, gene, obj):
        """Inicializa um cromossomo.
        
        Args:
            generation (int): Geração de nascimento
            gene (object): Representação genética
            obj (list): Valores dos objetivos [doors, iterations, distance]
        """
`

#### Classe ChromosomeFactory
`python
class ChromosomeFactory:
    """Factory para criação de cromossomos.
    
    Methods:
        create_chromosome(generation, gene): Cria novo cromossomo
        decode(gene): Decodifica gene em solução
    """
    
    def create_chromosome(self, generation, gene):
        """Cria um novo cromossomo.
        
        Args:
            generation (int): Geração de nascimento
            gene (object): Representação genética
        
        Returns:
            Chromosome: Novo cromossomo
        """
`

#### Função Principal
`python
def nsgaii(factory, selector, pop_size, mut_prob, max_gen):
    """Executa algoritmo NSGA-II.
    
    Args:
        factory (ChromosomeFactory): Factory para criação de cromossomos
        selector (function): Função de seleção
        pop_size (int): Tamanho da população
        mut_prob (float): Probabilidade de mutação
        max_gen (int): Número máximo de gerações
    
    Returns:
        list: Lista de cromossomos da frente de Pareto
    
    Complexity:
        O(n²) para ordenação não-dominada
    
    Raises:
        ValueError: Se parâmetros forem inválidos
        MemoryError: Se população for muito grande
    """
`

### mh_ga_factory.py

#### Classe Gene
`python
class Gene:
    """Representa um gene (configuração de portas).
    
    Attributes:
        configuration (list): Lista booleana indicando portas ativas
    
    Methods:
        __init__(configuration): Inicializa gene
    """
    
    def __init__(self, configuration):
        """Inicializa um gene.
        
        Args:
            configuration (list): Lista booleana de portas
        """
`

#### Classe Factory
`python
class Factory(ChromosomeFactory):
    """Factory para criação de genes e cromossomos.
    
    Attributes:
        instance (Instance): Instância do experimento
        exits (list): Lista de configurações de portas
        cache (dict): Cache para evitar recálculos
    
    Methods:
        decode(gene): Decodifica gene em solução
        create_gene(): Cria gene aleatório
        create_chromosome(generation, gene): Cria cromossomo
    """
    
    def __init__(self, instance):
        """Inicializa factory.
        
        Args:
            instance (Instance): Instância do experimento
        """
    
    def decode(self, gene):
        """Decodifica gene em solução.
        
        Args:
            gene (Gene): Gene a ser decodificado
        
        Returns:
            tuple: (doors_count, iterations, distance)
        
        Complexity:
            O(individuals  iterations) para simulação
        
        Raises:
            ValueError: Se gene for inválido
        """
`

### mh_ga_instance.py

#### Classe Instance
`python
class Instance:
    """Representa uma instância de experimento.
    
    Attributes:
        experiment (str): Nome do experimento
        draw (bool): Se deve desenhar visualizações
        scenario_seed (list): Lista de sementes para cenários
        simulation_seed (int): Semente para simulação
    """
    
    def __init__(self, experiment, draw, scenario_seed, simulation_seed):
        """Inicializa instância.
        
        Args:
            experiment (str): Nome do experimento
            draw (bool): Se deve desenhar
            scenario_seed (list): Sementes de cenário
            simulation_seed (int): Semente de simulação
        """
`

#### Função de Leitura
`python
def read_instance(experiment):
    """Lê configuração de experimento.
    
    Args:
        experiment (str): Nome do experimento
    
    Returns:
        Instance: Instância configurada
    
    Raises:
        FileNotFoundError: Se arquivo não for encontrado
        json.JSONDecodeError: Se JSON for inválido
    """
`

## Módulos Core - Heurísticas

### h_brute_force.py

#### Classe BruteForce
`python
class BruteForce:
    """Implementa algoritmo de força bruta.
    
    Attributes:
        exits (list): Lista de configurações de portas
        instance (Instance): Instância do experimento
    
    Methods:
        pareto(): Executa força bruta e retorna frente de Pareto
        decode(combination): Decodifica combinação em solução
    """
    
    def __init__(self, instance):
        """Inicializa força bruta.
        
        Args:
            instance (Instance): Instância do experimento
        """
    
    def pareto(self):
        """Executa força bruta e retorna frente de Pareto.
        
        Returns:
            list: Lista de soluções da frente de Pareto
        
        Complexity:
            O(2^n) onde n é número de portas
        
        Raises:
            MemoryError: Se houver explosão combinatória
        """
    
    def decode(self, combination):
        """Decodifica combinação em solução.
        
        Args:
            combination (tuple): Combinação de portas
        
        Returns:
            tuple: (doors_count, iterations, distance)
        """
`

## Módulos Core - Simulação

### sim_ca_scenario.py

#### Classe Scenario
`python
class Scenario:
    """Gerencia cenários de simulação.
    
    Attributes:
        directory (str): Diretório do experimento
        structure_map (StructureMap): Mapa estrutural
        doors_configurations (list): Configurações de portas
        wall_map (WallMap): Mapa de paredes
        static_map (StaticMap): Mapa estático
        crowd_map (CrowdMap): Mapa da multidão
        dinamic_map (DinamicMap): Mapa dinâmico
        individuals (list): Lista de indivíduos
    
    Methods:
        map_reset(doors): Reinicia mapa com portas
        scenario_reset(scenario_seed, simulation_seed): Reinicia cenário
        load_*(): Carrega diferentes tipos de mapa
    """
    
    def __init__(self, experiment, doors=None, draw=False, 
                 scenario_seed=0, simulation_seed=0, 
                 individuals_position=False):
        """Inicializa cenário.
        
        Args:
            experiment (str): Nome do experimento
            doors (list, optional): Lista de portas
            draw (bool): Se deve desenhar
            scenario_seed (int): Semente do cenário
            simulation_seed (int): Semente da simulação
            individuals_position (bool): Se deve posicionar indivíduos
        """
    
    def map_reset(self, doors):
        """Reinicia mapa com configuração de portas.
        
        Args:
            doors (list): Lista de portas ativas
        """
    
    def scenario_reset(self, scenario_seed, simulation_seed):
        """Reinicia cenário com novas sementes.
        
        Args:
            scenario_seed (int): Nova semente do cenário
            simulation_seed (int): Nova semente da simulação
        """
`

### sim_ca_simulator.py

#### Classe Simulator
`python
class Simulator:
    """Executa simulação de evacuação.
    
    Attributes:
        structure_map (StructureMap): Mapa estrutural
        wall_map (WallMap): Mapa de paredes
        static_map (StaticMap): Mapa estático
        crowd_map (CrowdMap): Mapa da multidão
        dinamic_map (DinamicMap): Mapa dinâmico
        individuals (list): Lista de indivíduos
        iteration (int): Iteração atual
        log (Logs): Sistema de logs
    
    Methods:
        simulate(): Executa simulação completa
        check_evacuated_individuals(): Verifica se todos evacuaram
        sort_individuals_by_distance(): Ordena indivíduos por distância
    """
    
    def __init__(self, scenario):
        """Inicializa simulador.
        
        Args:
            scenario (Scenario): Cenário de simulação
        """
    
    def simulate(self):
        """Executa simulação de evacuação.
        
        Returns:
            tuple: (iterations, total_distance)
        
        Complexity:
            O(iterations  individuals)
        
        Raises:
            RuntimeError: Se simulação falhar
        """
    
    def check_evacuated_individuals(self):
        """Verifica se todos os indivíduos evacuaram.
        
        Returns:
            bool: True se todos evacuaram
        """
`

### sim_ca_individual.py

#### Classe Individual
`python
class Individual:
    """Representa um indivíduo na simulação.
    
    Attributes:
        label (str): Rótulo do indivíduo
        color (tuple): Cor RGB
        speed (int): Velocidade de movimento
        KD (float): Constante do mapa dinâmico
        KS (float): Constante do mapa estático
        KW (float): Constante do mapa de paredes
        KI (float): Constante de inércia
        row (int): Posição Y atual
        col (int): Posição X atual
        evacuated (bool): Se já evacuou
        steps (int): Passos dados
    
    Methods:
        move(): Move indivíduo
        calculate_direction(): Calcula direção de movimento
    """
    
    def __init__(self, configuration, col, row):
        """Inicializa indivíduo.
        
        Args:
            configuration (dict): Configuração do indivíduo
            col (int): Posição X inicial
            row (int): Posição Y inicial
        """
    
    def move(self, structure_map, wall_map, static_map, 
             crowd_map, dinamic_map):
        """Move indivíduo na simulação.
        
        Args:
            structure_map (StructureMap): Mapa estrutural
            wall_map (WallMap): Mapa de paredes
            static_map (StaticMap): Mapa estático
            crowd_map (CrowdMap): Mapa da multidão
            dinamic_map (DinamicMap): Mapa dinâmico
        
        Returns:
            dict: Informações do movimento
        """
`

## Módulos de Mapa

### sim_ca_crowd_map.py

#### Classe CrowdMap
`python
class CrowdMap:
    """Gerencia posições dos indivíduos no mapa.
    
    Attributes:
        label (str): Nome do mapa
        structure_map (StructureMap): Mapa estrutural
        map (list): Matriz de posições
        len_row (int): Largura do mapa
        len_col (int): Altura do mapa
    
    Methods:
        load_map(individuals): Carrega mapa com indivíduos
        place_individuals(individuals): Posiciona indivíduos
        draw_map(directory, iteration): Desenha mapa
        update_individual_position(): Atualiza posição
        check_empty_position(): Verifica se posição está vazia
    """
    
    def __init__(self, label, structure_map):
        """Inicializa mapa da multidão.
        
        Args:
            label (str): Nome do mapa
            structure_map (StructureMap): Mapa estrutural
        """
    
    def load_map(self, individuals):
        """Carrega mapa com indivíduos.
        
        Args:
            individuals (list): Lista de indivíduos
        """
    
    def draw_map(self, directory, iteration):
        """Desenha mapa em arquivo.
        
        Args:
            directory (str): Diretório de saída
            iteration (int): Iteração atual
        """
`

### sim_ca_constants.py

#### Classe Constants
`python
class Constants:
    """Define constantes do sistema.
    
    Constantes de Mapa:
        M_EMPTY: Célula vazia
        M_WALL: Parede
        M_DOOR: Porta
        M_OBJECT: Objeto
        M_VOID: Vazio
    
    Constantes de Campo:
        S_WALL: Campo de parede
    
    Constantes de Direção:
        D_TOP: Cima
        D_TOP_RIGHT: Cima-direita
        D_RIGHT: Direita
        D_BOTTOM_RIGHT: Baixo-direita
        D_BOTTOM: Baixo
        D_BOTTOM_LEFT: Baixo-esquerda
        D_LEFT: Esquerda
        D_TOP_LEFT: Cima-esquerda
    
    Constantes de Cor:
        C_WHITE: Branco
        C_BLACK: Preto
        C_GRAY: Cinza
        C_LIGHT_BLACK: Preto claro
        C_RED: Vermelho
    
    Constantes de Difusão:
        DIFUSIONDECAY_ALFA: Alfa
        DIFUSIONDECAY_SIGMA: Sigma
        DISTANCE_MULTIPLIER: Multiplicador de distância
    """
`

## Exceções Personalizadas

### SimulatorError
`python
class SimulatorError(Exception):
    """Exceção base para erros de simulação."""
    pass
`

### ConfigurationError
`python
class ConfigurationError(SimulatorError):
    """Exceção para erros de configuração."""
    pass
`

### MapError
`python
class MapError(SimulatorError):
    """Exceção para erros de mapa."""
    pass
`

## Dependências Externas

### numpy
- **Versão**: 1.19.5
- **Uso**: Computação numérica, operações vetoriais
- **Módulos**: ndarray, random

### matplotlib
- **Versão**: 3.3.4
- **Uso**: Visualização de dados, gráficos
- **Módulos**: pyplot, figure

### Pillow
- **Versão**: 8.1.0
- **Uso**: Processamento de imagens
- **Módulos**: Image, ImageDraw

### pymoo
- **Versão**: Não especificada
- **Uso**: Algoritmos evolutivos (arquivos z*)
- **Módulos**: NSGA2, Problem, minimize

## Considerações de Performance

### Complexidade Assintótica
- **NSGA-II**: O(n²) para ordenação não-dominada
- **Força Bruta**: O(2^n) para exploração exaustiva
- **Simulação**: O(iterations  individuals)

### Otimizações
- **Cache**: Evita recálculos em mh_ga_factory.py
- **Early Termination**: Para quando todos evacuam
- **Vectorization**: Uso de numpy para operações vetoriais

### Limitações
- **Memória**: Explosão combinatória em força bruta
- **Thread Safety**: Módulos não são thread-safe
- **Cache Invalidation**: Cache pode ser invalidado
