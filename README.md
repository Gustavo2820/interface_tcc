# Sistema de Simulação e Otimização de Evacuação de Multidões

Sistema completo para simulação de evacuação de multidões usando Cellular Automata (CA) com otimização multiobjetivo da configuração de portas de saída. Inclui interface web desenvolvida em Streamlit para configuração, execução e análise de simulações.

## 📋 Índice

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Uso Rápido](#uso-rápido)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Documentação](#documentação)
- [Conceitos Básicos](#conceitos-básicos)

## ✨ Características

### Algoritmos de Otimização
- **NSGA-II Pymoo**: Implementação baseada na biblioteca pymoo com 3 objetivos (portas, iterações, distância)
- **NSGA-II Cached**: Implementação customizada com cache de avaliações para evitar re-simulações
- **Força Bruta**: Exploração exaustiva de combinações de portas

### Interface Web
- **Criação de Mapas**: Editor visual com validação automática
- **Configuração de Parâmetros**: Sistema de presets e configuração unificada
- **Execução de Simulações**: Otimização multiobjetivo com NSGA-II e Força Bruta
- **Análise de Resultados**: Visualização de métricas e Fronteira de Pareto
- **Gestão de Dados**: Banco de dados SQLite

### Simulador
- Modelo baseado em Cellular Automata (CA)
- Campos estáticos (paredes, portas, obstáculos) e dinâmicos (densidade, fluxo)
- Métricas detalhadas (tempo de evacuação, distância percorrida, eficiência)
- Suporte para múltiplas sementes de simulação

## 🔧 Requisitos

### Sistema
- Python 3.8 ou superior
- 4GB RAM (mínimo), 8GB recomendado
- Sistema operacional: Linux, macOS ou Windows

### Dependências Python
Principais bibliotecas necessárias:
- `streamlit` - Interface web
- `numpy` - Computação numérica
- `pandas` - Manipulação de dados
- `pymoo` - Algoritmos evolutivos
- `Pillow` - Processamento de imagens
- `matplotlib` - Visualização (opcional)

## 📦 Instalação

### 1. Clone o Repositório
```bash
git clone <repository-url>
cd interface_tcc
```

### 2. Crie um Ambiente Virtual
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate  # Windows
```

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o Ambiente
```bash
python setup_integration.py
```

Este script irá:
- Criar diretórios necessários (`uploads/`, `temp_nsga/`, etc.)
- Inicializar o banco de dados SQLite
- Verificar dependências
- Criar arquivos de configuração de exemplo

## 🚀 Uso Rápido

### Executar a Interface Web
```bash
streamlit run interface/App.py
```

A interface estará disponível em `http://localhost:8501`

### Fluxo Básico de Uso

1. **Criar/Importar Mapa**
   - Acesse a página "Mapas"
   - Use o editor visual ou faça upload de imagem PNG
   - Defina células vazias, paredes, portas e obstáculos

2. **Configurar Parâmetros**
   - Acesse "Parâmetros"
   - Escolha um algoritmo (NSGA-II, Força Bruta)
   - Carregue um preset ou configure manualmente
   - Salve a configuração

3. **Executar Simulação/Otimização**
   - Acesse "Simulação"
   - Selecione mapa e indivíduos
   - Carregue configuração salva
   - Execute otimização

4. **Analisar Resultados**
   - Acesse "Resultados"
   - Visualize métricas e comparações
   - Explore Fronteira de Pareto (otimização)
   - Exporte dados em JSON

### Executar Simulador Direto (CLI)
```bash
# Simulação simples
python -m simulador_heuristica.simulator.main -e meu_experimento

# Com opções
python -m simulador_heuristica.simulator.main -e meu_experimento -d -m 42 -s 100
```

Opções:
- `-e, --experiment`: Nome do experimento (requerido)
- `-d, --draw`: Gerar imagens de cada iteração
- `-m, --scenario_seed`: Semente para cenário
- `-s, --simulation_seed`: Semente para simulação

## 📁 Estrutura do Projeto

```
interface_tcc/
├── interface/              # Interface web Streamlit
│   ├── App.py             # Ponto de entrada principal
│   ├── pages/             # Páginas da interface
│   │   ├── Mapas.py       # Gestão de mapas
│   │   ├── Parâmetros.py  # Configuração
│   │   ├── Simulação.py   # Execução
│   │   └── Resultados.py  # Análise
│   └── services/          # Serviços de integração
│       ├── map_creation_integration.py
│       ├── nsga_integration.py
│       ├── nsga_cached_integration.py
│       ├── bruteforce_integration.py
│       └── simulator_integration.py
│
├── simulador_heuristica/  # Core do simulador
│   ├── simulator/         # Simulador principal
│   │   ├── main.py        # CLI do simulador
│   │   ├── scenario.py    # Configuração de cenários
│   │   └── simulator.py   # Motor de simulação
│   │
│   ├── unified/           # Módulos unificados
│   │   ├── mh_ga_nsgaii.py      # NSGA-II cached
│   │   ├── mh_ga_factory.py     # Factory de avaliação
│   │   ├── sim_ca_scenario.py   # Cenários CA
│   │   ├── sim_ca_simulator.py  # Simulador CA
│   │   └── sim_ca_*.py          # Componentes CA
│   │
│   └── heuristics/        # Algoritmos de otimização
│       └── brute_force.py
│
├── modulo_criacao_mapas/  # Criação e conversão de mapas
│   ├── map_converter.py
│   └── map_converter_utils.py
│
├── database/              # Banco de dados
│   ├── db.py              # Schema e inicialização
│   └── simulacoes.db      # SQLite database
│
├── presets/               # Configurações pré-definidas
│   ├── Teste_Rapido.json
│   ├── Producao_Media.json
│   └── Pesquisa_Pesada.json
│
├── docs/                  # Documentação
│   ├── ARCHITECTURE.md    # Arquitetura do sistema
│   ├── USER_GUIDE.md      # Guia do usuário
│   └── DEVELOPMENT.md     # Guia de desenvolvimento (APIs e exemplos)
│
├── tests/                 # Testes automatizados
├── scripts/               # Scripts auxiliares
├── uploads/               # Uploads de usuário
├── temp_nsga/             # Dados temporários NSGA
└── logs/                  # Logs de execução
```

## 📚 Documentação

A documentação completa está disponível na pasta `docs/`:

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Arquitetura do sistema, fluxo de dados e componentes
- **[USER_GUIDE.md](docs/USER_GUIDE.md)** - Guia detalhado de uso da interface
 - **[DEVELOPMENT.md](docs/DEVELOPMENT.md)** - Guia para desenvolvedores (APIs e integrações)
- **[DEVELOPMENT.md](docs/DEVELOPMENT.md)** - Guia para desenvolvedores
- **[UNIFIED_CONFIG_FORMAT.md](docs/UNIFIED_CONFIG_FORMAT.md)** - Formato de configuração unificada

## 🎓 Conceitos Básicos

### Cellular Automata (CA)
O simulador utiliza um modelo de Cellular Automata onde:
- O espaço é dividido em células (grid)
- Cada célula tem um estado (vazia, parede, porta, indivíduo)
- Indivíduos se movem baseado em campos estáticos e dinâmicos
- O sistema evolui em passos discretos (iterações)

### Campos Estáticos e Dinâmicos
**Campos Estáticos:**
- Estrutura do ambiente (paredes, portas)
- Não mudam durante a simulação
- Definem áreas navegáveis e saídas

**Campos Dinâmicos:**
- Densidade de pessoas (crowd map)
- Direções de movimento (dinamic map)
- Atualizados a cada iteração

### Otimização Multiobjetivo
O sistema otimiza simultaneamente:
1. **Número de Portas**: Minimizar (custo de construção)
2. **Iterações para Evacuação**: Minimizar (tempo total)
3. **Distância Total Percorrida**: Minimizar (eficiência de rotas)

Resultado: **Fronteira de Pareto** - conjunto de soluções ótimas onde melhorar um objetivo piora outro.

### Algoritmos Disponíveis

**NSGA-II (Non-dominated Sorting Genetic Algorithm II)**
- Algoritmo evolutivo multiobjetivo
- Mantém diversidade através de crowding distance
- Duas implementações: pymoo (padrão) e cached (customizada)

**Força Bruta**
- Testa todas as combinações possíveis de portas
- Garante encontrar a solução ótima
- Limitado a mapas pequenos devido à complexidade computacional

### Sistema de Presets
Presets são configurações salvas que incluem:
- Parâmetros do algoritmo (população, gerações, mutação)
- Parâmetros de simulação (sementes, iterações máximas)
- Formato unificado compatível com todos os algoritmos

### Banco de Dados e Persistência
- **SQLite**: Histórico de simulações, mapas e resultados
- **JSON**: Exportação de resultados e configurações
- **PNG**: Mapas visuais e frames de simulação

## 👥 Autores


## 📧 Contato

---

**Versão:** 1.0.0  
**Última Atualização:** Outubro 2024
