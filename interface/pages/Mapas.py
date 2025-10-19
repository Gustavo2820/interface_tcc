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

# ================= CSS GLOBAL =================
st.markdown("""
    <style>
     /* ===== MENU SUPERIOR ===== */
    .menu {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-bottom: 40px;
        font-size: 20px;
        font-weight: 600;
    }
    .menu a {
        text-decoration: none;
        color: #bbb;
        transition: color 0.2s;
    }
    .menu a:hover {
        color: #fff;
    }
    .menu a.active {
        color: #fff;
        font-weight: 700;
        border-bottom: 2px solid #1e90ff;
        padding-bottom: 4px;
    }       

    body { font-family: 'Inter', 'Roboto', sans-serif; background-color: white; color: #222; }
    .menu { display: flex; justify-content: center; gap: 40px; margin-bottom: 50px; font-size: 20px; font-weight: 600; }
    .menu a { text-decoration: none; color: #aaa; }
    .titulo { text-align: center; font-size: 36px; font-weight: 700; margin-bottom: 10px; }
    .linha { width: 200px; height: 2px; background-color: #444; margin: 0 auto 50px auto; }
    .mapa-container { text-align: center; }
    /* Cards e miniaturas normalizadas, mantendo proporção */
    .mapa-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; }
    .mapa-card { width: 100%; max-width: 520px; margin: 0 auto 20px; text-align: center; background:#fff; border:1px solid #e8e8e8; border-radius:12px; padding:12px; box-shadow:0 2px 8px rgba(0,0,0,0.04); }
    .mapa-legenda { font-size: 16px; font-weight: 500; margin-top: 8px; color: #333; }
    .mapa-link img { border-radius: 10px; transition: transform 0.2s ease; cursor: pointer; width:100%; height:auto; max-height: 360px; }
    .mapa-link img:hover { transform: scale(1.03); }
    </style>
""", unsafe_allow_html=True)

# ================= MENU SUPERIOR =================
st.markdown("""
<div class="menu">
    <a href="../app" >Menu</a>
    <a href="./Mapas" class="active" >Mapas</a>
    <a href="./Criacao_Mapas">Criação de Mapas</a>
    <a href="./Parâmetros">Parâmetros</a>
    <a href="./Resultados">Resultados</a>
    <a href="./Documentação">Documentação</a>
</div>
""", unsafe_allow_html=True)

# ================= TÍTULO =================
st.markdown('<div class="titulo">MAPAS</div>', unsafe_allow_html=True)
st.markdown('<div class="linha"></div>', unsafe_allow_html=True)

# ================= FUNCIONALIDADES DE UPLOAD =================
mapas_dir = Path("mapas")
mapas_dir.mkdir(exist_ok=True)

# Botão para criar novo mapa
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🎨 Criar Novo Mapa", help="Abre o editor de mapas"):
        st.markdown('<script>window.location.href = "./Criacao_Mapas";</script>', unsafe_allow_html=True)

with col2:
    st.write("ou faça upload de um mapa existente:")

uploaded = st.file_uploader("Adicionar novo mapa (.png)", type=["png"])
if uploaded:
    dest = mapas_dir / uploaded.name
    with open(dest, "wb") as f:
        shutil.copyfileobj(uploaded, f)
    st.success(f"Mapa '{uploaded.name}' adicionado com sucesso!")
    st.rerun()  # recarrega para mostrar o novo mapa imediatamente

# ================= EXIBIÇÃO DE MAPAS EXISTENTES =================
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
            href = f"/?page=Detalhes&mapa={mapa_nome_url}"

            st.markdown(
                f'''
                <div class="mapa-card">
                  <a class="mapa-link" href="{href}">
                    <img src="data:image/png;base64,{img_b64}" alt="{mapa_nome}" />
                  </a>
                  <div class="mapa-legenda">{mapa_nome}</div>
                </div>
                ''',
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Erro ao carregar {mapa.name}: {e}")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Nenhum mapa adicionado ainda. Use o botão acima para adicionar um.")

st.stop()
