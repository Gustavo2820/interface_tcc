# pages/Algoritmo_Genetico.py
"""
Interface para configuração do Algoritmo Genético.

Este módulo permite aos usuários fazer upload de arquivos de configuração
para execução do algoritmo genético de otimização.
"""
import streamlit as st
from pathlib import Path

# ================= CONFIGURAÇÃO =================
st.set_page_config(page_title="Algoritmo Genético", layout="wide")

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
    .menu { display: flex; justify-content: center; gap: 40px; margin-bottom: 40px; font-size: 20px; font-weight: 600; }
    .menu a { text-decoration: none; color: #aaa; }
    tulo { text-align: center; font-size: 36px; font-weight: 700; margin-bottom: 10px; }
    .linha { width: 200px; height: 2px; background-color: #444; margin: 0 auto 40px auto; }
    .upload-box { border: 2px dashed #083d77; border-radius: 12px; padding: 40px; background-color: #f9f9f9; text-align: center; }
    .success { text-align: center; color: green; font-weight: bold; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

# ================= MENU SUPERIOR =================
st.markdown("""
<div class="menu">
    <a href="../app">Menu</a>
    <a href="./Mapas">Mapas</a>
    <a href="./Parâmetros" class="active">Parâmetros</a>
    <a href="./Resultados">Resultados</a>
    <a href="./Documentação">Documentação</a>
</div>
""", unsafe_allow_html=True)

# ================= CONTEÚDO =================
st.markdown('<div class="titulo">Algoritmo Genético</div>', unsafe_allow_html=True)
st.markdown('<div class="linha"></div>', unsafe_allow_html=True)

st.markdown('<div class="upload-box">', unsafe_allow_html=True)
arquivo = st.file_uploader("Selecione o arquivo de parametrização (formato .json, .csv ou .txt):", type=["json", "csv", "txt"])
st.markdown('</div>', unsafe_allow_html=True)

if arquivo:
    pasta = Path("uploads/algoritmo_genetico")
    pasta.mkdir(parents=True, exist_ok=True)
    caminho = pasta / arquivo.name
    with open(caminho, "wb") as f:
        f.write(arquivo.getbuffer())
    st.markdown(f'<p class="success">✅ Arquivo "{arquivo.name}" enviado com sucesso!</p>', unsafe_allow_html=True)

st.stop()
