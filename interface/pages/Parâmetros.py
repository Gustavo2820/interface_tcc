# pages/Parâmetros.py
"""
Página hub para configuração de algoritmos de otimização.

Este módulo serve como ponto central de navegação para diferentes
algoritmos de otimização (Algoritmo Genético, NSGA-II, Força Bruta).
"""
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Parâmetros", layout="wide")

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

    /* ===== TÍTULO ===== */
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

    /* ===== PASTAS ===== */
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
    .folder:hover {
        transform: scale(1.07);
        box-shadow: 4px 8px 12px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# ================= MENU SUPERIOR =================
st.markdown("""
<div class="menu">
    <a href="../app" >Menu</a>
    <a href="./Mapas">Mapas</a>
    <a href="./Criacao_Mapas">Criação de Mapas</a>
    <a href="./Parâmetros" class="active">Parâmetros</a>
    <a href="./Resultados">Resultados</a>
    <a href="./Documentação">Documentação</a>
</div>
""", unsafe_allow_html=True)

# ================= TÍTULO =================
st.markdown('<div class="titulo">PARAMETRIZAÇÃO</div>', unsafe_allow_html=True)
st.markdown('<div class="linha"></div>', unsafe_allow_html=True)

# ================= PASTAS =================
st.markdown("""
<div class="folders">
    <a href="./Algoritmo_Genetico" class="folder">Algoritmo Genético</a>
    <a href="./NSGA_II" class="folder">NSGA-II</a>
    <a href="./Forca_Bruta" class="folder">Força Bruta</a>
</div>
""", unsafe_allow_html=True)

# Evita que Streamlit coloque rodapé padrão
st.stop()
