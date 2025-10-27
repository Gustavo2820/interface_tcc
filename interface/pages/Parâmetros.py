# pages/Parâmetros.py
"""
Página de gerenciamento de presets de parâmetros.

Este módulo permite criar, editar, salvar e carregar presets de configuração
que são compatíveis com NSGA-II (pymoo e cached) e Força Bruta.
"""
import streamlit as st
import json
from pathlib import Path
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Parâmetros", layout="wide")

# ================= CSS =================
st.markdown("""
    <style>
    /* Menu superior */
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
    .menu a:hover { color: #fff; }
    .menu a.active {
        color: #fff;
        font-weight: 600;
        border-bottom: 2px solid #667eea;
        padding-bottom: 4px;
    }

    /* Header */
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

    /* Preset card */
    .preset-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 10px;
        padding: 1.5rem;
        border: 2px solid rgba(102, 126, 234, 0.3);
        margin-bottom: 1rem;
    }
    .preset-card:hover {
        border-color: #667eea;
    }
    </style>
""", unsafe_allow_html=True)

# ===== MENU SUPERIOR =====
st.markdown("""
    <div class="menu">
        <a href="/">Menu</a>
        <a href="/Mapas">Mapas</a>
        <a href="/Criação_de_Mapas">Criação de Mapas</a>
        <a class="active" href="/Parâmetros">Parâmetros</a>
        <a href="/Simulação">Simulação</a>
        <a href="/Resultados">Resultados</a>
        <a href="/Documentação">Documentação</a>
    </div>
""", unsafe_allow_html=True)

# ===== CABEÇALHO =====
st.markdown("""
    <div class="page-header">
        <h1>⚙️ Gerenciamento de Presets de Parâmetros</h1>
        <p>Crie e gerencie configurações reutilizáveis para seus algoritmos de otimização</p>
    </div>
""", unsafe_allow_html=True)

# ================= DIRETÓRIOS =================
PRESETS_DIR = Path("presets")
PRESETS_DIR.mkdir(parents=True, exist_ok=True)

# ================= FUNÇÕES AUXILIARES =================
def load_preset(preset_path: Path) -> dict:
    """Carrega um preset de arquivo JSON."""
    try:
        with open(preset_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Erro ao carregar preset: {e}")
        return None

def save_preset(preset_data: dict, filename: str) -> bool:
    """Salva um preset em arquivo JSON."""
    try:
        preset_path = PRESETS_DIR / filename
        with open(preset_path, 'w', encoding='utf-8') as f:
            json.dump(preset_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar preset: {e}")
        return False

def list_presets() -> list:
    """Lista todos os presets disponíveis."""
    return sorted(PRESETS_DIR.glob("*.json"))

def delete_preset(preset_path: Path) -> bool:
    """Deleta um preset."""
    try:
        preset_path.unlink()
        return True
    except Exception as e:
        st.error(f"Erro ao deletar preset: {e}")
        return False

# ================= INTERFACE =================
tab1, tab2, tab3 = st.tabs(["📋 Presets Disponíveis", "➕ Criar Novo Preset", "ℹ️ Sobre Presets"])

# ===== TAB 1: LISTA DE PRESETS =====
with tab1:
    st.markdown("### 📂 Presets Salvos")
    
    presets = list_presets()
    
    if not presets:
        st.info("🔍 Nenhum preset encontrado. Crie um novo na aba **Criar Novo Preset**!")
    else:
        for preset_file in presets:
            preset_data = load_preset(preset_file)
            if preset_data:
                with st.expander(f"📄 {preset_file.stem}", expanded=False):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Descrição:** {preset_data.get('description', 'Sem descrição')}")
                        st.json(preset_data)
                    
                    with col2:
                        if st.button("🗑️ Deletar", key=f"del_{preset_file.stem}"):
                            if delete_preset(preset_file):
                                st.success(f"Preset '{preset_file.stem}' deletado!")
                                st.rerun()
                        
                        if st.button("📥 Exportar", key=f"exp_{preset_file.stem}"):
                            st.download_button(
                                label="⬇️ Download JSON",
                                data=json.dumps(preset_data, indent=2, ensure_ascii=False),
                                file_name=preset_file.name,
                                mime="application/json",
                                key=f"down_{preset_file.stem}"
                            )

# ===== TAB 2: CRIAR/EDITAR PRESET =====
with tab2:
    st.markdown("### ✨ Configurar Novo Preset")
    
    # Opção de carregar preset existente para editar
    edit_mode = st.checkbox("🔄 Editar preset existente")
    
    if edit_mode:
        presets = list_presets()
        if presets:
            selected_preset = st.selectbox(
                "Selecione o preset para editar:",
                presets,
                format_func=lambda x: x.stem
            )
            base_data = load_preset(selected_preset) if selected_preset else {}
        else:
            st.warning("Nenhum preset disponível para editar")
            base_data = {}
    else:
        base_data = {}
    
    with st.form("preset_form"):
        # Metadados
        st.markdown("#### 📝 Informações Gerais")
        preset_name = st.text_input(
            "Nome do Preset",
            value=base_data.get('preset_name', ''),
            placeholder="Ex: Teste Rápido"
        )
        description = st.text_area(
            "Descrição",
            value=base_data.get('description', ''),
            placeholder="Ex: Configuração leve para testes rápidos"
        )
        
        col1, col2 = st.columns(2)
        
        # ===== PARÂMETROS DE SIMULAÇÃO (COMPARTILHADOS) =====
        with col1:
            st.markdown("#### 🎯 Parâmetros de Simulação")
            st.caption("*Aplicados a todos os algoritmos*")
            
            sim_params = base_data.get('simulation_params', {})
            
            scenario_seed_input = st.text_input(
                "Scenario Seed(s)",
                value=str(sim_params.get('scenario_seed', 42)),
                help="Valor único (ex: 42) ou lista separada por vírgula (ex: 1,2,3)"
            )
            
            simulation_seed = st.number_input(
                "Simulation Seed",
                min_value=0,
                value=sim_params.get('simulation_seed', 123)
            )
            
            max_iterations = st.number_input(
                "Iterações Máximas",
                min_value=100,
                max_value=10000,
                value=sim_params.get('max_iterations', 1200),
                step=100,
                help="Limite de iterações por simulação"
            )
            
            draw_mode = st.checkbox(
                "Gerar Imagens (Draw Mode)",
                value=sim_params.get('draw_mode', False)
            )
            
            verbose = st.checkbox(
                "Modo Verboso",
                value=sim_params.get('verbose', False)
            )
        
        # ===== PARÂMETROS NSGA-II =====
        with col2:
            st.markdown("#### 🧬 Parâmetros NSGA-II")
            st.caption("*Usado por NSGA-II pymoo e cached*")
            
            nsga_conf = base_data.get('nsga_config', {})
            
            population_size = st.number_input(
                "Tamanho da População",
                min_value=2,
                value=nsga_conf.get('population_size', 20)
            )
            
            generations = st.number_input(
                "Número de Gerações",
                min_value=1,
                value=nsga_conf.get('generations', 10)
            )
            
            crossover_rate = st.number_input(
                "Taxa de Crossover",
                min_value=0.0,
                max_value=1.0,
                value=nsga_conf.get('crossover_rate', 0.8),
                step=0.05
            )
            
            mutation_rate = st.number_input(
                "Taxa de Mutação",
                min_value=0.0,
                max_value=1.0,
                value=nsga_conf.get('mutation_rate', 0.1),
                step=0.05
            )
            
            use_three_objectives = st.checkbox(
                "Usar 3 Objetivos (cached NSGA)",
                value=nsga_conf.get('use_three_objectives', False),
                help="Otimiza [num_doors, iterations, distance] ao invés de [num_doors, distance]"
            )
        
        # ===== PARÂMETROS BRUTE FORCE =====
        st.markdown("#### 🔍 Parâmetros Força Bruta")
        bf_conf = base_data.get('bruteforce_config', {})
        
        max_doors = st.number_input(
            "Máximo de Portas (Limite de Segurança)",
            min_value=1,
            max_value=20,
            value=bf_conf.get('max_doors', 15),
            help="Força bruta é inviável para >15 portas (2^n combinações)"
        )
        
        # Botão de salvar
        st.markdown("---")
        submitted = st.form_submit_button("💾 Salvar Preset", use_container_width=True)
        
        if submitted:
            if not preset_name:
                st.error("❌ Por favor, forneça um nome para o preset!")
            else:
                # Parse scenario_seed
                try:
                    scenario_seed_str = scenario_seed_input.strip()
                    if ',' in scenario_seed_str:
                        scenario_seed = [int(x.strip()) for x in scenario_seed_str.split(',')]
                    else:
                        scenario_seed = int(scenario_seed_str)
                except:
                    st.error("❌ Formato inválido para scenario_seed")
                    scenario_seed = 42
                
                # Monta o preset
                preset_data = {
                    "preset_name": preset_name,
                    "description": description,
                    "simulation_params": {
                        "scenario_seed": scenario_seed,
                        "simulation_seed": int(simulation_seed),
                        "max_iterations": int(max_iterations),
                        "draw_mode": bool(draw_mode),
                        "verbose": bool(verbose)
                    },
                    "nsga_config": {
                        "population_size": int(population_size),
                        "generations": int(generations),
                        "crossover_rate": float(crossover_rate),
                        "mutation_rate": float(mutation_rate),
                        "use_three_objectives": bool(use_three_objectives)
                    },
                    "bruteforce_config": {
                        "max_doors": int(max_doors)
                    },
                    "created_at": datetime.now().isoformat(),
                    "version": "1.0"
                }
                
                # Gera nome de arquivo seguro
                safe_name = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in preset_name)
                safe_name = safe_name.strip().replace(' ', '_')
                filename = f"{safe_name}.json"
                
                if save_preset(preset_data, filename):
                    st.success(f"✅ Preset '{preset_name}' salvo com sucesso!")
                    st.balloons()
                    # Mostra preview
                    with st.expander("📄 Preview do Preset Salvo"):
                        st.json(preset_data)

# ===== TAB 3: DOCUMENTAÇÃO =====
with tab3:
    st.markdown("""
    ### 📖 Sobre o Sistema de Presets
    
    **O que são presets?**
    
    Presets são configurações pré-definidas que podem ser reutilizadas em diferentes simulações e algoritmos.
    Eles contêm todos os parâmetros necessários para executar otimizações de forma consistente.
    
    **Estrutura de um Preset:**
    
    Um preset unificado contém três seções principais:
    
    1. **`simulation_params`** - Parâmetros compartilhados por todos os algoritmos:
       - `scenario_seed`: Seed(s) para geração do cenário
       - `simulation_seed`: Seed para execução da simulação
       - `max_iterations`: Limite máximo de iterações
       - `draw_mode`: Se deve gerar imagens de saída
       - `verbose`: Exibir informações detalhadas
    
    2. **`nsga_config`** - Parâmetros específicos do NSGA-II:
       - `population_size`: Tamanho da população
       - `generations`: Número de gerações
       - `crossover_rate`: Taxa de cruzamento
       - `mutation_rate`: Taxa de mutação
       - `use_three_objectives`: Otimizar 3 objetivos (apenas cached NSGA)
    
    3. **`bruteforce_config`** - Parâmetros específicos da Força Bruta:
       - `max_doors`: Limite de portas para evitar explosão combinatória
    
    **Compatibilidade:**
    
    ✅ Todos os algoritmos (NSGA-II pymoo, NSGA-II cached, Força Bruta) podem usar o mesmo preset!  
    Cada algoritmo usa apenas sua seção específica + `simulation_params`.
    
    **Onde usar:**
    
    - **Página de Simulação**: Carregar presets rapidamente antes de executar
    - **Páginas de Algoritmos**: Importar configurações completas
    - **Compartilhamento**: Exportar e compartilhar configurações com outros usuários
    
    **Dicas:**
    
    - 🎯 Crie presets para diferentes cenários (teste rápido, produção, pesado)
    - 💾 Sempre dê nomes descritivos aos seus presets
    - 🔄 Use a opção "Editar preset existente" para ajustar configurações
    - 📤 Exporte presets importantes para backup
    """)

st.stop()

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
        border-bottom: 2px solid #667eea;
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

    /* ===== CARDS DE ALGORITMOS ===== */
    .algorithms-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 30px;
        margin: 2rem 0;
        padding: 0 2rem;
    }
    .algorithm-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 15px;
        padding: 2rem;
        border: 2px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        text-decoration: none;
        display: block;
        position: relative;
        overflow: hidden;
    }
    .algorithm-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.3s;
    }
    .algorithm-card:hover::before {
        opacity: 1;
    }
    .algorithm-card:hover {
        transform: translateY(-10px);
        border-color: #667eea;
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.5);
    }
    .algorithm-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    .algorithm-title {
        color: #667eea;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .algorithm-desc {
        color: #aaa;
        font-size: 0.95rem;
        text-align: center;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# ===== MENU SUPERIOR =====
st.markdown("""
    <div class="menu">
        <a href="/">Menu</a>
        <a href="/Mapas">Mapas</a>
        <a href="/Criação_de_Mapas">Criação de Mapas</a>
        <a class="active" href="/Parâmetros">Parâmetros</a>
        <a href="/Simulação">Simulação</a>
        <a href="/Resultados">Resultados</a>
        <a href="/Documentação">Documentação</a>
    </div>
""", unsafe_allow_html=True)

# ===== CABEÇALHO DA PÁGINA =====
st.markdown("""
    <div class="page-header">
        <h1>⚙️ Parametrização de Algoritmos</h1>
        <p>Configure os parâmetros dos algoritmos de otimização para suas simulações</p>
    </div>
""", unsafe_allow_html=True)

# ===== CARDS DE ALGORITMOS =====
st.markdown("## 🧬 Algoritmos Disponíveis")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 15px; border: 2px solid rgba(102, 126, 234, 0.3);">
        <div style="font-size: 3rem;">💾</div>
        <h3 style="color: #667eea; margin: 1rem 0 0.5rem 0;">NSGA-II com Cache</h3>
        <p style="color: #aaa; font-size: 0.9rem; line-height: 1.5;">Algoritmo genético multiobjetivo otimizado com cache para melhor desempenho</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Configurar", key="btn_nsga_cache", use_container_width=True):
        st.switch_page("pages/Algoritmo_Genetico.py")

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 15px; border: 2px solid rgba(102, 126, 234, 0.3);">
        <div style="font-size: 3rem;">🎯</div>
        <h3 style="color: #667eea; margin: 1rem 0 0.5rem 0;">NSGA-II</h3>
        <p style="color: #aaa; font-size: 0.9rem; line-height: 1.5;">Algoritmo genético multiobjetivo com ordenação não-dominada e preservação de diversidade</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Configurar", key="btn_nsga", use_container_width=True):
        st.switch_page("pages/NSGA_II.py")

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 15px; border: 2px solid rgba(102, 126, 234, 0.3);">
        <div style="font-size: 3rem;">🔍</div>
        <h3 style="color: #667eea; margin: 1rem 0 0.5rem 0;">Força Bruta</h3>
        <p style="color: #aaa; font-size: 0.9rem; line-height: 1.5;">Busca exaustiva que avalia todas as combinações possíveis para garantir a solução ótima</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Configurar", key="btn_bruta", use_container_width=True):
        st.switch_page("pages/Forca_Bruta.py")

# Evita que Streamlit coloque rodapé padrão
st.stop()
