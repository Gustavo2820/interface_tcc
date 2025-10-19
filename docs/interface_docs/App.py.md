# Documentação - App.py

## Visão Geral

O arquivo `App.py` é o ponto de entrada principal da aplicação Streamlit, responsável por definir o layout geral, estilos CSS e menu de navegação da interface de simulação de evacuação.

## Estrutura do Arquivo

### Imports e Dependências
```python
import streamlit as st
```

**Dependências:**
- `streamlit`: Framework principal para interface web

### Configurações Gerais
```python
st.set_page_config(page_title="Simulação de Evacuação", layout="wide")
```

**Propósito:** Define configurações globais da página Streamlit
- **page_title**: Título exibido na aba do navegador
- **layout**: Layout "wide" para melhor aproveitamento do espaço

## CSS Global

### Estilos de Fonte e Cores
```css
body {
    font-family: 'Inter', 'Roboto', sans-serif;
    background-color: white;
    color: #222;
}
```

**Características:**
- Fonte moderna com fallbacks
- Fundo branco para clareza
- Cor de texto escura para legibilidade

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

**Funcionalidades:**
- Layout flexbox centralizado
- Espaçamento consistente entre itens
- Tamanho de fonte grande para navegação

**Estados dos Links:**
- **Normal**: Cor cinza (#bbb)
- **Hover**: Cor branca (#fff)
- **Ativo**: Cor branca com borda inferior azul

### Título Principal
```css
.titulo {
    text-align: center;
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 10px;
}
```

**Características:**
- Centralizado na página
- Fonte grande e bold
- Espaçamento adequado

### Botões de Página Principal
```css
.folder {
    width: 200px;
    height: 140px;
    border: 2px solid #001f3f;
    border-radius: 8px;
    background-color: #083d77;
    color: white;
    font-size: 18px;
    font-weight: 500;
    text-align: center;
    line-height: 140px;
    cursor: pointer;
    position: relative;
    box-shadow: 2px 4px 6px rgba(0,0,0,0.1);
    transition: all 0.2s ease-in-out;
    text-decoration: none;
}
```

**Design:**
- Simula pastas de arquivo com aba superior
- Cores azuis corporativas
- Efeitos de hover com escala e sombra
- Transições suaves

## Estrutura HTML

### Menu de Navegação
```html
<div class="menu">
    <a href="./app" class="active">Menu</a>
    <a href="./Mapas">Mapas</a>
    <a href="./Parâmetros">Parâmetros</a>
    <a href="./Resultados">Resultados</a>
    <a href="./Documentação">Documentação</a>
</div>
```

**Funcionalidades:**
- Navegação entre páginas principais
- Link "Menu" marcado como ativo
- Roteamento baseado em nomes de arquivo

### Título e Linha Divisória
```html
<div class="titulo">SIMULAÇÃO DE EVACUAÇÃO</div>
<div class="linha"></div>
```

**Propósito:**
- Título principal da aplicação
- Linha decorativa para separação visual

### Conteúdo Principal
```html
<div class="folders">
    <a href="./Mapas" class="folder">Mapas</a>
    <a href="./Parâmetros" class="folder">Parâmetros</a>
    <a href="./Resultados" class="folder">Resultados</a>
    <a href="./Documentação" class="folder">Documentação</a>
</div>
```

**Funcionalidades:**
- Botões principais de navegação
- Design de pastas para intuitividade
- Links diretos para páginas funcionais

## Fluxo de Execução

### 1. Inicialização
1. Configuração da página Streamlit
2. Aplicação de estilos CSS globais
3. Renderização do menu de navegação

### 2. Renderização
1. Exibição do título principal
2. Renderização dos botões de navegação
3. Exibição do conteúdo descritivo

### 3. Interação
1. Usuário clica em botões de navegação
2. Streamlit redireciona para páginas correspondentes
3. Estado da aplicação é mantido

## Responsabilidades

### Principais
- **Layout Global**: Define estrutura visual da aplicação
- **Navegação**: Fornece menu de navegação consistente
- **Estilos**: Aplica CSS customizado para interface moderna
- **Ponto de Entrada**: Serve como página inicial da aplicação

### Secundárias
- **Configuração**: Define configurações globais do Streamlit
- **Consistência Visual**: Mantém padrão visual em toda aplicação
- **Usabilidade**: Fornece interface intuitiva para navegação

## Dependências

### Internas
- Nenhuma dependência de outros módulos da aplicação

### Externas
- **streamlit**: Framework principal
- **Navegador Web**: Para renderização da interface

## Limitações

### Técnicas
- **CSS Inline**: Estilos definidos como string, dificultando manutenção
- **Sem Componentes**: Código não modularizado
- **Hardcoded**: Links e textos fixos no código

### Funcionais
- **Sem Validação**: Não há validação de navegação
- **Estático**: Conteúdo não dinâmico
- **Sem Estado**: Não mantém estado entre navegações

## Melhorias Sugeridas

### Estruturais
1. **Modularização**: Separar CSS em arquivo externo
2. **Componentes**: Criar componentes reutilizáveis
3. **Configuração**: Mover textos para arquivo de configuração

### Funcionais
1. **Validação**: Adicionar validação de rotas
2. **Estado**: Implementar gerenciamento de estado
3. **Responsividade**: Melhorar adaptação mobile

### Técnicas
1. **Type Hints**: Adicionar anotações de tipo
2. **Documentação**: Adicionar docstrings
3. **Testes**: Implementar testes unitários
