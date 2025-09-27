# Resumo da Documentação

## Índice de Documentos

###  Documentação Principal
- [README_PROJETO.md](./README_PROJETO.md) - Visão geral, instalação e execução
- [FILE_ROLES.md](./FILE_ROLES.md) - Mapa de responsabilidades por arquivo
- [API_REFERENCE.md](./API_REFERENCE.md) - Referência completa da API
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Diagramas e fluxo do sistema

## Estrutura do Projeto

###  Scripts de Execução
- **main3.py**: NSGA-II com cache
- **main4.py**: Força bruta
- **z_experiment*.py**: NSGA-II via pymoo

###  Módulos Core
- **h/**: Heurísticas base
- **mh/**: Meta-heurísticas (NSGA-II, GA)
- **sim_ca/**: Simulação por Cellular Automata

###  Interfaces
- **scenario**: Configuração de cenários
- **simulator**: Execução de simulação

## Objetivos de Otimização

1. **Quantidade de portas** (minimizar)
2. **Iterações** (minimizar)
3. **Distância** (minimizar)

## Como Executar

### NSGA-II com Cache
`ash
python unified/sim_ca_main3.py -e cult_experiment --pop_size 50 --max_gen 200
`

### Força Bruta
`ash
python unified/sim_ca_main4.py -e cult_experiment
`

### NSGA-II via pymoo
`ash
python unified/z_experiment1_audition.py
`

## Dependências

- Python 3.7+
- numpy==1.19.5
- matplotlib==3.3.4
- Pillow==8.1.0
- pymoo (para arquivos z*)



