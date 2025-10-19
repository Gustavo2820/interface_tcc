# pages/simulacao.py
"""
Interface para configuração de simulações de evacuação.

Permite:
- Seleção de mapas
- Upload de indivíduos
- Criação ou upload de parâmetros
- Execução da simulação
- Visualização de resultados
"""
import streamlit as st
from pathlib import Path
from PIL import Image
import json
import sys
import shutil

# =================== STATE ===================
if 'run_simulation' not in st.session_state:
    st.session_state.run_simulation = False
if 'view_results' not in st.session_state:
    st.session_state.view_results = False
if 'last_results' not in st.session_state:
    st.session_state.last_results = None
if 'last_experiment' not in st.session_state:
    st.session_state.last_experiment = None

# Adiciona caminho dos serviços
sys.path.append(str(Path(__file__).parent.parent))

from services.simulator_integration import SimulatorIntegration, DatabaseIntegration
from services.map_creation_integration import map_creation_service

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(page_title="Simulação", layout="wide")

# ================= CSS =================
st.markdown("""
<style>
body { font-family: 'Inter', 'Roboto', sans-serif; background-color: white; color: #222; }
.menu { display:flex; justify-content:center; gap:40px; margin-bottom:40px; font-size:20px; font-weight:600; }
.menu a { text-decoration:none; color:#bbb; transition:color 0.2s; }
.menu a:hover { color:#fff; }
.menu a.active { color:#fff; font-weight:700; border-bottom:2px solid #1e90ff; padding-bottom:4px; }
.botoes { display:flex; justify-content:flex-end; gap:20px; margin-right:40px; margin-bottom:30px; }
.botao { background-color:#142b3b; color:white; border:none; border-radius:8px; padding:10px 24px; font-size:16px; font-weight:600; cursor:pointer; display:inline-flex; align-items:center; gap:8px; }
.botao:hover { transform:scale(1.05); background-color:#1d3d57; }
.container { display:flex; flex-direction:row; justify-content:center; align-items:flex-start; gap:60px; width:100%; }
.painel-esquerda { display:flex; flex-direction:column; gap:25px; }
.bloco { background-color:#142b3b; color:white; text-align:center; border-radius:10px; padding:10px 0; font-weight:bold; }
.input { background-color:#b3b3b3; border:none; border-radius:6px; padding:6px; color:black; width:200px; text-align:center; }
.mapa { border:1px solid #ccc; border-radius:6px; width:800px; height:600px; display:flex; justify-content:center; align-items:center; }
</style>
""", unsafe_allow_html=True)

# ================= MENU =================
st.markdown("""
<div class="menu">
    <a href="../app">Menu</a>
    <a href="./Mapas" class="active">Mapas</a>
    <a href="./Criacao_Mapas">Criação de Mapas</a>
    <a href="./Parâmetros">Parâmetros</a>
    <a href="./Resultados">Resultados</a>
    <a href="./Documentação">Documentação</a>
</div>
""", unsafe_allow_html=True)

# ================= INICIALIZAÇÃO DOS SERVIÇOS =================
if 'simulator_integration' not in st.session_state:
    st.session_state.simulator_integration = SimulatorIntegration()
if 'db_integration' not in st.session_state:
    st.session_state.db_integration = DatabaseIntegration()

# ================= MAPA =================
params = st.query_params
mapa_nome = params.get("mapa", [""])[0] if isinstance(params.get("mapa"), list) else params.get("mapa", "")

mapas_dir = Path("mapas")
mapas_dir.mkdir(exist_ok=True)
map_options = sorted([p.stem for p in mapas_dir.glob("*.png")])

# ================= BOTÕES =================
col_btn1, col_btn2, col_btn3 = st.columns([1,1,1])

with col_btn1:
    if st.button("💾 Salvar Configuração", key="save_config"):
        st.success("Configuração salva!")

with col_btn2:
    if st.button("▶️ Executar Simulação", key="run_simulation"):
        st.session_state.run_simulation = True

with col_btn3:
    if st.button("📊 Ver Resultados", key="view_results"):
        st.session_state.view_results = True

# ================= CONTEÚDO =================
col1, col2 = st.columns([1,3])

with col1:
    st.markdown('<div class="bloco">Nome da Simulação</div>', unsafe_allow_html=True)
    simulation_name = st.text_input("", value=f"sim_{mapa_nome}", key="sim_name")

    st.markdown('<div class="bloco">Algoritmo</div>', unsafe_allow_html=True)
    algorithm = st.selectbox("", ["Simulação Direta", "Algoritmo Genético", "NSGA-II", "Força Bruta"], key="algorithm")

    st.markdown('<div class="bloco">Mapa</div>', unsafe_allow_html=True)
    selected_map = st.selectbox("", options=["(selecione)"] + map_options, 
                                index=(map_options.index(mapa_nome)+1) if mapa_nome in map_options else 0, key="selected_map")
    if selected_map != "(selecione)" and selected_map != mapa_nome:
        mapa_nome = selected_map
        st.session_state["selected_map_name"] = mapa_nome

    st.markdown('<div class="bloco">Arquivo de Parâmetros</div>', unsafe_allow_html=True)
    param_file = st.file_uploader("Upload JSON/TXT de parâmetros", type=["json", "txt"], key="param_file")

    # ================= FORMULÁRIO PARA CRIAR PARÂMETROS =================
    with st.expander("📝 Criar Parâmetros Manualmente"):
        with st.form("form_params"):
            pop_size = st.number_input("Tamanho da população (NSGA-II)", min_value=1, value=10)
            mut_prob = st.number_input("Probabilidade de mutação (NSGA-II)", min_value=0.0, max_value=1.0, value=0.4, step=0.05)
            max_gen = st.number_input("Máximo de gerações (NSGA-II)", min_value=1, value=300)
            scenario_seed = st.number_input("Seed do cenário", value=75, min_value=0)
            simulation_seed = st.number_input("Seed da simulação", value=75, min_value=0)
            draw_mode = st.checkbox("Gerar imagens", value=True)
            submit_params = st.form_submit_button("Criar Parâmetros")
        
        if submit_params:
            params_data = {
                "pop_size": pop_size,
                "mut_prob": mut_prob,
                "max_gen": max_gen,
                "scenario_seed": scenario_seed,
                "simulation_seed": simulation_seed,
                "draw": draw_mode
            }
            temp_params_path = Path("temp_params.json")
            with open(temp_params_path, 'w') as f:
                json.dump(params_data, f, indent=2)
            st.success("Parâmetros criados com sucesso!")
            param_file = temp_params_path  # substitui arquivo upload

    st.markdown('<div class="bloco">Arquivo de Indivíduos</div>', unsafe_allow_html=True)
    individuals_file = st.file_uploader("Upload de indivíduos JSON", type=["json"], key="individuals_file")

with col2:
    if mapa_nome:
        mapa_path = Path("mapas") / f"{mapa_nome}.png"
        if mapa_path.exists():
            img = Image.open(mapa_path)
            st.image(img, use_container_width=True)
        else:
            st.warning("Mapa não encontrado.")
    else:
        st.info("Selecione um mapa para visualizar.")

# ================= EXECUÇÃO =================
if st.session_state.get('run_simulation', False):
    if not mapa_nome:
        st.error("Selecione um mapa primeiro.")
    elif not individuals_file:
        st.error("Faça upload do arquivo de indivíduos.")
    elif not param_file:
        st.error("Informe ou crie os parâmetros.")
    else:
        with st.spinner("Executando simulação..."):
            try:
                temp_dir = Path("temp_simulation")
                temp_dir.mkdir(exist_ok=True)
                
                # Salva indivíduos
                individuals_path = temp_dir / "individuals.json"
                if hasattr(individuals_file, "read"):
                    data = json.load(individuals_file)
                    with open(individuals_path, 'w') as f:
                        json.dump(data, f, indent=2)
                else:
                    shutil.copy(param_file, individuals_path)  # caso seja arquivo temporário

                # Salva parâmetros
                params_path = temp_dir / "parameters.json"
                if hasattr(param_file, "read"):
                    param_data = json.load(param_file)
                    with open(params_path, 'w') as f:
                        json.dump(param_data, f, indent=2)
                else:
                    shutil.copy(param_file, params_path)

                # Executa simulação
                simulator = st.session_state.simulator_integration
                result = simulator.run_simulator_cli(
                    experiment_name=simulation_name,
                    draw=draw_mode,
                    scenario_seed=scenario_seed,
                    simulation_seed=simulation_seed
                )
                
                st.success("Simulação finalizada!")
                st.session_state.last_results = result
                st.session_state.run_simulation = False
            except Exception as e:
                st.error(f"Erro ao executar simulação: {e}")

# ================= RESULTADOS =================
if st.session_state.get('view_results', False):
    if st.session_state.last_results is None:
        st.warning("Nenhuma simulação realizada ainda.")
    else:
        st.markdown("### Resultados da Simulação")
        st.json(st.session_state.last_results)
