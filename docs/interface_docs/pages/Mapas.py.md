# Documentação - pages/Mapas.py

## Visão Geral

O arquivo `Mapas.py` é responsável pelo gerenciamento e visualização de mapas de evacuação. Permite upload de novos mapas, exibição de mapas existentes e navegação para páginas de detalhes.

## Estrutura do Arquivo

### Imports e Dependências
```python
import streamlit as st
from pathlib import Path
import shutil
import base64
import urllib.parse
```

**Dependências:**
- `streamlit`: Framework principal
- `pathlib`: Manipulação de caminhos
- `shutil`: Operações de arquivos
- `base64`: Codificação de imagens
- `urllib.parse`: Codificação de URLs

### Configuração da Página
```python
st.set_page_config(page_title="Mapas", layout="wide")
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

**Características:**
- Layout flexbox centralizado
- Espaçamento consistente
- Fonte grande para navegação

### Container de Mapas
```css
.mapa-container { text-align: center; }
.mapa-legenda { 
    font-size: 16px; 
    font-weight: 500; 
    margin-top: 8px; 
    color: #333; 
}
.mapa-link img { 
    border-radius: 10px; 
    transition: transform 0.2s ease; 
    cursor: pointer; 
    width:100%; 
    height:auto; 
}
.mapa-link img:hover { transform: scale(1.03); }
```

**Funcionalidades:**
- Centralização de mapas
- Legenda com nome do mapa
- Efeito hover com escala
- Imagens responsivas

## Funcionalidades Principais

### 1. Upload de Mapas
```python
uploaded = st.file_uploader("Adicionar novo mapa (.png)", type=["png"])
if uploaded:
    dest = mapas_dir / uploaded.name
    with open(dest, "wb") as f:
        shutil.copyfileobj(uploaded, f)
    st.success(f"Mapa '{uploaded.name}' adicionado com sucesso!")
    st.experimental_rerun()
```

**Características:**
- Aceita apenas arquivos PNG
- Salva no diretório `mapas/`
- Feedback de sucesso
- Recarrega página automaticamente

### 2. Exibição de Mapas
```python
mapas = sorted(mapas_dir.glob("*.png"))
if mapas:
    cols = st.columns(3)
    for i, mapa in enumerate(mapas):
        with cols[i % 3]:
            # Processamento da imagem
```

**Funcionalidades:**
- Lista mapas ordenados alfabeticamente
- Layout em 3 colunas
- Processamento individual de cada mapa

### 3. Codificação de Imagens
```python
with open(mapa, "rb") as f:
    data = f.read()
img_b64 = base64.b64encode(data).decode("utf-8")
```

**Propósito:**
- Converte imagens para base64
- Permite exibição inline no HTML
- Evita problemas de caminho de arquivo

### 4. Navegação para Detalhes
```python
mapa_nome_url = urllib.parse.quote_plus(mapa_nome)
href = f"/?page=Detalhes&mapa={mapa_nome_url}"
```

**Funcionalidades:**
- Codifica nome do mapa para URL
- Cria link para página de detalhes
- Passa parâmetro via query string

## Estrutura HTML

### Menu de Navegação
```html
<div class="menu">
    <a href="../app" >Menu</a>
    <a href="./Mapas" class="active" >Mapas</a>
    <a href="./Parâmetros">Parâmetros</a>
    <a href="./Resultados">Resultados</a>
    <a href="./Documentação">Documentação</a>
</div>
```

### Título da Página
```html
<div class="titulo">MAPAS</div>
<div class="linha"></div>
```

### Exibição de Mapas
```html
<a class="mapa-link" href="{href}">
  <img src="data:image/png;base64,{img_b64}" alt="{mapa_nome}" />
</a>
<div class="mapa-legenda">{mapa_nome}</div>
```

## Fluxo de Execução

### 1. Inicialização
1. Configuração da página
2. Aplicação de estilos CSS
3. Criação do diretório de mapas

### 2. Upload (se aplicável)
1. Usuário seleciona arquivo PNG
2. Arquivo é salvo no diretório `mapas/`
3. Página é recarregada

### 3. Exibição
1. Busca arquivos PNG no diretório
2. Processa cada imagem (base64)
3. Renderiza em layout de 3 colunas
4. Cria links para páginas de detalhes

## Responsabilidades

### Principais
- **Gerenciamento de Mapas**: Upload e organização de mapas
- **Visualização**: Exibição de mapas com preview
- **Navegação**: Links para páginas de detalhes
- **Interface**: Layout responsivo e intuitivo

### Secundárias
- **Validação**: Restrição a arquivos PNG
- **Feedback**: Mensagens de sucesso/erro
- **Organização**: Ordenação alfabética de mapas

## Tratamento de Erros

### Exceções de Arquivo
```python
try:
    with open(mapa, "rb") as f:
        data = f.read()
    # Processamento da imagem
except Exception as e:
    st.error(f"Erro ao carregar {mapa.name}: {e}")
```

**Funcionalidades:**
- Captura erros de leitura de arquivo
- Exibe mensagem de erro específica
- Continua processamento de outros mapas

### Estado Vazio
```python
else:
    st.info("Nenhum mapa adicionado ainda. Use o botão acima para adicionar um.")
```

**Funcionalidades:**
- Mensagem informativa quando não há mapas
- Instrução para o usuário

## Dependências

### Internas
- Nenhuma dependência de outros módulos

### Externas
- **streamlit**: Framework principal
- **pathlib**: Manipulação de caminhos
- **shutil**: Operações de arquivos
- **base64**: Codificação de imagens
- **urllib.parse**: Codificação de URLs

## Limitações

### Técnicas
- **Formato Fixo**: Aceita apenas PNG
- **Sem Validação**: Não valida conteúdo da imagem
- **Sem Metadados**: Não armazena informações adicionais

### Funcionais
- **Sem Edição**: Não permite editar mapas
- **Sem Categorização**: Não organiza por categorias
- **Sem Busca**: Não permite filtrar mapas

## Melhorias Sugeridas

### Funcionais
1. **Múltiplos Formatos**: Suporte a JPG, GIF, etc.
2. **Metadados**: Armazenar informações do mapa
3. **Categorização**: Organizar por tipo de ambiente
4. **Busca**: Filtros por nome ou categoria

### Técnicas
1. **Validação**: Verificar integridade das imagens
2. **Thumbnails**: Gerar miniaturas para performance
3. **Cache**: Implementar cache de imagens
4. **Compressão**: Otimizar tamanho das imagens

### Interface
1. **Drag & Drop**: Upload por arrastar e soltar
2. **Preview**: Visualização antes do upload
3. **Grid Responsivo**: Adaptar número de colunas
4. **Lazy Loading**: Carregar imagens sob demanda
