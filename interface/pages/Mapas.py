# pages/Mapas.py
"""
Página de gerenciamento e visualização de mapas de evacuação.

Este módulo permite aos usuários fazer upload de novos mapas, visualizar
mapas existentes e navegar para páginas de detalhes específicos.
"""
import streamlit as st
from pathlib import Path
import shutil
import base64
import urllib.parse

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(page_title="Mapas", layout="wide")

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
    
    /* ===== BOTÕES ===== */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 16px;
        border: none;
        transition: 0.2s ease-in-out;
        box-shadow: 0 3px 10px rgba(0,0,0,0.3);
    }
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.5);
    }
    
    /* ===== CARDS DE MAPAS ===== */
    .mapa-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 24px;
        margin-top: 2rem;
    }
    .mapa-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 12px;
        padding: 16px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        transition: 0.3s ease-in-out;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .mapa-card:hover {
        transform: translateY(-5px);
        border-color: #667eea;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    .mapa-link img {
        border-radius: 8px;
        width: 100%;
        height: auto;
        max-height: 250px;
        object-fit: contain;
        image-rendering: -webkit-optimize-contrast;
        image-rendering: crisp-edges;
        image-rendering: pixelated;
    }
    .mapa-legenda {
        font-size: 18px;
        font-weight: 600;
        margin-top: 12px;
        color: #667eea;
        text-align: center;
    }
    
    /* ===== UPLOAD SECTION ===== */
    .upload-section {
        background: rgba(26, 26, 46, 0.3);
        border-radius: 10px;
        padding: 1.5rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ===== MENU SUPERIOR =====
st.markdown("""
    <div class="menu">
        <a href="/">Menu</a>
        <a class="active" href="/Mapas">Mapas</a>
        <a href="/Criação_de_Mapas">Criação de Mapas</a>
        <a href="/Parâmetros">Parâmetros</a>
        <a href="/Simulação">Simulação</a>
        <a href="/Resultados">Resultados</a>
        <a href="/Documentação">Documentação</a>
    </div>
""", unsafe_allow_html=True)

# ===== CABEÇALHO DA PÁGINA =====
st.markdown("""
    <div class="page-header">
        <h1>🗺️ Gerenciamento de Mapas</h1>
        <p>Visualize, faça upload e gerencie mapas de evacuação</p>
    </div>
""", unsafe_allow_html=True)

# ================= FUNCIONALIDADES DE UPLOAD =================
mapas_dir = Path("mapas")
mapas_dir.mkdir(exist_ok=True)

st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown("### 📤 Adicionar Novo Mapa")

col1, col2 = st.columns([1, 2])
with col1:
    if st.button("🎨 Criar Novo Mapa", help="Abre o editor de mapas", use_container_width=True):
        st.switch_page("pages/Criacao_Mapas.py")

with col2:
    uploaded = st.file_uploader("Ou faça upload de um mapa (.png)", type=["png"], label_visibility="collapsed")
    if uploaded:
        dest = mapas_dir / uploaded.name
        with open(dest, "wb") as f:
            shutil.copyfileobj(uploaded, f)
        st.success(f"✅ Mapa '{uploaded.name}' adicionado com sucesso!")
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ================= EXIBIÇÃO DE MAPAS EXISTENTES =================
st.markdown("### 🗂️ Mapas Disponíveis")

mapas = sorted(mapas_dir.glob("*.png"))
if mapas:
    st.markdown('<div class="mapa-grid">', unsafe_allow_html=True)
    for mapa in mapas:
        try:
            with open(mapa, "rb") as f:
                data = f.read()
            img_b64 = base64.b64encode(data).decode("utf-8")
            mapa_nome = mapa.stem
            mapa_nome_url = urllib.parse.quote_plus(mapa_nome)
            
            # Cria botão para navegar para detalhes
            col_card = st.columns(1)[0]
            with col_card:
                st.markdown(
                    f'''
                    <div class="mapa-card">
                      <a class="mapa-link" href="/Detalhes?mapa={mapa_nome_url}">
                        <img src="data:image/png;base64,{img_b64}" alt="{mapa_nome}" />
                      </a>
                      <div class="mapa-legenda">{mapa_nome}</div>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
        except Exception as e:
            st.error(f"⚠️ Erro ao carregar {mapa.name}: {e}")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("📭 Nenhum mapa adicionado ainda. Use o botão acima para adicionar um.")

st.stop()
