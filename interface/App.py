# app.py
"""
Aplicação principal do sistema de simulação de evacuação.

Este módulo define o ponto de entrada da aplicação Streamlit, configurando
o layout geral, estilos CSS e menu de navegação da interface.
"""
import streamlit as st

# ================= CONFIGURAÇÕES GERAIS =================
st.set_page_config(page_title="Simulação de Evacuação", layout="wide")

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
    
    /* ===== CABEÇALHO PRINCIPAL ===== */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 3rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        text-align: center;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 3rem;
        font-weight: 800;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    .main-header p {
        color: rgba(255,255,255,0.95);
        margin: 1rem 0 0 0;
        font-size: 1.3rem;
        font-weight: 300;
    }
    
    /* ===== GRID DE PÁGINAS ===== */
    .pages-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 30px;
        margin: 2rem auto;
        max-width: 1200px;
        padding: 0 2rem;
    }
    
    .page-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 15px;
        padding: 2.5rem 2rem;
        border: 2px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        text-decoration: none;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        position: relative;
        overflow: hidden;
    }
    
    .page-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .page-card:hover::before {
        opacity: 1;
    }
    
    .page-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: #667eea;
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.5);
    }
    
    .page-icon {
        font-size: 4rem;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
    }
    
    .page-title {
        color: #667eea;
        font-size: 1.4rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
    }
    
    .page-desc {
        color: #aaa;
        font-size: 0.95rem;
        text-align: center;
        line-height: 1.6;
        margin: 0;
    }
    
    /* ===== BOTÕES (tema principal) ===== */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 10px 24px;
        border: none;
        transition: 0.2s ease-in-out;
        box-shadow: 0 3px 10px rgba(0,0,0,0.3);
    }
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.45);
    }
    </style>
""", unsafe_allow_html=True)

# ===== MENU SUPERIOR =====
st.markdown("""
    <div class="menu">
        <a class="active" href="/">Menu</a>
        <a href="/Mapas">Mapas</a>
        <a href="/Criação_de_Mapas">Criação de Mapas</a>
        <a href="/Parâmetros">Parâmetros</a>
        <a href="/Simulação">Simulação</a>
        <a href="/Resultados">Resultados</a>
        <a href="/Documentação">Documentação</a>
    </div>
""", unsafe_allow_html=True)

# ===== CABEÇALHO PRINCIPAL =====
st.markdown("""
    <div class="main-header">
        <h1>🏢 Simulação de Evacuação</h1>
        <p>Simule evacuações e otimize a segurança com algoritmos avançados</p>
    </div>
""", unsafe_allow_html=True)

# ===== GRID DE PÁGINAS =====
st.markdown("## 🚀 Acesso Rápido")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 15px; border: 2px solid rgba(102, 126, 234, 0.3);">
        <div style="font-size: 4rem;">🗺️</div>
        <h3 style="color: #667eea; margin: 1rem 0 0.5rem 0;">Mapas</h3>
        <p style="color: #aaa; font-size: 0.95rem;">Gerencie e visualize mapas de evacuação</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir para Mapas", key="btn_mapas", use_container_width=True):
        st.switch_page("pages/Mapas.py")

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 15px; border: 2px solid rgba(102, 126, 234, 0.3);">
        <div style="font-size: 4rem;">🎨</div>
        <h3 style="color: #667eea; margin: 1rem 0 0.5rem 0;">Criação de Mapas</h3>
        <p style="color: #aaa; font-size: 0.95rem;">Crie mapas personalizados com editor gráfico</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir para Criação", key="btn_criacao", use_container_width=True):
        st.switch_page("pages/Criacao_Mapas.py")

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 15px; border: 2px solid rgba(102, 126, 234, 0.3);">
        <div style="font-size: 4rem;">⚙️</div>
        <h3 style="color: #667eea; margin: 1rem 0 0.5rem 0;">Parâmetros</h3>
        <p style="color: #aaa; font-size: 0.95rem;">Configure algoritmos de otimização</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir para Parâmetros", key="btn_params", use_container_width=True):
        st.switch_page("pages/Parâmetros.py")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 15px; border: 2px solid rgba(102, 126, 234, 0.3);">
        <div style="font-size: 4rem;">🎯</div>
        <h3 style="color: #667eea; margin: 1rem 0 0.5rem 0;">Simulação</h3>
        <p style="color: #aaa; font-size: 0.95rem;">Execute simulações de evacuação</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir para Simulação", key="btn_sim", use_container_width=True):
        st.switch_page("pages/Simulação.py")

with col5:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 15px; border: 2px solid rgba(102, 126, 234, 0.3);">
        <div style="font-size: 4rem;">📊</div>
        <h3 style="color: #667eea; margin: 1rem 0 0.5rem 0;">Resultados</h3>
        <p style="color: #aaa; font-size: 0.95rem;">Visualize e analise resultados</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir para Resultados", key="btn_results", use_container_width=True):
        st.switch_page("pages/Resultados.py")

with col6:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 15px; border: 2px solid rgba(102, 126, 234, 0.3);">
        <div style="font-size: 4rem;">📚</div>
        <h3 style="color: #667eea; margin: 1rem 0 0.5rem 0;">Documentação</h3>
        <p style="color: #aaa; font-size: 0.95rem;">Guias, APIs e exemplos</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir para Documentação", key="btn_docs", use_container_width=True):
        st.switch_page("pages/Documentação.py")

st.markdown("<br>", unsafe_allow_html=True)

# Removed reset button per UI polish request

# Impede o rodapé padrão do Streamlit
st.stop()
