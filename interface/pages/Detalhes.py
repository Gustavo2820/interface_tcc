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

# ================= CSS GLOBAL MODERNIZADO =================
st.markdown("""
    <style>
    /* ===== RESET E GLOBAL ===== */
    body { 
        font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif; 
        background-color: #0e1117; 
        color: #e0e0e0; 
    }

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
        border-bottom: 2px solid #1e90ff;
        padding-bottom: 4px;
    }

    /* ===== CABEÇALHO DA PÁGINA ===== */
    .page-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        text-align: center;
    }
    .page-header h1 {
        color: white;
        margin: 0;
        font-size: 2.8rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .page-header p {
        color: rgba(255,255,255,0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }

    /* ===== CONTAINER DO MAPA ===== */
    .map-showcase {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem auto;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        border: 1px solid rgba(102, 126, 234, 0.2);
        max-width: 800px;
        text-align: center;
    }
    
    .map-showcase img {
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.5);
        max-width: 600px;
        width: auto;
        height: auto;
        display: inline-block;
        image-rendering: -webkit-optimize-contrast;
        image-rendering: crisp-edges;
        image-rendering: pixelated;
    }

    /* ===== BOTÕES PRINCIPAIS ===== */
    .action-buttons {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 14px 32px;
        font-size: 16px;
        font-weight: 600;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        border: none;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    
    .btn-secondary {
        background: #2d3748;
        color: white;
        border-radius: 10px;
        padding: 14px 32px;
        font-size: 16px;
        font-weight: 600;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        transition: all 0.3s ease;
        border: 1px solid #4a5568;
    }
    
    .btn-secondary:hover {
        background: #3d4758;
        transform: translateY(-2px);
    }

    /* ===== SEÇÃO DE SIMULAÇÕES ===== */
    .simulations-section {
        background: rgba(26, 26, 46, 0.5);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .section-title {
        color: #667eea;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.3);
    }

    /* ===== TABELA MODERNIZADA ===== */
    .modern-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 1.5rem 0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    .modern-table thead {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .modern-table th {
        padding: 16px 20px;
        color: white;
        font-weight: 600;
        text-align: left;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .modern-table tbody tr {
        background-color: #1a1a2e;
        transition: all 0.2s ease;
    }
    
    .modern-table tbody tr:hover {
        background-color: #252541;
        transform: scale(1.01);
    }
    
    .modern-table td {
        padding: 16px 20px;
        color: #e0e0e0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        font-size: 15px;
    }
    
    .modern-table tbody tr:last-child td {
        border-bottom: none;
    }

    /* ===== BADGES E INDICADORES ===== */
    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-success {
        background: rgba(72, 187, 120, 0.2);
        color: #68d391;
        border: 1px solid #68d391;
    }
    
    .badge-warning {
        background: rgba(237, 137, 54, 0.2);
        color: #ed8936;
        border: 1px solid #ed8936;
    }

    /* ===== BOTÃO DE AÇÃO NA TABELA ===== */
    .table-action-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 8px;
        text-decoration: none;
        font-size: 14px;
        font-weight: 600;
        transition: all 0.2s ease;
        display: inline-block;
    }
    
    .table-action-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }

    /* ===== INFO BOX ===== */
    .info-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .info-box-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
    }

    /* ===== RESPONSIVIDADE ===== */
    @media (max-width: 768px) {
        .action-buttons {
            flex-direction: column;
            align-items: stretch;
        }
        
        .btn-primary, .btn-secondary {
            width: 100%;
            justify-content: center;
        }
        
        .modern-table {
            font-size: 13px;
        }
        
        .modern-table th, .modern-table td {
            padding: 10px 12px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ================= MENU SUPERIOR =================
st.markdown("""
<div class="menu">
    <a href="/">Menu</a>
    <a href="/Mapas" class="active">Mapas</a>
    <a href="/Criação_de_Mapas">Criação de Mapas</a>
    <a href="/Parâmetros">Parâmetros</a>
    <a href="/Simulação">Simulação</a>
    <a href="/Resultados">Resultados</a>
    <a href="/Documentação">Documentação</a>
</div>
""", unsafe_allow_html=True)

# ================= OBTÉM O MAPA SELECIONADO =================
params = st.query_params
mapa_nome = params.get("mapa", [""])[0] if isinstance(params.get("mapa"), list) else params.get("mapa", "")

# ================= CABEÇALHO DA PÁGINA =================
if mapa_nome:
    st.markdown(f"""
        <div class="page-header">
            <h1>🗺️ {mapa_nome}</h1>
            <p>Visualização detalhada e simulações relacionadas</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="page-header">
            <h1>📋 Detalhes do Mapa</h1>
            <p>Selecione um mapa para visualizar informações detalhadas</p>
        </div>
    """, unsafe_allow_html=True)

# ================= EXIBE A IMAGEM DO MAPA =================
mapa_path = Path("mapas") / f"{mapa_nome}.png"
if mapa_nome and mapa_path.exists():
    with open(mapa_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")
    st.markdown(f"""
        <div class="map-showcase">
            <img src="data:image/png;base64,{img_b64}" alt="{mapa_nome}" />
        </div>
    """, unsafe_allow_html=True)
elif mapa_nome:
    st.markdown("""
        <div class="info-box">
            <span class="info-box-icon">⚠️</span>
            <span>Arquivo do mapa não encontrado no diretório.</span>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="info-box">
            <span class="info-box-icon">ℹ️</span>
            <span>Selecione um mapa na página de Mapas para visualizar detalhes.</span>
        </div>
    """, unsafe_allow_html=True)

# ================= BOTÕES DE AÇÃO PRINCIPAL =================
simulacao_url = f"/Simulação?mapa={urllib.parse.quote(mapa_nome)}" if mapa_nome else "/Simulação"
st.markdown(f"""
<div class="action-buttons">
    <a href="/Mapas" class="btn-secondary">← Voltar aos Mapas</a>
    <a href="{simulacao_url}" class="btn-primary">⚙️ Criar Simulação com este Mapa</a>
</div>
""", unsafe_allow_html=True)

# ================= SEÇÃO DE SIMULAÇÕES =================
sys.path.append(str(Path(__file__).parent.parent))
from services.simulator_integration import DatabaseIntegration

db = DatabaseIntegration()
simulations = []
if mapa_nome:
    try:
        simulations = db.get_simulations_by_map(mapa_nome)
    except Exception:
        simulations = []

st.markdown('<div class="simulations-section">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📊 Simulações Realizadas</h2>', unsafe_allow_html=True)

if simulations:
    rows_html = "".join([
        f"""<tr>
            <td><strong>#{sim['id']}</strong></td>
            <td>{sim['nome']}</td>
            <td><span class="badge badge-success">{sim['algoritmo']}</span></td>
            <td>{"<span class='badge badge-success'>✓ Sim</span>" if sim.get('simulado') == 'SIM' else "<span class='badge badge-warning'>✗ Não</span>"}</td>
            <td><a href='/Simulação?sim_id={sim['id']}' class='table-action-btn'>👁️ Visualizar</a></td>
        </tr>"""
        for sim in simulations
    ])

    table_html = f"""
        <table class="modern-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nome da Simulação</th>
                    <th>Algoritmo</th>
                    <th>Status</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Estatísticas rápidas
    total_sims = len(simulations)
    executadas = sum(1 for sim in simulations if sim.get('simulado') == 'SIM')
    
    st.markdown(f"""
        <div style="display: flex; gap: 20px; justify-content: center; margin-top: 1.5rem;">
            <div class="info-box" style="flex: 1; max-width: 300px; text-align: center;">
                <div style="font-size: 2rem; font-weight: 700; color: #667eea;">{total_sims}</div>
                <div style="color: #aaa; font-size: 0.9rem;">Total de Simulações</div>
            </div>
            <div class="info-box" style="flex: 1; max-width: 300px; text-align: center;">
                <div style="font-size: 2rem; font-weight: 700; color: #68d391;">{executadas}</div>
                <div style="color: #aaa; font-size: 0.9rem;">Simulações Executadas</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="info-box">
            <span class="info-box-icon">📭</span>
            <span>Nenhuma simulação registrada para este mapa. Crie uma nova simulação para começar!</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ================= BOTÕES DE AÇÃO FINAL =================
nova_sim_url = f"/Simulação?mapa={urllib.parse.quote(mapa_nome)}" if mapa_nome else "/Simulação"
st.markdown(f"""
<div class="action-buttons" style="margin-top: 2rem;">
    <a href="{nova_sim_url}" class="btn-primary">➕ Nova Simulação</a>
    <a href="/Resultados" class="btn-secondary">📈 Ver Todos os Resultados</a>
    <a href="/Mapas" class="btn-secondary">🗺️ Voltar aos Mapas</a>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.stop()
