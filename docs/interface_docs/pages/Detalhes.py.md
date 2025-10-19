# Documentação - pages/Detalhes.py

## Visão Geral

O arquivo `Detalhes.py` fornece uma interface para visualização detalhada de mapas específicos. Exibe a imagem do mapa, informações sobre simulações relacionadas e botões de navegação para outras funcionalidades.

## Estrutura do Arquivo

### Imports e Dependências
```python
import streamlit as st
import pandas as pd
from pathlib import Path
import base64
import urllib.parse
```

**Dependências:**
- `streamlit`: Framework principal para interface web
- `pandas`: Manipulação de dados (importado mas não utilizado)
- `pathlib`: Manipulação de caminhos de arquivos
- `base64`: Codificação de imagens
- `urllib.parse`: Codificação de URLs

### Configuração da Página
```python
st.set_page_config(page_title="Detalhes do Mapa", layout="wide")
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

### Título e Linha Divisória
```css
.titulo { 
    text-align: center; 
    font-size: 36px; 
    font-weight: 700; 
    margin-bottom: 10px; 
    color: #fff; 
}
.linha { 
    width: 200px; 
    height: 2px; 
    background-color: #1e90ff; 
    margin: 0 auto 40px auto; 
}
```

**Características:**
- Título centralizado em branco
- Linha azul (#1e90ff) para destaque
- Espaçamento consistente

### Botões de Ação
```css
.botoes { 
    display: flex; 
    justify-content: center; 
    gap: 20px; 
    margin-bottom: 40px; 
}
.botao { 
    background-color: #1e90ff; 
    color: white; 
    border-radius: 8px; 
    padding: 12px 28px; 
    font-size: 18px; 
    font-weight: 600; 
    text-decoration: none; 
    display: inline-flex; 
    align-items: center; 
    gap: 8px; 
    transition: all 0.2s ease-in-out; 
}
```

**Funcionalidades:**
- Botões centralizados com ícones
- Cor azul (#1e90ff) com hover
- Efeito de escala no hover
- Transições suaves

### Área de Imagem
```css
.mapa-imagem { 
    display: flex; 
    justify-content: center; 
    margin-bottom: 30px; 
}
.mapa-imagem img { 
    border-radius: 12px; 
    box-shadow: 0 4px 12px rgba(0,0,0,0.3); 
    max-width: 70%; 
    height: auto; 
}
```

**Características:**
- Imagem centralizada
- Bordas arredondadas
- Sombra para profundidade
- Responsiva (max-width: 70%)

### Tabela de Simulações
```css
.tabela-container { 
    display: flex; 
    justify-content: center; 
}
table.tabela { 
    border-collapse: collapse; 
    width: 80%; 
    font-size: 18px; 
    text-align: center; 
    border-radius: 10px; 
    overflow: hidden; 
    box-shadow: 0 0 15px rgba(255,255,255,0.1); 
}
```

**Funcionalidades:**
- Tabela centralizada
- Bordas arredondadas
- Sombra sutil
- Fonte grande para legibilidade

## Funcionalidades Principais

### 1. Obtenção de Parâmetros
```python
params = st.query_params
mapa_nome = params.get("mapa", [""])[0] if isinstance(params.get("mapa"), list) else params.get("mapa", "")
```

**Funcionalidades:**
- Captura parâmetros da URL
- Trata tanto listas quanto strings
- Valor padrão vazio se não encontrado

### 2. Exibição Dinâmica do Título
```python
if mapa_nome:
    st.markdown(f'<div class="titulo">{mapa_nome.upper()}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="titulo">DETALHES DO MAPA</div>', unsafe_allow_html=True)
```

**Características:**
- Título dinâmico baseado no mapa
- Fallback para título genérico
- Texto em maiúsculas

### 3. Carregamento e Exibição de Imagem
```python
mapa_path = Path("mapas") / f"{mapa_nome}.png"
if mapa_nome and mapa_path.exists():
    with open(mapa_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")
    st.markdown(f"""
        <div class="mapa-imagem">
            <img src="data:image/png;base64,{img_b64}" alt="{mapa_nome}" />
        </div>
    """, unsafe_allow_html=True)
```

**Funcionalidades:**
- Carrega imagem do mapa
- Converte para base64
- Exibe com HTML customizado
- Tratamento de erro se arquivo não existe

### 4. Botões de Navegação
```python
simulacao_url = f"./Simulação?mapa={urllib.parse.quote(mapa_nome)}" if mapa_nome else "./Simulação"
st.markdown(f"""
<div class="botoes">
    <a href="./Mapas" class="botao">← Voltar aos Mapas</a>
    <a href="#" class="botao">🔍 Pesquisar</a>
    <a href="{simulacao_url}" class="botao">⚙️ Criar simulação</a>
</div>
""", unsafe_allow_html=True)
```

**Funcionalidades:**
- Botão para voltar aos mapas
- Botão de pesquisa (não funcional)
- Botão para criar simulação
- URL codificada para parâmetros

### 5. Tabela de Simulações
```python
st.markdown("""
<div class="tabela-container">
<table class="tabela">
    <thead>
        <tr>
            <th>ID</th>
            <th>NOME</th>
            <th>MAPA</th>
            <th>ALGORITMO</th>
            <th>SIMULADO</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>capacidade_maxima</td>
            <td>{}</td>
            <td>NSGA-II</td>
            <td>SIM</td>
        </tr>
    </tbody>
</table>
</div>
""".format(mapa_nome if mapa_nome else "—"), unsafe_allow_html=True)
```

**Características:**
- Dados estáticos de exemplo
- Nome do mapa inserido dinamicamente
- Estrutura similar à página Resultados
- Fallback para "—" se mapa não definido

## Estrutura HTML

### Menu de Navegação
```html
<div class="menu">
    <a href="../app" >Menu</a>
    <a href="./Mapas" class="active">Mapas</a>
    <a href="./Parâmetros">Parâmetros</a>
    <a href="./Resultados">Resultados</a>
    <a href="./Documentação">Documentação</a>
</div>
```

### Título Dinâmico
```html
<div class="titulo">{mapa_nome.upper()}</div>
<div class="linha"></div>
```

### Botões de Ação
```html
<div class="botoes">
    <a href="./Mapas" class="botao">← Voltar aos Mapas</a>
    <a href="#" class="botao">🔍 Pesquisar</a>
    <a href="{simulacao_url}" class="botao">⚙️ Criar simulação</a>
</div>
```

### Imagem do Mapa
```html
<div class="mapa-imagem">
    <img src="data:image/png;base64,{img_b64}" alt="{mapa_nome}" />
</div>
```

## Fluxo de Execução

### 1. Inicialização
1. Configuração da página Streamlit
2. Aplicação de estilos CSS
3. Renderização do menu de navegação

### 2. Processamento de Parâmetros
1. Captura do nome do mapa da URL
2. Validação e tratamento de parâmetros
3. Definição do título dinâmico

### 3. Renderização
1. Exibição do título
2. Carregamento e exibição da imagem
3. Renderização dos botões de ação
4. Criação da tabela de simulações

## Responsabilidades

### Principais
- **Visualização**: Exibição detalhada de mapas
- **Navegação**: Links para outras funcionalidades
- **Parâmetros**: Processamento de parâmetros da URL
- **Imagens**: Carregamento e exibição de imagens

### Secundárias
- **Interface**: Design limpo e organizado
- **Dados**: Apresentação de simulações relacionadas
- **Feedback**: Mensagens de status

## Tratamento de Erros

### Arquivo Não Encontrado
```python
elif mapa_nome:
    st.warning("⚠️ Arquivo do mapa não encontrado.")
else:
    st.info("Selecione um mapa para ver os detalhes.")
```

**Funcionalidades:**
- Aviso quando arquivo não existe
- Mensagem informativa quando mapa não selecionado
- Feedback visual para o usuário

## Dependências

### Internas
- Nenhuma dependência de outros módulos

### Externas
- **streamlit**: Framework principal
- **pathlib**: Manipulação de caminhos
- **base64**: Codificação de imagens
- **urllib.parse**: Codificação de URLs
- **Sistema de Arquivos**: Para acesso aos mapas

## Limitações

### Funcionais
- **Dados Estáticos**: Tabela com dados hardcoded
- **Sem Pesquisa**: Botão de pesquisa não funcional
- **Sem Detalhes**: Não mostra detalhes das simulações
- **Sem Edição**: Não permite editar informações

### Técnicas
- **Sem Validação**: Não valida parâmetros da URL
- **Sem Tratamento de Erros**: Não captura erros de imagem
- **Hardcoded**: Valores fixos no código
- **Sem Estado**: Não mantém estado entre navegações

## Melhorias Sugeridas

### Funcionais
1. **Dados Dinâmicos**: Carregar dados de arquivo ou banco
2. **Pesquisa**: Implementar funcionalidade de busca
3. **Detalhes**: Links para detalhes das simulações
4. **Edição**: Permitir editar informações do mapa
5. **Metadados**: Exibir informações adicionais do mapa

### Técnicas
1. **Validação**: Validar parâmetros da URL
2. **Tratamento de Erros**: Capturar e exibir erros
3. **Estado**: Manter estado entre navegações
4. **Cache**: Implementar cache de imagens
5. **Logs**: Registrar atividades

### Interface
1. **Zoom**: Permitir zoom na imagem
2. **Anotações**: Adicionar anotações no mapa
3. **Comparação**: Comparar com outros mapas
4. **Export**: Exportar imagem
5. **Responsividade**: Melhor adaptação mobile

## Integração com Outros Módulos

### Fluxo de Dados
1. **Mapas.py**: Usuário seleciona mapa
2. **Detalhes.py**: Exibe detalhes do mapa
3. **Simulação.py**: Cria simulação para o mapa
4. **Resultados.py**: Visualiza resultados

### Dependências
- **Mapas.py**: Para seleção de mapas
- **Simulação.py**: Para criação de simulações
- **Resultados.py**: Para visualização de resultados
- **Sistema de Arquivos**: Para acesso aos mapas
