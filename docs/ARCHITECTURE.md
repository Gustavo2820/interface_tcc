# Arquitetura do Sistema

Documentação da arquitetura do Sistema de Simulação e Otimização de Evacuação de Multidões.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Componentes Principais](#componentes-principais)
- [Fluxo de Execução](#fluxo-de-execução)
- [Armazenamento de Dados](#armazenamento-de-dados)
- [Padrões de Design](#padrões-de-design)

## 🌟 Visão Geral

### Arquitetura em Camadas

```
┌─────────────────────────────────────────────────────────┐
│                 INTERFACE WEB (Streamlit)               │
│  - Páginas (Mapas, Parâmetros, Simulação, Resultados)  │
│  - Componentes visuais e interação com usuário         │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│            CAMADA DE INTEGRAÇÃO (Services)              │
│  - nsga_integration.py (NSGA-II pymoo)                  │
│  - nsga_cached_integration.py (NSGA-II customizado)     │
│  - bruteforce_integration.py (Força bruta)              │
│  - simulator_integration.py (Execução de simulador)     │
│  - map_creation_integration.py (Criação de mapas)       │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│         CORE DO SIMULADOR E OTIMIZAÇÃO                  │
│  simulador_heuristica/                                  │
│  ├── simulator/ (Simulador principal CLI)               │
│  ├── unified/ (NSGA-II cached + Cellular Automata)      │
│  └── heuristics/ (Algoritmos de otimização)             │
│                                                          │
│  modulo_criacao_mapas/                                  │
│  └── Conversão e validação de mapas                     │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              PERSISTÊNCIA DE DADOS                      │
│  - database/ (SQLite: histórico, mapas, resultados)     │
│  - uploads/ (Arquivos JSON de configuração/resultados)  │
│  - logs/ (Logs de execução)                             │
└─────────────────────────────────────────────────────────┘
```

### Princípios Arquiteturais

1. **Separação de Responsabilidades**
   - UI não conhece detalhes de implementação do simulador
   - Services fazem a ponte entre camadas
   - Core é independente da interface

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
    
                                

2. **Configuração Unificada**
   - Formato JSON único para todos os algoritmos
   - Presets reutilizáveis
   - Parâmetros de simulação e otimização separados

3. **Modularidade**
   - Componentes podem ser testados isoladamente
   - Fácil adição de novos algoritmos
   - Extensível para novas features

## 🔧 Componentes Principais

### Interface Web (Streamlit)

**App.py** - Ponto de entrada
- Configuração global (layout, CSS, theme)
- Gerenciamento de sessão (`st.session_state`)
- Menu de navegação e sidebar

**Pages** - Páginas da aplicação
- `Mapas.py`: Criação, edição e gestão de mapas
- `Parâmetros.py`: Configuração de algoritmos e presets
- `Simulação.py`: Execução de simulações e otimizações
- `Resultados.py`: Visualização e análise de resultados
- `Detalhes.py`: Informações detalhadas de simulações

### Camada de Integração (Services)

**NSGAIntegration** (`nsga_integration.py`)
- Integra NSGA-II pymoo com interface
- Gerencia Problem adapter para pymoo
- Extrai portas possíveis do mapa
- Coordena avaliações de fitness

**CachedNSGAIntegration** (`nsga_cached_integration.py`)
- Integra NSGA-II cached (customizado)
- Usa implementação em `simulador_heuristica/unified/`
- Cache de avaliações para evitar re-simulações
- Retorna 3 objetivos: [portas, iterações, distância]

**BruteForceIntegration** (`bruteforce_integration.py`)
- Integra algoritmo de força bruta
- Explora todas as combinações de portas
- Limitado a problemas pequenos

**SimulatorIntegration** (`simulator_integration.py`)
- Executa simulador via CLI subprocess
- Prepara arquivos de entrada
- Lê resultados de output/
- Gerencia banco de dados SQLite
- Funções: `prepare_experiment`, `run_simulator_cli`, `read_results`, `save_simulation`

**MapCreationIntegration** (`map_creation_integration.py`)
- Conversão PNG ↔ map.txt
- Validação de mapas (dimensões, cores, portas)
- Geração de previews
- Codificação: 0=vazio, 1=parede, 2=porta, 3=obstáculo

### Core do Simulador

**simulator/** - Simulador principal (CLI)
- `main.py`: Interface de linha de comando
  - Argumentos: -e (experiment), -d (draw), -m (scenario_seed), -s (simulation_seed)
- `scenario.py`: Configuração de cenários
- `simulator.py`: Motor de simulação básico

**unified/** - Implementação unificada CA + NSGA-II
- `mh_ga_nsgaii.py`: NSGA-II customizado com cache
- `mh_ga_factory.py`: Factory de avaliação de genes
- `mh_ga_instance.py`: Classe de instância (configuração)
- `sim_ca_scenario.py`: Cenários Cellular Automata
- `sim_ca_simulator.py`: Simulador CA
- `sim_ca_*.py`: Componentes CA (maps, individuals, etc.)

**heuristics/** - Algoritmos de otimização
- `brute_force.py`: Força bruta para teste exaustivo

### Módulo de Criação de Mapas

**modulo_criacao_mapas/**
- `map_converter.py`: Conversão entre formatos
- `map_converter_utils.py`: Utilitários de validação

## 🔄 Fluxo de Execução

### Otimização NSGA-II (Pymoo)

```
1. UI (Simulação.py)
   - Configuração NSGA-II carregada
   - Mapa template com possíveis portas

2. NSGAIntegration.setup_optimization()
   - Extrai coordenadas de portas possíveis
   - Cria EvacuationProblem (pymoo Problem)
   - Configura NSGA2 algorithm

3. NSGAIntegration.run_optimization()
   - minimize(problem, NSGA2(), termination)
   
4. Para cada indivíduo da população:
   - EvacuationProblem._evaluate(x)
     a. Decodifica gene binário → posições de portas
     b. Gera mapa com portas selecionadas
     c. Chama SimulatorIntegration.run_simulator_cli()
     d. Extrai objetivos: [num_doors, iterations, distance]
     e. Retorna fitness

5. Algoritmo evolui população por N gerações
   - Seleção, crossover, mutação
   - Non-dominated sorting
   - Crowding distance

6. Retorna Fronteira de Pareto
   - Conjunto de soluções ótimas

7. NSGAIntegration.save_results()
   - JSON com todas as soluções
   - Formato: [{objectives, doors, config}, ...]

8. Resultados salvos no banco de dados
   - Tabela de soluções com status e métricas
```

### Otimização NSGA-II (Cached)

```
1-2. Igual ao pymoo

3. NSGAIntegration.run_cached_nsga()
   - CachedNSGAIntegration.run_optimization()

4. CachedNSGAIntegration prepara Instance
   - Instance(experiment, draw, scenario_seed, simulation_seed, max_iterations)

5. Factory.decode() para cada gene
   - Verifica cache (configuração já avaliada?)
   - Se não: executa simulação
   - Se sim: retorna resultado cacheado

6-8. Igual ao pymoo
```

## 💾 Armazenamento de Dados

### Banco de Dados SQLite

**Localização:** `database/simulacoes.db`

**Tabelas:**

**Simulacao**
- id_simulacao (INTEGER PRIMARY KEY)
- nome (TEXT)
- data_criacao (TEXT)
- algoritmo (TEXT)
- mapa_id (INTEGER FK)
- resultado (TEXT JSON)
- executada (INTEGER 0/1)
- descricao (TEXT)

**Mapa**
- id_mapa (INTEGER PRIMARY KEY)
- nome (TEXT)
- caminho (TEXT)
- data_criacao (TEXT)
- dimensoes (TEXT)

**Resultado**
- id_resultado (INTEGER PRIMARY KEY)
- simulacao_id (INTEGER FK)
- metricas (TEXT JSON)
- data_execucao (TEXT)

### Arquivos JSON

**Configurações** (`presets/*.json`)
```json
{
  "nsga_config": {
    "population_size": 50,
    "generations": 30,
    "mutation_rate": 0.15
  },
  "simulation_params": {
    "scenario_seed": [0],
    "simulation_seed": 0,
    "max_iterations": 1000,
    "draw_mode": true,
    "verbose": false
  },
  "description": "Descrição do preset"
}
```

**Resultados** (`uploads/nsga_ii/*.json`)
```json
[
  {
    "objectives": [3, 450, 2345.6],
    "door_positions": [[4, 1], [4, 2], [10, 5]],
    "metrics": {
      "iterations": 450,
      "distance": 2345.6,
      "evacuated": 100
    }
  }
]
```

### Diretórios de Dados

```
uploads/
├── nsga_ii/          # Resultados de otimizações NSGA-II
├── forca_bruta/      # Resultados de força bruta
└── results/          # Exportações de dados

simulador_heuristica/
├── input/            # Arquivos de entrada temporários
│   └── <experiment>/
│       ├── map.txt
│       └── individuals.json
└── output/           # Resultados de simulações
    ├── <experiment>/
    │   ├── metrics.json
    │   ├── eventos.csv
    │   ├── crowd_map/     # PNGs de densidade
    │   └── dinamic_map/   # PNGs de movimento
    └── nsga_eval_*/       # Avaliações NSGA-II

temp_nsga/            # Dados temporários de otimização
logs/                 # Logs de execução
mapas/                # Mapas salvos
```

## 🎨 Padrões de Design

### Factory Pattern

**Uso:** `mh_ga_factory.py`

- Cria objetos complexos (Scenario, Genes)
- Encapsula lógica de instanciação
- Cache de avaliações implementado aqui

```python
class Factory:
    def __init__(self, instance):
        self.instance = instance
        self.cache = {}  # Cache de avaliações
    
    def decode(self, gene):
        # Cria cenário com portas do gene
        # Verifica cache antes de simular
        # Retorna fitness
```

### Strategy Pattern

**Uso:** Algoritmos intercambiáveis

- NSGA-II pymoo
- NSGA-II cached
- Força bruta

Interface comum via services permite trocar algoritmo sem alterar UI.

### Singleton Pattern

**Uso:** Services exportados

```python
# Em cada service
class SimulatorIntegration:
    # ... implementação

# No fim do arquivo
simulator_integration = SimulatorIntegration()  # Singleton
```

Garante instância única, evita re-inicialização.

### Observer Pattern (Implícito)

**Uso:** Logs e eventos

- `sim_ca_logs.py` observa eventos da simulação
- Registra em arquivo CSV
- UI pode ler logs para acompanhar progresso

## 🔗 Integrações Externas

### Pymoo (Algoritmos Evolutivos)

- Biblioteca: `pymoo`
- Usado em: `NSGAIntegration`
- Fornece: NSGA2, Problem, minimize()
- Custom Problem adapter: `EvacuationProblem`

### Streamlit (Web Framework)

- Framework: `streamlit`
- Features usadas:
  - Páginas automáticas (`pages/`)
  - Session state
  - Caching (`@st.cache_data`)
  - Widgets interativos
  - File uploads

### SQLite (Banco de Dados)

- Built-in do Python
- Driver: `sqlite3`
- Sem servidor necessário
- Arquivo único: `simulacoes.db`

### PIL/Pillow (Processamento de Imagens)

- Biblioteca: `Pillow`
- Usado em: Conversão de mapas
- Funções: load image, convert, resize

---

**Versão:** 1.0  
**Atualizado:** Outubro 2024
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
