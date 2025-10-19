# Documentação - pages/Forca_Bruta.py

## Visão Geral

O arquivo `Forca_Bruta.py` fornece uma interface para upload e configuração de arquivos de parametrização do método Força Bruta. É uma página especializada para configuração de algoritmos de busca exaustiva, utilizados para validação e comparação de resultados.

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
st.set_page_config(page_title="Força Bruta", layout="wide")
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
    border: 2px dashed #1e2b3b; 
    border-radius: 12px; 
    padding: 40px; 
    background-color: #f9f9f9; 
    text-align: center; 
}
```

**Características:**
- Borda tracejada azul escuro (#1e2b3b)
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
    "Selecione o arquivo de entrada para o método Força Bruta:", 
    type=["json", "csv", "txt"]
)
```

**Características:**
- Aceita múltiplos formatos (JSON, CSV, TXT)
- Interface de drag & drop
- Validação de tipo de arquivo
- Texto específico para Força Bruta

### 2. Processamento de Upload
```python
if arquivo:
    pasta = Path("uploads/forca_bruta")
    pasta.mkdir(parents=True, exist_ok=True)
    caminho = pasta / arquivo.name
    with open(caminho, "wb") as f:
        f.write(arquivo.getbuffer())
    st.markdown(f'<p class="success">✅ Arquivo "{arquivo.name}" enviado com sucesso!</p>', unsafe_allow_html=True)
```

**Funcionalidades:**
- Cria diretório específico para Força Bruta
- Salva arquivo com nome original
- Feedback visual de sucesso
- Criação automática de diretórios

### 3. Estrutura de Armazenamento
```
uploads/
└── forca_bruta/
    ├── config1.json
    ├── params.csv
    └── settings.txt
```

**Organização:**
- Diretório dedicado para Força Bruta
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
<div class="titulo">Força Bruta</div>
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
1. Exibição do título "Força Bruta"
2. Renderização da linha divisória
3. Criação da área de upload

### 3. Interação
1. Usuário seleciona arquivo
2. Sistema valida tipo de arquivo
3. Arquivo é salvo no diretório específico
4. Feedback de sucesso é exibido

## Responsabilidades

### Principais
- **Upload de Configurações**: Interface para envio de arquivos Força Bruta
- **Validação**: Verificação de tipos de arquivo aceitos
- **Armazenamento**: Organização de arquivos por algoritmo
- **Feedback**: Confirmação visual de sucesso

### Secundárias
- **Navegação**: Menu consistente com outras páginas
- **Interface**: Design limpo e intuitivo
- **Organização**: Estrutura de diretórios específica

## Formatos de Arquivo Suportados

### 1. JSON (.json)
```json
{
  "mapa": "igreja.png",
  "individuos": 200,
  "posicoes_saidas": [
    {"x": 10, "y": 20},
    {"x": 30, "y": 40}
  ],
  "objetivo": "minimizar_tempo_evacuacao",
  "restricoes": {
    "capacidade_maxima": 50,
    "distancia_minima": 5
  }
}
```

### 2. CSV (.csv)
```csv
parametro,valor
mapa,igreja.png
individuos,200
objetivo,minimizar_tempo_evacuacao
capacidade_maxima,50
```

### 3. TXT (.txt)
```
mapa=igreja.png
individuos=200
objetivo=minimizar_tempo_evacuacao
capacidade_maxima=50
```

## Parâmetros Específicos da Força Bruta

### Parâmetros Básicos
- **mapa**: Arquivo do mapa a ser utilizado
- **individuos**: Número de indivíduos na simulação
- **posicoes_saidas**: Lista de posições candidatas para saídas

### Parâmetros de Busca
- **espacamento**: Intervalo entre posições candidatas
- **limite_combinacoes**: Máximo de combinações a testar
- **timeout**: Tempo limite para execução

### Parâmetros de Otimização
- **objetivo**: Função objetivo a ser otimizada
- **restricoes**: Limitações do problema
- **criterio_parada**: Critério para parar a busca

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
- **Sem Validação de Posições**: Não verifica se posições são válidas

### Técnicas
- **Sem Tratamento de Erros**: Não captura erros de escrita
- **Sem Compressão**: Não otimiza tamanho dos arquivos
- **Sem Backup**: Não cria cópias de segurança

## Melhorias Sugeridas

### Funcionais
1. **Validação de Posições**: Verificar se posições são válidas no mapa
2. **Preview**: Exibir conteúdo antes do upload
3. **Templates**: Fornecer modelos específicos para Força Bruta
4. **Validação de Restrições**: Verificar restrições
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
2. **Armazenamento**: Arquivo salvo em `uploads/forca_bruta/`
3. **Processamento**: Simulador lê arquivo de configuração
4. **Execução**: Força Bruta testa todas as combinações
5. **Resultados**: Melhor solução encontrada

### Estrutura Esperada
O simulador espera arquivos com parâmetros específicos da Força Bruta:
- Definição do mapa e indivíduos
- Posições candidatas para saídas
- Parâmetros de busca e otimização
- Restrições e critérios de parada

## Características da Força Bruta

### Vantagens
- **Solução Ótima**: Garante encontrar a solução ótima
- **Simplicidade**: Algoritmo simples de implementar
- **Validação**: Útil para validar outros algoritmos
- **Determinístico**: Resultado sempre igual para mesma entrada

### Desvantagens
- **Complexidade**: Tempo de execução exponencial
- **Limitações**: Só viável para problemas pequenos
- **Recursos**: Consome muitos recursos computacionais
- **Escalabilidade**: Não escala para problemas grandes

### Aplicação
- **Validação**: Comparar com algoritmos heurísticos
- **Problemas Pequenos**: Quando espaço de busca é limitado
- **Benchmark**: Estabelecer limite superior de qualidade
- **Pesquisa**: Análise de comportamento de algoritmos
