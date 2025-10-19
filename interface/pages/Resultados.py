"""
Interface para visualização de resultados de simulações.
Versão aprimorada — visual simples e limpo mantendo identidade original.
"""
import streamlit as st
import json
import sys
from pathlib import Path

# Adiciona o caminho dos serviços ao sys.path
sys.path.append(str(Path(__file__).parent.parent))

from services.simulator_integration import DatabaseIntegration, SimulatorIntegration

# ================= CONFIGURAÇÃO DA PÁGINA =================
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

    /* ===== BOTÃO ATUALIZAR ===== */
    .stButton button {
        background-color: #1e90ff;
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
        background-color: #0072e0;
    }

    /* ===== TABELA ===== */
    .tabela-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    table.tabela {
        border-collapse: collapse;
        width: 85%;
        font-size: 17px;
        text-align: center;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 0 12px rgba(255,255,255,0.05);
    }
    table.tabela thead {
        background-color: #1e2b3b;
        color: #fff;
    }
    table.tabela th, table.tabela td {
        padding: 12px 18px;
        border-bottom: 1px solid #2a2f38;
    }
    table.tabela tr:hover td {
        background-color: rgba(255,255,255,0.05);
    }
    a.sim-link {
        color: #1e90ff;
        text-decoration: none;
    }
    a.sim-link:hover {
        text-decoration: underline;
    }

    /* ===== SEPARADORES E TÍTULOS ===== */
    hr {
        border: 0;
        height: 1px;
        background: #333;
        margin: 30px 0;
    }
    .section-title {
        font-size: 22px;
        font-weight: 600;
        color: #fff;
        margin-bottom: 12px;
    }

    /* ===== MÉTRICAS ===== */
    .metric-card {
        background-color: #181c24;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
    }
    .metric-label {
        color: #aaa;
        font-size: 14px;
    }
    .metric-value {
        color: #1e90ff;
        font-size: 28px;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# ================= MENU SUPERIOR =================
st.markdown("""
<div class="menu">
    <a href="../app">Menu</a>
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
if 'simulator_integration' not in st.session_state:
    st.session_state.simulator_integration = SimulatorIntegration()

# ================= BOTÃO ATUALIZAR =================
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🔄 Atualizar Lista"):
        st.rerun()

# ================= TABELA DE SIMULAÇÕES =================
simulations = st.session_state.db_integration.get_simulations()

if simulations:
    rows_html = "".join([
        f"<tr>"
        f"<td>{sim['id']}</td>"
        f"<td><a class='sim-link' href='?sim={sim['nome']}'>{sim['nome']}</a></td>"
        f"<td>{sim['mapa']}</td>"
        f"<td>{sim['algoritmo']}</td>"
        f"<td>{sim['simulado']}</td>"
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
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)
    # Filtro de seleção (fallback caso link não funcione)
    nomes = [s['nome'] for s in simulations]
    default_idx = nomes.index(st.query_params.get("sim")) if isinstance(st.query_params.get("sim"), str) and st.query_params.get("sim") in nomes else 0
    sel = st.selectbox("Selecione para ver detalhes", options=nomes, index=default_idx if nomes else 0, key="sel_resultados")
    if sel and sel != st.query_params.get("sim"):
        try:
            st.query_params["sim"] = sel
            st.rerun()
        except Exception:
            pass
else:
    st.info("Nenhuma simulação encontrada.")

# ================= DETALHES DA SIMULAÇÃO =================
params = st.query_params
selected_name = params.get("sim")
if isinstance(selected_name, list):
    selected_name = selected_name[0]

if selected_name:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>Detalhes da Simulação: <span style='color:#1e90ff'>{selected_name}</span></div>", unsafe_allow_html=True)

    res = st.session_state.simulator_integration.read_results(selected_name)

    if 'error' in res:
        st.warning(res['error'])
    else:
        metrics_files = res.get('metrics', [])
        shown_metric = False

        # ===== EXIBE MÉTRICAS =====
        for mf in metrics_files:
            if str(mf).endswith('.json'):
                try:
                    with open(mf, 'r') as f:
                        data = json.load(f)
                        iterations_value = data.get('iterations')
                        distance_value = data.get('distance')

                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"""
                                <div class='metric-card'>
                                    <div class='metric-label'>Iterações</div>
                                    <div class='metric-value'>{iterations_value}</div>
                                </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"""
                                <div class='metric-card'>
                                    <div class='metric-label'>Distância</div>
                                    <div class='metric-value'>{round(distance_value,3)}</div>
                                </div>
                            """, unsafe_allow_html=True)
                        # Série temporal se disponível
                        series = data.get('mean_distance_series') or []
                        if series:
                            st.markdown("<div class='section-title'>Média da distância por iteração</div>", unsafe_allow_html=True)
                            try:
                                import pandas as pd
                                import numpy as np
                                df = pd.DataFrame({"iteration": list(range(len(series))), "mean_distance": series})
                                st.line_chart(df.set_index("iteration"))
                            except Exception:
                                st.text("Série disponível mas não foi possível plotar.")
                        evac = data.get('evacuated_progress') or []
                        if evac:
                            st.markdown("<div class='section-title'>Progresso de evacuação (%)</div>", unsafe_allow_html=True)
                            try:
                                import pandas as pd
                                df2 = pd.DataFrame({"iteration": list(range(len(evac))), "evacuated_pct": evac})
                                st.line_chart(df2.set_index("iteration"))
                            except Exception:
                                st.text("Progresso disponível mas não foi possível plotar.")
                        shown_metric = True
                        break
                except Exception:
                    continue

        if not shown_metric:
            if metrics_files:
                st.markdown("#### Métricas (texto)")
                for mf in metrics_files:
                    try:
                        with open(mf, 'r') as f:
                            st.text(f"{mf.name}:\n" + f.read())
                    except Exception:
                        continue
            else:
                st.info("Nenhuma métrica encontrada.")

        # ===== FRAMES =====
        frames = res.get('frames', [])
        if frames:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Frames</div>", unsafe_allow_html=True)
            idx = st.slider("Frame", min_value=1, max_value=len(frames), value=len(frames))
            st.image(str(frames[idx-1]), use_container_width=True)

        # ===== RELATÓRIO =====
        report = res.get('report')
        if report:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(f"📄 **Relatório:** `{report}`")

        # ===== NSGA-II: soluções otimizadas (saídas/portas) =====
        # Heurística: quando a simulação foi NSGA-II, procurar resultados em uploads/nsga_ii/*.json
        try:
            # descobre algoritmo da linha selecionada
            alg = None
            for s in simulations:
                if s['nome'] == selected_name:
                    alg = s.get('algoritmo')
                    break
            if alg and 'NSGA' in alg:
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("<div class='section-title'>Soluções Otimizadas (NSGA-II)</div>", unsafe_allow_html=True)
                from pathlib import Path as _P
                nsga_dir = _P("uploads")/"nsga_ii"
                pareto_files = list(nsga_dir.glob("*.json")) if nsga_dir.exists() else []
                if pareto_files:
                    # tenta achar um arquivo com o nome da simulação, senão usa o mais recente
                    pf = None
                    for f in pareto_files:
                        if selected_name in f.stem:
                            pf = f
                            break
                    pf = pf or sorted(pareto_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]
                    with open(pf,'r') as f:
                        data_pf = json.load(f)
                    if isinstance(data_pf, list) and data_pf:
                        # Constrói uma pequena tabela e seleção
                        options = [f"gen {it.get('generation',0)} - obj {it.get('objectives',[None,None])}" for it in data_pf]
                        idx_sel = st.selectbox("Escolha uma solução da frente de Pareto", options=list(range(len(options))), format_func=lambda i: options[i])
                        sol = data_pf[idx_sel]
                        st.markdown("#### Objetivos")
                        st.json({"objectives": sol.get("objectives"), "rank": sol.get("rank"), "crowding_distance": sol.get("distance")})
                        gene = sol.get("gene")
                        if gene:
                            st.markdown("#### Portas (saídas) otimizadas")
                            try:
                                # lista de pares (x,y)
                                if isinstance(gene, list):
                                    st.code(str(gene))
                            except Exception:
                                pass
                    else:
                        st.info("Nenhum resultado de NSGA-II encontrado no arquivo.")
                else:
                    st.info("Nenhum arquivo de resultados do NSGA-II encontrado em uploads/nsga_ii/.")
        except Exception as e:
            st.warning(f"Falha ao carregar resultados NSGA-II: {e}")

st.stop()
