# Documentação - pages/Simulação.py

## Visão Geral

O arquivo `Simulação.py` fornece uma interface para configuração de parâmetros específicos de simulação de evacuação. Permite aos usuários configurar nome, algoritmo, parâmetros e visualizar o mapa selecionado antes de executar a simulação.

## Estrutura do Arquivo

### Imports e Dependências
```python
import streamlit as st
from pathlib import Path
from PIL import Image
```

**Dependências:**
- `streamlit`: Framework principal para interface web
- `pathlib`: Manipulação de caminhos de arquivos
- `PIL (Pillow)`: Processamento de imagens

### Configuração da Página
```python
st.set_page_config(page_title="Simulação", layout="wide")
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

### Botões Superiores
```css
.botoes {
    display: flex;
    justify-content: flex-end;
    gap: 20px;
    margin-right: 40px;
    margin-bottom: 30px;
}
.botao {
    background-color: #142b3b;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.2s ease-in-out;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}
```

**Características:**
- Botões alinhados à direita
- Cor azul escuro (#142b3b)
- Efeito hover com escala
- Ícones e texto

### Layout Central
```css
.container {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: flex-start;
    gap: 60px;
    width: 100%;
}
.painel-esquerda {
    display: flex;
    flex-direction: column;
    gap: 25px;
}
```

**Funcionalidades:**
- Layout flexível com duas colunas
- Painel esquerdo para controles
- Painel direito para visualização
- Espaçamento consistente

### Blocos de Controle
```css
.bloco {
    background-color: #142b3b;
    color: white;
    text-align: center;
    border-radius: 10px;
    padding: 10px 0;
    font-weight: bold;
}
.input {
    background-color: #b3b3b3;
    border: none;
    border-radius: 6px;
    padding: 6px;
    color: black;
    width: 200px;
    text-align: center;
}
```

**Características:**
- Blocos com fundo azul escuro
- Inputs com fundo cinza claro
- Centralização de texto
- Bordas arredondadas

### Área de Mapa
```css
.mapa {
    border: 1px solid #ccc;
    border-radius: 6px;
    width: 800px;
    height: 600px;
    display: flex;
    justify-content: center;
    align-items: center;
}
```

**Funcionalidades:**
- Área fixa para exibição do mapa
- Centralização da imagem
- Bordas definidas
- Tamanho responsivo

## Funcionalidades Principais

### 1. Configuração de Parâmetros
```python
with col1:
    st.markdown('<div class="bloco">Nome</div>', unsafe_allow_html=True)
    st.text_input("", value="Nome")

    st.markdown('<div class="bloco">Algoritmo ▼</div>', unsafe_allow_html=True)
    st.text_input("", value="Nome")

    st.markdown('<div class="bloco">Parâmetros</div>', unsafe_allow_html=True)
    st.text_input("", value="Nome do arquivo")
```

**Funcionalidades:**
- Campo para nome da simulação
- Seleção de algoritmo
- Upload de arquivo de parâmetros
- Interface organizada em blocos

### 2. Visualização do Mapa
```python
with col2:
    # Carregar imagem do mapa selecionado
    mapa_path = Path("mapas/3.png")  # Substituir dinamicamente depois
    if mapa_path.exists():
        img = Image.open(mapa_path)
        st.image(img, use_container_width=True)
    else:
        st.warning("Nenhum mapa selecionado ou encontrado.")
```

**Características:**
- Carregamento de imagem do mapa
- Exibição responsiva
- Tratamento de erro quando mapa não existe
- Integração com PIL para processamento

### 3. Botões de Ação
```python
st.markdown("""
<div class="botoes">
    <a href="#" class="botao">Salvar</a>
    <a href="./Simulado.py" class="botao">Simular</a>
</div>
""", unsafe_allow_html=True)
```

**Funcionalidades:**
- Botão para salvar configuração
- Botão para iniciar simulação
- Links para outras páginas
- Feedback visual

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

### Botões de Ação
```html
<div class="botoes">
    <a href="#" class="botao">Salvar</a>
    <a href="./Simulado.py" class="botao">Simular</a>
</div>
```

### Layout Principal
```html
<div class="container">
    <div class="painel-esquerda">
        <!-- Controles de configuração -->
    </div>
    <div class="painel-direita">
        <!-- Visualização do mapa -->
    </div>
</div>
```

## Fluxo de Execução

### 1. Inicialização
1. Configuração da página Streamlit
2. Aplicação de estilos CSS
3. Renderização do menu de navegação

### 2. Renderização
1. Exibição dos botões de ação
2. Criação do layout de duas colunas
3. Renderização dos controles de configuração
4. Carregamento e exibição do mapa

### 3. Interação
1. Usuário configura parâmetros
2. Sistema valida configurações
3. Usuário clica em "Simular"
4. Redirecionamento para página de simulação

## Responsabilidades

### Principais
- **Configuração**: Interface para parâmetros de simulação
- **Visualização**: Exibição do mapa selecionado
- **Navegação**: Links para outras páginas
- **Validação**: Verificação de configurações

### Secundárias
- **Interface**: Design limpo e organizado
- **Layout**: Estrutura de duas colunas
- **Feedback**: Mensagens de status

## Parâmetros de Configuração

### Básicos
- **Nome**: Identificador da simulação
- **Algoritmo**: Tipo de algoritmo a ser usado
- **Parâmetros**: Arquivo de configuração

### Avançados
- **Mapa**: Arquivo do mapa de evacuação
- **Indivíduos**: Número de pessoas na simulação
- **Tempo**: Duração máxima da simulação
- **Objetivos**: Critérios de otimização

## Dependências

### Internas
- Nenhuma dependência de outros módulos

### Externas
- **streamlit**: Framework principal
- **pathlib**: Manipulação de caminhos
- **PIL**: Processamento de imagens
- **Sistema de Arquivos**: Para acesso aos mapas

## Limitações

### Funcionais
- **Mapa Fixo**: Usa mapa hardcoded (3.png)
- **Sem Validação**: Não valida parâmetros
- **Sem Persistência**: Não salva configurações
- **Sem Preview**: Não mostra preview dos parâmetros

### Técnicas
- **Sem Tratamento de Erros**: Não captura erros de imagem
- **Sem Validação**: Não verifica integridade dos dados
- **Hardcoded**: Valores fixos no código

## Melhorias Sugeridas

### Funcionais
1. **Mapa Dinâmico**: Carregar mapa selecionado dinamicamente
2. **Validação**: Validar parâmetros antes de simular
3. **Persistência**: Salvar configurações em sessão
4. **Preview**: Mostrar preview dos parâmetros
5. **Templates**: Configurações pré-definidas

### Técnicas
1. **Tratamento de Erros**: Capturar e exibir erros
2. **Validação**: Verificar integridade dos dados
3. **Estado**: Manter estado entre navegações
4. **Logs**: Registrar atividades
5. **Configuração**: Mover valores para arquivo de config

### Interface
1. **Formulário**: Interface de formulário mais robusta
2. **Validação Visual**: Feedback em tempo real
3. **Help**: Ajuda contextual
4. **Presets**: Configurações pré-definidas
5. **Export**: Exportar configurações

## Integração com Outros Módulos

### Fluxo de Dados
1. **Configuração**: Usuário define parâmetros
2. **Validação**: Sistema valida configurações
3. **Simulação**: Redireciona para Simulado.py
4. **Processamento**: Executa simulação
5. **Resultados**: Retorna para visualização

### Dependências
- **Mapas.py**: Para seleção de mapas
- **Parâmetros.py**: Para configuração de algoritmos
- **Simulado.py**: Para execução da simulação
- **Resultados.py**: Para visualização de resultados
