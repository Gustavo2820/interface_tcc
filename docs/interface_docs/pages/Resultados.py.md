# Documentação - pages/Resultados.py

## Visão Geral

O arquivo `Resultados.py` fornece uma interface para visualização de resultados de simulações de evacuação. Exibe uma tabela com informações sobre simulações executadas, incluindo ID, nome, mapa, algoritmo e status de execução.

## Estrutura do Arquivo

### Imports e Dependências
```python
import streamlit as st
```

**Dependências:**
- `streamlit`: Framework principal para interface web

### Configuração da Página
```python
st.set_page_config(page_title="Resultados", layout="wide")
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

### Botão de Pesquisa
```css
.btn-pesquisar {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    background-color: #1e90ff;
    color: white;
    font-size: 18px;
    font-weight: 600;
    padding: 12px 30px;
    border-radius: 8px;
    margin: 0 auto 40px auto;
    width: fit-content;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    text-decoration: none;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}
```

**Características:**
- Botão centralizado com ícone de lupa
- Cor azul (#1e90ff) com sombra
- Efeito hover com escala
- Transições suaves

### Tabela de Resultados
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
- Tabela centralizada com 80% de largura
- Bordas arredondadas e sombra
- Fonte grande para legibilidade
- Cabeçalho e células estilizados

### Cabeçalho da Tabela
```css
table.tabela thead {
    background-color: #1e2b3b;
    color: #fff;
}
table.tabela th, table.tabela td {
    padding: 14px 20px;
    border-bottom: 1px solid #333;
}
```

**Características:**
- Fundo azul escuro (#1e2b3b)
- Texto branco
- Padding generoso
- Bordas sutis

### Células da Tabela
```css
table.tabela td {
    background-color: #181c24;
    color: #e0e0e0;
}
table.tabela tr:hover {
    background-color: rgba(255, 255, 255, 0.05);
}
table.tabela tr:last-child td {
    border-bottom: none;
}
```

**Funcionalidades:**
- Fundo escuro (#181c24)
- Texto cinza claro (#e0e0e0)
- Efeito hover sutil
- Última linha sem borda inferior

## Funcionalidades Principais

### 1. Botão de Pesquisa
```python
st.markdown('<a class="btn-pesquisar">Pesquisar</a>', unsafe_allow_html=True)
```

**Funcionalidades:**
- Botão centralizado com ícone
- Efeito hover com escala
- Preparado para funcionalidade de busca
- Design consistente com tema escuro

### 2. Tabela de Resultados
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
            <td>Igreja</td>
            <td>NSGA-II</td>
            <td>SIM</td>
        </tr>
        <tr>
            <td>2</td>
            <td>fluxo_otimizado</td>
            <td>Shopping</td>
            <td>Força Bruta</td>
            <td>NÃO</td>
        </tr>
    </tbody>
</table>
</div>
""", unsafe_allow_html=True)
```

**Características:**
- Dados estáticos de exemplo
- Estrutura de tabela HTML
- Colunas: ID, Nome, Mapa, Algoritmo, Status
- Linhas com dados de simulações

## Estrutura HTML

### Menu de Navegação
```html
<div class="menu">
    <a href="../app" >Menu</a>
    <a href="./Mapas">Mapas</a>
    <a href="./Parâmetros">Parâmetros</a>
    <a href="./Resultados" class="active">Resultados</a>
    <a href="./Documentação">Documentação</a>
</div>
```

### Botão de Pesquisa
```html
<a class="btn-pesquisar">Pesquisar</a>
```

### Tabela de Resultados
```html
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
        <!-- Dados das simulações -->
    </tbody>
</table>
</div>
```

## Fluxo de Execução

### 1. Inicialização
1. Configuração da página Streamlit
2. Aplicação de estilos CSS
3. Renderização do menu de navegação

### 2. Renderização
1. Exibição do botão de pesquisa
2. Criação da tabela de resultados
3. Renderização dos dados estáticos

### 3. Interação
1. Usuário pode clicar em "Pesquisar"
2. Tabela exibe informações das simulações
3. Efeito hover nas linhas da tabela

## Responsabilidades

### Principais
- **Visualização**: Exibição de resultados de simulações
- **Navegação**: Menu consistente com outras páginas
- **Interface**: Design limpo e organizado
- **Dados**: Apresentação de informações estruturadas

### Secundárias
- **Pesquisa**: Interface para busca de resultados
- **Status**: Indicação do status das simulações
- **Organização**: Estrutura clara dos dados

## Estrutura de Dados

### Colunas da Tabela
- **ID**: Identificador único da simulação
- **NOME**: Nome descritivo da simulação
- **MAPA**: Mapa utilizado na simulação
- **ALGORITMO**: Algoritmo de otimização usado
- **SIMULADO**: Status de execução (SIM/NÃO)

### Dados de Exemplo
```python
simulacoes = [
    {
        "id": 1,
        "nome": "capacidade_maxima",
        "mapa": "Igreja",
        "algoritmo": "NSGA-II",
        "status": "SIM"
    },
    {
        "id": 2,
        "nome": "fluxo_otimizado",
        "mapa": "Shopping",
        "algoritmo": "Força Bruta",
        "status": "NÃO"
    }
]
```

## Dependências

### Internas
- Nenhuma dependência de outros módulos

### Externas
- **streamlit**: Framework principal
- **Navegador Web**: Para renderização

## Limitações

### Funcionais
- **Dados Estáticos**: Não carrega dados dinâmicos
- **Sem Pesquisa**: Botão de pesquisa não funcional
- **Sem Detalhes**: Não permite ver detalhes das simulações
- **Sem Filtros**: Não permite filtrar resultados

### Técnicas
- **Sem Banco de Dados**: Dados hardcoded
- **Sem API**: Não conecta com backend
- **Sem Estado**: Não mantém estado entre navegações
- **Sem Validação**: Não valida dados

## Melhorias Sugeridas

### Funcionais
1. **Dados Dinâmicos**: Carregar dados de arquivo ou banco
2. **Pesquisa**: Implementar funcionalidade de busca
3. **Filtros**: Permitir filtrar por algoritmo, status, etc.
4. **Detalhes**: Links para páginas de detalhes
5. **Paginação**: Para grandes volumes de dados

### Técnicas
1. **Banco de Dados**: Integrar com sistema de persistência
2. **API**: Conectar com backend
3. **Estado**: Manter estado entre navegações
4. **Validação**: Validar dados antes de exibir
5. **Cache**: Implementar cache de resultados

### Interface
1. **Ordenação**: Permitir ordenar colunas
2. **Export**: Exportar dados para CSV/Excel
3. **Gráficos**: Visualizações adicionais
4. **Responsividade**: Melhor adaptação mobile
5. **Acessibilidade**: Melhorar acessibilidade

## Integração com Outros Módulos

### Fluxo de Dados
1. **Simulação**: Simulações são executadas
2. **Armazenamento**: Resultados são salvos
3. **Visualização**: Resultados.py exibe dados
4. **Navegação**: Links para outras páginas

### Dependências
- **Simulação.py**: Para execução de simulações
- **Detalhes.py**: Para visualização de detalhes
- **Mapas.py**: Para informações de mapas
- **Parâmetros.py**: Para informações de algoritmos

## Tema Visual

### Cores
- **Fundo**: Escuro (#0e1117)
- **Texto**: Cinza claro (#e0e0e0)
- **Cabeçalho**: Azul escuro (#1e2b3b)
- **Botões**: Azul (#1e90ff)

### Características
- **Tema Escuro**: Interface moderna e elegante
- **Contraste**: Boa legibilidade
- **Consistência**: Padrão visual uniforme
- **Profissional**: Aparência corporativa
