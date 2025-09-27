# Arquitetura do Sistema

## Visão Geral da Arquitetura

O sistema de simulação de evacuação de multidões é organizado em camadas bem definidas, separando interfaces de execução dos módulos core de simulação e otimização.

## Diagrama de Arquitetura

`

                        INTERFACES                               
─
  main3.py          main4.py          z_experiment*.py          
  (NSGA-II+cache)   (Força Bruta)    (NSGA-II via pymoo)       
──
                                   

                    META-HEURÍSTICAS (mh/)                      
─
  mh_ga_instance.py    mh_ga_factory.py    mh_ga_nsgaii.py      
  (Configuração)       (Factory)           (NSGA-II)            
─
                                   
─
                    HEURÍSTICAS (h/)                             

  h_brute_force.py                                               
  (Força Bruta)                                                  

                  

                SIMULAÇÃO (sim_ca/)                              
─
  scenario.py    simulator.py    individual.py                  
  (Cenários)     (Simulador)     (Indivíduos)                   
─
  crowd_map.py   static_map.py   dinamic_map.py                 
  (Multidão)     (Campos Est.)   (Campos Din.)                  

  wall_map.py    structure_map.py logs.py constants.py          
  (Paredes)      (Estrutura)     (Logs)    (Constantes)         
─
`

## Fluxo de Execução Principal

### 1. NSGA-II com Cache (main3)

`
main3.py
    
mh_ga_instance.py (read_instance)
    
mh_ga_factory.py (Factory)
    
mh_ga_nsgaii.py (nsgaii)
    
sim_ca_scenario.py (Scenario)
    
sim_ca_simulator.py (Simulator)
    
sim_ca_*.py (Módulos de simulação)
    
res.json (Resultados)
`

### 2. Força Bruta (main4)

`
main4.py
    
mh_ga_instance.py (read_instance)
    
h_brute_force.py (BruteForce)
    
sim_ca_scenario.py (Scenario)
    
sim_ca_simulator.py (Simulator)
    
sim_ca_*.py (Módulos de simulação)
    
res.json (Resultados)
`

### 3. NSGA-II via pymoo (z*)

`
z_experiment*.py
    
ScenarioOptimizationProblem (pymoo)
    
sim_ca_scenario.py (Scenario)
    
sim_ca_simulator.py (Simulator)
    
sim_ca_*.py (Módulos de simulação)
    
resultados_*.txt (Resultados)
`

## Tabela de Entradas, Processos e Saídas

| Componente | Entradas | Processos | Saídas |
|------------|----------|-----------|--------|
| **main3.py** | experiment, pop_size, mut_prob, max_gen, seed | Executa NSGA-II com cache | res.json |
| **main4.py** | experiment, seed | Executa força bruta | res.json |
| **z_experiment*.py** | experiment (hardcoded) | Executa NSGA-II via pymoo | resultados_*.txt |
| **mh_ga_instance.py** | experiment.json | Lê configuração do experimento | Instance object |
| **mh_ga_factory.py** | Instance, doors config | Cria genes e cromossomos | Gene objects |
| **mh_ga_nsgaii.py** | Population, parameters | Executa algoritmo NSGA-II | Pareto front |
| **h_brute_force.py** | Instance | Explora todas combinações | Pareto front |
| **sim_ca_scenario.py** | experiment, doors, seeds | Configura cenário de simulação | Scenario object |
| **sim_ca_simulator.py** | Scenario | Executa simulação de evacuação | iterations, distance |
| **sim_ca_individual.py** | configuration, position | Simula comportamento individual | movement, evacuation |
| **sim_ca_crowd_map.py** | individuals, positions | Gerencia posições na multidão | crowd_map |
| **sim_ca_static_map.py** | structure_map | Calcula campos de atração | static_fields |
| **sim_ca_dinamic_map.py** | individuals | Calcula campos de repulsão | dynamic_fields |
| **sim_ca_wall_map.py** | structure_map | Identifica paredes e obstáculos | wall_map |
| **sim_ca_structure_map.py** | map.txt | Carrega estrutura do ambiente | structure_map |
| **sim_ca_logs.py** | simulation_data | Registra logs e estatísticas | log_files |

## Diagrama de Dependências

`

   main3.py      

          
          
    
 mh_ga_instance       mh_ga_factory   
    
                                
                                
    
 mh_ga_nsgaii         sim_ca_scenario 
    
                                
                                
    
 sim_ca_simulator     sim_ca_individual
    
                                
                                
    
 sim_ca_crowd_map     sim_ca_static_map
    
                                
                                
    
 sim_ca_dinamic_map   sim_ca_wall_map 
    
                                
                                
    
 sim_ca_structure_map  sim_ca_logs     
    
                                
                                
    
 sim_ca_constants         res.json    
    
`

## Padrões de Design Utilizados

### 1. Factory Pattern
- **mh_ga_factory.py**: Cria genes e cromossomos
- **sim_ca_scenario.py**: Cria cenários de simulação

### 2. Strategy Pattern
- **main3.py**: Estratégia NSGA-II com cache
- **main4.py**: Estratégia força bruta
- **z_experiment*.py**: Estratégia NSGA-II via pymoo

### 3. Observer Pattern
- **sim_ca_logs.py**: Observa e registra eventos da simulação

### 4. Template Method Pattern
- **mh_ga_nsgaii.py**: Define estrutura do algoritmo NSGA-II

## Fluxo de Dados

### Entrada de Dados
1. **experiment.json**: Configuração do experimento
2. **map.txt**: Mapa estrutural do ambiente
3. **individuals.json**: Configuração dos indivíduos
4. **positions.txt**: Posições iniciais

### Processamento
1. **Leitura de configuração**: mh_ga_instance.py
2. **Criação de genes**: mh_ga_factory.py
3. **Otimização**: mh_ga_nsgaii.py ou h_brute_force.py
4. **Simulação**: sim_ca_simulator.py
5. **Cálculo de objetivos**: iterations, distance, doors

### Saída de Dados
1. **res.json**: Resultados da otimização
2. **output/**: Visualizações da simulação
3. **resultados_*.txt**: Resultados específicos por seed

## Considerações de Performance

### Complexidade Assintótica
- **NSGA-II**: O(n²) para ordenação não-dominada
- **Força Bruta**: O(2^n) para exploração exaustiva
- **Simulação**: O(iterations  individuals)

### Otimizações Implementadas
- **Cache**: mh_ga_factory.py implementa cache para evitar recálculos
- **Early Termination**: sim_ca_simulator.py para quando todos evacuam
- **Vectorization**: Uso de numpy para operações vetoriais

### Gargalos Identificados
- **h_brute_force.py**: Explosão combinatória
- **mh_ga_nsgaii.py**: Ordenação não-dominada
- **sim_ca_simulator.py**: Loop principal da simulação

## Riscos Arquiteturais

### 1. Acoplamento Alto
- **Problema**: Módulos sim_ca_* são altamente acoplados
- **Solução**: Implementar interfaces mais claras

### 2. Cache Invalidation
- **Problema**: Cache em mh_ga_factory.py pode ser invalidado
- **Solução**: Implementar controle de versão do cache

### 3. Memory Leaks
- **Problema**: Múltiplas instâncias de Scenario podem vazar memória
- **Solução**: Implementar gerenciamento de ciclo de vida

### 4. Thread Safety
- **Problema**: Módulos não são thread-safe
- **Solução**: Implementar locks ou usar multiprocessing
