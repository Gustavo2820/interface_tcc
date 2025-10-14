# pages/simulacao.py
import streamlit as st
from pathlib import Path
from PIL import Image

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(page_title="Simulação", layout="wide")

# ================= CSS GLOBAL =================
st.markdown("""
    <style>
    body {
        font-family: 'Inter', 'Roboto', sans-serif;
        background-color: white;
        color: #222;
    }

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

    /* ===== BOTÕES ===== */
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
    .botao:hover {
        transform: scale(1.05);
        background-color: #1d3d57;
    }

    /* ===== LAYOUT CENTRAL ===== */
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
    .mapa {
        border: 1px solid #ccc;
        border-radius: 6px;
        width: 800px;
        height: 600px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# ================= MENU SUPERIOR =================
st.markdown("""
<div class="menu">
    <a href="../app" >Menu</a>
    <a href="./Mapas" class="active">Mapas</a>
    <a href="./Parâmetros">Parâmetros</a>
    <a href="./Resultados">Resultados</a>
    <a href="./Documentação">Documentação</a>
</div>
""", unsafe_allow_html=True)

# ================= BOTÕES SUPERIORES =================
st.markdown("""
<div class="botoes">
    <a href="#" class="botao">Salvar</a>
    <a href="./Simulado.py" class="botao">Simular</a>
</div>
""", unsafe_allow_html=True)

# ================= CONTEÚDO PRINCIPAL =================
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown('<div class="bloco">Nome</div>', unsafe_allow_html=True)
    st.text_input("", value="Nome")

    st.markdown('<div class="bloco">Algoritmo ▼</div>', unsafe_allow_html=True)
    st.text_input("", value="Nome")

    st.markdown('<div class="bloco">Parâmetros</div>', unsafe_allow_html=True)
    st.text_input("", value="Nome do arquivo")

with col2:
    # Carregar imagem do mapa selecionado
    mapa_path = Path("mapas/3.png")  # Substituir dinamicamente depois
    if mapa_path.exists():
        img = Image.open(mapa_path)
        st.image(img, use_container_width=True)
    else:
        st.warning("Nenhum mapa selecionado ou encontrado.")
