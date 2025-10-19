# Documentação - pages/Parâmetros.py

## Visão Geral

O arquivo `Parâmetros.py` atua como um hub central para configuração de algoritmos de otimização. Apresenta uma interface com botões que direcionam para páginas específicas de cada algoritmo (Algoritmo Genético, NSGA-II, Força Bruta).

## Estrutura do Arquivo

### Imports e Dependências
```python
import streamlit as st
```

**Dependências:**
- `streamlit`: Framework principal para interface web

### Configuração da Página
```python
st.set_page_config(page_title="Parâmetros", layout="wide")
```

## CSS e Estilos

### Estilos Base
```css
body {
    font-family: 'Inter', 'Roboto', sans-serif;
    background-color: white;
    color: #222;
}
```

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
}
.linha {
    width: 200px;
    height: 2px;
    background-color: #444;
    margin: 0 auto 50px auto;
}
```

### Botões de Algoritmos
```css
.folders {
    display: flex;
    justify-content: center;
    gap: 60px;
    flex-wrap: wrap;
}
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

**Características dos Botões:**
- Design de pastas com aba superior
- Cores azuis corporativas (#083d77, #001f3f)
- Efeitos de hover com escala e sombra
- Transições suaves (0.2s ease-in-out)
- Layout flexível com wrap

### Aba Superior dos Botões
```css
.folder::before {
    content: "";
    position: absolute;
    top: -20px;
    left: 0;
    width: 80px;
    height: 20px;
    background-color: #f8f4e3;
    border: 2px solid #001f3f;
    border-bottom: none;
    border-radius: 6px 6px 0 0;
}
```

**Efeito Visual:**
- Simula aba de pasta de arquivo
- Cor creme (#f8f4e3) para contraste
- Posicionamento absoluto

## Estrutura HTML

### Menu de Navegação
```html
<div class="menu">
    <a href="../app" >Menu</a>
    <a href="./Mapas">Mapas</a>
    <a href="./Parâmetros" class="active">Parâmetros</a>
    <a href="./Resultados">Resultados</a>
    <a href="./Documentação">Documentação</a>
</div>
```

### Título da Página
```html
<div class="titulo">PARAMETRIZAÇÃO</div>
<div class="linha"></div>
```

### Botões de Algoritmos
```html
<div class="folders">
    <a href="./Algoritmo_Genetico" class="folder">Algoritmo Genético</a>
    <a href="./NSGA_II" class="folder">NSGA-II</a>
    <a href="./Forca_Bruta" class="folder">Força Bruta</a>
</div>
```

## Funcionalidades Principais

### 1. Navegação Centralizada
- **Propósito**: Serve como ponto central para acesso aos algoritmos
- **Implementação**: Botões que redirecionam para páginas específicas
- **Benefício**: Interface organizada e intuitiva

### 2. Design Consistente
- **Estilos**: CSS compartilhado com outras páginas
- **Layout**: Estrutura similar ao App.py
- **Navegação**: Menu superior consistente

### 3. Responsividade
- **Flexbox**: Layout flexível com wrap
- **Gap**: Espaçamento consistente entre elementos
- **Mobile**: Adaptação para diferentes tamanhos de tela

## Fluxo de Execução

### 1. Inicialização
1. Configuração da página Streamlit
2. Aplicação de estilos CSS
3. Renderização do menu de navegação

### 2. Renderização
1. Exibição do título "PARAMETRIZAÇÃO"
2. Renderização da linha divisória
3. Criação dos botões de algoritmos

### 3. Interação
1. Usuário clica em um botão de algoritmo
2. Streamlit redireciona para página correspondente
3. Estado da aplicação é mantido

## Responsabilidades

### Principais
- **Hub de Navegação**: Centraliza acesso aos algoritmos
- **Interface Consistente**: Mantém padrão visual
- **Organização**: Estrutura clara para diferentes algoritmos

### Secundárias
- **Configuração**: Define configurações da página
- **Estilos**: Aplica CSS customizado
- **Navegação**: Fornece menu de navegação

## Algoritmos Suportados

### 1. Algoritmo Genético
- **Página**: `./Algoritmo_Genetico`
- **Descrição**: Algoritmo evolutivo para otimização
- **Uso**: Configuração de parâmetros genéticos

### 2. NSGA-II
- **Página**: `./NSGA_II`
- **Descrição**: Algoritmo genético multi-objetivo
- **Uso**: Otimização com múltiplos objetivos

### 3. Força Bruta
- **Página**: `./Forca_Bruta`
- **Descrição**: Busca exaustiva de soluções
- **Uso**: Validação e comparação de resultados

## Dependências

### Internas
- Nenhuma dependência de outros módulos

### Externas
- **streamlit**: Framework principal
- **Navegador Web**: Para renderização

## Limitações

### Funcionais
- **Sem Validação**: Não valida se algoritmos estão disponíveis
- **Estático**: Não permite adicionar novos algoritmos dinamicamente
- **Sem Estado**: Não mantém informações sobre algoritmos

### Técnicas
- **CSS Inline**: Estilos definidos como string
- **Hardcoded**: Links fixos no código
- **Sem Componentes**: Código não modularizado

## Melhorias Sugeridas

### Funcionais
1. **Algoritmos Dinâmicos**: Carregar algoritmos de configuração
2. **Validação**: Verificar disponibilidade dos algoritmos
3. **Descrições**: Adicionar descrições dos algoritmos
4. **Status**: Mostrar status de cada algoritmo

### Técnicas
1. **Modularização**: Separar CSS em arquivo externo
2. **Componentes**: Criar componentes reutilizáveis
3. **Configuração**: Mover links para arquivo de configuração
4. **Type Hints**: Adicionar anotações de tipo

### Interface
1. **Ícones**: Adicionar ícones para cada algoritmo
2. **Tooltips**: Informações adicionais ao hover
3. **Animações**: Efeitos visuais mais elaborados
4. **Responsividade**: Melhor adaptação mobile

## Integração com Outros Módulos

### Páginas de Algoritmos
- **Algoritmo_Genetico.py**: Configuração de parâmetros genéticos
- **NSGA_II.py**: Configuração de NSGA-II
- **Forca_Bruta.py**: Configuração de força bruta

### Fluxo de Dados
1. **Seleção**: Usuário escolhe algoritmo
2. **Redirecionamento**: Navega para página específica
3. **Configuração**: Define parâmetros do algoritmo
4. **Upload**: Envia arquivos de configuração
5. **Processamento**: Algoritmo processa dados
6. **Resultados**: Retorna para visualização
