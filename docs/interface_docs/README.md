# Módulo Interface - Simulação de Evacuação

## Descrição Geral

O módulo `interface/` é uma aplicação web desenvolvida em Streamlit que fornece uma interface gráfica intuitiva para simulação de evacuação de emergência. A aplicação permite aos usuários gerenciar mapas, configurar parâmetros de algoritmos de otimização e visualizar resultados de simulações de evacuação.

## Estrutura de Diretórios

```
interface/
├── App.py                    # Arquivo principal da aplicação Streamlit
├── mapas/                    # Diretório para armazenamento de mapas
│   └── 1.py                  # Arquivo de configuração de mapas
├── pages/                    # Páginas da aplicação web
│   ├── Algoritmo_Genetico.py # Interface para configuração de Algoritmo Genético
│   ├── Detalhes.py          # Página de detalhes de mapas específicos
│   ├── Documentação.py      # Página de documentação (vazia)
│   ├── Forca_Bruta.py       # Interface para configuração de Força Bruta
│   ├── Mapas.py             # Gerenciamento e visualização de mapas
│   ├── NSGA_II.py           # Interface para configuração de NSGA-II
│   ├── Parâmetros.py        # Página principal de parametrização
│   ├── Resultados.py        # Visualização de resultados de simulações
│   ├── Simulação.py         # Interface de configuração de simulações
│   └── Simulado.py          # Página de simulação (vazia)
└── TCC.zip                  # Arquivo compactado do projeto
```

## Propósito de Cada Arquivo

### Arquivo Principal
- **App.py**: Ponto de entrada da aplicação, define o layout principal, CSS global e menu de navegação.

### Páginas de Navegação
- **Mapas.py**: Gerencia upload, visualização e seleção de mapas para simulação.
- **Parâmetros.py**: Página hub que direciona para diferentes algoritmos de otimização.
- **Resultados.py**: Exibe tabela de simulações executadas com status e detalhes.
- **Documentação.py**: Página destinada à documentação (atualmente vazia).

### Páginas de Algoritmos
- **Algoritmo_Genetico.py**: Interface para upload de arquivos de configuração do Algoritmo Genético.
- **NSGA_II.py**: Interface para upload de arquivos de configuração do algoritmo NSGA-II.
- **Forca_Bruta.py**: Interface para upload de arquivos de configuração do método Força Bruta.

### Páginas de Simulação
- **Simulação.py**: Interface para configuração de parâmetros de simulação específicos.
- **Detalhes.py**: Página de detalhes de mapas com visualização e tabela de simulações.
- **Simulado.py**: Página de execução de simulações (atualmente vazia).

### Diretório de Mapas
- **mapas/**: Armazena arquivos de imagem (.png) dos mapas de evacuação.
- **1.py**: Arquivo de configuração de mapas (atualmente vazio).

## Requisitos e Dependências

### Bibliotecas Python
- **streamlit**: Framework principal para interface web
- **pathlib**: Manipulação de caminhos de arquivos
- **PIL (Pillow)**: Processamento de imagens
- **pandas**: Manipulação de dados (usado em Detalhes.py)
- **base64**: Codificação de imagens para exibição
- **urllib.parse**: Codificação de URLs
- **shutil**: Operações de arquivos

### Instalação
```bash
pip install streamlit pillow pandas
```

## Como Executar

1. **Navegue até o diretório da interface:**
   ```bash
   cd interface/
   ```

2. **Execute a aplicação Streamlit:**
   ```bash
   streamlit run App.py
   ```

3. **Acesse no navegador:**
   ```
   http://localhost:8501
   ```

## Exemplos de Uso

### Fluxo Principal de Uso

1. **Seleção de Mapa**: Acesse "Mapas" para fazer upload ou selecionar um mapa existente.
2. **Configuração de Parâmetros**: Vá para "Parâmetros" e escolha o algoritmo desejado:
   - Algoritmo Genético
   - NSGA-II
   - Força Bruta
3. **Upload de Configuração**: Faça upload do arquivo de configuração (.json, .csv, .txt).
4. **Criação de Simulação**: Acesse "Simulação" para configurar parâmetros específicos.
5. **Visualização de Resultados**: Consulte "Resultados" para ver simulações executadas.

### Funcionalidades Principais

- **Upload de Mapas**: Suporte a arquivos .png com preview visual
- **Gerenciamento de Arquivos**: Upload de configurações para diferentes algoritmos
- **Interface Responsiva**: Design adaptável com CSS customizado
- **Navegação Intuitiva**: Menu superior consistente em todas as páginas
- **Visualização de Dados**: Tabelas e imagens integradas

## Características Técnicas

### Arquitetura
- **Single Page Application (SPA)**: Baseada em Streamlit com roteamento de páginas
- **CSS Customizado**: Estilos personalizados para interface moderna
- **Responsive Design**: Layout adaptável para diferentes tamanhos de tela

### Armazenamento
- **Uploads**: Arquivos salvos em `uploads/[algoritmo]/`
- **Mapas**: Imagens armazenadas em `mapas/`
- **Sessão**: Estado mantido pelo Streamlit

### Segurança
- **Validação de Tipos**: Upload restrito a formatos específicos
- **Sanitização**: URLs e nomes de arquivos tratados adequadamente

## Integração com o Projeto

O módulo interface se conecta com o `simulador_heuristica/` através de:
- Upload de arquivos de configuração que são processados pelo simulador
- Interface para execução de algoritmos de otimização
- Visualização de resultados gerados pelo simulador

Para mais detalhes sobre a arquitetura geral, consulte [overview.md](overview.md).
