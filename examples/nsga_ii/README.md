# Configurações de Exemplo - NSGA-II

Este diretório contém arquivos de configuração de exemplo para o algoritmo NSGA-II.

## Arquivos disponíveis:

### `unified_config.json` ⭐ **RECOMENDADO**
Configuração unificada padrão (NSGA-II + parâmetros de simulação):
- **População**: 20 indivíduos
- **Gerações**: 10
- **Taxa de crossover**: 0.8
- **Taxa de mutação**: 0.1
- **Inclui parâmetros de simulação**

### `unified_config_light.json` ⭐ **RECOMENDADO**
Configuração unificada leve para testes rápidos:
- **População**: 8 indivíduos  
- **Gerações**: 3
- **Taxa de crossover**: 0.8
- **Taxa de mutação**: 0.1
- **Inclui parâmetros de simulação**

> **Nota**: Esta configuração executa apenas ~24 simulações, ideal para validação rápida.

### `example_config.json` e `config_light.json`
Configurações legadas (apenas parâmetros NSGA-II):
- Mantidas para compatibilidade
- **Recomendado**: Use os arquivos `unified_config*.json`

## Estrutura da Configuração Unificada

```json
{
  "nsga_config": {
    "population_size": 20,
    "generations": 10,
    "crossover_rate": 0.8,
    "mutation_rate": 0.1
  },
  "simulation_params": {
    "scenario_seed": 42,
    "simulation_seed": 123,
    "draw_mode": true,
    "verbose": true
  },
  "description": "Configuração unificada para NSGA-II"
}
```

## Como usar:

1. Copie um dos arquivos de exemplo para `uploads/nsga_ii/`
2. Renomeie para `config.json` ou outro nome de sua escolha
3. Ajuste os parâmetros conforme necessário
4. Carregue na interface Streamlit

## Parâmetros explicados:

### NSGA-II (`nsga_config`)
- **population_size**: Número de indivíduos na população
- **generations**: Número de gerações para evolução
- **crossover_rate**: Probabilidade de crossover (0.0 a 1.0)
- **mutation_rate**: Probabilidade de mutação (0.0 a 1.0)

### Simulação (`simulation_params`)
- **scenario_seed**: Seed para geração do cenário (opcional)
- **simulation_seed**: Seed para execução da simulação (opcional)
- **draw_mode**: Gerar imagens de saída (true/false)
- **verbose**: Modo verboso (true/false)

### Geral
- **description**: Descrição opcional da configuração
