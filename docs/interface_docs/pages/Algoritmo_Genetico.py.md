# Documentação - pages/Algoritmo_Genetico.py

## Visão Geral

O arquivo `Algoritmo_Genetico.py` fornece uma interface para upload e configuração de arquivos de parametrização do Algoritmo Genético. É uma página especializada que permite aos usuários enviar arquivos de configuração para execução do algoritmo evolutivo.

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
st.set_page_config(page_title="Algoritmo Genético", layout="wide")
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
    border: 2px dashed #083d77; 
    border-radius: 12px; 
    padding: 40px; 
    background-color: #f9f9f9; 
    text-align: center; 
}
```

**Características:**
- Borda tracejada azul (#083d77)
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
    "Selecione o arquivo de parametrização (formato .json, .csv ou .txt):", 
    type=["json", "csv", "txt"]
)
```

**Características:**
- Aceita múltiplos formatos (JSON, CSV, TXT)
- Interface de drag & drop
- Validação de tipo de arquivo
- Texto descritivo claro

### 2. Processamento de Upload
```python
if arquivo:
    pasta = Path("uploads/algoritmo_genetico")
    pasta.mkdir(parents=True, exist_ok=True)
    caminho = pasta / arquivo.name
    with open(caminho, "wb") as f:
        f.write(arquivo.getbuffer())
    st.markdown(f'<p class="success">✅ Arquivo "{arquivo.name}" enviado com sucesso!</p>', unsafe_allow_html=True)
```

**Funcionalidades:**
- Cria diretório específico para o algoritmo
- Salva arquivo com nome original
- Feedback visual de sucesso
- Criação automática de diretórios

### 3. Estrutura de Armazenamento
```
uploads/
└── algoritmo_genetico/
    ├── config1.json
    ├── params.csv
    └── settings.txt
```

**Organização:**
- Diretório dedicado por algoritmo
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
<div class="titulo">Algoritmo Genético</div>
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
1. Exibição do título "Algoritmo Genético"
2. Renderização da linha divisória
3. Criação da área de upload

### 3. Interação
1. Usuário seleciona arquivo
2. Sistema valida tipo de arquivo
3. Arquivo é salvo no diretório específico
4. Feedback de sucesso é exibido

## Responsabilidades

### Principais
- **Upload de Configurações**: Interface para envio de arquivos
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
  "populacao": 100,
  "geracoes": 50,
  "crossover_rate": 0.8,
  "mutation_rate": 0.1,
  "elitismo": true
}
```

### 2. CSV (.csv)
```csv
parametro,valor
populacao,100
geracoes,50
crossover_rate,0.8
mutation_rate,0.1
```

### 3. TXT (.txt)
```
populacao=100
geracoes=50
crossover_rate=0.8
mutation_rate=0.1
```

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
- **Sem Histórico**: Não mantém histórico de uploads

### Técnicas
- **Sem Tratamento de Erros**: Não captura erros de escrita
- **Sem Compressão**: Não otimiza tamanho dos arquivos
- **Sem Backup**: Não cria cópias de segurança

## Melhorias Sugeridas

### Funcionais
1. **Validação de Conteúdo**: Verificar estrutura dos arquivos
2. **Preview**: Exibir conteúdo antes do upload
3. **Edição**: Permitir modificar parâmetros
4. **Histórico**: Listar uploads anteriores
5. **Templates**: Fornecer modelos de configuração

### Técnicas
1. **Tratamento de Erros**: Capturar e exibir erros
2. **Validação**: Verificar integridade dos arquivos
3. **Compressão**: Otimizar armazenamento
4. **Backup**: Sistema de versionamento
5. **Logs**: Registrar atividades de upload

### Interface
1. **Progress Bar**: Indicador de progresso
2. **Drag & Drop**: Interface mais intuitiva
3. **Múltiplos Arquivos**: Upload em lote
4. **Preview**: Visualização de conteúdo
5. **Validação Visual**: Feedback em tempo real

## Integração com Simulador

### Fluxo de Dados
1. **Upload**: Usuário envia arquivo de configuração
2. **Armazenamento**: Arquivo salvo em `uploads/algoritmo_genetico/`
3. **Processamento**: Simulador lê arquivo de configuração
4. **Execução**: Algoritmo genético é executado
5. **Resultados**: Dados retornados para visualização

### Estrutura Esperada
O simulador espera arquivos com parâmetros específicos do algoritmo genético:
- Tamanho da população
- Número de gerações
- Taxa de crossover
- Taxa de mutação
- Configurações de elitismo
- Critérios de parada
