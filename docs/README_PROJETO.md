# Simulador de Heurística - Documentação do Projeto

## Visão Geral

Este projeto implementa um simulador de evacuação de multidões com algoritmos de otimização multiobjetivo. O sistema utiliza Cellular Automata (CA) para simular o movimento de indivíduos em cenários de evacuação, otimizando a configuração de portas de saída através de diferentes abordagens:

- **NSGA-II com cache** (main3): Implementação customizada do algoritmo NSGA-II com sistema de cache para otimização
- **Força bruta** (main4): Exploração exaustiva de todas as combinações possíveis de portas
- **NSGA-II via pymoo** (arquivos z*): Implementação usando a biblioteca pymoo para algoritmos evolutivos

## Arquitetura do Sistema

O projeto está organizado em módulos core e interfaces:

### Módulos Core
- **h/**: Módulos base de heurísticas
- **mh/**: Módulos de meta-heurísticas (NSGA-II, GA)
- **sim_ca/**: Módulos de simulação por Cellular Automata

### Interfaces
- **main***: Scripts de execução principal
- **scenario**: Interface de configuração de cenários
- **simulator**: Interface de simulação

## Pré-requisitos

### Dependências do Sistema
- Python 3.7+
- Windows/Linux/macOS

### Dependências Python
`ash
pip install -r requirements.txt
`

Dependências principais:
- 
umpy==1.19.5: Computação numérica
- matplotlib==3.3.4: Visualização de dados
- Pillow==8.1.0: Processamento de imagens
- pymoo: Algoritmos evolutivos (para arquivos z*)

## Instalação

1. **Clone o repositório:**
`ash
git clone <repository-url>
cd simulador_heuristica-main
`

2. **Crie um ambiente virtual:**
`ash
python3 -m venv venv
`

3. **Ative o ambiente virtual:**
`ash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
`

4. **Instale as dependências:**
`ash
pip install -r requirements.txt
`

## Como Executar

### 1. NSGA-II com Cache (main3)

`ash
python unified/sim_ca_main3.py -e <experiment_name> [opções]
`

**Parâmetros:**
- -e, --experiment: Nome do experimento (obrigatório)
- --pop_size: Tamanho da população (padrão: 10)
- --mut_prob: Probabilidade de mutação (padrão: 0.4)
- --max_gen: Número máximo de gerações (padrão: 300)
- --seed: Semente para gerador aleatório (padrão: 75)
- -o, --out: Pasta de saída (padrão: 'results')

**Exemplo:**
`ash
python unified/sim_ca_main3.py -e cult_experiment --pop_size 50 --max_gen 200
`

### 2. Força Bruta (main4)

`ash
python unified/sim_ca_main4.py -e <experiment_name> [opções]
`

**Parâmetros:**
- -e, --experiment: Nome do experimento (obrigatório)
- --seed: Semente para gerador aleatório (padrão: 75)
- -o, --out: Pasta de saída (padrão: 'results')

**Exemplo:**
`ash
python unified/sim_ca_main4.py -e cult_experiment
`

### 3. NSGA-II via pymoo (z*)

`ash
python unified/z_experiment1_audition.py
`

**Nota:** Os arquivos z* são configurados para experimentos específicos e podem precisar de ajustes nos parâmetros internos.

## Estrutura de Experimentos

Os experimentos estão localizados em input/<experiment_name>/ e contêm:

- experiment.json: Configuração do experimento
- map.txt: Mapa estrutural do ambiente
- individuals.json: Configuração dos indivíduos
- positions.txt: Posições iniciais dos indivíduos

### Exemplo de experiment.json:
`json
{
    "experiment": "cult_experiment",
    "draw": false,
    "scenario_seed": [1],
    "simulation_seed": 14
}
`

## Saídas Esperadas

### Arquivos de Resultado
- es.json: Resultados da otimização com configurações ótimas
- output/<experiment>/: Visualizações da simulação (quando draw=true)

### Estrutura do res.json:
`json
[
  {
    "qtd_doors": 3,
    "iterations": 150,
    "distance": 250.5,
    "gene": [true, false, true, false],
    "generation": 45,
    "configuration": [{"x": 10, "y": 5}, ...]
  }
]
`

## Objetivos de Otimização

O sistema otimiza três objetivos simultaneamente:

1. **Quantidade de portas** (minimizar): Reduzir o número de portas necessárias
2. **Iterações** (minimizar): Reduzir o tempo de evacuação
3. **Distância** (minimizar): Reduzir a distância total percorrida pelos indivíduos

## Exemplos de Execução

### Exemplo 1: Otimização básica
`ash
python unified/sim_ca_main3.py -e cult_experiment --pop_size 30 --max_gen 100
`

### Exemplo 2: Análise de força bruta
`ash
python unified/sim_ca_main4.py -e audition_experiment
`

### Exemplo 3: Experimentos com pymoo
`ash
python unified/z_experiment1_audition.py
`

## Troubleshooting

### Problemas Comuns

1. **Erro de importação**: Verifique se todas as dependências estão instaladas
2. **Arquivo de experimento não encontrado**: Verifique se o experimento existe em input/
3. **Erro de memória**: Reduza o tamanho da população ou número de gerações
4. **Simulação muito lenta**: Desabilite o desenho (draw: false no experiment.json)

### Logs e Debug

- Ative o modo verbose nos arquivos z* para acompanhar o progresso
- Verifique os logs de simulação em output/<experiment>/logs/
- Use --seed para reproduzir resultados

## Próximos Passos

Consulte os documentos adicionais na pasta docs/:
- FILE_ROLES.md: Mapa de responsabilidades por arquivo
- API_REFERENCE.md: Referência completa da API
- ARCHITECTURE.md: Diagramas e fluxo do sistema
- TODOs_AND_REFACTORING.md: Melhorias recomendadas
