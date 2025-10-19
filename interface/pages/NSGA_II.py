# pages/NSGA_II.py
"""
Interface para configuração do algoritmo NSGA-II.

Este módulo permite aos usuários fazer upload de arquivos de configuração
para execução do algoritmo NSGA-II (Non-dominated Sorting Genetic Algorithm II).
"""
import streamlit as st
from pathlib import Path
import json
import sys

# Adiciona o caminho dos serviços ao sys.path
sys.path.append(str(Path(__file__).parent.parent))

from services.simulator_integration import SimulatorIntegration, DatabaseIntegration
from services.nsga_integration import NSGAIntegration

st.set_page_config(page_title="NSGA-II", layout="wide")

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
    .titulo { text-align: center; font-size: 36px; font-weight: 700; margin-bottom: 10px; }
    .linha { width: 200px; height: 2px; background-color: #444; margin: 0 auto 40px auto; }
    .upload-box { border: 2px dashed #142b3b; border-radius: 12px; padding: 40px; background-color: #f9f9f9; text-align: center; }
    .success { text-align: center; color: green; font-weight: bold; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="menu">
    <a href="../app">Menu</a>
    <a href="./Mapas">Mapas</a>
    <a href="./Parâmetros" class="active">Parâmetros</a>
    <a href="./Resultados">Resultados</a>
    <a href="./Documentação">Documentação</a>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="titulo">NSGA-II</div>', unsafe_allow_html=True)
st.markdown('<div class="linha"></div>', unsafe_allow_html=True)

# ================= INICIALIZAÇÃO DOS SERVIÇOS =================
if 'simulator_integration' not in st.session_state:
    st.session_state.simulator_integration = SimulatorIntegration()
if 'db_integration' not in st.session_state:
    st.session_state.db_integration = DatabaseIntegration()
if 'nsga_integration' not in st.session_state:
    st.session_state.nsga_integration = NSGAIntegration(st.session_state.simulator_integration)

# ================= UPLOAD DE CONFIGURAÇÃO =================
st.markdown('<div class="upload-box">', unsafe_allow_html=True)
st.markdown("**💡 Recomendado**: Use arquivos de configuração unificada que incluem tanto parâmetros NSGA-II quanto de simulação!")
st.markdown("**Exemplos**: `unified_config.json` ou `unified_config_light.json`")
config_file = st.file_uploader("Envie o arquivo de configuração para o algoritmo NSGA-II:", type=["json"], 
                              help="Suporta formato unificado (recomendado) e formato legado")
st.markdown('</div>', unsafe_allow_html=True)

if config_file:
    pasta = Path("uploads/nsga_ii")
    pasta.mkdir(parents=True, exist_ok=True)
    caminho = pasta / config_file.name
    with open(caminho, "wb") as f:
        f.write(config_file.getbuffer())
    st.markdown(f'<p class="success">✅ Arquivo "{config_file.name}" enviado com sucesso!</p>', unsafe_allow_html=True)
    
    # Carrega a configuração
    if st.session_state.nsga_integration.load_configuration(caminho):
        st.success("Configuração carregada com sucesso!")
        st.session_state.nsga_config_loaded = True
        
        # Mostra informações sobre o formato detectado
        if st.session_state.nsga_integration.is_unified_config():
            st.info("✅ **Formato unificado detectado** - parâmetros de simulação incluídos!")
            sim_params = st.session_state.nsga_integration.get_simulation_params()
            if sim_params:
                st.markdown("**Parâmetros de simulação carregados:**")
                st.json(sim_params)
        else:
            st.warning("⚠️ **Formato legado detectado** - apenas parâmetros NSGA-II")
            st.info("💡 Considere usar o formato unificado para incluir parâmetros de simulação!")
    else:
        st.error("Erro ao carregar configuração. Verifique o formato do arquivo.")

# ================= CONFIGURAÇÃO DE OTIMIZAÇÃO =================
if st.session_state.get('nsga_config_loaded', False):
    st.markdown("### ⚙️ Configuração da Otimização")
    
    # Formulário unificado para criar/editar configuração
    with st.expander("🔧 Editar Configuração Unificada"):
        st.markdown("**💡 Edite os parâmetros da configuração carregada**")
        
        with st.form("form_edit_unified_config"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🧬 Parâmetros NSGA-II")
                # Obtém valores atuais da configuração
                current_config = st.session_state.nsga_integration.config
                current_sim_params = st.session_state.nsga_integration.get_simulation_params()
                
                population_size = st.number_input("Tamanho da população", min_value=2, value=current_config.get('population_size', 20), help="Número de indivíduos na população")
                generations = st.number_input("Número de gerações", min_value=1, value=current_config.get('generations', 10), help="Número de gerações para evolução")
                crossover_rate = st.number_input("Taxa de crossover", min_value=0.0, max_value=1.0, value=current_config.get('crossover_rate', 0.8), step=0.05, help="Probabilidade de crossover")
                mutation_rate = st.number_input("Taxa de mutação", min_value=0.0, max_value=1.0, value=current_config.get('mutation_rate', 0.1), step=0.05, help="Probabilidade de mutação")
            
            with col2:
                st.markdown("### 🎯 Parâmetros de Simulação")
                scenario_seed = st.number_input("Seed do cenário", min_value=0, value=current_sim_params.get('scenario_seed', 42), help="Seed para geração do cenário")
                simulation_seed = st.number_input("Seed da simulação", min_value=0, value=current_sim_params.get('simulation_seed', 123), help="Seed para execução da simulação")
                draw_mode = st.checkbox("Gerar imagens", value=current_sim_params.get('draw_mode', True), help="Gerar imagens de saída da simulação")
                verbose = st.checkbox("Modo verboso", value=current_sim_params.get('verbose', False), help="Exibir informações detalhadas durante execução")
            
            description = st.text_input("Descrição da configuração", value="Configuração editada para NSGA-II", help="Descrição opcional da configuração")
            
            submit_edit = st.form_submit_button("💾 Salvar Configuração Editada")
        
        if submit_edit:
            try:
                # Cria nova configuração unificada
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
                
                # Salva configuração editada
                config_dir = Path("uploads")/"configs"
                config_dir.mkdir(parents=True, exist_ok=True)
                from datetime import datetime as _dt
                config_path = config_dir / f"edited_config_{_dt.now().strftime('%Y%m%d_%H%M%S')}.json"
                config_path.write_text(json.dumps(unified_config, indent=2))
                
                # Recarrega configuração
                st.session_state.nsga_integration.load_configuration(config_path)
                
                st.success(f"✅ Configuração editada salva em: `{config_path}`")
                st.json(unified_config)
                
            except Exception as e:
                st.error(f"Erro ao salvar configuração editada: {e}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Arquivo de Mapa:**")
        map_file = st.file_uploader("", type=["txt"], key="nsga_map")
        
        st.markdown("**Arquivo de Indivíduos:**")
        individuals_file = st.file_uploader("", type=["json"], key="nsga_individuals")
    
    with col2:
        st.markdown("**Configuração Atual:**")
        st.json(st.session_state.nsga_integration.config)
        if st.session_state.nsga_integration.is_unified_config():
            st.markdown("**Parâmetros de Simulação:**")
            st.json(st.session_state.nsga_integration.get_simulation_params())

# ================= EXECUÇÃO DA OTIMIZAÇÃO =================
if st.session_state.get('nsga_config_loaded', False) and map_file and individuals_file:
    if st.button("🚀 Executar Otimização NSGA-II", key="run_nsga"):
        with st.spinner("Executando otimização NSGA-II..."):
            try:
                # Carrega template do mapa
                map_content = map_file.read().decode('utf-8')
                
                # Carrega configuração dos indivíduos
                individuals_data = json.load(individuals_file)
                
                # Configura a otimização
                if st.session_state.nsga_integration.setup_optimization(
                    map_content, individuals_data
                ):
                    # Executa a otimização
                    pareto_front = st.session_state.nsga_integration.run_optimization()
                    
                    if pareto_front:
                        st.success(f"Otimização concluída! {len(pareto_front)} soluções na frente de Pareto.")
                        
                        # Salva resultados
                        output_file = Path("uploads/nsga_ii") / f"results_{st.session_state.nsga_integration.create_experiment_name()}.json"
                        if st.session_state.nsga_integration.save_results(pareto_front, output_file):
                            st.success(f"Resultados salvos em: {output_file}")
                        
                        # Exibe algumas soluções
                        st.markdown("### 📊 Soluções Encontradas")
                        for i, solution in enumerate(pareto_front[:5]):  # Mostra apenas as primeiras 5
                            st.write(f"**Solução {i+1}:** Objetivos = {solution.obj}")
                    else:
                        st.error("Erro na execução da otimização.")
                else:
                    st.error("Erro na configuração da otimização.")
                    
            except Exception as e:
                st.error(f"Erro na execução: {e}")

# ================= VISUALIZAÇÃO DE RESULTADOS =================
if st.session_state.get('nsga_results'):
    st.markdown("### 📈 Resultados da Otimização")
    # Aqui seria implementada a visualização dos resultados
    # como gráficos da frente de Pareto, etc.

st.stop()
