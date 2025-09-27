# Mapa de Responsabilidades por Arquivo e Pasta

## Estrutura do Projeto

### Interfaces (Scripts de Execução)
- **main***: Scripts de execução principal que chamam outros módulos
- **scenario**: Interface de configuração de cenários
- **simulator**: Interface de simulação

### Módulos Core
- **h/**: Módulos base de heurísticas
- **mh/**: Módulos de meta-heurísticas (NSGA-II, GA)
- **sim_ca/**: Módulos de simulação por Cellular Automata

## Mapeamento Detalhado

### Scripts de Execução Principal

#### unified/sim_ca_main3.py
- **Tipo**: Interface de execução
- **Responsabilidade**: Implementa NSGA-II com cache
- **Parâmetros**: experiment, pop_size, mut_prob, max_gen, seed, out
- **Saída**: res.json com resultados da otimização
- **Dependências**: mh_ga_instance, mh_ga_factory, mh_ga_nsgaii

#### unified/sim_ca_main4.py
- **Tipo**: Interface de execução
- **Responsabilidade**: Implementa força bruta
- **Parâmetros**: experiment, seed, out
- **Saída**: res.json com resultados da otimização
- **Dependências**: mh_ga_instance, h_brute_force

#### unified/sim_ca_main5.py
- **Tipo**: Interface de execução
- **Responsabilidade**: Script adicional de execução
- **Parâmetros**: experiment, seed, out
- **Saída**: res.json com resultados da otimização

### Scripts de Teste e Experimentos

#### unified/mh_teste_nsga2.py
- **Tipo**: Script de teste
- **Responsabilidade**: Testa implementação NSGA-II via pymoo
- **Parâmetros**: Configurado para cult_experiment
- **Saída**: Resultados de otimização via pymoo

#### unified/z_experiment*.py
- **Tipo**: Scripts de experimento
- **Responsabilidade**: Implementam NSGA-II via pymoo para experimentos específicos
- **Arquivos**:
  - z_experiment1_audition.py: Experimento de audição
  - z_experiment2_formatura.py: Experimento de formatura
  - z_experiment3_balad.py: Experimento de balada
- **Parâmetros**: Configurados para experimentos específicos
- **Saída**: Arquivos de resultados por seed

### Módulos Core - Meta-heurísticas (mh/)

#### unified/mh_ga_nsgaii.py
- **Tipo**: Módulo core
- **Responsabilidade**: Implementação customizada do NSGA-II
- **Classes principais**:
  - Chromosome: Representa um indivíduo
  - ChromosomeFactory: Factory para criação de cromossomos
  - nsgaii: Função principal do algoritmo NSGA-II
- **Complexidade**: O(n²) para ordenação não-dominada
- **Dependências**: numpy, ctypes

#### unified/mh_ga_factory.py
- **Tipo**: Módulo core
- **Responsabilidade**: Factory para criação de genes e cromossomos
- **Classes principais**:
  - Gene: Representa um gene (configuração de portas)
  - Factory: Factory para criação de cromossomos
- **Dependências**: mh_ga_nsgaii, sim_ca_scenario, sim_ca_simulator

#### unified/mh_ga_instance.py
- **Tipo**: Módulo core
- **Responsabilidade**: Leitura e configuração de instâncias de experimento
- **Classes principais**:
  - Instance: Representa uma instância de experimento
  - read_instance: Função para ler configuração do experimento
- **Dependências**: json, os

#### unified/mh_ga_selectors.py
- **Tipo**: Módulo core
- **Responsabilidade**: Seletores para algoritmo genético
- **Dependências**: mh_ga_nsgaii

### Módulos Core - Heurísticas (h/)

#### unified/h_brute_force.py
- **Tipo**: Módulo core
- **Responsabilidade**: Implementação de força bruta para exploração exaustiva
- **Classes principais**:
  - BruteForce: Implementa algoritmo de força bruta
- **Complexidade**: O(2^n) onde n é o número de portas
- **Risco**: Explosão combinatória para muitos portas
- **Dependências**: sim_ca_simulator, sim_ca_scenario, itertools

### Módulos Core - Simulação (sim_ca/)

#### unified/sim_ca_scenario.py
- **Tipo**: Interface/Módulo core
- **Responsabilidade**: Configuração e gerenciamento de cenários de simulação
- **Classes principais**:
  - Scenario: Gerencia cenários de simulação
- **Dependências**: sim_ca_crowd_map, sim_ca_individual, sim_ca_dinamic_map, sim_ca_static_map, sim_ca_structure_map, sim_ca_wall_map

#### unified/sim_ca_simulator.py
- **Tipo**: Interface/Módulo core
- **Responsabilidade**: Execução da simulação de evacuação
- **Classes principais**:
  - Simulator: Executa a simulação
- **Complexidade**: O(iterations  individuals)
- **Dependências**: sim_ca_logs

#### unified/sim_ca_individual.py
- **Tipo**: Módulo core
- **Responsabilidade**: Representação e comportamento de indivíduos
- **Classes principais**:
  - Individual: Representa um indivíduo na simulação
- **Dependências**: sim_ca_constants, random, math

#### unified/sim_ca_crowd_map.py
- **Tipo**: Módulo core
- **Responsabilidade**: Controle de posicionamento de indivíduos no mapa
- **Classes principais**:
  - CrowdMap: Gerencia posições dos indivíduos
- **Dependências**: PIL, random, os, sim_ca_constants

#### unified/sim_ca_static_map.py
- **Tipo**: Módulo core
- **Responsabilidade**: Mapa estático com campos de atração
- **Classes principais**:
  - StaticMap: Gerencia campos estáticos
- **Dependências**: sim_ca_constants

#### unified/sim_ca_dinamic_map.py
- **Tipo**: Módulo core
- **Responsabilidade**: Mapa dinâmico com campos de repulsão
- **Classes principais**:
  - DinamicMap: Gerencia campos dinâmicos
- **Dependências**: sim_ca_constants

#### unified/sim_ca_wall_map.py
- **Tipo**: Módulo core
- **Responsabilidade**: Mapa de paredes e obstáculos
- **Classes principais**:
  - WallMap: Gerencia paredes e obstáculos
- **Dependências**: sim_ca_constants

#### unified/sim_ca_structure_map.py
- **Tipo**: Módulo core
- **Responsabilidade**: Mapa estrutural do ambiente
- **Classes principais**:
  - StructureMap: Gerencia estrutura do ambiente
- **Dependências**: sim_ca_constants

#### unified/sim_ca_logs.py
- **Tipo**: Módulo core
- **Responsabilidade**: Sistema de logging e estatísticas
- **Classes principais**:
  - Logs: Gerencia logs e estatísticas
- **Dependências**: json, os

#### unified/sim_ca_constants.py
- **Tipo**: Módulo core
- **Responsabilidade**: Constantes do sistema
- **Classes principais**:
  - Constants: Define constantes do sistema
- **Dependências**: Nenhuma

### Arquivos de Configuração

#### input/<experiment>/
- **experiment.json**: Configuração do experimento
- **map.txt**: Mapa estrutural
- **individuals.json**: Configuração dos indivíduos
- **positions.txt**: Posições iniciais

#### requirements.txt
- **Responsabilidade**: Dependências Python do projeto
- **Dependências**: numpy, matplotlib, Pillow, pymoo

## Fluxo de Execução

1. **main***  **mh_ga_instance** (leitura de configuração)
2. **main***  **mh_ga_factory** (criação de genes)
3. **mh_ga_factory**  **sim_ca_scenario** (configuração de cenário)
4. **sim_ca_scenario**  **sim_ca_simulator** (execução da simulação)
5. **sim_ca_simulator**  **sim_ca_*** (módulos de simulação)
6. **main***  **res.json** (salvamento de resultados)

## Riscos e Considerações

### Riscos de Performance
- **h_brute_force.py**: Explosão combinatória O(2^n)
- **mh_ga_nsgaii.py**: Complexidade O(n²) para ordenação
- **sim_ca_simulator.py**: O(iterations  individuals)

### Riscos de Cache
- **mh_ga_factory.py**: Cache pode ser invalidado sem controle
- **sim_ca_scenario.py**: Múltiplas instâncias podem conflitar

### Dependências Externas
- **pymoo**: Para arquivos z*
- **PIL**: Para geração de imagens
- **numpy**: Para computação numérica
- **matplotlib**: Para visualização
