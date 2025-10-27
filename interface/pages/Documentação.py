# pages/Documentação.py
"""
Página de documentação do sistema de simulação de evacuação.

Este módulo fornece acesso à documentação técnica, guias de uso
e informações sobre o sistema.
"""
import streamlit as st

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(page_title="Documentação", layout="wide")

# ================= CSS E CABEÇALHO DECORATIVO =================
st.markdown("""
    <style>
    /* ===== MENU SUPERIOR ===== */
    .menu {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-bottom: 40px;
        font-size: 18px;
        font-weight: 500;
    }
    .menu a {
        text-decoration: none;
        color: #aaa;
        transition: color 0.2s;
    }
    .menu a:hover {
        color: #fff;
    }
    .menu a.active {
        color: #fff;
        font-weight: 600;
        border-bottom: 2px solid #667eea;
        padding-bottom: 4px;
    }

    /* ===== CABEÇALHO DA PÁGINA ===== */
    .page-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .page-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .page-header p {
        color: rgba(255,255,255,0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(26, 26, 46, 0.3);
        border-radius: 8px;
        padding: 10px 20px;
        color: #aaa;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* ===== EXPANDERS ===== */
    .streamlit-expanderHeader {
        background-color: rgba(26, 26, 46, 0.4) !important;
        border-radius: 8px;
        font-weight: 600;
        color: #667eea !important;
    }
    
    /* ===== CODE BLOCKS ===== */
    code {
        background-color: rgba(26, 26, 46, 0.5);
        padding: 2px 6px;
        border-radius: 4px;
        color: #667eea;
    }
    </style>
""", unsafe_allow_html=True)

# ===== MENU SUPERIOR =====
st.markdown("""
    <div class="menu">
        <a href="/">Menu</a>
        <a href="/Mapas">Mapas</a>
        <a href="/Criação_de_Mapas">Criação de Mapas</a>
        <a href="/Parâmetros">Parâmetros</a>
        <a href="/Simulação">Simulação</a>
        <a href="/Resultados">Resultados</a>
        <a class="active" href="/Documentação">Documentação</a>
    </div>
""", unsafe_allow_html=True)

# ===== CABEÇALHO DA PÁGINA =====
st.markdown("""
    <div class="page-header">
        <h1>📚 Documentação</h1>
        <p>Guias, referências e exemplos para usar o sistema de simulação de evacuação</p>
    </div>
""", unsafe_allow_html=True)

# ================= CONTEÚDO =================
st.write("""
Esta página fornece acesso à documentação completa do sistema de simulação de evacuação.
""")

# Seções de documentação
tab1, tab2, tab3, tab4 = st.tabs(["📚 Guias", "🔧 API", "📖 Exemplos", "❓ FAQ"])

with tab1:
    st.markdown("### 📚 Guias de Uso")
    
    with st.expander("🎨 Criação de Mapas"):
        st.markdown("""
        **Como criar mapas personalizados:**
        
        1. Acesse a página "Criação de Mapas"
        2. Configure as dimensões do mapa (linhas e colunas)
        3. Selecione um template inicial (vazio, sala, corredor)
        4. Use o editor de pixels para desenhar seu mapa
        5. Visualize o resultado e baixe os arquivos gerados
        
        **Esquema de cores:**
        - **Preto**: Paredes (obstáculos)
        - **Branco**: Espaço vazio (caminhável)
        - **Laranja**: Tapete/caminho preferencial
        - **Vermelho**: Porta/saída de emergência
        - **Verde**: Janelas
        - **Prata**: Área inocupável
        """)
    
    with st.expander("🔄 Conversão de Imagens"):
        st.markdown("""
        **Como converter imagens PNG em mapas:**
        
        1. Prepare uma imagem PNG seguindo o esquema de cores
        2. Use a aba "Conversor de Imagens"
        3. Faça upload da imagem
        4. Clique em "Converter Imagem"
        5. Baixe os arquivos .map gerados
        
        **Arquivos gerados:**
        - `mapa.map`: Mapa principal
        - `mapa_fogo.map`: Mapa de propagação de fogo
        - `mapa_vento.map`: Mapa de direção do vento
        """)
    
    with st.expander("🎯 Simulação"):
        st.markdown("""
        **Como executar simulações:**
        
        1. Acesse a página "Simulação"
        2. Selecione um mapa existente ou crie um novo
        3. Faça upload do arquivo de indivíduos
        4. Configure os parâmetros da simulação
        5. Clique em "Executar Simulação"
        6. Visualize os resultados na página "Resultados"
        """)

with tab2:
    st.markdown("### 🔧 Referência da API")
    
    st.markdown("""
    **Serviços principais:**
    
    - `map_creation_service`: Serviço de criação e conversão de mapas
    - `simulator_integration`: Integração com o simulador
    - `nsga_integration`: Integração com NSGA-II
    
    **Métodos principais:**
    
    ```python
    # Criar mapa a partir de template
    map_data = map_creation_service.create_map_from_template('room', 20, 20)
    
    # Converter imagem em mapas
    files = map_creation_service.convert_image_to_maps('input.png', 'output')
    
    # Obter estatísticas do mapa
    stats = map_creation_service.get_map_statistics(map_data)
    ```
    """)

with tab3:
    st.markdown("### 📖 Exemplos Práticos")
    
    st.markdown("""
    **Exemplo 1: Criando uma sala simples**
    
    1. Configure um mapa 15x15
    2. Selecione template "room"
    3. Adicione portas extras conforme necessário
    4. Salve como "sala_simples"
    
    **Exemplo 2: Convertendo um mapa existente**
    
    1. Crie uma imagem PNG 20x20 pixels
    2. Use cores compatíveis (preto para paredes, branco para espaço)
    3. Converta usando a interface
    4. Use os arquivos .map gerados nas simulações
    
    **Exemplo 3: Simulação completa**
    
    1. Crie ou selecione um mapa
    2. Prepare arquivo de indivíduos (JSON)
    3. Execute simulação
    4. Analise resultados
    """)

with tab4:
    st.markdown("### ❓ Perguntas Frequentes")
    
    with st.expander("Qual o tamanho ideal para um mapa?"):
        st.markdown("""
        Mapas entre 15x15 e 30x30 pixels funcionam bem para a maioria das simulações.
        Mapas muito pequenos podem limitar a simulação, enquanto mapas muito grandes
        podem tornar a simulação lenta.
        """)
    
    with st.expander("Quantas saídas devo colocar?"):
        st.markdown("""
        Recomenda-se pelo menos 2-3 saídas para mapas pequenos e 4-6 para mapas maiores.
        A distribuição das saídas é importante para a eficiência da evacuação.
        """)
    
    with st.expander("Posso usar outras cores além das padrão?"):
        st.markdown("""
        Não. O sistema só reconhece as cores específicas do esquema padrão.
        Usar outras cores pode causar erros na conversão ou simulação.
        """)
    
    with st.expander("Como funciona a conversão de imagens?"):
        st.markdown("""
        O sistema analisa cada pixel da imagem e converte para códigos numéricos
        baseados no esquema de cores. Cada tipo de terreno tem um código específico
        que é usado pelo simulador.
        """)

st.stop()







