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

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(page_title="Simulação", layout="wide")

# ================= INICIALIZAÇÃO DOS SERVIÇOS =================
if 'simulator_integration' not in st.session_state:
    st.session_state.simulator_integration = SimulatorIntegration()
if 'db_integration' not in st.session_state:
    st.session_state.db_integration = DatabaseIntegration()
if 'nsga_integration' not in st.session_state:
    st.session_state.nsga_integration = NSGAIntegration(st.session_state.simulator_integration)

# ================= CARREGAMENTO DE MAPAS =================
mapas_dir = Path("mapas")
mapas_dir.mkdir(exist_ok=True)
map_options = sorted([p.stem for p in mapas_dir.glob("*.png")])

# ================= FUNÇÕES =================
def start_simulation():
    st.session_state.run_sim = True

def quantize_map_colors(image_path):
    valid_colors = {
        "wall": np.array([0,0,0]),
        "door": np.array([255,0,0]),
        "empty": np.array([255,255,255]),
        "drawing": np.array([255,165,0]),
        "window": np.array([0,255,0])
    }
    img = Image.open(image_path).convert("RGB")
    arr = np.array(img)
    def closest_color(pixel):
        distances = {name: np.sum((pixel - col)**2) for name, col in valid_colors.items()}
        return valid_colors[min(distances, key=distances.get)]
    new_arr = np.zeros_like(arr)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            new_arr[i,j] = closest_color(arr[i,j])
    Image.fromarray(new_arr).save(image_path)

# ================= MENU SUPERIOR =================
st.markdown("""
<div style="display:flex; gap:30px; margin-bottom:20px;">
    <a href="../app">Menu</a>
    <a href="./Mapas" style="font-weight:bold;">Mapas</a>
    <a href="./Criacao_Mapas">Criação de Mapas</a>
    <a href="./Parâmetros">Parâmetros</a>
    <a href="./Resultados">Resultados</a>
    <a href="./Documentação">Documentação</a>
</div>
""", unsafe_allow_html=True)

# ================= BOTÕES =================
col_btn1, col_btn2, col_btn3 = st.columns([1,1,1])
with col_btn1:
    if st.button("💾 Salvar Configuração"):
        st.success("Configuração salva!")
with col_btn2:
    st.button("▶️ Executar Simulação", on_click=start_simulation)
with col_btn3:
    if st.button("📊 Ver Resultados"):
        st.session_state.view_results = True

# ================= FORMULÁRIO PRINCIPAL =================
col1, col2 = st.columns([1,3])
with col1:
    simulation_name = st.text_input("Nome da Simulação", value="sim_default")
    algorithm = st.selectbox("Algoritmo", ["Simulação Direta","Algoritmo Genético","NSGA-II","Força Bruta"])
    selected_map = st.selectbox("Mapa", options=["(selecione)"] + map_options)
    mapa_nome = selected_map if selected_map != "(selecione)" else None

    # Upload de configuração unificada
    uploaded_config_file = st.file_uploader("Carregar configuração (.json)", type=["json"], 
                                           help="Arquivo de configuração unificada (recomendado) ou formato legado")
    config_uploaded_path = None
    
    if uploaded_config_file:
        try:
            config_dir = Path("uploads")/"configs"
            config_dir.mkdir(parents=True, exist_ok=True)
            from datetime import datetime as _dt
            config_path = config_dir / f"config_{_dt.now().strftime('%Y%m%d_%H%M%S')}.json"
            config_path.write_text(uploaded_config_file.read().decode('utf-8'))
            config_uploaded_path = config_path
            
            # Carrega configuração
            if algorithm == "NSGA-II":
                if st.session_state.nsga_integration.load_configuration(config_path):
                    st.success("Configuração carregada com sucesso!")
                    if st.session_state.nsga_integration.is_unified_config():
                        st.info("✅ **Formato unificado detectado** - parâmetros de simulação incluídos!")
                        sim_params = st.session_state.nsga_integration.get_simulation_params()
                        if sim_params:
                            st.json(sim_params)
                    else:
                        st.warning("⚠️ **Formato legado detectado** - apenas parâmetros NSGA-II")
                        st.info("💡 Considere usar o formato unificado para incluir parâmetros de simulação!")
                else:
                    st.error("Falha ao carregar configuração")
            else:
                # Para outros algoritmos, carrega parâmetros diretamente
                loaded_config = json.loads(config_path.read_text())
                for k, v in loaded_config.items():
                    st.session_state[k] = v
                st.success("Configuração carregada!")
        except Exception as e:
            st.error(f"Erro ao carregar configuração: {e}")

    # Formulário unificado de criação de configuração
    with st.expander("⚙️ Criar/Editar Configuração Unificada"):
        st.markdown("**💡 Formato Unificado**: Combina parâmetros do algoritmo e de simulação em um único arquivo")
        
        with st.form("form_unified_config"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🧬 Parâmetros do Algoritmo")
                if algorithm == "NSGA-II":
                    population_size = st.number_input("Tamanho da população", min_value=2, value=20, help="Número de indivíduos na população")
                    generations = st.number_input("Número de gerações", min_value=1, value=10, help="Número de gerações para evolução")
                    crossover_rate = st.number_input("Taxa de crossover", min_value=0.0, max_value=1.0, value=0.8, step=0.05, help="Probabilidade de crossover")
                    mutation_rate = st.number_input("Taxa de mutação", min_value=0.0, max_value=1.0, value=0.1, step=0.05, help="Probabilidade de mutação")
                else:
                    # Parâmetros para outros algoritmos
                    pop_size = st.number_input("Tamanho da população", min_value=1, value=10, help="Número de indivíduos")
                    mut_prob = st.number_input("Probabilidade de mutação", min_value=0.0, max_value=1.0, value=0.4, step=0.01, help="Taxa de mutação")
                    max_gen = st.number_input("Máximo de gerações", min_value=1, value=300, help="Número máximo de gerações")
            
            with col2:
                st.markdown("### 🎯 Parâmetros de Simulação")
                scenario_seed = st.number_input("Seed do cenário", min_value=0, value=42, help="Seed para geração do cenário")
                simulation_seed = st.number_input("Seed da simulação", min_value=0, value=123, help="Seed para execução da simulação")
                draw_mode = st.checkbox("Gerar imagens", value=True, help="Gerar imagens de saída da simulação")
                verbose = st.checkbox("Modo verboso", value=False, help="Exibir informações detalhadas durante execução")
            
            description = st.text_input("Descrição da configuração", value=f"Configuração para {algorithm}", help="Descrição opcional da configuração")
            
            submit_config = st.form_submit_button("💾 Salvar Configuração Unificada")
        
        if submit_config:
            try:
                config_dir = Path("uploads")/"configs"
                config_dir.mkdir(parents=True, exist_ok=True)
                
                if algorithm == "NSGA-II":
                    # Formato unificado para NSGA-II
                    unified_config = {
                        "nsga_config": {
                            "population_size": int(population_size),
                            "generations": int(generations),
                            "crossover_rate": float(crossover_rate),
                            "mutation_rate": float(mutation_rate)
                        },
                        "simulation_params": {
                            "scenario_seed": int(scenario_seed),
                            "simulation_seed": int(simulation_seed),
                            "draw_mode": bool(draw_mode),
                            "verbose": bool(verbose)
                        },
                        "description": description
                    }
                else:
                    # Formato unificado para outros algoritmos
                    unified_config = {
                        "algorithm_params": {
                            "pop_size": int(pop_size),
                            "mut_prob": float(mut_prob),
                            "max_gen": int(max_gen)
                        },
                        "simulation_params": {
                            "scenario_seed": int(scenario_seed),
                            "simulation_seed": int(simulation_seed),
                            "draw_mode": bool(draw_mode),
                            "verbose": bool(verbose)
                        },
                        "description": description
                    }
                
                # Salva configuração
                from datetime import datetime as _dt
                config_path = config_dir / f"unified_config_{algorithm.lower().replace(' ', '_')}_{_dt.now().strftime('%Y%m%d_%H%M%S')}.json"
                config_path.write_text(json.dumps(unified_config, indent=2))
                
                # Carrega configuração se for NSGA-II
                if algorithm == "NSGA-II":
                    st.session_state.nsga_integration.load_configuration(config_path)
                
                st.success(f"✅ Configuração unificada salva em: `{config_path}`")
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
            quantize_map_colors(mapa_path)
            img = Image.open(mapa_path).resize((800,600),Image.NEAREST)
            st.image(img,use_column_width=False)
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

                # Se NSGA-II, executa otimização multiobjetivo
                if algorithm == "NSGA-II":
                    st.info("Iniciando execução NSGA-II...")
                    # exige configuração NSGA-II carregada
                    if not getattr(st.session_state.nsga_integration, 'config', None):
                        st.error("Configuração NSGA-II não encontrada no session_state")
                        raise RuntimeError("Configuração do NSGA-II não carregada. Crie ou carregue uma configuração acima.")
                    st.info(f"Configuração NSGA-II encontrada: {st.session_state.nsga_integration.config}")
                    
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
                        
                        ok = st.session_state.nsga_integration.setup_optimization(
                            map_template=map_template,
                            individuals_template=individuals_template,
                            door_positions=door_positions
                        )
                        st.info(f"setup_optimization retornou: {ok}")
                    except Exception as e:
                        import traceback
                        st.error(f"Exceção ao chamar setup_optimization: {e}")
                        st.text("Traceback completo:")
                        st.code(traceback.format_exc())
                        ok = False
                    if not ok:
                        st.error("setup_optimization retornou False - verifique os logs acima")
                        raise RuntimeError("Falha ao configurar NSGA-II")
                    pareto = st.session_state.nsga_integration.run_optimization()
                    if not pareto:
                        raise RuntimeError("NSGA-II não retornou resultados")
                    # salva resultados em uploads/nsga_ii
                    out_dir_nsga = Path("uploads")/"nsga_ii"
                    out_dir_nsga.mkdir(parents=True, exist_ok=True)
                    from datetime import datetime as _dt
                    nsga_file = out_dir_nsga / f"results_{simulation_name}_{_dt.now().strftime('%Y%m%d_%H%M%S')}.json"
                    st.session_state.nsga_integration.save_results(pareto, nsga_file)
                    # marca como sucesso
                    completed_process = type("Proc", (), {"returncode": 0, "stdout": "NSGA-II concluído", "stderr": ""})()
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
                    if saved:
                        st.success("Resultados registrados no banco de dados.")
                        # Se NSGA-II, vincula frente de Pareto ao banco
                        if algorithm == "NSGA-II":
                            try:
                                fp_json = nsga_file.read_text()
                                st.session_state.db_integration.save_nsga_results(id_simulacao, fp_json)
                            except Exception:
                                pass
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
