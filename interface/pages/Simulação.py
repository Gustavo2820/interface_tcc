# pages/simulacao.py
"""
Interface para configuração de simulações de evacuação.

Este módulo permite aos usuários configurar parâmetros específicos de simulação,
visualizar o mapa selecionado e iniciar a execução de simulações.
"""
import streamlit as st
from pathlib import Path
from PIL import Image
import json
import sys
import os

# Adiciona o caminho dos serviços ao sys.path
sys.path.append(str(Path(__file__).parent.parent))

from services.simulator_integration import SimulatorIntegration, DatabaseIntegration
from services.map_creation_integration import map_creation_service

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(page_title="Simulação", layout="wide")

# ================= CSS GLOBAL =================
st.markdown("""
    <style>
    body {
        font-family: 'Inter', 'Roboto', sans-serif;
        background-color: white;
        color: #222;
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

    /* ===== BOTÕES ===== */
    .botoes {
        display: flex;
        justify-content: flex-end;
        gap: 20px;
        margin-right: 40px;
        margin-bottom: 30px;
    }
    .botao {
        background-color: #142b3b;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
        transition: all 0.2s ease-in-out;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    .botao:hover {
        transform: scale(1.05);
        background-color: #1d3d57;
    }

    /* ===== LAYOUT CENTRAL ===== */
    .container {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: flex-start;
        gap: 60px;
        width: 100%;
    }
    .painel-esquerda {
        display: flex;
        flex-direction: column;
        gap: 25px;
    }
    .bloco {
        background-color: #142b3b;
        color: white;
        text-align: center;
        border-radius: 10px;
        padding: 10px 0;
        font-weight: bold;
    }
    .input {
        background-color: #b3b3b3;
        border: none;
        border-radius: 6px;
        padding: 6px;
        color: black;
        width: 200px;
        text-align: center;
    }
    .mapa {
        border: 1px solid #ccc;
        border-radius: 6px;
        width: 800px;
        height: 600px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# ================= MENU SUPERIOR =================
st.markdown("""
<div class="menu">
    <a href="../app" >Menu</a>
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

# ================= OBTÉM PARÂMETROS DA URL E LISTA MAPAS =================
params = st.query_params
mapa_nome = params.get("mapa", [""])[0] if isinstance(params.get("mapa"), list) else params.get("mapa", "")

# Carrega mapas disponíveis do diretório 'mapas/'
mapas_dir = Path("mapas")
mapas_dir.mkdir(exist_ok=True)
map_options = sorted([p.stem for p in mapas_dir.glob("*.png")])

# ================= BOTÕES SUPERIORES =================
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn1:
    if st.button("💾 Salvar Configuração", key="save_config"):
        st.success("Configuração salva!")

with col_btn2:
    if st.button("▶️ Executar Simulação", key="run_simulation"):
        st.session_state.run_simulation = True

with col_btn3:
    if st.button("📊 Ver Resultados", key="view_results"):
        st.session_state.view_results = True

# ================= CONTEÚDO PRINCIPAL =================
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown('<div class="bloco">Nome da Simulação</div>', unsafe_allow_html=True)
    simulation_name = st.text_input("", value=f"sim_{mapa_nome}", key="sim_name")

    st.markdown('<div class="bloco">Algoritmo</div>', unsafe_allow_html=True)
    algorithm = st.selectbox("", ["Simulação Direta", "Algoritmo Genético", "NSGA-II", "Força Bruta"], key="algorithm")

    st.markdown('<div class="bloco">Mapa</div>', unsafe_allow_html=True)
    selected_map = st.selectbox("", options=["(selecione)"] + map_options, index=(map_options.index(mapa_nome)+1) if mapa_nome in map_options else 0, key="selected_map")
    if selected_map != "(selecione)" and selected_map != mapa_nome:
        mapa_nome = selected_map
        st.session_state["selected_map_name"] = mapa_nome

    st.markdown('<div class="bloco">Arquivo de Parâmetros</div>', unsafe_allow_html=True)
    param_file = st.file_uploader("", type=["json", "txt"], key="param_file")

    st.markdown('<div class="bloco">Arquivo de Indivíduos</div>', unsafe_allow_html=True)
    individuals_file = st.file_uploader("", type=["json"], key="individuals_file")

    # Configurações avançadas
    with st.expander("⚙️ Configurações Avançadas"):
        draw_mode = st.checkbox("Gerar imagens", value=True)
        scenario_seed = st.number_input("Seed do cenário", value=None, min_value=0)
        simulation_seed = st.number_input("Seed da simulação", value=None, min_value=0)

with col2:
    # Carregar imagem do mapa selecionado
    if mapa_nome:
        mapa_path = Path("mapas") / f"{mapa_nome}.png"
        if mapa_path.exists():
            img = Image.open(mapa_path)
            st.image(img, use_container_width=True)
        else:
            st.warning("Mapa não encontrado.")
    else:
        st.info("Selecione um mapa para visualizar.")

# ================= EXECUÇÃO DA SIMULAÇÃO =================
if st.session_state.get('run_simulation', False):
    if not mapa_nome:
        st.error("Selecione um mapa primeiro.")
    elif not individuals_file:
        st.error("Faça upload do arquivo de indivíduos.")
    else:
        with st.spinner("Executando simulação..."):
            try:
                # Salva arquivos temporários
                temp_dir = Path("temp_simulation")
                temp_dir.mkdir(exist_ok=True)
                
                # Salva arquivo de indivíduos
                individuals_path = temp_dir / "individuals.json"
                with open(individuals_path, 'w') as f:
                    json.dump(json.load(individuals_file), f, indent=2)
                
                # Converte o PNG escolhido para map.txt para o simulador
                # Estratégia: garantir estabilidade com o simulador (usa map.txt)
                png_chosen = Path("mapas") / f"{mapa_nome}.png"
                if not png_chosen.exists():
                    st.error("PNG do mapa selecionado não encontrado.")
                    raise RuntimeError("Mapa PNG ausente")
                
                # Converter PNG → .map principal (códigos) usando utilitário existente
                # Em seguida, traduzir .map para map.txt no formato do simulador (0/1/2... como já usa)
                # Para manter simplicidade e compatibilidade, usaremos o .map gerado como map.txt
                base_tmp = temp_dir / "selected_map"
                from services.map_creation_integration import map_creation_service
                gen = map_creation_service.convert_image_to_maps(str(png_chosen), str(base_tmp))
                main_map_path = Path(gen.get("main", ""))
                if not main_map_path.exists():
                    st.error("Falha ao gerar arquivo .map a partir do PNG selecionado.")
                    raise RuntimeError("Conversão .map falhou")
                
                # Copiar/renomear para map.txt esperado pelo simulador
                map_path = temp_dir / "map.txt"
                with open(main_map_path, 'r') as fsrc, open(map_path, 'w') as fdst:
                    fdst.write(fsrc.read())
                    
                    # Cria nome único para o experimento
                    experiment_name = st.session_state.simulator_integration.create_experiment_name()
                    
                    # Prepara o experimento
                    st.session_state.simulator_integration.prepare_experiment_from_uploads(
                        experiment_name, map_path, individuals_path
                    )
                    
                    # Executa a simulação
                    result = st.session_state.simulator_integration.run_simulator_cli(
                        experiment_name, 
                        draw=draw_mode,
                        scenario_seed=scenario_seed,
                        simulation_seed=simulation_seed
                    )
                    
                    # Lê os resultados
                    results = st.session_state.simulator_integration.read_results(experiment_name)
                    
                    st.success("Simulação executada com sucesso!")
                    st.session_state.last_experiment = experiment_name
                    st.session_state.last_results = results
                    
                    # Salva no banco de dados
                    st.session_state.db_integration.save_simulation(
                        id_simulacao=1,  # Em produção, gerar ID único
                        id_mapa=1,       # Em produção, buscar ID do mapa
                        nome=simulation_name,
                        algoritmo=algorithm,
                        config_pedestres_json=json.dumps({"uploaded": True}),
                        pos_pedestres_json=json.dumps({"default": True}),
                        config_simulacao_json=json.dumps({"draw": draw_mode}),
                        cli_config_json=json.dumps({"scenario_seed": scenario_seed, "simulation_seed": simulation_seed}),
                        executada=1
                    )
                # Limpa arquivos temporários
                import shutil
                if temp_dir.exists():
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    
            except Exception as e:
                st.error(f"Erro na execução da simulação: {e}")
        
        st.session_state.run_simulation = False

# ================= VISUALIZAÇÃO DE RESULTADOS =================
if st.session_state.get('view_results', False):
    if 'last_results' in st.session_state:
        results = st.session_state.last_results
        
        st.markdown("### 📊 Resultados da Simulação")
        
        if 'error' in results:
            st.error(f"Erro: {results['error']}")
        else:
            if results['report']:
                st.markdown(f"**Relatório:** {results['report']}")
            
            if results['frames']:
                st.markdown(f"**Frames gerados:** {len(results['frames'])}")
                
                # Mostra algumas imagens dos frames
                for i, frame in enumerate(results['frames'][:3]):  # Mostra apenas os primeiros 3
                    st.image(str(frame), caption=f"Frame {i+1}")
            
            if results['metrics']:
                st.markdown(f"**Arquivos de métricas:** {len(results['metrics'])}")
    else:
        st.info("Execute uma simulação primeiro para ver os resultados.")
    
    st.session_state.view_results = False
