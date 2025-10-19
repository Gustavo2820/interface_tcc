"""
Interface para visualização de resultados de simulações.

Este módulo exibe uma tabela com informações sobre simulações executadas,
incluindo ID, nome, mapa, algoritmo e status de execução.
"""
import streamlit as st
import sys
from pathlib import Path

# Adiciona o caminho dos serviços ao sys.path
sys.path.append(str(Path(__file__).parent.parent))

from services.simulator_integration import DatabaseIntegration

# Configuração da página
st.set_page_config(page_title="Resultados", layout="wide")

# ================= CSS GLOBAL =================
st.markdown("""
    <style>
    body {
        font-family: 'Inter', 'Roboto', sans-serif;
        background-color: #0e1117;
        color: #e0e0e0;
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

    /* ===== BOTÃO PESQUISAR ===== */
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
    .btn-pesquisar:hover {
        transform: scale(1.05);
        background-color: #0072e0;
    }
    .btn-pesquisar::before {
        content: "\\1F50D"; /* Lupa */
        font-size: 20px;
    }

    /* ===== TABELA ===== */
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
    table.tabela thead {
        background-color: #1e2b3b;
        color: #fff;
    }
    table.tabela th, table.tabela td {
        padding: 14px 20px;
        border-bottom: 1px solid #333;
    }
    table.tabela tr:hover {
        background-color: rgba(255, 255, 255, 0.05);
    }
    table.tabela td {
        background-color: #181c24;
        color: #e0e0e0;
    }
    table.tabela tr:last-child td {
        border-bottom: none;
    }
    </style>
""", unsafe_allow_html=True)

# ================= MENU SUPERIOR =================
st.markdown("""
<div class="menu">
    <a href="../app" >Menu</a>
    <a href="./Mapas">Mapas</a>
    <a href="./Criacao_Mapas">Criação de Mapas</a>
    <a href="./Parâmetros">Parâmetros</a>
    <a href="./Resultados" class="active">Resultados</a>
    <a href="./Documentação">Documentação</a>
</div>
""", unsafe_allow_html=True)

# ================= INICIALIZAÇÃO DO BANCO =================
if 'db_integration' not in st.session_state:
    st.session_state.db_integration = DatabaseIntegration()

# ================= BOTÃO PESQUISAR =================
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🔄 Atualizar Lista", key="refresh_button"):
        st.rerun()

# ================= CARREGA DADOS DO BANCO =================
simulations = st.session_state.db_integration.get_simulations()

# ================= TABELA =================
if simulations:
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
    """, unsafe_allow_html=True)
    
    for sim in simulations:
        st.markdown(f"""
            <tr>
                <td>{sim['id']}</td>
                <td>{sim['nome']}</td>
                <td>{sim['mapa']}</td>
                <td>{sim['algoritmo']}</td>
                <td>{sim['simulado']}</td>
            </tr>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        </tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)
else:
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
                <td colspan="5" style="text-align: center; color: #888;">Nenhuma simulação encontrada</td>
            </tr>
        </tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

# Evita que Streamlit coloque rodapé padrão
st.stop()
