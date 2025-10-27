# pages/simulacao.py
"""
Interface para configuração de simulações de evacuação.
Permite criar ou carregar parâmetros de simulação, criar/editar indivíduos,
selecionar mapas e executar a simulação.
"""
import streamlit as st
from pathlib import Path
from PIL import Image
import json
import sys
import numpy as np
import shutil
from datetime import datetime

# ================= SESSION STATE =================
for key in ['run_sim', 'view_results', 'last_results', 'last_experiment', 'individuals_textarea']:
    if key not in st.session_state:
        st.session_state[key] = False if 'run' in key or 'view' in key else None
st.session_state.individuals_textarea = st.session_state.individuals_textarea or "[]"

# Session state for label-based individuals editor
if 'ind_labels' not in st.session_state:
    st.session_state.ind_labels = []  # list of characterization dicts
if 'label_edit_index' not in st.session_state:
    st.session_state.label_edit_index = -1

def _reset_label_tmp():
    st.session_state.tmp_label_name = ""
    st.session_state.tmp_amount = 1
    st.session_state.tmp_r = 255
    st.session_state.tmp_g = 0
    st.session_state.tmp_b = 0
    st.session_state.tmp_speed = 1
    st.session_state.tmp_KD = 1.0
    st.session_state.tmp_KS = 1.0
    st.session_state.tmp_KW = 1.0
    st.session_state.tmp_KI = 0.5

# initialize tmp fields if not present
if 'tmp_label_name' not in st.session_state:
    _reset_label_tmp()

# Adiciona diretórios necessários ao sys.path
services_dir = str(Path(__file__).parent.parent)
if services_dir not in sys.path:
    sys.path.append(services_dir)

# Adiciona o diretório raiz do projeto para permitir importar 'simulador_heuristica'
project_root = str(Path(__file__).resolve().parents[2])
if project_root not in sys.path:
    sys.path.append(project_root)

from services.simulator_integration import SimulatorIntegration, DatabaseIntegration
from services.map_creation_integration import map_creation_service
from services.nsga_integration import NSGAIntegration
from services.bruteforce_integration import get_bruteforce_integration

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(page_title="Simulação", layout="wide")

# ================= CSS E CABEÇALHO DECORATIVO =================
st.markdown("""
    <style>
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
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .page-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .page-header p {
        color: rgba(255,255,255,0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    /* ===== PREVIEW DO MAPA ===== */
    .map-preview {
        border: 3px solid #667eea;
        border-radius: 12px;
        padding: 20px;
        background: #1a1a2e;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    .map-preview-title {
        color: #667eea;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 10px;
        text-align: center;
    }
    
    /* ===== QUALIDADE DE IMAGEM ===== */
    .map-preview img, .map-preview .map-img {
        width: 100%;
        height: auto;
        min-height: 300px;
        max-height: 600px;
        object-fit: contain;
        image-rendering: -webkit-optimize-contrast;
        image-rendering: crisp-edges;
        image-rendering: pixelated;
        border-radius: 8px;
        display: block;
        margin: 0 auto;
    }
    img {
        image-rendering: -webkit-optimize-contrast;
        image-rendering: crisp-edges;
        image-rendering: pixelated;
    }
    [data-testid="stImage"] img {
        image-rendering: -webkit-optimize-contrast !important;
        image-rendering: crisp-edges !important;
        image-rendering: pixelated !important;
        object-fit: contain !important;
    }
    
    /* ===== SEÇÕES ===== */
    .section-divider {
        border-top: 2px solid #667eea;
        margin: 2rem 0;
        opacity: 0.3;
    }
    
    /* ===== BOTÕES ===== */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.5);
    }
    
    /* ===== BOTÃO FIXO DE EXECUÇÃO ===== */
    .fixed-button-container {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 999;
        animation: pulse 2s infinite;
    }
    
    .fixed-exec-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        padding: 16px 40px !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        text-decoration: none !important;
        display: inline-block !important;
    }
    
    .fixed-exec-button:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.8) !important;
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        }
        50% {
            box-shadow: 0 8px 35px rgba(102, 126, 234, 0.9);
        }
    }
    
    /* ===== BOTÃO DE EXECUÇÃO PRINCIPAL ===== */
    button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        padding: 14px 32px !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    button[kind="primary"]:hover {
        transform: scale(1.08) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* ===== EXPANDERS ===== */
    .streamlit-expanderHeader {
        background-color: #1a1a2e !important;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* ===== CARDS ===== */
    .info-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    /* ===== MÉTRICAS ===== */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    /* ===== TÍTULOS DE SEÇÃO ===== */
    h3 {
        color: #667eea;
        border-bottom: 2px solid rgba(102, 126, 234, 0.3);
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    
    /* ===== ESPAÇAMENTO GERAL ===== */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    
    /* ===== FORMULÁRIO =====  */
    .stForm {
        background: rgba(26, 26, 46, 0.3);
        border-radius: 10px;
        padding: 1.5rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# ===== MENU SUPERIOR =====
st.markdown("""
    <div class="menu">
        <a href="/">Menu</a>
        <a href="/Mapas">Mapas</a>
        <a href="/Criação_de_Mapas">Criação de Mapas</a>
        <a href="/Parâmetros">Parâmetros</a>
        <a class="active" href="/Simulação">Simulação</a>
        <a href="/Resultados">Resultados</a>
        <a href="/Documentação">Documentação</a>
    </div>
""", unsafe_allow_html=True)

# ===== CABEÇALHO DA PÁGINA =====
st.markdown("""
    <div class="page-header">
        <h1>🎯 Simulação de Evacuação</h1>
        <p>Configure e execute simulações com diferentes algoritmos de otimização</p>
    </div>
""", unsafe_allow_html=True)

# ================= FUNÇÕES =================
def start_simulation():
    st.session_state.run_sim = True

# ================= BOTÃO DE EXECUÇÃO NO TOPO =================
col_top1, col_top2, col_top3 = st.columns([3, 2, 3])
with col_top2:
    st.button("▶️ EXECUTAR SIMULAÇÃO", on_click=start_simulation, type="primary", use_container_width=True, key="exec_button_top")
st.markdown("---")

# ================= INICIALIZAÇÃO DOS SERVIÇOS =================
if 'simulator_integration' not in st.session_state:
    st.session_state.simulator_integration = SimulatorIntegration()
if 'db_integration' not in st.session_state:
    st.session_state.db_integration = DatabaseIntegration()
if 'nsga_integration' not in st.session_state:
    st.session_state.nsga_integration = NSGAIntegration(st.session_state.simulator_integration)
if 'bruteforce_integration' not in st.session_state:
    st.session_state.bruteforce_integration = get_bruteforce_integration(st.session_state.simulator_integration)

# ================= CARREGAMENTO DE MAPAS =================
mapas_dir = Path("mapas")
mapas_dir.mkdir(exist_ok=True)
map_options = sorted([p.stem for p in mapas_dir.glob("*.png")])
# Prefill defaults (will be overridden if query params or existing simulation present)
prefill_simulation_name = "sim_default"
algorithms_list = ["NSGA-II","NSGA-II com Cache","Força Bruta"]
prefill_algorithm = algorithms_list[0]
prefill_mapa = None

# ================= QUERY PARAMS: pre-load mapa or simulation =================
params = st.query_params
preselected_map = None
preselected_sim_id = None
if params:
    if 'mapa' in params:
        v = params.get('mapa')
        if isinstance(v, list):
            v = v[0]
        if v and v in map_options:
            preselected_map = v
    if 'sim_id' in params:
        try:
            sid = params.get('sim_id')
            if isinstance(sid, list):
                sid = sid[0]
            preselected_sim_id = int(sid) if sid else None
        except Exception:
            preselected_sim_id = None

db = DatabaseIntegration()

# If editing an existing simulation, load its data
existing_sim = None
if preselected_sim_id is not None:
    try:
        existing_sim = db.get_simulation(preselected_sim_id)
    except Exception:
        existing_sim = None

# If simulation exists, override prefill defaults and populate session state
if existing_sim:
    prefill_simulation_name = existing_sim.get('nome', prefill_simulation_name)
    # Map stored algorithm values may match one of algorithms_list; otherwise keep default
    prefill_algorithm = existing_sim.get('algoritmo', prefill_algorithm)
    prefill_mapa = existing_sim.get('mapa', prefill_mapa)
    # populate session_state with saved individuals/config so UI fields show them
    try:
        cfg_ped = existing_sim.get('config_pedestres_json')
        if cfg_ped:
            # store as pretty JSON string
            try:
                parsed = json.loads(cfg_ped)
                st.session_state.individuals_textarea = json.dumps(parsed, indent=2)
            except Exception:
                st.session_state.individuals_textarea = cfg_ped
    except Exception:
        pass
    # If NSGA config is present, try to load it into nsga_integration
    try:
        nsga_cfg = existing_sim.get('nsga_config_json')
        if nsga_cfg and hasattr(st.session_state, 'nsga_integration'):
            # attempt to write a temp file and let the integration load it if it provides a loader
            try:
                tmp = Path('temp_simulation')
                tmp.mkdir(exist_ok=True)
                fpath = tmp / f'nsga_config_sim_{existing_sim.get("id", "tmp")}.json'
                fpath.write_text(nsga_cfg)
                st.session_state.nsga_integration.load_configuration(fpath)
            except Exception:
                pass
    except Exception:
        pass

else:
    # If a map was preselected from query params, set it
    if preselected_map:
        prefill_mapa = preselected_map

# ================= FUNÇÕES AUXILIARES =================
def quantize_map_colors(image_path):
    """
    Força cores da imagem para serem exatamente as cores válidas do simulador.
    Aceita variações de cinza (128,128,128 e 192,192,192) como inocupável.
    """
    valid_colors = {
        "wall": np.array([0,0,0]),
        "door": np.array([255,0,0]),
        "empty": np.array([255,255,255]),
        "drawing": np.array([255,165,0]),
        "inocupavel": np.array([192,192,192]),
        "inocupavel_alt": np.array([128,128,128])  # Cinza alternativo
    }
    
    # Mapeamento de cores alternativas para cores principais
    color_mapping = {
        "inocupavel_alt": "inocupavel"  # Mapeia cinza escuro para cinza claro
    }
    
    img = Image.open(image_path).convert("RGB")
    arr = np.array(img)
    
    def closest_color(pixel):
        distances = {name: np.sum((pixel - col)**2) for name, col in valid_colors.items()}
        closest_name = min(distances, key=distances.get)
        # Se for uma cor alternativa, usa a cor principal mapeada
        if closest_name in color_mapping:
            return valid_colors[color_mapping[closest_name]]
        return valid_colors[closest_name]
    
    new_arr = np.zeros_like(arr)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            new_arr[i,j] = closest_color(arr[i,j])
    Image.fromarray(new_arr).save(image_path)

# ================= FORMULÁRIO PRINCIPAL =================
col1, col2 = st.columns([1,3])
with col1:
    simulation_name = st.text_input("Nome da Simulação", value=prefill_simulation_name)
    algorithm = st.selectbox("Algoritmo", algorithms_list, index=algorithms_list.index(prefill_algorithm) if prefill_algorithm in algorithms_list else 0)
    # Determine default index for map selectbox
    map_options_with_placeholder = ["(selecione)"] + map_options
    default_map_index = 0
    if prefill_mapa and prefill_mapa in map_options:
        try:
            default_map_index = map_options_with_placeholder.index(prefill_mapa)
        except Exception:
            default_map_index = 0
    selected_map = st.selectbox("Mapa", options=map_options_with_placeholder, index=default_map_index)
    mapa_nome = selected_map if selected_map != "(selecione)" else None
    
    # Salva o mapa selecionado no session_state para preview
    if mapa_nome:
        st.session_state.selected_map_name = mapa_nome

with col1:
    # ===== SELETOR DE PRESETS =====
    st.markdown("##### 🎨 Carregar Preset Rápido")
    presets_dir = Path("presets")
    preset_files = sorted(presets_dir.glob("*.json")) if presets_dir.exists() else []
    
    # Initialize loaded_preset in session_state if not present
    if 'loaded_preset' not in st.session_state:
        st.session_state.loaded_preset = {}
    
    if preset_files:
        preset_options = ["(nenhum)"] + [p.stem for p in preset_files]
        selected_preset = st.selectbox(
            "Preset de Parâmetros",
            preset_options,
            help="Carregue rapidamente configurações pré-definidas"
        )
        
        if selected_preset != "(nenhum)":
            preset_path = presets_dir / f"{selected_preset}.json"
            if st.button(f"📥 Carregar '{selected_preset}'", use_container_width=True):
                try:
                    preset_data = json.loads(preset_path.read_text())
                    
                    # Carrega preset para o session_state para preencher o formulário
                    st.session_state.loaded_preset = preset_data
                    
                    # Também carrega para NSGA se aplicável
                    if algorithm in ["NSGA-II", "NSGA-II com Cache"]:
                        temp_config_path = Path("uploads/configs") / f"preset_{selected_preset}.json"
                        temp_config_path.parent.mkdir(parents=True, exist_ok=True)
                        temp_config_path.write_text(json.dumps(preset_data, indent=2))
                        st.session_state.nsga_integration.load_configuration(temp_config_path)
                    
                    st.success(f"✅ Preset '{selected_preset}' carregado! Edite os valores abaixo se necessário.")
                    st.info(f"📝 {preset_data.get('description', '')}")
                    
                except Exception as e:
                    st.error(f"Erro ao carregar preset: {e}")
    else:
        st.info("💡 Nenhum preset encontrado. Crie presets na página **Parâmetros**")
    
    st.markdown("---")
    
    # Formulário unificado de criação/edição de configuração
    with st.expander("⚙️ Criar/Editar Configuração Unificada", expanded=True):
        st.markdown("**💡 Formato Unificado**: Combina parâmetros do algoritmo e de simulação em um único arquivo")
        
        # Extract values from loaded preset if available (com verificação de None)
        loaded_preset = st.session_state.get('loaded_preset')
        if loaded_preset is None:
            loaded_preset = {}
        
        nsga_cfg = loaded_preset.get('nsga_config', {})
        sim_params = loaded_preset.get('simulation_params', {})
        bf_cfg = loaded_preset.get('bruteforce_config', {})
        
        with st.form("form_unified_config"):
            col_form1, col_form2 = st.columns(2)
            
            with col_form1:
                st.markdown("### 🧬 Parâmetros do Algoritmo")
                if algorithm in ["NSGA-II", "NSGA-II com Cache"]:
                    population_size = st.number_input(
                        "Tamanho da população", 
                        min_value=2, 
                        value=nsga_cfg.get('population_size', 20), 
                        help="Número de indivíduos na população"
                    )
                    generations = st.number_input(
                        "Número de gerações", 
                        min_value=1, 
                        value=nsga_cfg.get('generations', 10), 
                        help="Número de gerações para evolução"
                    )
                    crossover_rate = st.number_input(
                        "Taxa de crossover", 
                        min_value=0.0, 
                        max_value=1.0, 
                        value=float(nsga_cfg.get('crossover_rate', 0.8)), 
                        step=0.05, 
                        help="Probabilidade de crossover"
                    )
                    mutation_rate = st.number_input(
                        "Taxa de mutação", 
                        min_value=0.0, 
                        max_value=1.0, 
                        value=float(nsga_cfg.get('mutation_rate', 0.1)), 
                        step=0.05, 
                        help="Probabilidade de mutação"
                    )
                    # use_three_objectives SEMPRE True - não mostra checkbox, apenas informa
                    use_three_obj = True
                    
                elif algorithm == "Força Bruta":
                    max_doors = st.number_input(
                        "Máximo de portas", 
                        min_value=1, 
                        value=bf_cfg.get('max_doors', 15), 
                        help="Número máximo de portas a testar"
                    )
                else:
                    # Parâmetros para outros algoritmos
                    pop_size = st.number_input("Tamanho da população", min_value=1, value=10, help="Número de indivíduos")
                    mut_prob = st.number_input("Probabilidade de mutação", min_value=0.0, max_value=1.0, value=0.4, step=0.01, help="Taxa de mutação")
                    max_gen = st.number_input("Máximo de gerações", min_value=1, value=300, help="Número máximo de gerações")
            
            with col_form2:
                st.markdown("### 🎯 Parâmetros de Simulação")
                
                # Handle scenario_seed (can be int or list)
                scenario_seed_val = sim_params.get('scenario_seed', 42)
                if isinstance(scenario_seed_val, list):
                    scenario_seed_str = ",".join(map(str, scenario_seed_val))
                else:
                    scenario_seed_str = str(scenario_seed_val)
                
                scenario_seed_input = st.text_input(
                    "Seed(s) do cenário",
                    value=scenario_seed_str,
                    help="Um único seed (ex: 42) ou múltiplos seeds separados por vírgula (ex: 1,2,3)"
                )
                
                simulation_seed = st.number_input(
                    "Seed da simulação", 
                    min_value=0, 
                    value=sim_params.get('simulation_seed', 123), 
                    help="Seed para execução da simulação"
                )
                max_iterations = st.number_input(
                    "Máximo de iterações",
                    min_value=100,
                    max_value=10000,
                    value=sim_params.get('max_iterations', 1200),
                    step=100,
                    help="Número máximo de iterações por simulação"
                )
                draw_mode = st.checkbox(
                    "Gerar imagens", 
                    value=sim_params.get('draw_mode', True), 
                    help="Gerar imagens de saída da simulação"
                )
                verbose = st.checkbox(
                    "Modo verboso", 
                    value=sim_params.get('verbose', False), 
                    help="Exibir informações detalhadas durante execução"
                )
            
            description = st.text_input(
                "Descrição da configuração", 
                value=loaded_preset.get('description', f"Configuração para {algorithm}"), 
                help="Descrição opcional da configuração"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit_config = st.form_submit_button("💾 Salvar e Usar Configuração", use_container_width=True)
            with col_btn2:
                clear_preset = st.form_submit_button("🗑️ Limpar Preset", use_container_width=True)
        
        if clear_preset:
            st.session_state.loaded_preset = {}
            st.success("Preset limpo! Valores padrão restaurados.")
            st.rerun()
        
        if submit_config:
            try:
                config_dir = Path("uploads")/"configs"
                config_dir.mkdir(parents=True, exist_ok=True)
                
                # Parse scenario_seed (pode ser único ou lista)
                scenario_seed_parsed = None
                try:
                    if ',' in scenario_seed_input:
                        scenario_seed_parsed = [int(s.strip()) for s in scenario_seed_input.split(',')]
                    else:
                        scenario_seed_parsed = int(scenario_seed_input.strip())
                except Exception:
                    st.error("Formato inválido para scenario_seed. Use um número ou números separados por vírgula.")
                    scenario_seed_parsed = 42
                
                if algorithm in ["NSGA-II", "NSGA-II com Cache"]:
                    # Formato unificado para NSGA-II
                    unified_config = {
                        "preset_name": f"{algorithm}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        "description": description,
                        "nsga_config": {
                            "population_size": int(population_size),
                            "generations": int(generations),
                            "crossover_rate": float(crossover_rate),
                            "mutation_rate": float(mutation_rate),
                            "use_three_objectives": bool(use_three_obj)
                        },
                        "simulation_params": {
                            "scenario_seed": scenario_seed_parsed,
                            "simulation_seed": int(simulation_seed),
                            "max_iterations": int(max_iterations),
                            "draw_mode": bool(draw_mode),
                            "verbose": bool(verbose)
                        },
                        "bruteforce_config": {
                            "max_doors": 15  # default para compatibilidade
                        }
                    }
                elif algorithm == "Força Bruta":
                    # Formato unificado para Força Bruta
                    unified_config = {
                        "preset_name": f"BruteForce_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        "description": description,
                        "bruteforce_config": {
                            "max_doors": int(max_doors)
                        },
                        "simulation_params": {
                            "scenario_seed": scenario_seed_parsed,
                            "simulation_seed": int(simulation_seed),
                            "max_iterations": int(max_iterations),
                            "draw_mode": bool(draw_mode),
                            "verbose": bool(verbose)
                        },
                        "nsga_config": {
                            "population_size": 20,  # defaults para compatibilidade
                            "generations": 10,
                            "crossover_rate": 0.8,
                            "mutation_rate": 0.1,
                            "use_three_objectives": True  # SEMPRE True
                        }
                    }
                else:
                    # Formato unificado para outros algoritmos
                    unified_config = {
                        "preset_name": f"{algorithm}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        "description": description,
                        "algorithm_params": {
                            "pop_size": int(pop_size),
                            "mut_prob": float(mut_prob),
                            "max_gen": int(max_gen)
                        },
                        "simulation_params": {
                            "scenario_seed": scenario_seed_parsed,
                            "simulation_seed": int(simulation_seed),
                            "max_iterations": int(max_iterations),
                            "draw_mode": bool(draw_mode),
                            "verbose": bool(verbose)
                        }
                    }
                
                # Salva configuração
                config_path = config_dir / f"unified_config_{algorithm.lower().replace(' ', '_').replace('-', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                config_path.write_text(json.dumps(unified_config, indent=2))
                
                # Carrega configuração se for NSGA-II ou NSGA-II com Cache
                if algorithm in ["NSGA-II", "NSGA-II com Cache"]:
                    st.session_state.nsga_integration.load_configuration(config_path)
                elif algorithm == "Força Bruta":
                    st.session_state.bruteforce_integration.load_configuration(config_path)
                
                st.success(f"✅ Configuração unificada salva e carregada!")
                with st.expander("👀 Ver Configuração Salva"):
                    st.json(unified_config)
                
            except Exception as e:
                st.error(f"Erro ao salvar configuração: {e}")

    # Upload ou criação de indivíduos (editor interativo)
    uploaded_individuals_file = st.file_uploader("Arquivo de indivíduos (.json)", type=["json"])
    if uploaded_individuals_file:
        try:
            st.session_state.individuals_textarea = json.dumps(json.load(uploaded_individuals_file), indent=2)
            st.success("Indivíduos carregados!")
        except Exception as e:
            st.error(f"Erro ao carregar indivíduos: {e}")

    # =================== LABELS (TIPOS DE INDIVÍDUOS) ===================
    # session state for labels
    if 'individual_labels' not in st.session_state:
        st.session_state.individual_labels = []
    if 'labels_description' not in st.session_state:
        st.session_state.labels_description = f"Individuals of the {simulation_name} experiment"

    st.markdown("---")
    st.markdown("#### Editor de Tipos de Indivíduos (Labels)")
    with st.expander("➕ Criar novo tipo de indivíduo", expanded=False):
        with st.form("form_add_label"):
            lbl_name = st.text_input("Nome do tipo", value="New Type")
            amount = st.number_input("Quantidade (amount)", min_value=1, value=10)
            c1, c2, c3 = st.columns(3)
            with c1:
                red = st.number_input("R", min_value=0, max_value=255, value=255)
            with c2:
                green = st.number_input("G", min_value=0, max_value=255, value=0)
            with c3:
                blue = st.number_input("B", min_value=0, max_value=255, value=0)
            speed = st.number_input("Velocidade", min_value=1, value=1)
            KD = st.number_input("KD", min_value=0.0, value=1.0, step=0.1)
            KS = st.number_input("KS", min_value=0.0, value=1.0, step=0.1)
            KW = st.number_input("KW", min_value=0.0, value=0.3, step=0.1)
            KI = st.number_input("KI", min_value=0.0, value=1.0, step=0.1)
            add_label = st.form_submit_button("Adicionar tipo")
        if add_label:
            new = {
                "label": lbl_name,
                "amount": int(amount),
                "red": int(red),
                "green": int(green),
                "blue": int(blue),
                "speed": int(speed),
                "KD": float(KD),
                "KS": float(KS),
                "KW": float(KW),
                "KI": float(KI)
            }
            st.session_state.individual_labels.append(new)
            st.success(f"Tipo '{lbl_name}' adicionado")

    # List and edit existing labels
    if st.session_state.individual_labels:
        st.markdown("**Tipos criados**")
        for idx, lab in enumerate(list(st.session_state.individual_labels)):
            with st.expander(f"{lab.get('label','Tipo')} (x{lab.get('amount',1)})", expanded=False):
                col_a, col_b = st.columns([3,1])
                with col_a:
                    new_label = st.text_input(f"Nome {idx}", value=lab.get('label',''), key=f'label_edit_{idx}')
                    new_amount = st.number_input(f"Quantidade {idx}", min_value=1, value=int(lab.get('amount',1)), key=f'amount_edit_{idx}')
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        new_r = st.number_input(f"R {idx}", min_value=0, max_value=255, value=int(lab.get('red',255)), key=f'r_edit_{idx}')
                    with c2:
                        new_g = st.number_input(f"G {idx}", min_value=0, max_value=255, value=int(lab.get('green',0)), key=f'g_edit_{idx}')
                    with c3:
                        new_b = st.number_input(f"B {idx}", min_value=0, max_value=255, value=int(lab.get('blue',0)), key=f'b_edit_{idx}')
                    new_speed = st.number_input(f"Speed {idx}", min_value=1, value=int(lab.get('speed',1)), key=f'spd_edit_{idx}')
                    new_KD = st.number_input(f"KD {idx}", min_value=0.0, value=float(lab.get('KD',1.0)), step=0.1, key=f'kd_edit_{idx}')
                    new_KS = st.number_input(f"KS {idx}", min_value=0.0, value=float(lab.get('KS',1.0)), step=0.1, key=f'ks_edit_{idx}')
                    new_KW = st.number_input(f"KW {idx}", min_value=0.0, value=float(lab.get('KW',0.3)), step=0.1, key=f'kw_edit_{idx}')
                    new_KI = st.number_input(f"KI {idx}", min_value=0.0, value=float(lab.get('KI',1.0)), step=0.1, key=f'ki_edit_{idx}')
                with col_b:
                    if st.button("Salvar", key=f'save_label_{idx}'):
                        st.session_state.individual_labels[idx] = {
                            "label": new_label,
                            "amount": int(new_amount),
                            "red": int(new_r),
                            "green": int(new_g),
                            "blue": int(new_b),
                            "speed": int(new_speed),
                            "KD": float(new_KD),
                            "KS": float(new_KS),
                            "KW": float(new_KW),
                            "KI": float(new_KI)
                        }
                        st.success("Tipo atualizado")
                    if st.button("Remover", key=f'del_label_{idx}'):
                        st.session_state.individual_labels.pop(idx)
                        st.experimental_rerun()

        # Description and export
        st.text_input("Descrição (export)", value=st.session_state.labels_description, key='labels_description')
        col_e1, col_e2 = st.columns([1,1])
        with col_e1:
            if st.button("📤 Exportar labels (grupo)"):
                try:
                    temp_dir = Path("temp_simulation")
                    temp_dir.mkdir(exist_ok=True)
                    # build grouped schema
                    group = {
                        "description": st.session_state.get('labels_description', f"Individuals of the {simulation_name} experiment"),
                        "caracterizations": st.session_state.individual_labels
                    }
                    grp_path = temp_dir / "individuals_labels.json"
                    grp_path.write_text(json.dumps(group, indent=2, ensure_ascii=False))

                    # also build expanded individual list for simulator compatibility
                    expanded = []
                    for c in st.session_state.individual_labels:
                        amt = int(c.get('amount', 1))
                        for _ in range(amt):
                            expanded.append({
                                "label": c.get('label'),
                                "color": [int(c.get('red',255)), int(c.get('green',0)), int(c.get('blue',0))],
                                "speed": int(c.get('speed',1)),
                                "KD": float(c.get('KD',1.0)),
                                "KS": float(c.get('KS',1.0)),
                                "KW": float(c.get('KW',0.3)),
                                "KI": float(c.get('KI',1.0)),
                                "row": 0,
                                "col": 0
                            })
                    expanded_path = temp_dir / "individuals.json"
                    expanded_path.write_text(json.dumps(expanded, indent=2, ensure_ascii=False))
                    # update session textarea so existing editor reflects the expanded individuals
                    st.session_state.individuals_textarea = json.dumps(expanded, indent=2, ensure_ascii=False)
                    st.success(f"Labels exportados para: {grp_path} (grupo) e {expanded_path} (expandido)")
                except Exception as e:
                    st.error(f"Erro ao exportar labels: {e}")
        with col_e2:
            if st.button("🔁 Sincronizar para indivíduos (Salvar temporário) "):
                try:
                    temp_dir = Path("temp_simulation")
                    temp_dir.mkdir(exist_ok=True)
                    expanded = []
                    for c in st.session_state.individual_labels:
                        amt = int(c.get('amount',1))
                        for _ in range(amt):
                            expanded.append({
                                "label": c.get('label'),
                                "color": [int(c.get('red',255)), int(c.get('green',0)), int(c.get('blue',0))],
                                "speed": int(c.get('speed',1)),
                                "KD": float(c.get('KD',1.0)),
                                "KS": float(c.get('KS',1.0)),
                                "KW": float(c.get('KW',0.3)),
                                "KI": float(c.get('KI',1.0)),
                                "row": 0,
                                "col": 0
                            })
                    expanded_path = temp_dir / "individuals.json"
                    expanded_path.write_text(json.dumps(expanded, indent=2, ensure_ascii=False))
                    st.session_state.individuals_textarea = json.dumps(expanded, indent=2, ensure_ascii=False)
                    st.success("Sincronizado para temp_simulation/individuals.json")
                except Exception as e:
                    st.error(f"Erro ao sincronizar: {e}")
    else:
        st.info("Nenhum tipo de indivíduo criado ainda. Use o formulário acima para adicionar.")

    st.markdown("---")
    st.markdown("#### Editor de Indivíduos")
    try:
        current_list = json.loads(st.session_state.get("individuals_textarea","[]"))
        if isinstance(current_list, dict) and "caracterizations" in current_list:
            # Converte caracterizations (formato de grupos) para lista simples para edição
            tmp = []
            for c in current_list.get("caracterizations", []):
                amount = int(c.get("amount", 1))
                for _ in range(amount):
                    tmp.append({
                        "label": c.get("label","Individuo"),
                        "color": [c.get("red",255), c.get("green",0), c.get("blue",0)],
                        "speed": c.get("speed",1),
                        "KD": c.get("KD",1.0),
                        "KS": c.get("KS",1.0),
                        "KW": c.get("KW",1.0),
                        "KI": c.get("KI",0.5),
                        "row": 0,
                        "col": 0
                    })
            current_list = tmp
        if not isinstance(current_list, list):
            current_list = []
    except Exception:
        current_list = []

    num_inds = st.number_input("Quantidade de indivíduos", min_value=0, value=len(current_list))
    # Ajusta tamanho da lista
    if num_inds > len(current_list):
        for _ in range(num_inds - len(current_list)):
            current_list.append({"label":"Individuo","color":[255,0,0],"speed":1,"KD":1.0,"KS":1.0,"KW":1.0,"KI":0.5,"row":0,"col":0})
    elif num_inds < len(current_list):
        current_list = current_list[:num_inds]

    for i in range(len(current_list)):
        with st.expander(f"Indivíduo {i+1}", expanded=False):
            ind = current_list[i]
            ind["label"] = st.text_input(f"Label {i+1}", value=ind.get("label","Individuo"), key=f"lbl_{i}")
            c1, c2, c3 = st.columns(3)
            with c1:
                r = st.number_input(f"R {i+1}", min_value=0, max_value=255, value=int(ind.get("color",[255,0,0])[0]), key=f"r_{i}")
            with c2:
                g = st.number_input(f"G {i+1}", min_value=0, max_value=255, value=int(ind.get("color",[255,0,0])[1]), key=f"g_{i}")
            with c3:
                b = st.number_input(f"B {i+1}", min_value=0, max_value=255, value=int(ind.get("color",[255,0,0])[2]), key=f"b_{i}")
            ind["color"] = [r,g,b]
            c4, c5 = st.columns(2)
            with c4:
                # Garante que o valor padrão respeite o min_value (evita erro quando JSON traz 0 ou negativo)
                _spd_default = ind.get("speed", 1)
                try:
                    _spd_default = int(_spd_default)
                except Exception:
                    _spd_default = 1
                if _spd_default < 1:
                    _spd_default = 1
                ind["speed"] = st.number_input(
                    f"Velocidade {i+1}",
                    min_value=1,
                    value=_spd_default,
                    key=f"spd_{i}"
                )
            with c5:
                ind["KD"] = st.number_input(f"KD {i+1}", min_value=0.0, value=float(ind.get("KD",1.0)), step=0.1, key=f"kd_{i}")
            c6, c7 = st.columns(2)
            with c6:
                ind["KS"] = st.number_input(f"KS {i+1}", min_value=0.0, value=float(ind.get("KS",1.0)), step=0.1, key=f"ks_{i}")
            with c7:
                ind["KW"] = st.number_input(f"KW {i+1}", min_value=0.0, value=float(ind.get("KW",1.0)), step=0.1, key=f"kw_{i}")
            ind["KI"] = st.number_input(f"KI {i+1}", min_value=0.0, value=float(ind.get("KI",0.5)), step=0.1, key=f"ki_{i}")
            c8, c9 = st.columns(2)
            with c8:
                ind["row"] = st.number_input(f"Row {i+1}", min_value=0, value=int(ind.get("row",0)), key=f"row_{i}")
            with c9:
                ind["col"] = st.number_input(f"Col {i+1}", min_value=0, value=int(ind.get("col",0)), key=f"col_{i}")

    # Sincroniza JSON de indivíduos e permite salvar
    st.session_state.individuals_textarea = json.dumps(current_list, indent=2)
    st.text_area("JSON de indivíduos", value=st.session_state.individuals_textarea, height=160, key="inds_json_view")

    if st.button("💾 Salvar indivíduos"):
        Path("temp_simulation").mkdir(exist_ok=True)
        Path("temp_simulation/individuals.json").write_text(st.session_state.individuals_textarea)
        st.success("Indivíduos salvos!")

with col2:
    if mapa_nome:
        mapa_path = Path("mapas") / f"{mapa_nome}.png"
        if mapa_path.exists():
            # Exibe imagem original sem processamento para manter qualidade máxima
            # A quantização só será feita durante a execução da simulação
            img = Image.open(mapa_path)
            st.image(img, use_container_width=True, output_format="PNG")
        else:
            st.warning("Mapa não encontrado.")
    else:
        st.info("Selecione um mapa para visualizar.")

# ================= EXECUÇÃO =================
if st.session_state.run_sim:
    if not mapa_nome:
        st.error("Selecione um mapa primeiro.")
    elif not st.session_state.get("individuals_textarea"):
        st.error("Defina ou carregue indivíduos antes de executar a simulação.")
    else:
        with st.spinner("Executando simulação..."):
            try:
                temp_dir = Path("temp_simulation")
                temp_dir.mkdir(exist_ok=True)

                individuals_path = temp_dir / "individuals.json"
                with open(individuals_path,"w") as f:
                    json.dump(json.loads(st.session_state.individuals_textarea),f,indent=2)

                gen = map_creation_service.convert_image_to_maps(str(mapa_path), str(temp_dir / "selected_map"))
                main_map_path = Path(gen.get("main",""))
                if not main_map_path.exists():
                    raise RuntimeError("Falha ao gerar .map")

                simulator_input_dir = Path("simulador_heuristica") / "input" / simulation_name
                simulator_input_dir.mkdir(parents=True, exist_ok=True)

                shutil.copy2(main_map_path, simulator_input_dir / "map.txt")
                shutil.copy2(individuals_path, simulator_input_dir / "individuals.json")

                # Se NSGA-II (standard ou cached), executa otimização multiobjetivo
                if algorithm in ["NSGA-II", "NSGA-II com Cache"]:
                    use_cached = (algorithm == "NSGA-II com Cache")
                    st.info(f"Iniciando execução {algorithm}...")
                    
                    # exige configuração NSGA-II carregada
                    if not getattr(st.session_state.nsga_integration, 'config', None):
                        st.error("Configuração NSGA-II não encontrada no session_state")
                        raise RuntimeError("Configuração do NSGA-II não carregada. Crie ou carregue uma configuração acima.")
                    st.info(f"Configuração NSGA-II encontrada: {st.session_state.nsga_integration.config}")
                    
                    # Set the workflow mode (standard or cached)
                    st.session_state.nsga_integration.set_use_cached(use_cached)
                    if use_cached:
                        st.success("✓ Modo Cached NSGA-II habilitado (com cache de simulações)")
                    else:
                        st.info("Usando NSGA-II padrão (pymoo)")
                    
                    # Obtém parâmetros de simulação da configuração unificada
                    sim_params = st.session_state.nsga_integration.get_simulation_params()
                    scenario_seed = sim_params.get('scenario_seed', 42)
                    simulation_seed = sim_params.get('simulation_seed', 123)
                    draw_mode = sim_params.get('draw_mode', True)
                    
                    st.info(f"Parâmetros de simulação: scenario_seed={scenario_seed}, simulation_seed={simulation_seed}, draw_mode={draw_mode}")
                    
                    # Prepara templates para NSGA-II
                    st.info("Preparando templates para NSGA-II...")
                    map_template = Path(simulator_input_dir / "map.txt").read_text()
                    individuals_template = json.loads(Path(simulator_input_dir / "individuals.json").read_text())
                    st.info(f"Map template carregado: {len(map_template)} caracteres")
                    st.info(f"Individuals template carregado: {len(individuals_template)} indivíduos")
                    
                    st.info("Chamando setup_optimization...")
                    try:
                        # Extrai posições das portas do mapa
                        door_positions = st.session_state.nsga_integration.extract_door_positions_from_map(map_template)
                        st.info(f"Posições de portas extraídas: {len(door_positions)} posições")
                        
                        # Setup only for standard NSGA-II (cached has different flow)
                        if not use_cached:
                            ok = st.session_state.nsga_integration.setup_optimization(
                                map_template=map_template,
                                individuals_template=individuals_template,
                                door_positions=door_positions
                            )
                            st.info(f"setup_optimization retornou: {ok}")
                            if not ok:
                                st.error("setup_optimization retornou False - verifique os logs acima")
                                raise RuntimeError("Falha ao configurar NSGA-II")
                        else:
                            st.info("Modo cached: pulando setup_optimization (não necessário)")
                            ok = True
                    except Exception as e:
                        import traceback
                        st.error(f"Exceção ao chamar setup_optimization: {e}")
                        st.text("Traceback completo:")
                        st.code(traceback.format_exc())
                        ok = False
                    
                    if not ok:
                        raise RuntimeError("Falha ao configurar NSGA-II")
                    
                    # Run optimization (experiment_name required for cached)
                    pareto = st.session_state.nsga_integration.run_optimization(
                        experiment_name=simulation_name if use_cached else None
                    )
                    if not pareto:
                        raise RuntimeError("NSGA-II não retornou resultados")
                    # salva resultados em uploads/nsga_ii
                    out_dir_nsga = Path("uploads")/"nsga_ii"
                    out_dir_nsga.mkdir(parents=True, exist_ok=True)
                    from datetime import datetime as _dt
                    nsga_file = out_dir_nsga / f"results_{simulation_name}_{_dt.now().strftime('%Y%m%d_%H%M%S')}.json"
                    st.session_state.nsga_integration.save_results(pareto, nsga_file)
                    # marca como sucesso
                    completed_process = type("Proc", (), {"returncode": 0, "stdout": f"{algorithm} concluído", "stderr": ""})()
                
                elif algorithm == "Força Bruta":
                    st.info("🔍 Iniciando Brute Force...")
                    
                    # Usa configuração já carregada ou defaults
                    if not hasattr(st.session_state.bruteforce_integration, 'config') or not st.session_state.bruteforce_integration.config:
                        st.info("Usando configuração padrão para Brute Force")
                    
                    # Obtém parâmetros de simulação
                    sim_params = st.session_state.bruteforce_integration.config.get('simulation_params', {})
                    scenario_seed = sim_params.get('scenario_seed', 42)
                    num_scenarios = sim_params.get('num_scenarios', 20)
                    
                    st.info(f"Parâmetros: scenario_seed={scenario_seed}, num_scenarios={num_scenarios}")
                    
                    # Arquivos já foram preparados em simulator_input_dir acima
                    # Brute Force vai ler de lá via Instance
                    
                    # Executa Brute Force
                    st.info("Executando busca exaustiva com barra de progresso...")
                    draw_mode = sim_params.get('draw_mode', False)
                    
                    result = st.session_state.bruteforce_integration.run_optimization(
                        experiment_name=simulation_name,
                        draw=draw_mode
                    )
                    
                    if not result:
                        raise RuntimeError("Brute Force não retornou resultados")
                    
                    # Desempacota resultado: (combinations, objectives, exits_info)
                    pareto_combinations, pareto_objectives, exits_info = result
                    
                    st.success(f"✓ Brute Force concluído: {len(pareto_combinations)} soluções na fronteira de Pareto")
                    
                    # Salva resultados
                    out_dir_bf = Path("uploads") / "brute_force"
                    out_dir_bf.mkdir(parents=True, exist_ok=True)
                    from datetime import datetime as _dt
                    bf_file = out_dir_bf / f"results_{simulation_name}_{_dt.now().strftime('%Y%m%d_%H%M%S')}.json"
                    st.session_state.bruteforce_integration.save_results(
                        pareto_combinations, 
                        pareto_objectives, 
                        exits_info, 
                        bf_file
                    )
                    st.success(f"Resultados salvos em {bf_file}")
                    
                    # Marca como sucesso
                    completed_process = type("Proc", (), {"returncode": 0, "stdout": f"Brute Force concluído: {len(pareto_combinations)} soluções Pareto", "stderr": ""})()
                
                else:
                    # Para outros algoritmos, usa parâmetros da configuração unificada ou padrões
                    sim_params = st.session_state.get('simulation_params', {})
                    scenario_seed = sim_params.get('scenario_seed', st.session_state.get('scenario_seed', 75))
                    simulation_seed = sim_params.get('simulation_seed', st.session_state.get('simulation_seed', 75))
                    draw_mode = sim_params.get('draw_mode', True)
                    
                    completed_process = st.session_state.simulator_integration.run_simulator_cli(
                        experiment_name=simulation_name,
                        draw=draw_mode,
                        scenario_seed=scenario_seed,
                        simulation_seed=simulation_seed
                    )

                st.text("STDOUT do simulador:")
                st.code(completed_process.stdout)
                st.text("STDERR do simulador:")
                st.code(completed_process.stderr)

                if completed_process.returncode==0:
                    st.success("Simulação executada com sucesso!")
                else:
                    st.error(f"Simulador retornou código {completed_process.returncode}")

                st.session_state.last_results = completed_process

                # ===== Persistência no banco de dados =====
                try:
                    db = st.session_state.db_integration
                    # Salva/obtém ID do mapa
                    map_id = db.save_map(mapa_nome or simulation_name, str(simulator_input_dir / "map.txt"))

                    # Monta payloads JSON para salvar
                    cli_config = {
                        "experiment_name": simulation_name,
                        "draw": True,
                        "scenario_seed": scenario_seed,
                        "simulation_seed": simulation_seed,
                        "timestamp": datetime.now().isoformat()
                    }
                    # Lê conteúdos para armazenar
                    with open(simulator_input_dir / "individuals.json", "r") as f:
                        individuals_json_str = f.read()
                    params_path = Path("temp_simulation") / "parameters.json"
                    config_simulacao_json_str = params_path.read_text() if params_path.exists() else "{}"

                    # Gera um id_simulacao baseado em timestamp
                    id_simulacao = int(datetime.now().timestamp())

                    saved = db.save_simulation(
                        id_simulacao=id_simulacao,
                        id_mapa=map_id if isinstance(map_id, int) else -1,
                        nome=simulation_name,
                        algoritmo=algorithm,
                        config_pedestres_json=individuals_json_str,
                        pos_pedestres_json="[]",
                        config_simulacao_json=config_simulacao_json_str,
                        cli_config_json=json.dumps(cli_config, ensure_ascii=False),
                        nsga_config_json=None,
                        executada=1 if completed_process.returncode==0 else 0
                    )
                    # If primary save failed, try to insert without specified id and get assigned id
                    if not saved:
                        try:
                            new_id = db.create_simulation_return_id(
                                id_mapa=map_id if isinstance(map_id, int) else -1,
                                nome=simulation_name,
                                algoritmo=algorithm,
                                config_pedestres_json=individuals_json_str,
                                pos_pedestres_json="[]",
                                config_simulacao_json=config_simulacao_json_str,
                                cli_config_json=json.dumps(cli_config, ensure_ascii=False),
                                nsga_config_json=None,
                                executada=1 if completed_process.returncode==0 else 0
                            )
                            if new_id:
                                id_simulacao = new_id
                                saved = True
                        except Exception:
                            saved = False

                    if saved:
                        st.success("Simulação registrada no banco de dados.")
                        # ===== Save metrics.json (if produced) =====
                        try:
                            out_dir = Path("simulador_heuristica") / "output" / simulation_name
                            metrics_path = out_dir / "metrics.json"
                            if metrics_path.exists():
                                metrics_json = metrics_path.read_text()
                                ok_res = st.session_state.db_integration.save_result(id_simulacao, metrics_json)
                                if ok_res:
                                    st.success("Métricas salvas no banco de dados.")
                                else:
                                    st.warning("Falha ao salvar métricas no banco de dados.")
                        except Exception as e:
                            st.warning(f"Erro ao salvar métricas: {e}")

                        # ===== NSGA-II specific results (pareto) =====
                        if algorithm in ["NSGA-II", "NSGA-II com Cache"]:
                            try:
                                if nsga_file and nsga_file.exists():
                                    fp_json = nsga_file.read_text()
                                    ok_pf = st.session_state.db_integration.save_nsga_results(id_simulacao, fp_json)
                                    if ok_pf:
                                        st.success("Resultados NSGA-II salvos no banco de dados.")
                                    else:
                                        st.warning("Falha ao salvar resultados NSGA-II no banco de dados.")
                            except Exception as e:
                                st.warning(f"Erro ao salvar resultados NSGA-II: {e}")
                        
                        # ===== Brute Force specific results (pareto) =====
                        if algorithm == "Força Bruta":
                            try:
                                if bf_file and bf_file.exists():
                                    bf_json = bf_file.read_text()
                                    ok_bf = st.session_state.db_integration.save_nsga_results(id_simulacao, bf_json)
                                    if ok_bf:
                                        st.success("Resultados Brute Force salvos no banco de dados.")
                                    else:
                                        st.warning("Falha ao salvar resultados Brute Force no banco de dados.")
                            except Exception as e:
                                st.warning(f"Erro ao salvar resultados Brute Force: {e}")
                    else:
                        st.warning("Não foi possível salvar os resultados no banco.")
                except Exception as e:
                    st.warning(f"Falha ao salvar no banco: {e}")

                # ===== Persistir métricas em output/<experiment>/metrics.json =====
                try:
                    out_dir = Path("simulador_heuristica") / "output" / simulation_name
                    out_dir.mkdir(parents=True, exist_ok=True)
                    # extração básica do stdout
                    iters = None
                    dist = None
                    mean_distance_series = []
                    evacuated_progress = []
                    for line in completed_process.stdout.splitlines():
                        if line.strip().startswith("qtd iteracoes"):
                            try:
                                iters = int(line.split()[-1])
                            except Exception:
                                pass
                        if line.strip().startswith("qtd distancia"):
                            try:
                                dist = float(line.split()[-1])
                            except Exception:
                                pass
                    # tenta ler série auxiliar, se produzirmos no futuro
                    metrics = {}
                    if iters is not None:
                        metrics["iterations"] = iters
                        # Map to expected key for NSGA integration
                        metrics["tempo_total"] = iters
                    if dist is not None:
                        metrics["distance"] = dist
                        # Map to expected key for NSGA integration
                        metrics["distancia_total"] = dist
                    if mean_distance_series:
                        metrics["mean_distance_series"] = mean_distance_series
                    if evacuated_progress:
                        metrics["evacuated_progress"] = evacuated_progress
                    metrics["algorithm"] = algorithm
                    metrics["scenario_seed"] = scenario_seed
                    metrics["simulation_seed"] = simulation_seed
                    if metrics:
                        metrics_path = out_dir / "metrics.json"
                        with open(metrics_path, "w") as f:
                            json.dump(metrics, f, indent=2)
                        # quick verification log
                        try:
                            written = metrics_path.read_text()
                            st.info(f"Metrics written to {metrics_path}")
                            st.code(written)
                        except Exception as e:
                            st.warning(f"Não foi possível ler metrics.json após escrita: {e}")
                except Exception as e:
                    st.warning(f"Falha ao salvar métricas: {e}")

            except Exception as e:
                st.error(f"Erro na execução: {e}")
                # Exibe rastreio de erro como "stderr" para diagnóstico
                import traceback as _tb
                st.text("STDERR:")
                st.code(_tb.format_exc())

            finally:
                st.session_state.run_sim = False

# ================= RESULTADOS =================
if st.session_state.view_results:
    if st.session_state.last_results:
        results = st.session_state.last_results
        st.markdown("### Resultados da Simulação")
        st.json(results)
    else:
        st.info("Execute a simulação primeiro.")
    st.session_state.view_results = False
