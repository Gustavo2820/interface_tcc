# pages/Documentação.py
"""
Página de documentação do sistema de simulação de evacuação.

Este módulo fornece acesso à documentação técnica, guias de uso
e informações sobre o sistema.
"""
import streamlit as st

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(page_title="Documentação", layout="wide")

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
    
    /* ===== EXPANDERS ===== */
    .streamlit-expanderHeader {
        background-color: rgba(26, 26, 46, 0.4) !important;
        border-radius: 8px;
        font-weight: 600;
        color: #667eea !important;
    }
    
    /* ===== CODE BLOCKS ===== */
    code {
        background-color: rgba(26, 26, 46, 0.5);
        padding: 2px 6px;
        border-radius: 4px;
        color: #667eea;
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
        <a href="/Simulação">Simulação</a>
        <a href="/Resultados">Resultados</a>
        <a class="active" href="/Documentação">Documentação</a>
    </div>
""", unsafe_allow_html=True)

# ===== CABEÇALHO DA PÁGINA =====
st.markdown("""
    <div class="page-header">
        <h1>📚 Documentação</h1>
        <p>Guias, referências e exemplos para usar o sistema de simulação de evacuação</p>
    </div>
""", unsafe_allow_html=True)

# ================= CONTEÚDO =================
st.markdown("""
### 🚀 Bem-vindo ao Sistema de Simulação de Evacuação

Este sistema permite simular e otimizar processos de evacuação usando diferentes algoritmos de inteligência artificial.
""")

# Seções de documentação
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎯 Início Rápido", "�️ Mapas", "⚙️ Simulação", "🧬 Algoritmos", "📊 Resultados"])

with tab1:
    st.markdown("## 🎯 Guia de Início Rápido")
    
    st.markdown("""
    ### Passo 1: Crie ou Selecione um Mapa
    
    **Opção A: Criar Novo Mapa**
    1. Acesse `Criação de Mapas` no menu
    2. Defina as dimensões (recomendado: 15x15 a 30x30)
    3. Escolha um template inicial:
       - **Vazio**: Canvas em branco
       - **Sala**: Sala com paredes externas
       - **Corredor**: Corredor simples
    4. Use o editor de pixels para personalizar
    5. Salve o mapa com um nome descritivo
    
    **Opção B: Converter Imagem PNG**
    1. Crie uma imagem PNG com o esquema de cores
    2. Use a aba `Conversor de Imagens`
    3. Faça upload e converta
    
    ---
    
    ### Passo 2: Configure os Parâmetros
    
    1. Acesse `Parâmetros` no menu
    2. Na aba `Criar Novo Preset`:
       - **Nome**: Escolha um nome descritivo (ex: "Teste_Rapido")
       - **Descrição**: Descreva o propósito do preset
       - **Algoritmo**: Configure parâmetros específicos
       - **Simulação**: Defina seeds e iterações
    3. Clique em `💾 Salvar Preset`
    
    **Presets Incluídos:**
    - `Teste_Rapido`: Para testes rápidos (pop:10, gen:5)
    - `Producao_Media`: Balanceado (pop:20, gen:10)
    - `Pesquisa_Pesada`: Intensivo (pop:50, gen:50)
    
    ---
    
    ### Passo 3: Execute a Simulação
    
    1. Acesse `Simulação` no menu
    2. Selecione o mapa desejado
    3. Escolha o algoritmo:
       - **NSGA-II**: Otimização multi-objetivo com pymoo
       - **NSGA-II com Cache**: Versão otimizada com cache
       - **Força Bruta**: Busca exaustiva (mapas pequenos)
    4. Carregue um preset (opcional)
    5. Configure ou edite indivíduos
    6. Clique em `▶️ EXECUTAR SIMULAÇÃO` (topo da página)
    
    ---
    
    ### Passo 4: Analise os Resultados
    
    1. Acesse `Resultados` no menu
    2. Selecione a simulação na lista
    3. Visualize:
       - **Métricas**: Iterações, distância, tempo
       - **Gráficos**: Fronteira de Pareto, evolução
       - **Comparações**: Diferentes soluções
    """)
    
    st.success("💡 **Dica**: Comece com o preset `Teste_Rapido` para se familiarizar com o sistema!")

with tab2:
    st.markdown("## 🗺️ Trabalhando com Mapas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Esquema de Cores (PNG)
        
        | Cor | RGB | Significado |
        |-----|-----|-------------|
        | ⬛ Preto | (0,0,0) | **Parede** - Obstáculo sólido |
        | ⬜ Branco | (255,255,255) | **Espaço Vazio** - Área caminhável |
        | 🟧 Laranja | (255,165,0) | **Tapete** - Caminho preferencial |
        | 🟥 Vermelho | (255,0,0) | **Porta/Saída** - Saída de emergência |
        | 🟩 Verde | (0,255,0) | **Janela** - Saída alternativa |
        | ⬜ Cinza | (192,192,192) | **Inocupável** - Não pode ter pedestres |
        
        ### Códigos do Mapa (.map)
        
        | Código | Terreno |
        |--------|---------|
        | 0 | Parede |
        | 1 | Espaço vazio |
        | 2 | Porta/Saída |
        | 3 | Tapete |
        | 4 | Janela |
        | 5 | Inocupável |
        """)
    
    with col2:
        st.markdown("""
        ### Dimensões Recomendadas
        
        - **Mínimo**: 5x5 pixels
        - **Máximo**: 100x100 pixels
        - **Ideal**: 15x15 a 30x30 pixels
        
        ### Boas Práticas
        
        ✅ **Faça**:
        - Use múltiplas saídas (2-6)
        - Distribua saídas uniformemente
        - Deixe espaço para circulação
        - Teste com poucos indivíduos primeiro
        
        ❌ **Evite**:
        - Mapas muito grandes (lentidão)
        - Apenas 1 saída (gargalo)
        - Corredores muito estreitos
        - Cores fora do esquema padrão
        
        ### Arquivos Gerados
        
        Ao converter/salvar, você recebe:
        - `mapa.map`: Mapa principal
        - `mapa_fogo.map`: Propagação de fogo
        - `mapa_vento.map`: Direção do vento
        - `mapa.png`: Visualização
        """)
    
    st.markdown("---")
    st.info("💡 **Exemplo Prático**: Uma sala 20x20 com 4 portas nas paredes e espaço central vazio é um bom ponto de partida.")

with tab3:
    st.markdown("## ⚙️ Configurando Simulações")
    
    st.markdown("""
    ### Parâmetros de Simulação
    
    #### Seeds
    - **Scenario Seed**: Controla a geração do cenário
      - Use o mesmo seed para cenários reproduzíveis
      - Liste múltiplos seeds (ex: `1,2,3`) para testar variações
    
    - **Simulation Seed**: Controla a execução da simulação
      - Mantém consistência entre execuções
    
    #### Iterações Máximas
    - **Padrão**: 1200 iterações
    - **Mínimo**: 100 (testes rápidos)
    - **Máximo**: 10000 (simulações longas)
    - Afeta o tempo limite de evacuação
    
    #### Modo de Desenho
    - ✅ **Ativado**: Gera imagens frame-by-frame (útil para análise visual)
    - ⬜ **Desativado**: Mais rápido, sem visualização
    
    #### Modo Verboso
    - ✅ **Ativado**: Logs detalhados no console
    - ⬜ **Desativado**: Apenas informações essenciais
    
    ---
    
    ### Indivíduos (Pedestres)
    
    Você pode definir indivíduos de duas formas:
    
    #### 1. Editor de Tipos (Recomendado)
    - Crie "tipos" de indivíduos com características comuns
    - Defina quantidade de cada tipo
    - Sistema expande automaticamente
    
    **Parâmetros por tipo**:
    - **Label**: Nome do tipo (ex: "Adulto", "Idoso")
    - **Quantidade**: Número de indivíduos deste tipo
    - **Cor (RGB)**: Visualização na simulação
    - **Velocidade**: 1-10 (afeta movimento)
    - **KD, KS, KW, KI**: Pesos do modelo de força social
    
    #### 2. JSON Manual
    ```json
    [
      {
        "label": "Adulto",
        "color": [255, 0, 0],
        "speed": 1,
        "KD": 1.0,
        "KS": 1.0,
        "KW": 1.0,
        "KI": 0.5,
        "row": 0,
        "col": 0
      }
    ]
    ```
    
    ---
    
    ### Salvando Configurações
    
    Use o formulário `Criar/Editar Configuração Unificada` para:
    1. Ajustar parâmetros do algoritmo e simulação
    2. Salvar como arquivo JSON
    3. Reutilizar em futuras simulações
    
    O arquivo salvo pode ser carregado como preset na página `Parâmetros`.
    """)

with tab4:
    st.markdown("## 🧬 Algoritmos de Otimização")
    
    st.markdown("""
    ### NSGA-II (Pymoo)
    
    **Descrição**: Algoritmo genético multi-objetivo usando a biblioteca pymoo.
    
    **Quando usar**:
    - ✅ Primeira execução com um mapa
    - ✅ Mapas médios a grandes
    - ✅ Quando quer explorar trade-offs
    
    **Objetivos Otimizados** (sempre 3):
    1. **Minimizar portas**: Menos saídas = menor custo
    2. **Minimizar distância total**: Caminhos mais curtos
    3. **Minimizar tempo**: Evacuação mais rápida
    
    **Parâmetros**:
    - **População**: 10-50 (recomendado: 20)
    - **Gerações**: 5-100 (recomendado: 10-20)
    - **Taxa de Crossover**: 0.7-0.9 (padrão: 0.8)
    - **Taxa de Mutação**: 0.05-0.2 (padrão: 0.1)
    
    ---
    
    ### NSGA-II com Cache
    
    **Descrição**: Versão otimizada que armazena resultados de simulações idênticas.
    
    **Quando usar**:
    - ✅ Múltiplas execuções com mesmo mapa
    - ✅ Quando quer economizar tempo
    - ✅ Simulações com muitas gerações
    
    **Vantagens**:
    - 🚀 Muito mais rápido em execuções subsequentes
    - 💾 Reutiliza cálculos já feitos
    - 📊 Mesmos resultados que NSGA-II padrão
    
    **Mesmos parâmetros do NSGA-II**.
    
    ---
    
    ### Força Bruta
    
    **Descrição**: Testa **todas** as combinações possíveis de portas.
    
    **Quando usar**:
    - ✅ Mapas pequenos (< 10 portas)
    - ✅ Quando quer garantir solução ótima global
    - ✅ Validação de outros algoritmos
    
    ⚠️ **Atenção**:
    - Com 10 portas = 1.024 combinações
    - Com 15 portas = 32.768 combinações
    - Com 20 portas = 1.048.576 combinações (muito lento!)
    
    **Parâmetros**:
    - **Max Doors**: Limite de portas a considerar (recomendado: ≤15)
    
    ---
    
    ### Comparação Rápida
    
    | Algoritmo | Velocidade | Precisão | Mapas Ideais | Cache |
    |-----------|-----------|----------|--------------|-------|
    | NSGA-II | ⭐⭐⭐ | ⭐⭐⭐⭐ | Médios/Grandes | ❌ |
    | NSGA-II Cache | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Médios/Grandes | ✅ |
    | Força Bruta | ⭐ | ⭐⭐⭐⭐⭐ | Pequenos | ❌ |
    
    """)

with tab5:
    st.markdown("## 📊 Interpretando Resultados")
    
    st.markdown("""
    ### Métricas Principais
    
    #### 🚪 Número de Portas
    - **Menor é melhor**: Menos portas = menor custo de construção
    - Mas: Muito poucas portas podem causar congestionamento
    
    #### 📏 Distância Total Percorrida
    - **Menor é melhor**: Pedestres percorrem menos
    - Indica eficiência dos caminhos até as saídas
    
    #### ⏱️ Tempo de Evacuação (Iterações)
    - **Menor é melhor**: Evacuação mais rápida
    - Relacionado ao tempo real de evacuação
    
    ---
    
    ### Fronteira de Pareto
    
    **O que é?**
    - Conjunto de soluções ótimas onde não é possível melhorar um objetivo sem piorar outro
    - Representa os melhores trade-offs possíveis
    
    **Como interpretar?**
    - Cada ponto = uma configuração diferente de portas
    - **Soluções dominadas**: Existem outras melhores em todos os objetivos
    - **Soluções não-dominadas**: Fazem parte da fronteira de Pareto
    
    **Escolhendo uma solução**:
    - ✅ Mais portas, evacuação rápida → Prioriza segurança
    - ✅ Menos portas, tempo aceitável → Prioriza custo
    - ✅ Meio-termo → Equilíbrio
    
    ---
    
    ### Gráficos Comuns
    
    #### 1. Scatter Plot (Fronteira de Pareto)
    - **Eixo X**: Geralmente distância ou tempo
    - **Eixo Y**: Número de portas
    - **Pontos azuis**: Soluções da fronteira
    - **Pontos vermelhos**: Soluções dominadas
    
    #### 2. Gráfico de Evolução
    - Mostra como as métricas melhoram ao longo das gerações
    - Convergência indica que o algoritmo encontrou boas soluções
    
    #### 3. Heatmap de Uso
    - Mostra quais portas são mais utilizadas
    - Útil para identificar gargalos
    
    ---
    
    ### Exportando Resultados
    
    Os resultados são salvos automaticamente em:
    - **Banco de dados**: Para consulta na interface
    - **Arquivos JSON**: `uploads/nsga_ii/results_*.json`
    - **Imagens** (se draw_mode ativado): `simulador_heuristica/output/<experiment>/`
    
    Você pode:
    - 📥 Baixar JSONs para análise externa
    - 📊 Gerar gráficos personalizados
    - 🔄 Reexecutar simulações com mesmos parâmetros
    """)

st.markdown("---")
st.markdown("""
### 📞 Suporte e Recursos Adicionais

- 📖 **Documentação Técnica Completa**: Veja a pasta `docs/` no repositório
- 🔧 **API Reference**: `docs/API_REFERENCE.md`
- 🏗️ **Arquitetura**: `docs/ARCHITECTURE.md`
- ❓ **FAQ**: `docs/INDEX.md`

---

**Desenvolvido com ❤️ para simulações de evacuação eficientes e seguras.**
""")

st.stop()







