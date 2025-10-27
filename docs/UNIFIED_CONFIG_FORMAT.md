
# Formato de Preset / Configuração Unificada

Este documento descreve o formato de preset usado pelo projeto. Presets ficam na pasta `presets/` e são usados pela interface e pelos scripts de integração (`setup_integration.py`) como exemplos e pontos de partida.

Observação: os presets seguem um formato unificado que contém parâmetros de otimização (NSGA-II), parâmetros de simulação e metadados do preset.

## Estrutura mínima recomendada

```json
{
  "preset_name": "Teste Rápido",
  "description": "Descrição curta do preset",
  "nsga_config": {
    "population_size": 10,
    "generations": 5,
    "crossover_rate": 0.8,
    "mutation_rate": 0.1,
    "use_three_objectives": true
  },
  "simulation_params": {
    "scenario_seed": 42,
    "simulation_seed": 123,
    "max_iterations": 800,
    "draw_mode": false,
    "verbose": false
  },
  "bruteforce_config": {
    "max_doors": 10
  },
  "created_at": "2025-10-27T00:00:00",
  "version": "1.0"
}
```

## Campos e significado

- `preset_name` (string) — Nome humano do preset.
- `description` (string) — Texto livre descrevendo quando usar o preset.
- `nsga_config` (object) — Parâmetros do algoritmo NSGA-II:
  - `population_size` (int)
  - `generations` (int)
  - `crossover_rate` (float)
  - `mutation_rate` (float)
- `simulation_params` (object) — Parâmetros da simulação:
  - `scenario_seed` (int | array[int]) — Seed(s) para gerar cenários; pode ser um número ou uma lista de seeds para múltiplos cenários
  - `simulation_seed` (int) — Seed para a execução da simulação
  - `max_iterations` (int) — Limite de iterações por simulação
  - `draw_mode` (bool) — Se imagens/frames devem ser gerados
  - `verbose` (bool) — Verbosidade
- `bruteforce_config` (object, opcional) — Parâmetros usados pela integração de força bruta (por exemplo `max_doors`).
- `created_at` (string, ISO8601) — Data de criação do preset (opcional, mas recomendado).
- `version` (string) — Versão do schema/preset.

## Regras e boas práticas

- Prefira nomes claros em `preset_name` para facilitar a seleção na UI.
- Mantenha `scenario_seed` como número quando quiser um único cenário, ou como lista quando desejar avaliar vários cenários no mesmo experimento.
- Versione presets (campo `version`) quando alterar semanticamente os campos.

## Exemplos práticos

### Preset leve (Teste Rápido)

```json
{
  "preset_name": "Teste Rápido",
  "description": "Configuração leve para testes rápidos e desenvolvimento",
  "nsga_config": { "population_size": 10, "generations": 5, "crossover_rate": 0.8, "mutation_rate": 0.1 },
  "simulation_params": { "scenario_seed": 42, "simulation_seed": 123, "max_iterations": 800, "draw_mode": false, "verbose": false },
  "bruteforce_config": { "max_doors": 10 },
  "created_at": "2025-10-27T00:00:00",
  "version": "1.0"
}
```

### Preset de produção (exemplo gerado a partir do template)

```json
{
  "preset_name": "Produção Média",
  "description": "Configuração balanceada para uso geral",
  "nsga_config": { "population_size": 50, "generations": 30, "crossover_rate": 0.8, "mutation_rate": 0.15 },
  "simulation_params": { "scenario_seed": 42, "simulation_seed": 123, "max_iterations": 1000, "draw_mode": true, "verbose": false },
  "created_at": "2025-10-27T00:00:00",
  "version": "1.0"
}
```

## Compatibilidade com formatos legados

O código aceita formatos legados (onde os parâmetros NSGA-II estavam no nível superior) e tenta mapear para o formato unificado quando detectado.

## Onde colocar os presets

Coloque arquivos `.json` seguindo o schema acima em `presets/`. Prefira utilizar a interface para criar e editar presets (aba "Parâmetros)

## Exemplos prontos

Verifique `presets/` para presets fornecidos com o repositório (por exemplo `Teste_Rapido.json`, `Producao_Media.json`, `Pesquisa_Pesada.json`).

