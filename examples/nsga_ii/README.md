# Configurações de Exemplo - NSGA-II

Este diretório contém arquivos de configuração de exemplo para o algoritmo NSGA-II.

## Arquivos disponíveis:

### `example_config.json`
Configuração padrão para testes:
- **População**: 20 indivíduos
- **Gerações**: 10
- **Taxa de crossover**: 0.8
- **Taxa de mutação**: 0.1

### `config_light.json`
Configuração leve para testes rápidos:
- **População**: 8 indivíduos  
- **Gerações**: 3
- **Taxa de crossover**: 0.8
- **Taxa de mutação**: 0.1

> **Nota**: Esta configuração executa apenas ~24 simulações, ideal para validação rápida.

## Como usar:

1. Copie um dos arquivos de exemplo para `uploads/nsga_ii/`
2. Renomeie para `config.json` ou outro nome de sua escolha
3. Ajuste os parâmetros conforme necessário
4. Carregue na interface Streamlit

## Parâmetros explicados:

- **population_size**: Número de indivíduos na população
- **generations**: Número de gerações para evolução
- **crossover_rate**: Probabilidade de crossover (0.0 a 1.0)
- **mutation_rate**: Probabilidade de mutação (0.0 a 1.0)
- **description**: Descrição opcional da configuração
