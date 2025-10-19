# Visão Geral da Arquitetura - Módulo Interface

## Arquitetura Geral do Sistema

O módulo `interface/` atua como a camada de apresentação de um sistema de simulação de evacuação, fornecendo uma interface web intuitiva para interação com algoritmos de otimização e simulação de multidões.

## Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                   │
│                        (interface/)                         │
├─────────────────────────────────────────────────────────────┤
│  App.py (Entry Point)                                      │
│  ├── Menu de Navegação                                     │
│  ├── CSS Global                                            │
│  └── Layout Principal                                       │
├─────────────────────────────────────────────────────────────┤
│  Páginas de Interface (pages/)                             │
│  ├── Mapas.py (Gerenciamento de Mapas)                     │
│  ├── Parâmetros.py (Hub de Algoritmos)                     │
│  ├── Algoritmo_Genetico.py (Configuração AG)               │
│  ├── NSGA_II.py (Configuração NSGA-II)                     │
│  ├── Forca_Bruta.py (Configuração Força Bruta)             │
│  ├── Simulação.py (Configuração de Simulações)             │
│  ├── Detalhes.py (Detalhes de Mapas)                       │
│  └── Resultados.py (Visualização de Resultados)            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE PROCESSAMENTO                  │
│                  (simulador_heuristica/)                    │
├─────────────────────────────────────────────────────────────┤
│  Algoritmos de Otimização                                  │
│  ├── Algoritmo Genético (unified/mh_ga_*.py)               │
│  ├── NSGA-II (unified/mh_ga_nsgaii.py)                     │
│  └── Força Bruta (unified/h_brute_force.py)                │
├─────────────────────────────────────────────────────────────┤
│  Simulador de Multidões                                    │
│  ├── Simulador Principal (simulator/simulator.py)          │
│  ├── Mapas (simulator/*_map.py)                            │
│  ├── Indivíduos (simulator/individual.py)                  │
│  └── Cenários (simulator/scenario.py)                      │
└─────────────────────────────────────────────────────────────┘
```

## Fluxo de Dados

### 1. Upload e Configuração
```
Usuário → Interface → Upload de Arquivos → Armazenamento Local
```

**Detalhamento:**
- Usuário acessa páginas de algoritmos (Algoritmo_Genetico.py, NSGA_II.py, Forca_Bruta.py)
- Faz upload de arquivos de configuração (.json, .csv, .txt)
- Arquivos são salvos em `uploads/[algoritmo]/`

### 2. Configuração de Simulação
```
Mapa Selecionado → Parâmetros → Arquivo de Configuração → Simulação
```

**Detalhamento:**
- Usuário seleciona mapa em Mapas.py
- Configura parâmetros em Simulação.py
- Sistema prepara dados para processamento

### 3. Processamento
```
Interface → Simulador → Algoritmos → Resultados
```

**Detalhamento:**
- Interface envia configurações para simulador_heuristica/
- Algoritmos de otimização processam os dados
- Simulador executa simulações de evacuação
- Resultados são gerados e armazenados

### 4. Visualização
```
Resultados → Interface → Tabelas/Gráficos → Usuário
```

**Detalhamento:**
- Resultados são exibidos em Resultados.py
- Detalhes específicos em Detalhes.py
- Interface permite navegação e análise

## Conexões com simulador_heuristica/

### Pontos de Integração

1. **Upload de Configurações**
   - **Origem**: Páginas de algoritmos (Algoritmo_Genetico.py, NSGA_II.py, Forca_Bruta.py)
   - **Destino**: Diretórios `uploads/[algoritmo]/`
   - **Formato**: Arquivos JSON, CSV ou TXT com parâmetros de configuração

2. **Execução de Simulações**
   - **Origem**: Simulação.py
   - **Destino**: Módulos do simulador_heuristica/
   - **Processo**: Chamada para algoritmos de otimização

3. **Visualização de Resultados**
   - **Origem**: Simulador_heuristica/ (output/)
   - **Destino**: Resultados.py, Detalhes.py
   - **Formato**: Dados tabulares e visualizações

### Estrutura de Dados Compartilhada

#### Arquivos de Configuração
```json
{
  "algoritmo": "NSGA-II",
  "parametros": {
    "populacao": 100,
    "geracoes": 50,
    "crossover_rate": 0.8,
    "mutation_rate": 0.1
  },
  "mapa": "igreja.png",
  "simulacao": {
    "individuos": 200,
    "tempo_maximo": 300
  }
}
```

#### Estrutura de Resultados
```json
{
  "simulacao_id": 1,
  "nome": "capacidade_maxima",
  "mapa": "igreja",
  "algoritmo": "NSGA-II",
  "status": "SIM",
  "resultados": {
    "tempo_evacuacao": 120,
    "eficiencia": 0.85,
    "posicoes_saidas": [...]
  }
}
```

## Padrões de Comunicação

### 1. Upload de Arquivos
- **Método**: Streamlit file_uploader
- **Validação**: Tipos de arquivo específicos
- **Armazenamento**: Sistema de arquivos local

### 2. Navegação entre Páginas
- **Método**: Links HTML com roteamento Streamlit
- **Estado**: Mantido pela sessão do Streamlit
- **Parâmetros**: Passados via query parameters

### 3. Exibição de Dados
- **Método**: Tabelas HTML customizadas
- **Imagens**: Base64 encoding para exibição
- **Responsividade**: CSS flexbox e grid

## Considerações de Design

### Princípios Arquiteturais

1. **Separação de Responsabilidades**
   - Interface: Apresentação e interação
   - Simulador: Processamento e algoritmos
   - Dados: Armazenamento e persistência

2. **Modularidade**
   - Páginas independentes para cada funcionalidade
   - CSS compartilhado para consistência
   - Componentes reutilizáveis

3. **Escalabilidade**
   - Estrutura preparada para novos algoritmos
   - Sistema de uploads organizado
   - Interface extensível

### Limitações Atuais

1. **Acoplamento com Streamlit**
   - Dependência forte do framework
   - Limitações de customização

2. **Armazenamento Local**
   - Dados não persistidos entre sessões
   - Sem banco de dados

3. **Processamento Síncrono**
   - Interface bloqueia durante processamento
   - Sem feedback de progresso

## Melhorias Futuras

### Arquitetura
- Implementar camada de API REST
- Adicionar banco de dados para persistência
- Implementar processamento assíncrono

### Interface
- Adicionar feedback de progresso
- Implementar validação de dados mais robusta
- Melhorar responsividade mobile

### Integração
- Implementar comunicação via API
- Adicionar logs de execução
- Melhorar tratamento de erros
