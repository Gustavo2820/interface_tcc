# Formato de Configuração Unificada - NSGA-II

## Visão Geral

O formato de configuração unificada combina parâmetros do algoritmo NSGA-II e parâmetros de simulação em um único arquivo JSON, eliminando a redundância de múltiplos arquivos de configuração.

## Estrutura do Arquivo

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

## Parâmetros Detalhados

### NSGA-II (`nsga_config`)

| Parâmetro | Tipo | Range | Descrição |
|-----------|------|-------|-----------|
| `population_size` | integer | 5-100 | Tamanho da população |
| `generations` | integer | 1-100 | Número de gerações |
| `crossover_rate` | float | 0.0-1.0 | Taxa de crossover |
| `mutation_rate` | float | 0.0-1.0 | Taxa de mutação |

### Simulação (`simulation_params`)

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `scenario_seed` | integer | null | Seed para geração do cenário |
| `simulation_seed` | integer | null | Seed para execução da simulação |
| `draw_mode` | boolean | false | Gerar imagens de saída |
| `verbose` | boolean | false | Modo verboso |

### Geral

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `description` | string | Descrição opcional da configuração |

## Exemplos de Configuração

### Configuração Padrão
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
  "description": "Configuração padrão para NSGA-II"
}
```

### Configuração Leve (Testes Rápidos)
```json
{
  "nsga_config": {
    "population_size": 8,
    "generations": 3,
    "crossover_rate": 0.8,
    "mutation_rate": 0.1
  },
  "simulation_params": {
    "scenario_seed": 1,
    "simulation_seed": 1,
    "draw_mode": false,
    "verbose": false
  },
  "description": "Configuração leve para testes rápidos - apenas 24 simulações"
}
```

### Configuração de Produção
```json
{
  "nsga_config": {
    "population_size": 100,
    "generations": 50,
    "crossover_rate": 0.9,
    "mutation_rate": 0.05
  },
  "simulation_params": {
    "scenario_seed": 12345,
    "simulation_seed": 67890,
    "draw_mode": true,
    "verbose": false
  },
  "description": "Configuração de produção para resultados finais"
}
```

## Compatibilidade

### Formato Legado
O sistema mantém compatibilidade com o formato legado:

```json
{
  "population_size": 20,
  "generations": 10,
  "crossover_rate": 0.8,
  "mutation_rate": 0.1,
  "description": "Configuração legada"
}
```

### Detecção Automática
O sistema detecta automaticamente o formato:
- **Formato unificado**: Contém chave `nsga_config`
- **Formato legado**: Não contém chave `nsga_config`

## Vantagens do Formato Unificado

1. **Redução de Redundância**: Um único arquivo para todos os parâmetros
2. **Facilidade de Uso**: Menos arquivos para gerenciar
3. **Consistência**: Parâmetros relacionados agrupados logicamente
4. **Manutenibilidade**: Mais fácil de versionar e compartilhar
5. **Compatibilidade**: Suporte ao formato legado

## Como Usar

### 1. Na Interface Streamlit
1. Acesse a página NSGA-II
2. Faça upload do arquivo de configuração unificada
3. O sistema detectará automaticamente o formato
4. Configure mapa e indivíduos
5. Execute a otimização

### 2. Programaticamente
```python
from services.nsga_integration import NSGAIntegration

# Carrega configuração
nsga_integration = NSGAIntegration(simulator_integration)
nsga_integration.load_configuration(Path("unified_config.json"))

# Verifica formato
if nsga_integration.is_unified_config():
    print("Formato unificado detectado")
    sim_params = nsga_integration.get_simulation_params()
    print(f"Parâmetros de simulação: {sim_params}")
```

## Migração do Formato Legado

Para migrar configurações legadas para o formato unificado:

1. **Identifique os parâmetros NSGA-II** no arquivo legado
2. **Adicione parâmetros de simulação** conforme necessário
3. **Reestruture o JSON** seguindo o formato unificado
4. **Teste a configuração** antes de usar em produção

### Exemplo de Migração

**Antes (Legado):**
```json
{
  "population_size": 20,
  "generations": 10,
  "crossover_rate": 0.8,
  "mutation_rate": 0.1
}
```

**Depois (Unificado):**
```json
{
  "nsga_config": {
    "population_size": 20,
    "generations": 10,
    "crossover_rate": 0.8,
    "mutation_rate": 0.1
  },
  "simulation_params": {
    "draw_mode": true,
    "verbose": false
  },
  "description": "Migrado do formato legado"
}
```

## Arquivos de Exemplo

Os seguintes arquivos de exemplo estão disponíveis em `examples/nsga_ii/`:

- `unified_config.json` - Configuração padrão
- `unified_config_light.json` - Configuração para testes rápidos
- `example_config.json` - Formato legado (compatibilidade)
- `config_light.json` - Formato legado leve (compatibilidade)
