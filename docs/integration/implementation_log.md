# Log de Implementação da Integração

Este documento registra todas as modificações realizadas para implementar a integração entre a interface Streamlit e o simulador de heurística.

## Resumo das Modificações

### 1. Módulos de Integração Criados

#### `interface/services/simulator_integration.py`
- **Classe `SimulatorIntegration`**: Gerencia a comunicação com o simulador
  - `prepare_experiment_from_uploads()`: Copia arquivos de upload para o diretório de entrada
  - `run_simulator_cli()`: Executa o simulador via CLI
  - `read_results()`: Lê resultados gerados pelo simulador
  - `create_experiment_name()`: Gera nomes únicos para experimentos
  - `validate_upload_files()`: Valida arquivos de entrada

- **Classe `DatabaseIntegration`**: Gerencia persistência de dados
  - `save_simulation()`: Salva simulações no banco SQLite
  - `get_simulations()`: Recupera simulações do banco
  - `save_map()`: Salva mapas no banco

#### `interface/services/nsga_integration.py`
- **Classe `EvacuationChromosomeFactory`**: Fábrica de cromossomos para evacuação
  - Implementa interface necessária para NSGA-II
  - Decodifica genes em posições de portas
  - Gera mapas com portas posicionadas
  - Avalia soluções executando o simulador

- **Classe `NSGAIntegration`**: Coordena execução do NSGA-II
  - `load_configuration()`: Carrega configuração de arquivo
  - `setup_optimization()`: Configura otimização
  - `run_optimization()`: Executa algoritmo NSGA-II
  - `save_results()`: Salva resultados da otimização

### 2. Páginas da Interface Atualizadas

#### `interface/pages/Simulação.py`
**Modificações realizadas:**
- Adicionada integração com serviços de simulação
- Implementado upload de arquivos de indivíduos
- Adicionada execução de simulações via simulador
- Implementada visualização de resultados
- Integração com banco de dados para persistência

**Funcionalidades adicionadas:**
- Upload de arquivo de indivíduos (JSON)
- Configurações avançadas (seeds, modo de desenho)
- Execução de simulação com feedback visual
- Exibição de resultados (frames, relatórios, métricas)
- Salvamento automático no banco de dados

#### `interface/pages/Resultados.py`
**Modificações realizadas:**
- Integração com banco de dados SQLite
- Carregamento dinâmico de simulações
- Atualização em tempo real da lista

**Funcionalidades adicionadas:**
- Exibição de simulações do banco de dados
- Botão de atualização da lista
- Tratamento de casos sem dados

#### `interface/pages/NSGA_II.py`
**Modificações realizadas:**
- Integração completa com NSGA-II
- Upload de configuração e arquivos de entrada
- Execução de otimização multiobjetivo
- Visualização de resultados da frente de Pareto

**Funcionalidades adicionadas:**
- Upload de arquivo de configuração NSGA-II
- Upload de mapa e arquivo de indivíduos
- Configurações de otimização (gerações, população)
- Execução da otimização com feedback
- Salvamento de resultados

### 3. Script de Configuração

#### `setup_integration.py`
**Funcionalidades:**
- Criação automática de diretórios necessários
- Inicialização do banco de dados SQLite
- Verificação de dependências Python
- Validação da estrutura do simulador
- Criação de arquivos de configuração de exemplo

### 4. Estrutura de Diretórios Criada

```
interface/
├── services/
│   ├── __init__.py
│   ├── simulator_integration.py
│   └── nsga_integration.py
├── pages/
│   ├── Simulação.py (atualizada)
│   ├── Resultados.py (atualizada)
│   └── NSGA_II.py (atualizada)
└── ...

uploads/
├── algoritmo_genetico/
├── nsga_ii/
└── forca_bruta/

temp_simulation/
temp_nsga/
```

## Fluxos de Integração Implementados

### Fluxo A: Simulação Direta
1. Usuário seleciona mapa na interface
2. Faz upload de arquivo de indivíduos
3. Configura parâmetros de simulação
4. Clica em "Executar Simulação"
5. Sistema copia arquivos para `simulador_heuristica/input/<experiment>/`
6. Executa simulador via CLI
7. Lê resultados de `simulador_heuristica/output/<experiment>/`
8. Exibe resultados na interface
9. Salva simulação no banco de dados

### Fluxo B: Otimização NSGA-II
1. Usuário faz upload de configuração NSGA-II
2. Faz upload de mapa e arquivo de indivíduos
3. Configura parâmetros de otimização
4. Clica em "Executar Otimização NSGA-II"
5. Sistema configura fábrica de cromossomos
6. Executa NSGA-II com avaliação via simulador
7. Coleta frente de Pareto
8. Exibe soluções encontradas
9. Salva resultados em arquivo

## Pontos de Integração Preservados

### Contratos de I/O Mantidos
- **Entrada do simulador**: `map.txt` e `individuals.json` em `input/<experiment>/`
- **Saída do simulador**: Arquivos em `output/<experiment>/`
- **Formato de mapas**: Preservado exatamente como esperado
- **Formato de indivíduos**: JSON com estrutura `caracterizations`

### Lógica Principal Preservada
- Nenhuma modificação nos módulos do simulador
- Simulador executado como subprocesso via CLI
- Formatos de arquivo mantidos inalterados
- Comportamento do simulador preservado

## Arquivos de Configuração de Exemplo

### NSGA-II (`uploads/nsga_ii/example_config.json`)
```json
{
  "population_size": 20,
  "generations": 10,
  "crossover_rate": 0.8,
  "mutation_rate": 0.1,
  "description": "Configuração de exemplo para NSGA-II"
}
```

## Como Executar

### 1. Configuração Inicial
```bash
python setup_integration.py
```

### 2. Executar Interface
```bash
streamlit run interface/App.py
```

### 3. Executar Simulador Diretamente (opcional)
```bash
python -m simulador_heuristica.simulator.main -e cult_experiment
```

## Dependências Adicionadas

- `sqlite3` (built-in Python)
- `subprocess` (built-in Python)
- `pathlib` (built-in Python)
- `json` (built-in Python)

## Validações Implementadas

- Validação de arquivos de upload
- Verificação de dependências
- Validação de estrutura do simulador
- Tratamento de erros em execuções
- Limpeza de arquivos temporários

## Próximos Passos Recomendados

1. **Testes**: Implementar testes unitários para os módulos de integração
2. **Visualização**: Adicionar gráficos para frente de Pareto
3. **Configuração**: Interface para configuração de parâmetros do simulador
4. **Monitoramento**: Logs detalhados de execução
5. **Performance**: Otimização para execuções longas

## Notas Importantes

- Todos os arquivos originais foram preservados
- A integração é não-destrutiva
- O simulador mantém sua funcionalidade original
- A interface adiciona funcionalidades sem modificar o core
- O banco de dados é opcional e pode ser desabilitado
