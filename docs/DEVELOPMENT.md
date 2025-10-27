# Guia de Desenvolvimento

Documentação técnica para desenvolvedores contribuindo com o Sistema de Simulação e Otimização de Evacuação.

## 📋 Índice

- [Arquitetura](#arquitetura)
- [Estrutura de Código](#estrutura-de-código)
- [Fluxo de Dados](#fluxo-de-dados)
- [APIs e Integrações](#apis-e-integrações)
- [Adicionando Funcionalidades](#adicionando-funcionalidades)
- [Testes](#testes)
- [Convenções de Código](#convenções-de-código)

## 🏗️ Arquitetura

### Visão Geral

O sistema segue uma arquitetura em camadas:

```
┌─────────────────────────────────────────┐
│         Interface Web (Streamlit)       │
│     interface/pages/ + interface/App.py │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│      Camada de Integração (Services)    │
│         interface/services/             │
│  - nsga_integration.py                  │
│  - nsga_cached_integration.py           │
│  - bruteforce_integration.py            │
│  - simulator_integration.py             │
│  - map_creation_integration.py          │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│    Core do Simulador e Otimização       │
│      simulador_heuristica/              │
│  - simulator/ (simulador principal)     │
│  - unified/ (NSGA-II cached + CA)       │
│  - heuristics/ (força bruta)            │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│         Persistência de Dados           │
│  - database/ (SQLite)                   │
│  - uploads/ (arquivos JSON)             │
│  - logs/ (logging)                      │
└─────────────────────────────────────────┘
```

### Padrões Arquiteturais

**1. Factory Pattern**
- Usado em `mh_ga_factory.py` para criação de cenários
- Encapsula lógica de instanciação complexa
- Permite cache de avaliações

**2. Strategy Pattern**
- Algoritmos intercambiáveis (NSGA-II, Força Bruta)
- Interface comum via services
- Configuração unificada

**3. Singleton Pattern**
- Services exportados como instâncias únicas
- Evita re-inicialização de recursos
- Exemplo: `simulator_integration = SimulatorIntegration()`

## 📁 Estrutura de Código

### Módulos Principais

**interface/App.py**
- Ponto de entrada da aplicação Streamlit
- Configuração global (layout, CSS, menu)
- Gerenciamento de sessão

**interface/pages/**
- `Mapas.py`: CRUD de mapas
- `Parâmetros.py`: Configuração de algoritmos
- `Simulação.py`: Execução de simulações/otimizações
- `Resultados.py`: Visualização e análise
- `Detalhes.py`: Informações detalhadas

**interface/services/**
- **Integration Layer**: Adaptadores entre UI e core
- Responsabilidades:
  - Validação de entrada
  - Conversão de formatos
  - Chamadas ao simulador
  - Leitura de resultados

**simulador_heuristica/simulator/**
- `main.py`: CLI do simulador
- `scenario.py`: Configuração de cenários
- `simulator.py`: Motor de simulação CA

**simulador_heuristica/unified/**
- `mh_ga_nsgaii.py`: NSGA-II com cache
- `mh_ga_factory.py`: Factory de avaliação
- `mh_ga_instance.py`: Classe de instância
- `sim_ca_*.py`: Componentes CA (scenario, simulator, maps)

**database/db.py**
- Schema do banco de dados
- Funções de inicialização
- Migrations (se necessário)

## 🔄 Fluxo de Dados

### Otimização NSGA-II

```
1. Usuário configura parâmetros NSGA-II (UI)
   ↓
2. NSGAIntegration.setup_optimization()
   - Prepara mapa template
   - Extrai posições de portas possíveis
   - Cria problema pymoo
   ↓
3. NSGAIntegration.run_optimization()
   - Modo cached: CachedNSGAIntegration.run_optimization()
   - Modo pymoo: minimize(problem, NSGA2(), ...)
   ↓
4. Para cada avaliação:
   - EvacuationProblem._evaluate()
   - Gera mapa com portas específicas
   - Chama SimulatorIntegration.run_simulator_cli()
   - Extrai objetivos: [num_doors, iterations, distance]
   ↓
5. Algoritmo retorna Fronteira de Pareto
   ↓
6. NSGAIntegration.save_results()
   - Salva JSON com todas as soluções
   ↓
7. UI exibe Fronteira de Pareto
```

### Criação de Mapas

```
1. Usuário desenha mapa (UI) ou upload PNG
   ↓
2. MapCreationIntegration.validate_map_image()
   - Verifica dimensões (5x5 a 100x100)
   - Valida cores RGB
   - Confirma existência de portas
   ↓
3. MapCreationIntegration.convert_image_to_map()
   - Converte PNG → map.txt
   - Formato: largura altura\n + grid de códigos
   ↓
4. MapCreationIntegration.save_map()
   - Salva em mapas/<nome>.txt
   - Registra no banco de dados
   ↓
5. MapCreationIntegration.generate_map_preview()
   - Cria PNG de visualização
```

## 🔌 APIs e Integrações

### SimulatorIntegration

**Principais Métodos:**

```python
prepare_experiment_from_uploads(experiment_name, map_file, individuals_file)
# Prepara arquivos de entrada para simulador

run_simulator_cli(experiment_name, draw=False, scenario_seed=None, 
                 simulation_seed=None, max_iterations=None)
# Executa simulador via subprocess

read_results(experiment_name)
# Lê resultados de simulador_heuristica/output/<experiment>/

save_simulation(nome, algoritmo, mapa_id, resultado, executada=1, ...)
# Salva simulação no banco de dados
```

**Uso Típico:**

```python
from interface.services.simulator_integration import simulator_integration

# Preparar experimento
simulator_integration.prepare_experiment_from_uploads(
    "teste_001", 
    map_file, 
    individuals_file
)

# Executar
result = simulator_integration.run_simulator_cli(
    "teste_001",
    draw=True,
    simulation_seed=42
)

# Ler resultados
data = simulator_integration.read_results("teste_001")
metrics = data.get('metrics', {})
```

### NSGAIntegration

**Principais Métodos:**

```python
load_configuration(config_file)
# Carrega configuração unificada (JSON)

setup_optimization(map_template, individuals_data)
# Prepara otimização (extrai portas, cria problema)

run_optimization(experiment_name=None)
# Executa NSGA-II (pymoo ou cached)

save_results(pareto_front, output_file)
# Salva Fronteira de Pareto em JSON
```

**Uso Típico:**

```python
from interface.services.nsga_integration import nsga_integration

# Carregar config
nsga_integration.load_configuration("presets/Producao_Media.json")

# Setup
nsga_integration.setup_optimization(map_template, individuals_data)

# Executar
result = nsga_integration.run_optimization(experiment_name="opt_001")

# Salvar
nsga_integration.save_results(
    result['results'], 
    "uploads/nsga_ii/result_001.json"
)
```

### MapCreationIntegration

**Principais Métodos:**

```python
validate_map_image(image)
# Valida imagem PNG para conversão

convert_image_to_map(image, output_path)
# Converte PNG → map.txt

save_map(name, map_content)
# Salva mapa em arquivo

generate_map_preview(map_path)
# Gera PNG de preview
```

## ➕ Adicionando Funcionalidades

### Nova Página Streamlit

1. **Criar arquivo em `interface/pages/`**

```python
# interface/pages/MinhaNovaPage.py
import streamlit as st
from interface.services.simulator_integration import simulator_integration

st.set_page_config(page_title="Minha Nova Página", page_icon="🎯")

st.title("🎯 Minha Nova Funcionalidade")

# Seu código aqui
```

2. **Acessar via navegação**
   - Streamlit detecta automaticamente arquivos em `pages/`
   - Aparece no menu lateral

### Novo Algoritmo de Otimização

1. **Criar integration service**

```python
# interface/services/meu_algoritmo_integration.py
from pathlib import Path
from .simulator_integration import simulator_integration

class MeuAlgoritmoIntegration:
    def __init__(self):
        self.config = {}
    
    def load_configuration(self, config_file):
        # Carregar config
        pass
    
    def run_optimization(self, experiment_name):
        # Lógica do algoritmo
        # Usar simulator_integration para executar simulações
        pass
    
    def save_results(self, results, output_file):
        # Salvar resultados
        pass

# Singleton
meu_algoritmo_integration = MeuAlgoritmoIntegration()
```

2. **Integrar na UI**

```python
# Em interface/pages/Parâmetros.py
algoritmo = st.selectbox(
    "Algoritmo",
    ["NSGA-II", "Força Bruta", "Meu Algoritmo"]  # Adicionar aqui
)

if algoritmo == "Meu Algoritmo":
    from interface.services.meu_algoritmo_integration import meu_algoritmo_integration
    # Configurar...
```

### Novo Tipo de Visualização

1. **Adicionar em `interface/pages/Resultados.py`**

```python
import matplotlib.pyplot as plt

def plot_minha_visualizacao(data):
    fig, ax = plt.subplots()
    # Plotar dados
    ax.plot(data['x'], data['y'])
    ax.set_title("Minha Visualização")
    return fig

# Usar na página
if st.button("Mostrar Minha Visualização"):
    data = {...}  # Obter dados
    fig = plot_minha_visualizacao(data)
    st.pyplot(fig)
```

## 🧪 Testes

### Estrutura de Testes

```
tests/
├── test_integration_api.py       # Testes de integração
├── test_nsga_cached.py           # Testes NSGA-II cached
├── test_simulator_outputs.py     # Testes de saída do simulador
└── test_streamlit_pages.py       # Testes de páginas
```

### Executar Testes

```bash
# Todos os testes
pytest tests/

# Teste específico
pytest tests/test_integration_api.py

# Com cobertura
pytest --cov=interface --cov=simulador_heuristica tests/

# Verbose
pytest -v tests/
```

### Escrever Novos Testes

```python
# tests/test_minha_feature.py
import pytest
from interface.services.meu_algoritmo_integration import meu_algoritmo_integration

def test_load_configuration():
    # Arrange
    config_file = "presets/Teste_Rapido.json"
    
    # Act
    result = meu_algoritmo_integration.load_configuration(config_file)
    
    # Assert
    assert result is True
    assert meu_algoritmo_integration.config is not None

def test_run_optimization():
    # Setup
    meu_algoritmo_integration.load_configuration("presets/Teste_Rapido.json")
    
    # Executar
    result = meu_algoritmo_integration.run_optimization("test_exp")
    
    # Verificar
    assert result is not None
    assert 'results' in result
```

## 📝 Convenções de Código

### Python Style Guide

Seguir **PEP 8**:

```python
# Bom
def calculate_evacuation_time(iterations, max_iterations):
    """
    Calcula tempo de evacuação baseado em iterações.
    
    Args:
        iterations: Número de iterações até evacuação
        max_iterations: Limite máximo de iterações
        
    Returns:
        float: Tempo normalizado (0.0 a 1.0)
    """
    return iterations / max_iterations

# Evitar
def calcTime(i,m):
    return i/m
```

### Docstrings

Usar formato **Google Style**:

```python
def minha_funcao(param1, param2):
    """
    Breve descrição em uma linha.
    
    Descrição mais detalhada do que a função faz,
    se necessário.
    
    Args:
        param1 (str): Descrição do primeiro parâmetro
        param2 (int): Descrição do segundo parâmetro
        
    Returns:
        dict: Descrição do retorno
        
    Raises:
        ValueError: Quando param2 é negativo
        
    Example:
        >>> minha_funcao("teste", 42)
        {'resultado': 'sucesso'}
    """
    # Implementação
```

### Logging

```python
from interface.services.logger import default_log as logger

# Usar níveis apropriados
logger.debug("Informação de debug detalhada")
logger.info("Informação geral do fluxo")
logger.warning("Aviso de condição não-crítica")
logger.error("Erro que afeta operação")
logger.exception("Erro com traceback completo")
```

### Tratamento de Erros

```python
# Específico e informativo
try:
    result = simulator_integration.run_simulator_cli(experiment)
except FileNotFoundError as e:
    logger.error(f"Arquivo de entrada não encontrado: {e}")
    st.error("⚠️ Arquivos de entrada não encontrados. Verifique mapa e indivíduos.")
    return None
except subprocess.CalledProcessError as e:
    logger.error(f"Simulador falhou: {e.stderr}")
    st.error(f"❌ Erro ao executar simulador: {e.stderr}")
    return None
except Exception as e:
    logger.exception("Erro inesperado ao executar simulação")
    st.error(f"❌ Erro inesperado: {str(e)}")
    return None
```

### Commits

Mensagens de commit claras:

```bash
# Bom
git commit -m "Adiciona validação de dimensões de mapa"
git commit -m "Fix: Corrige cálculo de distância em sim_ca_simulator"
git commit -m "Refactor: Extrai lógica de conversão para helper"

# Evitar
git commit -m "mudanças"
git commit -m "fix bug"
git commit -m "wip"
```

## 🔧 Ferramentas de Desenvolvimento

### Setup do Ambiente

```bash
# Instalar em modo desenvolvimento
pip install -e .

# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Pre-commit hooks
pre-commit install
```

### Formatação de Código

```bash
# Black (formatador)
black interface/ simulador_heuristica/

# isort (organizar imports)
isort interface/ simulador_heuristica/

# flake8 (linter)
flake8 interface/ simulador_heuristica/
```

### Debugging

**Streamlit:**
```python
# Usar st.write para debug rápido
st.write("Debug:", variable)

# Expandir para ver estrutura
with st.expander("Debug Info"):
    st.json(complex_data)

# Session state
st.write("Session State:", st.session_state)
```

**Logs:**
```bash
# Acompanhar logs em tempo real
tail -f logs/interface.log
tail -f logs/simulator.log
```

---

**Versão:** 1.0  
**Atualizado:** Outubro 2024
