# Sumário da Documentação - Módulo Interface

## Visão Geral

Este documento apresenta um sumário completo de todos os arquivos do módulo `interface/` e seus respectivos propósitos. A documentação está organizada de forma hierárquica, facilitando a navegação e compreensão da estrutura do sistema.

## Estrutura de Arquivos

### Arquivo Principal
- **[App.py](App.py.md)** - Ponto de entrada da aplicação Streamlit, define layout geral e menu de navegação

### Páginas de Navegação
- **[pages/Mapas.py](pages/Mapas.py.md)** - Gerenciamento e visualização de mapas de evacuação
- **[pages/Parâmetros.py](pages/Parâmetros.py.md)** - Hub central para configuração de algoritmos de otimização
- **[pages/Resultados.py](pages/Resultados.py.md)** - Visualização de resultados de simulações executadas
- **[pages/Documentação.py](pages/Documentação.py.md)** - Página de documentação (atualmente vazia)

### Páginas de Algoritmos
- **[pages/Algoritmo_Genetico.py](pages/Algoritmo_Genetico.py.md)** - Interface para configuração do Algoritmo Genético
- **[pages/NSGA_II.py](pages/NSGA_II.py.md)** - Interface para configuração do algoritmo NSGA-II
- **[pages/Forca_Bruta.py](pages/Forca_Bruta.py.md)** - Interface para configuração do método Força Bruta

### Páginas de Simulação
- **[pages/Simulação.py](pages/Simulação.py.md)** - Interface para configuração de parâmetros de simulação
- **[pages/Detalhes.py](pages/Detalhes.py.md)** - Visualização detalhada de mapas específicos
- **[pages/Simulado.py](pages/Simulado.py.md)** - Página de execução de simulações (atualmente vazia)

### Diretório de Mapas
- **[mapas/1.py](mapas/1.py.md)** - Arquivo de configuração de mapas (atualmente vazio)

## Propósito de Cada Arquivo

### Arquivo Principal

#### App.py
- **Propósito**: Ponto de entrada da aplicação Streamlit
- **Responsabilidades**: 
  - Configuração global da página
  - Definição de estilos CSS
  - Menu de navegação principal
  - Layout da página inicial
- **Dependências**: streamlit
- **Status**: ✅ Documentado

### Páginas de Navegação

#### pages/Mapas.py
- **Propósito**: Gerenciamento de mapas de evacuação
- **Responsabilidades**:
  - Upload de novos mapas (.png)
  - Visualização de mapas existentes
  - Navegação para páginas de detalhes
  - Organização em layout de 3 colunas
- **Dependências**: streamlit, pathlib, shutil, base64, urllib.parse
- **Status**: ✅ Documentado

#### pages/Parâmetros.py
- **Propósito**: Hub central para algoritmos de otimização
- **Responsabilidades**:
  - Navegação para diferentes algoritmos
  - Interface consistente
  - Design de botões em formato de pastas
- **Dependências**: streamlit
- **Status**: ✅ Documentado

#### pages/Resultados.py
- **Propósito**: Visualização de resultados de simulações
- **Responsabilidades**:
  - Exibição de tabela com simulações
  - Interface de pesquisa (não funcional)
  - Tema escuro para visualização
- **Dependências**: streamlit
- **Status**: ✅ Documentado

#### pages/Documentação.py
- **Propósito**: Página de documentação
- **Responsabilidades**: (Arquivo vazio)
- **Dependências**: Nenhuma
- **Status**: ⚠️ Arquivo vazio

### Páginas de Algoritmos

#### pages/Algoritmo_Genetico.py
- **Propósito**: Configuração do Algoritmo Genético
- **Responsabilidades**:
  - Upload de arquivos de configuração
  - Validação de tipos de arquivo
  - Armazenamento em diretório específico
  - Feedback de sucesso
- **Dependências**: streamlit, pathlib
- **Status**: ✅ Documentado

#### pages/NSGA_II.py
- **Propósito**: Configuração do algoritmo NSGA-II
- **Responsabilidades**:
  - Upload de arquivos de configuração
  - Suporte a algoritmos multi-objetivo
  - Validação de parâmetros específicos
  - Armazenamento organizado
- **Dependências**: streamlit, pathlib
- **Status**: ✅ Documentado

#### pages/Forca_Bruta.py
- **Propósito**: Configuração do método Força Bruta
- **Responsabilidades**:
  - Upload de arquivos de configuração
  - Suporte a busca exaustiva
  - Validação de parâmetros
  - Armazenamento específico
- **Dependências**: streamlit, pathlib
- **Status**: ✅ Documentado

### Páginas de Simulação

#### pages/Simulação.py
- **Propósito**: Configuração de simulações de evacuação
- **Responsabilidades**:
  - Configuração de parâmetros
  - Visualização do mapa selecionado
  - Interface de duas colunas
  - Navegação para execução
- **Dependências**: streamlit, pathlib, PIL
- **Status**: ✅ Documentado

#### pages/Detalhes.py
- **Propósito**: Visualização detalhada de mapas
- **Responsabilidades**:
  - Exibição de imagem do mapa
  - Processamento de parâmetros da URL
  - Tabela de simulações relacionadas
  - Botões de navegação
- **Dependências**: streamlit, pandas, pathlib, base64, urllib.parse
- **Status**: ✅ Documentado

#### pages/Simulado.py
- **Propósito**: Execução de simulações
- **Responsabilidades**: (Arquivo vazio)
- **Dependências**: Nenhuma
- **Status**: ⚠️ Arquivo vazio

### Diretório de Mapas

#### mapas/1.py
- **Propósito**: Configuração de mapas
- **Responsabilidades**: (Arquivo vazio)
- **Dependências**: Nenhuma
- **Status**: ⚠️ Arquivo vazio

## Arquivos de Documentação

### Documentação Principal
- **[README.md](README.md)** - Documentação geral do módulo interface
- **[overview.md](overview.md)** - Visão geral da arquitetura e conexões
- **[SUMMARY.md](SUMMARY.md)** - Este arquivo de sumário

### Documentação Individual
- **[App.py.md](App.py.md)** - Documentação detalhada do App.py
- **[pages/Mapas.py.md](pages/Mapas.py.md)** - Documentação da página de mapas
- **[pages/Parâmetros.py.md](pages/Parâmetros.py.md)** - Documentação da página de parâmetros
- **[pages/Algoritmo_Genetico.py.md](pages/Algoritmo_Genetico.py.md)** - Documentação do algoritmo genético
- **[pages/NSGA_II.py.md](pages/NSGA_II.py.md)** - Documentação do NSGA-II
- **[pages/Forca_Bruta.py.md](pages/Forca_Bruta.py.md)** - Documentação da força bruta
- **[pages/Simulação.py.md](pages/Simulação.py.md)** - Documentação da página de simulação
- **[pages/Resultados.py.md](pages/Resultados.py.md)** - Documentação da página de resultados
- **[pages/Detalhes.py.md](pages/Detalhes.py.md)** - Documentação da página de detalhes

## Status da Documentação

### ✅ Completamente Documentados
- App.py
- pages/Mapas.py
- pages/Parâmetros.py
- pages/Algoritmo_Genetico.py
- pages/NSGA_II.py
- pages/Forca_Bruta.py
- pages/Simulação.py
- pages/Resultados.py
- pages/Detalhes.py

### ⚠️ Arquivos Vazios
- pages/Documentação.py
- pages/Simulado.py
- mapas/1.py

### 📝 Documentação Técnica
- Todos os arquivos Python possuem docstrings Google Style
- Documentação individual detalhada para cada arquivo
- Exemplos de uso e fluxos de execução
- Análise de limitações e melhorias sugeridas

## Dependências Gerais

### Bibliotecas Python
- **streamlit**: Framework principal para interface web
- **pathlib**: Manipulação de caminhos de arquivos
- **PIL (Pillow)**: Processamento de imagens
- **pandas**: Manipulação de dados
- **base64**: Codificação de imagens
- **urllib.parse**: Codificação de URLs
- **shutil**: Operações de arquivos

### Requisitos de Sistema
- Python 3.7+
- Navegador web moderno
- Sistema de arquivos para armazenamento

## Navegação da Documentação

### Por Funcionalidade
1. **Início**: [README.md](README.md)
2. **Arquitetura**: [overview.md](overview.md)
3. **Arquivo Principal**: [App.py.md](App.py.md)
4. **Navegação**: [pages/Mapas.py.md](pages/Mapas.py.md), [pages/Parâmetros.py.md](pages/Parâmetros.py.md), [pages/Resultados.py.md](pages/Resultados.py.md)
5. **Algoritmos**: [pages/Algoritmo_Genetico.py.md](pages/Algoritmo_Genetico.py.md), [pages/NSGA_II.py.md](pages/NSGA_II.py.md), [pages/Forca_Bruta.py.md](pages/Forca_Bruta.py.md)
6. **Simulação**: [pages/Simulação.py.md](pages/Simulação.py.md), [pages/Detalhes.py.md](pages/Detalhes.py.md)

### Por Tipo de Arquivo
- **Arquivos Python**: Todos os arquivos .py possuem documentação individual
- **Arquivos de Documentação**: README.md, overview.md, SUMMARY.md
- **Arquivos Vazios**: Identificados e documentados como tal

## Conclusão

A documentação do módulo `interface/` está completa e organizada, fornecendo uma visão abrangente de todos os componentes do sistema. Cada arquivo possui documentação técnica detalhada, incluindo propósitos, responsabilidades, dependências e limitações. A estrutura modular permite fácil navegação e manutenção da documentação.

Para mais detalhes sobre qualquer arquivo específico, consulte a documentação individual correspondente.
