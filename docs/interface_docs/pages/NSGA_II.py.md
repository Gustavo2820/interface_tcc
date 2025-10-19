# Documentação - pages/NSGA_II.py

## Visão Geral

O arquivo `NSGA_II.py` fornece uma interface para upload e configuração de arquivos de parametrização do algoritmo NSGA-II (Non-dominated Sorting Genetic Algorithm II). É uma página especializada para configuração de algoritmos genéticos multi-objetivo.

## Estrutura do Arquivo

### Imports e Dependências
```python
import streamlit as st
from pathlib import Path
```

**Dependências:**
- `streamlit`: Framework principal para interface web
- `pathlib`: Manipulação de caminhos de arquivos

### Configuração da Página
```python
st.set_page_config(page_title="NSGA-II", layout="wide")
```

## CSS e Estilos

### Menu Superior
```css
.menu {
    display: flex;
    justify-content: center;
    gap: 40px;
    margin-bottom: 40px;
    font-size: 20px;
    font-weight: 600;
}
```

**Estados dos Links:**
- **Normal**: Cor cinza (#bbb)
- **Hover**: Cor branca (#fff)
- **Ativo**: Cor branca com borda inferior azul

### Estilos Base
```css
body { 
    font-family: 'Inter', 'Roboto', sans-serif; 
    background-color: white; 
    color: #222; 
}
```

### Título e Linha Divisória
```css
.titulo { 
    text-align: center; 
    font-size: 36px; 
    font-weight: 700; 
    margin-bottom: 10px; 
}
.linha { 
    width: 200px; 
    height: 2px; 
    background-color: #444; 
    margin: 0 auto 40px auto; 
}
```

### Área de Upload
```css
.upload-box { 
    border: 2px dashed #142b3b; 
    border-radius: 12px; 
    padding: 40px; 
    background-color: #f9f9f9; 
    text-align: center; 
}
```

**Características:**
- Borda tracejada azul escuro (#142b3b)
- Fundo cinza claro (#f9f9f9)
- Padding generoso para área de drop
- Bordas arredondadas

### Mensagem de Sucesso
```css
.success { 
    text-align: center; 
    color: green; 
    font-weight: bold; 
    font-size: 18px; 
}
```

## Funcionalidades Principais

### 1. Upload de Arquivos
```python
arquivo = st.file_uploader(
    "Envie o arquivo de configuração para o algoritmo NSGA-II:", 
    type=["json", "csv", "txt"]
)
```

**Características:**
- Aceita múltiplos formatos (JSON, CSV, TXT)
- Interface de drag & drop
- Validação de tipo de arquivo
- Texto específico para NSGA-II

### 2. Processamento de Upload
```python
if arquivo:
    pasta = Path("uploads/nsga_ii")
    pasta.mkdir(parents=True, exist_ok=True)
    caminho = pasta / arquivo.name
    with open(caminho, "wb") as f:
        f.write(arquivo.getbuffer())
    st.markdown(f'<p class="success">✅ Arquivo "{arquivo.name}" enviado com sucesso!</p>', unsafe_allow_html=True)
```

**Funcionalidades:**
- Cria diretório específico para NSGA-II
- Salva arquivo com nome original
- Feedback visual de sucesso
- Criação automática de diretórios

### 3. Estrutura de Armazenamento
```
uploads/
└── nsga_ii/
    ├── config1.json
    ├── params.csv
    └── settings.txt
```

**Organização:**
- Diretório dedicado para NSGA-II
- Preserva nomes originais dos arquivos
- Estrutura hierárquica clara

## Estrutura HTML

### Menu de Navegação
```html
<div class="menu">
    <a href="../app">Menu</a>
    <a href="./Mapas">Mapas</a>
    <a href="./Parâmetros" class="active">Parâmetros</a>
    <a href="./Resultados">Resultados</a>
    <a href="./Documentação">Documentação</a>
</div>
```

### Título da Página
```html
<div class="titulo">NSGA-II</div>
<div class="linha"></div>
```

### Área de Upload
```html
<div class="upload-box">
    <!-- Streamlit file_uploader widget -->
</div>
```

## Fluxo de Execução

### 1. Inicialização
1. Configuração da página Streamlit
2. Aplicação de estilos CSS
3. Renderização do menu de navegação

### 2. Renderização
1. Exibição do título "NSGA-II"
2. Renderização da linha divisória
3. Criação da área de upload

### 3. Interação
1. Usuário seleciona arquivo
2. Sistema valida tipo de arquivo
3. Arquivo é salvo no diretório específico
4. Feedback de sucesso é exibido

## Responsabilidades

### Principais
- **Upload de Configurações**: Interface para envio de arquivos NSGA-II
- **Validação**: Verificação de tipos de arquivo aceitos
- **Armazenamento**: Organização de arquivos por algoritmo
- **Feedback**: Confirmação visual de sucesso

### Secundárias
- **Navegação**: Menu consistente com outras páginas
- **Interface**: Design limpo e intuitivo
- **Organização**: Estrutura de diretórios específica

## Formatos de Arquivo Suportados

### 1. Formato Unificado (Recomendado) ⭐
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

### 2. Formato Legado (Compatibilidade)
```json
{
  "population_size": 20,
  "generations": 10,
  "crossover_rate": 0.8,
  "mutation_rate": 0.1,
  "description": "Configuração legada"
}
```

## Parâmetros Específicos do NSGA-II

### Formato Unificado

#### NSGA-II (`nsga_config`)
- **population_size**: Tamanho da população (5-100)
- **generations**: Número de gerações (1-100)
- **crossover_rate**: Taxa de crossover (0.0-1.0)
- **mutation_rate**: Taxa de mutação (0.0-1.0)

#### Simulação (`simulation_params`)
- **scenario_seed**: Seed para geração do cenário (opcional)
- **simulation_seed**: Seed para execução da simulação (opcional)
- **draw_mode**: Gerar imagens de saída (true/false)
- **verbose**: Modo verboso (true/false)

### Formato Legado (Compatibilidade)
- **population_size**: Tamanho da população
- **generations**: Número de gerações
- **crossover_rate**: Taxa de crossover
- **mutation_rate**: Taxa de mutação
- **description**: Descrição opcional da configuração

## Dependências

### Internas
- Nenhuma dependência de outros módulos

### Externas
- **streamlit**: Framework principal
- **pathlib**: Manipulação de caminhos
- **Sistema de Arquivos**: Para armazenamento

## Limitações

### Funcionais
- **Sem Validação de Conteúdo**: Não verifica estrutura interna dos arquivos
- **Sem Preview**: Não exibe conteúdo do arquivo
- **Sem Edição**: Não permite modificar arquivos enviados
- **Sem Validação de Objetivos**: Não verifica se objetivos são válidos

### Técnicas
- **Sem Tratamento de Erros**: Não captura erros de escrita
- **Sem Compressão**: Não otimiza tamanho dos arquivos
- **Sem Backup**: Não cria cópias de segurança

## Melhorias Sugeridas

### Funcionais
1. **Validação de Objetivos**: Verificar se objetivos são válidos
2. **Preview**: Exibir conteúdo antes do upload
3. **Templates**: Fornecer modelos específicos para NSGA-II
4. **Validação de Constraints**: Verificar restrições
5. **Wizard**: Assistente para configuração

### Técnicas
1. **Tratamento de Erros**: Capturar e exibir erros
2. **Validação**: Verificar integridade dos arquivos
3. **Compressão**: Otimizar armazenamento
4. **Backup**: Sistema de versionamento
5. **Logs**: Registrar atividades de upload

### Interface
1. **Formulário**: Interface de formulário para parâmetros
2. **Validação Visual**: Feedback em tempo real
3. **Help**: Ajuda contextual para parâmetros
4. **Presets**: Configurações pré-definidas
5. **Export**: Exportar configurações

## Integração com Simulador

### Fluxo de Dados
1. **Upload**: Usuário envia arquivo de configuração
2. **Armazenamento**: Arquivo salvo em `uploads/nsga_ii/`
3. **Processamento**: Simulador lê arquivo de configuração
4. **Execução**: NSGA-II é executado com parâmetros
5. **Resultados**: Fronts de Pareto retornados

### Estrutura Esperada
O simulador espera arquivos com parâmetros específicos do NSGA-II:
- Parâmetros básicos de algoritmo genético
- Definição de objetivos múltiplos
- Configuração de restrições
- Parâmetros de convergência
- Configurações de elitismo e crowding

## Diferenças do Algoritmo Genético Simples

### Multi-objetivo
- **Objetivos Múltiplos**: Otimiza vários objetivos simultaneamente
- **Front de Pareto**: Gera conjunto de soluções não-dominadas
- **Crowding Distance**: Mantém diversidade no front

### Seleção
- **Non-dominated Sorting**: Classifica soluções por dominância
- **Crowding Distance**: Usado como critério de desempate
- **Elitismo**: Preserva melhores soluções

### Aplicação
- **Problemas Complexos**: Ideal para problemas com múltiplos objetivos conflitantes
- **Evacuação**: Otimiza tempo e eficiência simultaneamente
- **Trade-offs**: Permite análise de compromissos entre objetivos
