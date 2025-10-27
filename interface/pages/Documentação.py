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
    2. Defina as dimensões
    3. Use o editor de pixels para personalizar
    4. Salve o mapa com um nome descritivo
    
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
        | 🟥 Vermelho | (255,0,0) | **Porta/Saída** - Saída |
        | ⬜ Cinza | (192,192,192) | **Inocupável** - Não pode ter pedestres |
        """)
    
    with col2:
        st.markdown("""
        ### Dimensões Recomendadas
        
        - **Mínimo**: 5x5 pixels
        - **Ideal**: 15x15 a 50x50 pixels
        
        ### Boas Práticas
        
        ✅ **Faça**:
        - Use múltiplas saídas (2-6)
        - Distribua saídas uniformemente
        - Deixe espaço para circulação
        - Teste com poucos indivíduos primeiro
        
        ❌ **Evite**:
        - Mapas muito grandes (lentidão)
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
    
        ### Explicação dos pesos (KD, KS, KW, KI)

        Estes parâmetros controlam como cada indivíduo reage a forças modeladas na simulação (modelo de "força social"). Abaixo uma explicação em linguagem simples e dicas práticas:

        - KD — Força de direção/propulsão (driving force)
            - O quanto o indivíduo se esforça para seguir seu objetivo (ir até a saída).
            - Valores maiores → movimento mais determinado em direção à saída (pessoa "empurrando" na direção do objetivo).
            - Faixa sugerida: 0.0 — 5.0. Exemplo: 0.5 = passivo, 2.0 = determinado.

        - KS — Força social (repulsão entre pessoas)
            - Controla quanto o indivíduo evita colisões com outras pessoas.
            - Valores maiores → mantém mais distância, evita aglomerações.
            - Faixa sugerida: 0.0 — 5.0. Exemplo: 0.2 = pouco evasivo, 1.5 = evita fortemente contato.

        - KW — Força de parede/obstáculo (repulsão de objetos)
            - Determina o quanto o indivíduo evita paredes e obstáculos.
            - Valores maiores → mantém-se mais afastado de paredes/colunas.
            - Faixa sugerida: 0.0 — 5.0. Exemplo: 0.5 = aproxima-se de paredes, 2.0 = evita paredes.

        - KI — Peso de interações internas / inércia / coesão (termo adicional de interação)
            - Usado pelo modelo para efeitos extra (por exemplo, coesão de pequenos grupos, inércia ou componentes de ruído). A interpretação exata pode variar conforme a implementação.
            - Valores maiores → aumentam a influência dessas interações adicionais.
            - Faixa sugerida: 0.0 — 2.0. Exemplo: 0.0 = desativado, 0.5 — leve efeito de coesão.
    
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
    - ✅ Mapas médios a grandes
    - ✅ Quando quer explorar trade-offs
    
    **Objetivos Otimizados**:
    1. **Minimizar portas**: Menos saídas = menor custo
    2. **Minimizar distância total**: Caminhos mais curtos
    3. **Minimizar tempo**: Evacuação mais rápida
    
    **Parâmetros**:
    - **População**
    - **Gerações**
    - **Taxa de Crossover**
    - **Taxa de Mutação**
    
    ---
    
    ### NSGA-II com Cache
    
    **Descrição**: Versão otimizada que armazena resultados de simulações idênticas.
    
    **Quando usar**:
    - ✅ Múltiplas execuções
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
    
    ### Exportando Resultados
    
    Os resultados são salvos automaticamente em:
    - **Banco de dados**: Para consulta na interface
    - **Arquivos JSON**: `uploads/nsga_ii/results_*.json`
    - **Imagens** (se draw_mode ativado): `simulador_heuristica/output/<experiment>/`
    
    Você pode:
    - 📥 Baixar JSONs para análise externa
    - 🔄 Reexecutar simulações com mesmos parâmetros
    """)

st.markdown("---")
st.markdown("""
### 📞 Suporte e Recursos Adicionais

- 📖 **Documentação Técnica Completa**: Veja a pasta `docs/` no repositório
- 🔧 **API Reference**: `docs/API_REFERENCE.md`
- 🔧 **Developer Guide**: `docs/DEVELOPMENT.md`
- 🏗️ **Arquitetura**: `docs/ARCHITECTURE.md`

---

**Desenvolvido com ❤️ para simulações de evacuação eficientes e seguras.**
""")

st.stop()







