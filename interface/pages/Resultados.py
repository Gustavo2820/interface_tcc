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
    
    res = st.session_state.simulator_integration.read_results(selected_name)

    if 'error' in res:
        st.warning(res['error'])
    else:
        # ===== Obtém informações da simulação do banco =====
        sim_info = None
        for s in simulations:
            if s['nome'] == selected_name:
                sim_info = s
                break
        
        # ===== CABEÇALHO UNIFICADO =====
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%); padding: 25px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
            <h2 style='color: #fff; margin: 0 0 15px 0; font-size: 28px;'>📊 {selected_name}</h2>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 15px;'>
                <div style='background: rgba(255,255,255,0.1); padding: 12px; border-radius: 8px;'>
                    <div style='color: #93c5fd; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;'>Algoritmo</div>
                    <div style='color: #fff; font-size: 18px; font-weight: bold; margin-top: 5px;'>{sim_info.get('algoritmo', '—') if sim_info else '—'}</div>
                </div>
                <div style='background: rgba(255,255,255,0.1); padding: 12px; border-radius: 8px;'>
                    <div style='color: #93c5fd; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;'>Mapa</div>
                    <div style='color: #fff; font-size: 18px; font-weight: bold; margin-top: 5px;'>{sim_info.get('mapa', '—') if sim_info else '—'}</div>
                </div>
                <div style='background: rgba(255,255,255,0.1); padding: 12px; border-radius: 8px;'>
                    <div style='color: #93c5fd; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;'>Status</div>
                    <div style='color: #fff; font-size: 18px; font-weight: bold; margin-top: 5px;'>{sim_info.get('simulado', '—') if sim_info else '—'}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ===== Coleta métricas agregadas (para fallback em soluções otimizadas) =====
        metrics_files = res.get('metrics', [])
        iterations_value = None
        series = None
        non_ev = None
        term = None

        for mf in metrics_files:
            if not str(mf).endswith('.json'):
                continue
            try:
                with open(mf, 'r') as f:
                    data = json.load(f)
                    if iterations_value is None:
                        iterations_value = data.get('iterations') or data.get('tempo_total') or data.get('total_time')
                    if series is None:
                        series = data.get('mean_distance_series') or data.get('individuals_distances') or []
                    if non_ev is None:
                        non_ev = data.get('per_iteration_non_evacuated') or []
                    if term is None:
                        term = data.get('termination_reason') or data.get('termination') or None
            except Exception:
                continue

        # ===== GRÁFICOS DIAGNÓSTICOS (se disponíveis) =====
        if series or non_ev or term:
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Termination reason (se disponível)
            if term is not None:
                st.markdown(f"""
                <div style='background: #0f172a; border-left: 4px solid #3b82f6; padding: 15px; border-radius: 8px; margin: 15px 0;'>
                    <div style='color: #93c5fd; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;'>🎯 Causa de Terminação</div>
                    <div style='color: #e2e8f0; font-size: 16px;'>{term}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Gráficos temporais
            if series or non_ev:
                st.markdown("""
                <div style='background: #1e293b; padding: 15px; border-radius: 10px; margin: 20px 0;'>
                    <h3 style='color: #cbd5e1; margin: 0 0 15px 0; font-size: 18px;'>📈 Análise Temporal</h3>
                </div>
                """, unsafe_allow_html=True)
            
            # Série temporal de distância
            if series:
                st.markdown("<div style='color: #cbd5e1; font-weight: 600; margin: 15px 0 10px 0;'>Média da Distância por Iteração</div>", unsafe_allow_html=True)
                try:
                    import pandas as pd
                    df = pd.DataFrame({"iteration": list(range(len(series))), "mean_distance": series})
                    st.line_chart(df.set_index("iteration"))
                except Exception:
                    st.text("Série disponível mas não foi possível plotar.")

            # Série de não-evacuados
            if non_ev:
                st.markdown("<div style='color: #cbd5e1; font-weight: 600; margin: 15px 0 10px 0;'>Taxa de Evacuação por Iteração</div>", unsafe_allow_html=True)
                try:
                    import pandas as pd
                    df3 = pd.DataFrame({"iteration": list(range(len(non_ev))), "non_evacuated": non_ev})
                    initial = non_ev[0] if len(non_ev) > 0 else None
                    if initial and initial > 0:
                        evac_pct = [round((initial - n) / initial * 100.0, 1) for n in non_ev]
                        df3['evacuated_pct'] = evac_pct
                        st.line_chart(df3.set_index('iteration'))
                    else:
                        st.line_chart(df3.set_index('iteration'))
                except Exception:
                    st.text("Série disponível mas não foi possível plotar.")

        # ===== Fallback para simulações sem otimização =====
        if not (series or non_ev or term):
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

        # ===== NSGA-II e Brute Force: soluções otimizadas (saídas/portas) =====
        try:
            from pathlib import Path as _P
            
            # descobre algoritmo da linha selecionada
            alg = None
            for s in simulations:
                if s['nome'] == selected_name:
                    alg = s.get('algoritmo')
                    break
            
            # Verifica se é NSGA-II ou Força Bruta
            if alg and ('NSGA' in alg or 'Força Bruta' in alg or 'Brute Force' in alg):
                # Define título e diretório baseado no algoritmo
                if 'NSGA' in alg:
                    title = "Soluções Otimizadas (NSGA-II)"
                    icon = "🧬"
                    results_dir = _P("uploads") / "nsga_ii"
                else:
                    title = "Soluções Otimizadas (Força Bruta)"
                    icon = "🔍"
                    results_dir = _P("uploads") / "brute_force"
                
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #581c87 0%, #6b21a8 100%); padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
                    <h3 style='color: #fff; margin: 0; font-size: 22px;'>{icon} {title}</h3>
                    <p style='color: #e9d5ff; margin: 10px 0 0 0; font-size: 14px;'>Fronteira de Pareto com soluções não-dominadas</p>
                </div>
                """, unsafe_allow_html=True)
                pareto_files = list(results_dir.glob("*.json")) if results_dir.exists() else []
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
                        # ===== SELETOR DE SOLUÇÃO NO TOPO =====
                        options = [f"Solução {i+1}: {it.get('objectives',[None,None,None])}" for i, it in enumerate(data_pf)]
                        idx_sel = st.selectbox("🎯 Escolha uma solução da fronteira de Pareto", options=list(range(len(options))), format_func=lambda i: options[i], key="pareto_selector")
                        sol = data_pf[idx_sel]
                        
                        # ===== EXTRAI VALORES DA SOLUÇÃO =====
                        objs = sol.get('objectives') or []
                        doors_val = objs[0] if len(objs) >= 1 else sol.get('num_doors', 0)
                        iters_val = objs[1] if len(objs) >= 3 else sol.get('iterations', iterations_value)
                        dist_val = objs[2] if len(objs) >= 3 else (objs[1] if len(objs) == 2 else sol.get('distance', 0))
                        
                        # Fallback para iterações se não encontrado
                        if iters_val is None:
                            for mf in metrics_files:
                                try:
                                    if str(mf).endswith('.json'):
                                        with open(mf, 'r') as fh:
                                            md = json.load(fh)
                                        iters_val = md.get('iterations') or md.get('tempo_total')
                                        if iters_val is not None:
                                            break
                                except Exception:
                                    continue
                        
                        # ===== CARDS DE MÉTRICAS DA SOLUÇÃO (ATUALIZAM COM SELEÇÃO) =====
                        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%); padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                                <div style='color: #7dd3fc; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;'>🚪 Número de Portas</div>
                                <div style='color: #fff; font-size: 36px; font-weight: bold;'>{int(doors_val) if doors_val is not None else '—'}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #065f46 0%, #047857 100%); padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                                <div style='color: #6ee7b7; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;'>⏱️ Iterações</div>
                                <div style='color: #fff; font-size: 36px; font-weight: bold;'>{int(iters_val) if iters_val is not None else '—'}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #7c2d12 0%, #9a3412 100%); padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                                <div style='color: #fdba74; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;'>📏 Distância</div>
                                <div style='color: #fff; font-size: 36px; font-weight: bold;'>{round(float(dist_val), 1) if dist_val is not None else '—'}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # ===== MINI-MAPA INTERATIVO E BONITO =====
                        st.markdown("<div style='margin: 30px 0 15px 0;'></div>", unsafe_allow_html=True)
                        
                        # Carrega layout do mapa
                        map_layout = None
                        try:
                            map_path = Path('simulador_heuristica') / 'input' / selected_name / 'map.txt'
                            if map_path.exists():
                                txt = map_path.read_text().splitlines()
                                map_layout = [list(line.rstrip('\n')) for line in txt]
                        except Exception:
                            map_layout = None
                        
                        if map_layout is not None:
                            st.markdown("""
                            <div style='background: #1e293b; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
                                <h4 style='color: #cbd5e1; margin: 0; font-size: 16px;'>🗺️ Mapa com Portas Selecionadas</h4>
                                <p style='color: #94a3b8; margin: 5px 0 0 0; font-size: 13px;'>
                                    <span style='color: #fff; background: #000; padding: 2px 6px; border-radius: 3px; margin-right: 8px;'>⬛ Parede</span>
                                    <span style='color: #fff; background: #ef4444; padding: 2px 6px; border-radius: 3px; margin-right: 8px;'>🔴 Porta disponível</span>
                                    <span style='color: #fff; background: #10b981; padding: 2px 6px; border-radius: 3px;'>🟢 Porta selecionada</span>
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            try:
                                dp = sol.get('door_positions') or []
                                grid_h = len(map_layout)
                                grid_w = len(map_layout[0]) if grid_h > 0 else 0
                                
                                import numpy as _np
                                import matplotlib.pyplot as _plt
                                import matplotlib.colors as _colors
                                
                                arr = _np.zeros((grid_h, grid_w), dtype=int)
                                
                                # Preenche mapa base: 0=vazio, 1=parede, 2=porta disponível
                                for y, row in enumerate(map_layout):
                                    for x, ch in enumerate(row):
                                        if ch in ('1', '|', '#'):
                                            arr[y, x] = 1  # Parede
                                        elif ch == '2':
                                            arr[y, x] = 2  # Porta disponível
                                        else:
                                            arr[y, x] = 0  # Vazio
                                
                                # Marca portas SELECIONADAS (sobrescreve)
                                for p in dp:
                                    try:
                                        x, y = int(p[0]), int(p[1])
                                        if 0 <= y < arr.shape[0] and 0 <= x < arr.shape[1]:
                                            arr[y, x] = 3  # Porta selecionada (verde)
                                    except Exception:
                                        continue
                                
                                # Configuração visual aprimorada
                                target_cell_px = 32
                                max_total_px = 2000
                                est_w_px = grid_w * target_cell_px
                                est_h_px = grid_h * target_cell_px
                                scale = min(1.0, max_total_px / max(est_w_px, est_h_px, 1))
                                cell_px = int(max(10, target_cell_px * scale))
                                
                                dpi = 120
                                fig_w = max(5, min(16, (grid_w * cell_px) / dpi))
                                fig_h = max(5, min(16, (grid_h * cell_px) / dpi))
                                
                                # Paleta de cores moderna
                                cmap = _colors.ListedColormap([
                                    '#f8fafc',  # 0: Vazio (branco suave)
                                    '#0f172a',  # 1: Parede (preto azulado)
                                    '#ef4444',  # 2: Porta disponível (vermelho)
                                    '#10b981'   # 3: Porta selecionada (verde)
                                ])
                                bounds = [0, 1, 2, 3, 4]
                                norm = _colors.BoundaryNorm(bounds, cmap.N)
                                
                                fig, ax = _plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
                                ax.imshow(arr, cmap=cmap, norm=norm, interpolation='nearest')
                                
                                # Grid sutil para melhor visualização
                                ax.set_xticks(_np.arange(-0.5, grid_w, 1), minor=True)
                                ax.set_yticks(_np.arange(-0.5, grid_h, 1), minor=True)
                                ax.grid(which="minor", color="#cbd5e1", linestyle='-', linewidth=0.5, alpha=0.3)
                                ax.tick_params(which="minor", size=0)
                                
                                # Remove ticks principais
                                ax.set_xticks([])
                                ax.set_yticks([])
                                
                                # Título com informações
                                ax.set_title(f'Solução {idx_sel + 1} - {int(doors_val)} portas ativas', 
                                           fontsize=14, fontweight='bold', color='#1e293b', pad=15)
                                
                                # Adiciona borda ao redor do mapa
                                for spine in ax.spines.values():
                                    spine.set_edgecolor('#64748b')
                                    spine.set_linewidth(2)
                                
                                # Salva como imagem
                                import io
                                buf = io.BytesIO()
                                fig.tight_layout(pad=0.8)
                                fig.savefig(buf, format='png', bbox_inches='tight', facecolor='white', edgecolor='none')
                                _plt.close(fig)
                                buf.seek(0)
                                
                                st.image(buf, use_container_width=True)
                                
                            except Exception as e:
                                st.error(f'Não foi possível desenhar o mini-mapa: {e}')
                        else:
                            st.info("Mapa não encontrado para visualização.")
                    else:
                        st.info(f"Nenhum resultado encontrado no arquivo ({title}).")
                else:
                    st.info(f"Nenhum arquivo de resultados encontrado em {results_dir}.")
        except Exception as e:
            st.warning(f"Falha ao carregar resultados de otimização: {e}")

st.stop()
