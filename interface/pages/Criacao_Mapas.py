# pages/Criacao_Mapas.py
"""
Página de criação e conversão de mapas para simulação de evacuação.

Este módulo permite aos usuários:
- Acessar o editor Tkinter nativo para criação de mapas
- Converter imagens PNG existentes em arquivos .map
- Visualizar e gerenciar mapas criados
- Integrar com o sistema de simulação existente
"""
import streamlit as st
import numpy as np
from PIL import Image
import io
import base64
from pathlib import Path
import sys
import os
import time

# Adicionar serviços ao path
current_dir = Path(__file__).parent
services_dir = current_dir.parent / "services"
sys.path.append(str(services_dir))

try:
    from tkinter_map_editor_integration import tkinter_map_editor_service
except ImportError as e:
    st.error(f"Erro ao importar serviço de editor Tkinter: {e}")
    st.stop()

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(page_title="Criação de Mapas", layout="wide")

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
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(26, 26, 46, 0.3);
        border-radius: 8px;
        padding: 10px 20px;
        color: #aaa;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* ===== CARDS E SEÇÕES ===== */
    .map-editor {
        background: rgba(26, 26, 46, 0.2);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .color-legend {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 12px;
        margin: 15px 0;
        padding: 15px;
        background: rgba(26, 26, 46, 0.3);
        border-radius: 8px;
    }
    
    .color-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px;
        background: rgba(0,0,0,0.2);
        border-radius: 6px;
    }
    
    .color-box {
        width: 24px;
        height: 24px;
        border: 2px solid #667eea;
        border-radius: 4px;
    }
    
    /* ===== EXPANDERS ===== */
    .streamlit-expanderHeader {
        background-color: rgba(26, 26, 46, 0.4) !important;
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ===== MENU SUPERIOR =====
st.markdown("""
    <div class="menu">
        <a href="/">Menu</a>
        <a href="/Mapas">Mapas</a>
        <a class="active" href="/Criação_de_Mapas">Criação de Mapas</a>
        <a href="/Parâmetros">Parâmetros</a>
        <a href="/Simulação">Simulação</a>
        <a href="/Resultados">Resultados</a>
        <a href="/Documentação">Documentação</a>
    </div>
""", unsafe_allow_html=True)

# ===== CABEÇALHO DA PÁGINA =====
st.markdown("""
    <div class="page-header">
        <h1>🎨 Criação de Mapas</h1>
        <p>Crie mapas personalizados usando o editor gráfico ou converta imagens existentes</p>
    </div>
""", unsafe_allow_html=True)

# ================= CONFIGURAÇÕES INICIAIS =================
# Obter esquema de cores do serviço
COLORS = tkinter_map_editor_service.get_color_scheme()

# ================= FUNÇÕES AUXILIARES =================
def download_file(data, filename, mime_type):
    """Cria um link de download para o Streamlit"""
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:{mime_type};base64,{b64}" download="{filename}">📥 Baixar {filename}</a>'
    return href

def refresh_map_list():
    """Atualiza a lista de mapas na sessão"""
    st.session_state.map_list = tkinter_map_editor_service.get_recent_maps()

# ================= INTERFACE PRINCIPAL =================
st.write("""
Crie mapas personalizados para suas simulações de evacuação usando o editor gráfico nativo 
ou converta imagens PNG existentes em arquivos de mapa compatíveis com o simulador.
""")

# ================= ABA 1: EDITOR TKINTER =================
tab1, tab2, tab3 = st.tabs(["🎨 Editor Gráfico", "🔄 Conversor de Imagens", "📁 Gerenciar Mapas"])

with tab1:
    st.markdown('<div class="map-editor">', unsafe_allow_html=True)
    
    st.markdown("### 🎨 Editor de Mapas Gráfico")
    st.write("""
    Use o editor gráfico nativo para criar mapas com interface intuitiva e funcionalidades avançadas.
    O editor será aberto em uma janela separada.
    """)
    
    # Configurações do mapa
    col1, col2, col3 = st.columns(3)
    with col1:
        width_px = st.number_input("Largura (px)", min_value=5, max_value=200, value=20, help="Largura do mapa em pixels (colunas)")
    with col2:
        height_px = st.number_input("Altura (px)", min_value=5, max_value=200, value=20, help="Altura do mapa em pixels (linhas)")
    with col3:
        cell_size = st.number_input("Tamanho do pixel", min_value=10, max_value=50, value=25, help="Tamanho visual de cada pixel")
    
    st.markdown("---")
    
    # Mostrar esquema de cores
    st.markdown("#### 🎨 Esquema de Cores Suportado")
    
    cols = st.columns(len(COLORS))
    for idx, (name, (rgb, hex_color, code)) in enumerate(COLORS.items()):
        with cols[idx]:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: rgba(26, 26, 46, 0.3); border-radius: 8px;">
                <div style="width: 40px; height: 40px; background-color: {hex_color}; border: 2px solid #667eea; border-radius: 6px; margin: 0 auto 0.5rem;"></div>
                <p style="color: #667eea; font-weight: 600; margin: 0.25rem 0;">{name}</p>
                <p style="color: #aaa; font-size: 0.8rem; margin: 0;">RGB: {rgb}</p>
                <p style="color: #aaa; font-size: 0.8rem; margin: 0;">Código: {code}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Botões de ação
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Abrir Editor Gráfico", help="Abre o editor Tkinter com as configurações acima", use_container_width=True):
            with st.spinner("Abrindo editor gráfico..."):
                success = tkinter_map_editor_service.launch_tkinter_editor(width_px, height_px, cell_size)
                if success:
                    st.success("✅ Editor gráfico aberto! Crie seu mapa e salve no sistema.")
                    st.info("💡 **Dica:** Use o botão 'Salvar no Sistema' no editor para salvar o mapa diretamente no sistema.")
                else:
                    st.error("❌ Erro ao abrir editor gráfico. Verifique se o Tkinter está disponível.")
    
    with col2:
        if st.button("🎯 Editor Padrão (20x20)", help="Abre o editor com configuração padrão", use_container_width=True):
            with st.spinner("Abrindo editor padrão..."):
                success = tkinter_map_editor_service.launch_simple_editor()
                if success:
                    st.success("✅ Editor padrão aberto!")
                else:
                    st.error("❌ Erro ao abrir editor padrão.")
    
    # Status do editor
    status = tkinter_map_editor_service.check_editor_status()
    if status["running"]:
        st.info(f"🟢 **Status:** {status['message']}")
    else:
        st.info(f"🔴 **Status:** {status['message']}")
    
    # Informações sobre o editor
    with st.expander("ℹ️ Sobre o Editor Gráfico"):
        st.markdown("""
        **Funcionalidades do Editor Tkinter:**
        
        - **Interface gráfica nativa**: Editor pixel art com interface intuitiva
        - **Seleção de cores**: Botões para escolher tipos de terreno
        - **Desenho livre**: Clique e arraste para pintar pixels
        - **Templates**: Mapas pré-configurados (sala, corredor, vazio)
        - **Salvamento automático**: Salva diretamente no sistema
        - **Conversão automática**: Gera arquivos .map automaticamente
        - **Carregamento**: Abra mapas PNG existentes para edição
        
        **Como usar:**
        1. Clique em "Abrir Editor Gráfico" ou "Editor Padrão"
        2. Configure o mapa conforme necessário
        3. Use os botões de cor para selecionar o tipo de terreno
        4. Clique nos pixels para pintar
        5. Use "Salvar no Sistema" para salvar o mapa
        6. O mapa ficará disponível na aba "Gerenciar Mapas"
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ================= ABA 2: CONVERSOR DE IMAGENS =================
with tab2:
    st.markdown('<div class="map-editor">', unsafe_allow_html=True)
    
    st.markdown("### 🔄 Conversor de Imagens PNG")
    st.write("""
    Converta imagens PNG existentes em arquivos de mapa compatíveis com o simulador.
    A imagem deve seguir o esquema de cores padrão:
    """)
    
    # Mostrar esquema de cores
    st.markdown("#### 🎨 Esquema de Cores Suportado:")
    for name, (rgb, hex_color, code) in COLORS.items():
        st.markdown(f"**{name}** (RGB: {rgb}) → Código: `{code}`")
    
    # Upload de arquivo
    uploaded_file = st.file_uploader("Selecione uma imagem PNG", type=['png'], help="A imagem deve seguir o esquema de cores acima")
    
    if uploaded_file is not None:
        try:
            # Carregar imagem
            img = Image.open(uploaded_file)
            st.image(img, caption="Imagem carregada", use_column_width=True)
            
            # Mostrar informações da imagem
            st.info(f"**Dimensões:** {img.size[0]} x {img.size[1]} pixels")
            
            # Nome do arquivo de saída
            output_name = st.text_input("Nome do mapa (sem extensão)", value=uploaded_file.name.rsplit('.', 1)[0])
            
            # Botão de conversão
            if st.button("🔄 Converter Imagem", help="Converte a imagem em arquivos .map"):
                with st.spinner("Convertendo imagem..."):
                    try:
                        # Salvar temporariamente
                        temp_png = f"temp_{uploaded_file.name}"
                        img.save(temp_png)
                        
                        # Converter usando o serviço
                        generated_files = tkinter_map_editor_service.convert_existing_image(temp_png, output_name)
                        
                        st.success("✅ Conversão concluída!")
                        
                        # Download dos arquivos gerados
                        st.markdown('<div class="download-section">', unsafe_allow_html=True)
                        st.markdown("### 📥 Arquivos Gerados:")
                        
                        file_names = {
                            "main": f"{output_name}.map",
                            "fire": f"{output_name}_fogo.map",
                            "wind": f"{output_name}_vento.map",
                            "png": f"{output_name}.png"
                        }
                        
                        for key, filename in file_names.items():
                            if key in generated_files:
                                if key == "png":
                                    # Para PNG, mostrar imagem
                                    st.image(generated_files[key], caption=filename, width=300)
                                else:
                                    # Para arquivos .map, criar download
                                    with open(generated_files[key], 'r') as f:
                                        content = f.read()
                                    st.markdown(download_file(content.encode(), filename, "text/plain"), unsafe_allow_html=True)
                        
                        os.remove(temp_png)  # Limpar PNG temporário
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"Erro na conversão: {e}")
                        
        except Exception as e:
            st.error(f"Erro ao carregar imagem: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ================= ABA 3: GERENCIAR MAPAS =================
with tab3:
    st.markdown('<div class="map-editor">', unsafe_allow_html=True)
    
    st.markdown("### 📁 Gerenciar Mapas Criados")
    st.write("Visualize, baixe e gerencie os mapas criados no sistema.")
    
    # Botão para atualizar lista
    if st.button("🔄 Atualizar Lista"):
        refresh_map_list()
        st.rerun()
    
    # Obter lista de mapas
    if 'map_list' not in st.session_state:
        refresh_map_list()
    
    map_list = st.session_state.get('map_list', [])
    
    if not map_list:
        st.info("📭 Nenhum mapa encontrado. Crie um mapa usando o editor gráfico ou converta uma imagem.")
    else:
        st.markdown(f"**Total de mapas:** {len(map_list)}")
        
        # Mostrar mapas em cards
        for i, map_path in enumerate(map_list):
            with st.expander(f"🗺️ {map_path.stem}", expanded=False):
                try:
                    # Obter informações do mapa
                    map_info = tkinter_map_editor_service.get_map_info(map_path)
                    
                    if "error" in map_info:
                        st.error(map_info["error"])
                        continue
                    
                    # Mostrar informações
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Nome:** {map_info['name']}")
                        st.markdown(f"**Dimensões:** {map_info['size'][0]} x {map_info['size'][1]} pixels")
                        st.markdown(f"**Modificado:** {map_info['modified']}")
                    
                    with col2:
                        # Mostrar imagem
                        img = Image.open(map_path)
                        st.image(img, caption=f"Preview: {map_info['name']}", width=200)
                    
                    # Botões de ação
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        # Download PNG
                        with open(map_path, 'rb') as f:
                            png_data = f.read()
                        st.markdown(download_file(png_data, f"{map_info['name']}.png", "image/png"), unsafe_allow_html=True)
                    
                    with col2:
                        # Download arquivos .map
                        base_name = map_info['name']
                        map_files = {
                            "main": f"{base_name}.map",
                            "fire": f"{base_name}_fogo.map",
                            "wind": f"{base_name}_vento.map"
                        }
                        
                        for key, filename in map_files.items():
                            map_file_path = map_path.parent / filename
                            if map_file_path.exists():
                                with open(map_file_path, 'r') as f:
                                    content = f.read()
                                st.markdown(download_file(content.encode(), filename, "text/plain"), unsafe_allow_html=True)
                    
                    with col3:
                        # Botão para abrir no editor
                        if st.button(f"✏️ Editar", key=f"edit_{i}"):
                            st.info("💡 Use o editor gráfico para editar este mapa. Carregue o arquivo PNG no editor.")
                    
                    with col4:
                        # Botão para remover
                        if st.button(f"🗑️ Remover", key=f"remove_{i}"):
                            if tkinter_map_editor_service.delete_map(map_info['name']):
                                st.success(f"✅ Mapa {map_info['name']} removido!")
                                refresh_map_list()
                                st.rerun()
                            else:
                                st.error(f"❌ Erro ao remover mapa {map_info['name']}")
                
                except Exception as e:
                    st.error(f"Erro ao processar mapa {map_path.name}: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ================= INFORMAÇÕES ADICIONAIS =================
st.markdown("---")
st.markdown("### 📚 Informações Importantes")

with st.expander("🎨 Guia de Cores"):
    st.markdown("""
    **Esquema de cores para mapas de evacuação:**
    
    - **Parede (Preto)**: Obstáculos intransponíveis
    - **Espaço vazio (Branco)**: Áreas onde pessoas podem caminhar
    - **Tapete/Caminho (Laranja)**: Caminhos preferenciais ou áreas especiais
    - **Porta/Saída (Vermelho)**: Saídas de emergência
    - **Inocupável (Prata)**: Áreas que não podem ser ocupadas
    
    **Dicas:**
    - Use paredes para definir limites e obstáculos
    - Coloque portas/saídas estrategicamente
    - Mantenha caminhos livres entre saídas e áreas ocupadas
    """)

with st.expander("📁 Formatos de Arquivo"):
    st.markdown("""
    **Arquivos gerados:**
    
    - **`.map`**: Mapa principal com códigos de terreno
    - **`_fogo.map`**: Mapa de propagação de fogo
    - **`_vento.map`**: Mapa de direção do vento
    
    **Compatibilidade:**
    - Todos os arquivos são compatíveis com o simulador de evacuação
    - Podem ser usados diretamente nas simulações
    - Formatos de texto simples, editáveis manualmente se necessário
    """)

with st.expander("🔧 Dicas de Uso"):
    st.markdown("""
    **Para melhores resultados:**
    
    1. **Tamanho adequado**: Mapas muito pequenos podem limitar a simulação
    2. **Múltiplas saídas**: Sempre inclua várias portas/saídas
    3. **Caminhos claros**: Evite labirintos complexos desnecessários
    4. **Teste antes**: Valide o mapa com uma simulação simples
    
    **Workflow recomendado:**
    1. Use o editor gráfico para criar o mapa
    2. Salve no sistema usando "Salvar no Sistema"
    3. Gerencie mapas na aba "Gerenciar Mapas"
    4. Teste em uma simulação
    5. Ajuste conforme necessário
    """)

with st.expander("🖥️ Sobre o Editor Tkinter"):
    st.markdown("""
    **Vantagens do Editor Gráfico:**
    
    - **Interface nativa**: Editor pixel art com interface intuitiva e responsiva
    - **Funcionalidades avançadas**: Desenho livre, templates, carregamento de mapas
    - **Salvamento integrado**: Salva diretamente no sistema de mapas
    - **Conversão automática**: Gera arquivos .map automaticamente
    - **Compatibilidade total**: Mantém todos os formatos e códigos originais
    
    **Requisitos:**
    - Sistema com suporte a Tkinter (incluído no Python padrão)
    - Interface gráfica disponível
    - Permissões para criar processos
    
    **Nota:** O editor abre em uma janela separada. Se não conseguir abrir, 
    use o conversor de imagens como alternativa.
    """)

st.stop()
