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
from typing import List
import matplotlib.pyplot as _plt
import matplotlib.colors as _colors

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
                        # Accept multiple historical key names: prefer explicit 'iterations' but fallback to simulator's 'tempo_total'
                        iterations_value = data.get('iterations') or data.get('tempo_total') or data.get('total_time')
                        # distance may be stored under different keys historically
                        distance_value = data.get('distance') or data.get('distancia_total') or data.get('total_distance')

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
                                    <div class='metric-value'>{round(distance_value,3) if distance_value is not None else None}</div>
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
                # Try to parse JSON metrics and display them as readable metrics; fallback to raw text
                displayed = False
                for mf in metrics_files:
                    try:
                        with open(mf, 'r') as f:
                            data = json.load(f)
                        # prefer canonical keys if present
                        t = data.get('tempo_total') or data.get('iterations') or data.get('total_time')
                        d = data.get('distancia_total') or data.get('distance') or data.get('total_distance')
                        if t is not None or d is not None:
                            col1, col2 = st.columns(2)
                            with col1:
                                try:
                                    st.metric(label='Tempo total', value=str(round(float(t), 3)) if t is not None else '—')
                                except Exception:
                                    st.markdown(f"**Tempo total:** {t}")
                            with col2:
                                try:
                                    st.metric(label='Distância total', value=str(round(float(d), 3)) if d is not None else '—')
                                except Exception:
                                    st.markdown(f"**Distância total:** {d}")
                            displayed = True
                            # also offer a collapsible view of the full JSON
                            with st.expander(f"Detalhes — {mf.name}"):
                                st.json(data)
                            break
                        else:
                            # show the JSON in an expander if we couldn't find keys
                            with st.expander(f"Métrica (raw) — {mf.name}"):
                                st.json(data)
                            displayed = True
                    except Exception:
                        try:
                            with open(mf, 'r') as f:
                                st.text(f"{mf.name}:\n" + f.read())
                                displayed = True
                        except Exception:
                            continue
                if not displayed:
                    st.info("Nenhuma métrica legível encontrada nos arquivos de métrica.")
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
                        # Small friendly info under the NSGA section
                        st.markdown("""
                        <div style='background:#0f1720;padding:10px;border-radius:8px;margin-bottom:10px'>
                        <small style='color:#cbd5e1'>Dica: "Iterações" é uma métrica auxiliar registrada por simulação. Se estiver ausente na solução, procuramos no arquivo de métricas consolidado desta simulação.</small>
                        </div>
                        """, unsafe_allow_html=True)
                        # attempt to load map layout from input folder for this simulation
                        map_layout = None
                        try:
                            map_path = Path('simulador_heuristica') / 'input' / selected_name / 'map.txt'
                            if map_path.exists():
                                txt = map_path.read_text().splitlines()
                                # convert to list of lists of chars
                                map_layout = [list(line.rstrip('\n')) for line in txt]
                        except Exception:
                            map_layout = None

                        def display_solution_streamlit(solution: dict, map_layout: List[List[str]] = None):
                            # Section container to keep each solution visually separated
                            with st.container():
                                st.markdown(f"### Solução {solution.get('solution_id')}")

                                # Objectives mapping (handle both 2- and 3-objective result formats):
                                # - If len == 2: [num_doors, distance]
                                # - If len >=3: [num_doors, iterations, distance] (iterations treated as auxiliary)
                                objs = solution.get('objectives') or []
                                label_doors = 'Num portas'
                                label_iters = 'Iterações'
                                label_dist = 'Distância'

                                # Determine values robustly
                                doors_val = None
                                iters_val = None
                                dist_val = None

                                if len(objs) >= 1:
                                    doors_val = objs[0]
                                else:
                                    doors_val = solution.get('num_doors') or solution.get('num_doors', None)

                                if len(objs) == 2:
                                    # legacy/compact format: [num_doors, distance]
                                    dist_val = objs[1]
                                    # iterations should be read from auxiliary fields if present
                                    iters_val = solution.get('iterations') or solution.get('iteracoes') or solution.get('qtd_iteracoes')
                                elif len(objs) >= 3:
                                    # full format: [num_doors, iterations, distance]
                                    iters_val = objs[1]
                                    dist_val = objs[2]
                                else:
                                    # no objectives array: try auxiliary fields
                                    iters_val = solution.get('iterations') or solution.get('iteracoes') or solution.get('qtd_iteracoes')
                                    dist_val = solution.get('distancia') or solution.get('distance') or solution.get('distancia_total')

                                # As extra fallback, check for distance-like auxiliary keys
                                if dist_val is None:
                                    dist_val = solution.get('distancia') or solution.get('distance') or solution.get('distancia_total')

                                # If iterations still missing, try to find it in the simulation metrics collected for this run (res in outer scope)
                                if iters_val is None:
                                    try:
                                        metrics_candidates = res.get('metrics', [])
                                        for candidate in metrics_candidates:
                                            try:
                                                if str(candidate).endswith('.json'):
                                                    with open(candidate, 'r') as fh:
                                                        md = json.load(fh)
                                                    # direct top-level iterations
                                                    it = md.get('iterations') or md.get('qtd_iteracoes') or md.get('iters')
                                                    if it is not None:
                                                        iters_val = it
                                                        break
                                                    # check consolidated structure produced by NSGA save_results
                                                    evs = md.get('evaluations') or md.get('evals') or None
                                                    if isinstance(evs, list) and evs:
                                                        # find first non-null iterations entry
                                                        for e in evs:
                                                            if e is None:
                                                                continue
                                                            if isinstance(e, dict):
                                                                cand_it = e.get('iterations') or e.get('qtd_iteracoes') or e.get('iters')
                                                                if cand_it is not None:
                                                                    iters_val = cand_it
                                                                    break
                                                        if iters_val is not None:
                                                            break
                                            except Exception:
                                                continue
                                    except Exception:
                                        pass

                                        # Additional fallback: if we still don't have iterations, try consolidated metrics
                                        # under simulador_heuristica/output/<selected_name>/metrics.json produced by NSGA aggregation.
                                        if iters_val is None:
                                            try:
                                                from pathlib import Path as _P
                                                cons_path = _P('simulador_heuristica') / 'output' / (selected_name or '') / 'metrics.json'
                                                if cons_path.exists():
                                                    try:
                                                        with open(cons_path, 'r') as cf:
                                                            cons = json.load(cf)
                                                        evs = cons.get('evaluations') or []
                                                        # prepare solution matching keys
                                                        try:
                                                            sol_num_doors = int(doors_val) if doors_val is not None else int(solution.get('num_doors') or 0)
                                                        except Exception:
                                                            sol_num_doors = None
                                                        try:
                                                            sol_dist = float(dist_val) if dist_val is not None else None
                                                        except Exception:
                                                            sol_dist = None

                                                        for e in evs:
                                                            try:
                                                                ev_num = e.get('num_doors')
                                                                ev_dist = e.get('distancia_total') if e.get('distancia_total') is not None else e.get('distancia') or e.get('distance') or e.get('dist')
                                                                if sol_num_doors is not None and ev_num is not None and int(sol_num_doors) == int(ev_num):
                                                                    matched = False
                                                                    if sol_dist is not None and ev_dist is not None:
                                                                        try:
                                                                            if abs(float(ev_dist) - float(sol_dist)) <= max(1e-6, 0.001 * abs(float(sol_dist))):
                                                                                matched = True
                                                                        except Exception:
                                                                            matched = False
                                                                    else:
                                                                        matched = True

                                                                    if matched:
                                                                        iters_val = e.get('iterations') or e.get('qtd_iteracoes') or e.get('iters') or e.get('tempo_total')
                                                                        break
                                                            except Exception:
                                                                continue
                                                    except Exception:
                                                        pass
                                            except Exception:
                                                pass

                                        # Use Streamlit metrics for a clean, intuitive display
                                cols = st.columns([1,1,2])
                                with cols[0]:
                                    try:
                                        st.metric(label=label_doors, value=str(int(doors_val)) if doors_val is not None else '—')
                                    except Exception:
                                        st.markdown(f"**{label_doors}**: {doors_val}")
                                with cols[1]:
                                    try:
                                        if iters_val is None:
                                            display_iters = 'Não definido'
                                        else:
                                            display_iters = str(int(iters_val)) if float(iters_val).is_integer() else str(round(float(iters_val), 3))
                                        st.metric(label=label_iters, value=display_iters)
                                    except Exception:
                                        st.markdown(f"**{label_iters}**: {iters_val}")
                                with cols[2]:
                                    try:
                                        st.metric(label=label_dist, value=str(round(float(dist_val),3)) if dist_val is not None else '—')
                                    except Exception:
                                        st.markdown(f"**{label_dist}**: {dist_val}")
                                with cols[2]:
                                    st.markdown('**Gene**')
                                    gene = solution.get('gene') or []
                                    try:
                                        # Accept lists, tuples, numpy arrays
                                        seq = list(gene)
                                        symbols = ['✓' if int(x) else '✗' for x in seq]
                                        # split into rows of 40 for readability
                                        row_len = 40
                                        rows = [''.join(symbols[i:i+row_len]) for i in range(0, len(symbols), row_len)]
                                        for r in rows:
                                            st.code(r)
                                        num_doors_calc = int(solution.get('num_doors', sum(int(bool(x)) for x in seq)))
                                        st.markdown(f"**Num portas:** {num_doors_calc}")
                                    except Exception:
                                        # Fallback: render as-is
                                        st.write(gene)

                                # Door positions
                                dp = solution.get('door_positions') or []
                                if dp:
                                    st.markdown('**Posições de portas**')
                                    try:
                                        # Render a clearer table with pandas dataframe and fixed height
                                        import pandas as _pd
                                        rows = []
                                        for i,p in enumerate(dp):
                                            rows.append({'#': i+1, 'x': int(p[0]), 'y': int(p[1])})
                                        df = _pd.DataFrame(rows)
                                        st.dataframe(df, height=180)
                                    except Exception:
                                        st.write(dp)

                                # Mini-map if layout provided — make it larger and proportional but capped
                                if map_layout is not None:
                                    st.markdown('**Mini-mapa (portas destacadas)**')
                                    try:
                                        grid_h = len(map_layout)
                                        grid_w = len(map_layout[0]) if grid_h>0 else 0
                                        import numpy as _np
                                        arr = _np.zeros((grid_h, grid_w), dtype=int)
                                        # fill base: 0 empty, 1 wall, 2 door
                                        for y,row in enumerate(map_layout):
                                            for x,ch in enumerate(row):
                                                if ch in ('1','|','#'):
                                                    arr[y,x] = 1
                                                elif ch in ('2',) or (isinstance(ch, str) and ch.upper()=='P'):
                                                    arr[y,x] = 2
                                                else:
                                                    arr[y,x] = 0
                                        # mark selected doors from solution
                                        for p in dp:
                                            try:
                                                x = int(p[0]); y = int(p[1])
                                                if 0 <= y < arr.shape[0] and 0 <= x < arr.shape[1]:
                                                    arr[y,x] = 3
                                            except Exception:
                                                continue

                                        # Larger target cell size for readability, but cap overall image
                                        target_cell_px = 28
                                        max_total_px = 1800
                                        est_w_px = grid_w * target_cell_px
                                        est_h_px = grid_h * target_cell_px
                                        scale = min(1.0, max_total_px / max(est_w_px, est_h_px, 1))
                                        cell_px = int(max(8, target_cell_px * scale))

                                        dpi = 100
                                        fig_w = max(4, min(14, (grid_w * cell_px) / dpi))
                                        fig_h = max(4, min(14, (grid_h * cell_px) / dpi))

                                        cmap = _colors.ListedColormap(['#ffffff','#000000','#ff5555','#00cc66'])
                                        bounds=[0,1,2,3,4]
                                        norm = _colors.BoundaryNorm(bounds, cmap.N)
                                        fig, ax = _plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
                                        ax.imshow(arr, cmap=cmap, norm=norm, interpolation='nearest')
                                        ax.set_xticks([]); ax.set_yticks([])
                                        ax.set_title('Mapa simplificado', fontsize=12)

                                        import io
                                        buf = io.BytesIO()
                                        fig.tight_layout(pad=0.5)
                                        fig.savefig(buf, format='png', bbox_inches='tight')
                                        _plt.close(fig)
                                        buf.seek(0)
                                        # use_container_width is the current Streamlit parameter
                                        st.image(buf, use_container_width=True)
                                    except Exception:
                                        st.text('Não foi possível desenhar o mini-mapa.')

                        display_solution_streamlit(sol, map_layout)
                    else:
                        st.info("Nenhum resultado de NSGA-II encontrado no arquivo.")
                else:
                    st.info("Nenhum arquivo de resultados do NSGA-II encontrado em uploads/nsga_ii/.")
        except Exception as e:
            st.warning(f"Falha ao carregar resultados NSGA-II: {e}")

st.stop()
