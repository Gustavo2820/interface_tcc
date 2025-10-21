# pages/Detalhes.py
"""
Interface para visualização detalhada de mapas específicos.

Este módulo exibe a imagem do mapa, informações sobre simulações relacionadas
e botões de navegação para outras funcionalidades.
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import base64
import urllib.parse

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(page_title="Detalhes do Mapa", layout="wide")

# ================= CSS GLOBAL =================
st.markdown("""
    <style>
    body { font-family: 'Inter', 'Roboto', sans-serif; background-color: #0e1117; color: #e0e0e0; }

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
    .titulo { text-align: center; font-size: 36px; font-weight: 700; margin-bottom: 10px; color: #fff; }
    .linha { width: 200px; height: 2px; background-color: #1e90ff; margin: 0 auto 40px auto; }

    /* ===== BOTÕES ===== */
    .botoes { display: flex; justify-content: center; gap: 20px; margin-bottom: 40px; }
    .botao { background-color: #1e90ff; color: white; border-radius: 8px; padding: 12px 28px; font-size: 18px; font-weight: 600; text-decoration: none; display: inline-flex; align-items: center; gap: 8px; transition: all 0.2s ease-in-out; }
    .botao:hover { background-color: #0072e0; transform: scale(1.05); }

    /* ===== IMAGEM ===== */
    .mapa-imagem { display: flex; justify-content: center; margin-bottom: 30px; }
    .mapa-imagem img { border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); max-width: 70%; height: auto; }

    /* ===== TABELA ===== */
    .tabela-container { display: flex; justify-content: center; }
    table.tabela { border-collapse: collapse; width: 80%; font-size: 18px; text-align: center; border-radius: 10px; overflow: hidden; box-shadow: 0 0 15px rgba(255,255,255,0.1); }
    table.tabela thead { background-color: #1e2b3b; color: #fff; }
    table.tabela th, table.tabela td { padding: 14px 20px; border-bottom: 1px solid #333; }
    table.tabela td { background-color: #181c24; color: #e0e0e0; }
    table.tabela tr:hover { background-color: rgba(255,255,255,0.05); }
    table.tabela tr:last-child td { border-bottom: none; }
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

# ================= OBTÉM O MAPA SELECIONADO =================
params = st.query_params
mapa_nome = params.get("mapa", [""])[0] if isinstance(params.get("mapa"), list) else params.get("mapa", "")

# ================= TÍTULO =================
if mapa_nome:
    st.markdown(f'<div class="titulo">{mapa_nome.upper()}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="titulo">DETALHES DO MAPA</div>', unsafe_allow_html=True)
st.markdown('<div class="linha"></div>', unsafe_allow_html=True)

# ================= EXIBE A IMAGEM DO MAPA =================
mapa_path = Path("mapas") / f"{mapa_nome}.png"
if mapa_nome and mapa_path.exists():
    with open(mapa_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")
    st.markdown(f"""
        <div class="mapa-imagem">
            <img src="data:image/png;base64,{img_b64}" alt="{mapa_nome}" />
        </div>
    """, unsafe_allow_html=True)
elif mapa_nome:
    st.warning("⚠️ Arquivo do mapa não encontrado.")
else:
    st.info("Selecione um mapa para ver os detalhes.")

# ================= BOTÕES =================
simulacao_url = f"./Simulação?mapa={urllib.parse.quote(mapa_nome)}" if mapa_nome else "./Simulação"
st.markdown(f"""
<div class="botoes">
    <a href="./Mapas" class="botao">← Voltar aos Mapas</a>
    <a href="#" class="botao">🔍 Pesquisar</a>
    <a href="{simulacao_url}" class="botao">⚙️ Criar simulação</a>
</div>
""", unsafe_allow_html=True)

# ================= TABELA DE SIMULAÇÕES (REAL) =================
sys.path.append(str(Path(__file__).parent.parent))
from services.simulator_integration import DatabaseIntegration

db = DatabaseIntegration()
simulations = []
if mapa_nome:
    try:
        simulations = db.get_simulations_by_map(mapa_nome)
    except Exception:
        simulations = []

if simulations:
    rows_html = "".join([
        f"<tr>"
        f"<td>{sim['id']}</td>"
        f"<td>{sim['nome']}</td>"
        f"<td>{sim['mapa']}</td>"
        f"<td>{sim['algoritmo']}</td>"
        f"<td>{sim['simulado']}</td>"
    f"<td><a href='./Simulação?sim_id={sim['id']}' class='botao' style='background:#2d7dff;padding:6px 10px;border-radius:6px;color:#fff;text-decoration:none;'>Ver</a></td>"
        f"</tr>"
        for sim in simulations
    ])

    table_html = f"""
    <div class="tabela-container">
        <table class="tabela">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>NOME</th>
                    <th>MAPA</th>
                    <th>ALGORITMO</th>
                    <th>SIMULADO</th>
                    <th>AÇÕES</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)
else:
    st.info("Nenhuma simulação registrada para este mapa.")

# Botões de ação: Nova Simulação (pre-seleciona mapa)
nova_sim_url = f"./Simulação?mapa={urllib.parse.quote(mapa_nome)}" if mapa_nome else "./Simulação"
st.markdown(f"""
<div style='display:flex; gap:12px; justify-content:center; margin-top:18px;'>
    <a href="{nova_sim_url}" class="botao">+ Nova Simulação</a>
    <a href="./Mapas" class="botao" style='background:#333;'>Voltar</a>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.stop()
