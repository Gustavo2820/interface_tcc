# Guia do Usuário

Guia completo para utilização da interface web do Sistema de Simulação e Otimização de Evacuação de Multidões.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Navegação](#navegação)
- [Criação de Mapas](#criação-de-mapas)
- [Configuração de Parâmetros](#configuração-de-parâmetros)
- [Execução de Simulações](#execução-de-simulações)
- [Análise de Resultados](#análise-de-resultados)
- [Gestão de Dados](#gestão-de-dados)

## 🌟 Visão Geral

A interface web permite:
- Criar e gerenciar mapas de evacuação
- Configurar parâmetros de simulação e otimização
- Executar simulações diretas ou otimizações multiobjetivo
- Analisar resultados e comparar soluções
- Exportar e armazenar dados

## 🧭 Navegação

### Menu Principal

**Mapas** - Criação e gerenciamento de mapas  
**Parâmetros** - Configuração de algoritmos e simulação  
**Simulação** - Execução de simulações e otimizações  
**Resultados** - Análise de resultados executados  

## 🗺️ Criação de Mapas

### Editor Visual de Mapas

1. **Acessar Editor**
   - Vá para página "Mapas"
   - Clique em "Criar Novo Mapa"

2. **Configurar Dimensões**
   - Largura: 5-100 células
   - Altura: 5-100 células
   - Tamanho padrão recomendado: 20x20

3. **Desenhar Mapa**
   - **Branco**: Células vazias (navegáveis)
   - **Preto**: Paredes (bloqueiam movimento)
   - **Vermelho**: Portas (saídas de evacuação)
   - **Laranja**: Caminhos (preferência de locomoção)

4. **Ferramentas**
   - **Pincel**: Desenha células individuais
   - **Borracha**: Remove células (basta pintar por cima com espaço vazio)

5. **Salvar Mapa**
   - Dê um nome descritivo
   - Clique em "Salvar Mapa"
   - Mapa ficará disponível para uso

### Importar Mapa de Imagem

1. **Preparar Imagem**
   - Formato: PNG
   - Cores aceitas: RGB exato
     - Branco: (255, 255, 255)
     - Preto: (0, 0, 0)
     - Vermelho: (255, 0, 0)
     - Laranja: (255, 165, 0)

2. **Upload**
   - Clique em "Upload de Imagem"
   - Selecione arquivo PNG
   - Sistema validará automaticamente

3. **Conversão**
   - Imagem é convertida para formato .txt
   - Visualização automática gerada
   - Mapa salvo se válido

### Validação de Mapas

Requisitos automáticos verificados:
- ✅ Tamanho entre 5x5 e 100x100
- ✅ Pelo menos uma porta (célula vermelha)
- ✅ Área navegável conectada
- ✅ Cores válidas (sem pixels intermediários)

## ⚙️ Configuração de Parâmetros

### Sistema de Presets

**Presets Disponíveis:**

1. **Teste Rápido**
   - População: 20
   - Gerações: 10
   - Iterações: 500
   - Uso: Testes rápidos e debug

2. **Produção Média**
   - População: 50
   - Gerações: 30
   - Iterações: 1000
   - Uso: Uso geral e análises padrão

3. **Pesquisa Pesada**
   - População: 100
   - Gerações: 50
   - Iterações: 1500
   - Uso: Pesquisa e análises detalhadas

### Carregar Preset

1. Vá para "Parâmetros"
2. Selecione algoritmo (NSGA-II Pymoo, NSGA-II Cached ou Força Bruta)
3. Escolha preset no dropdown
4. Clique em "Carregar Configuração"
5. Parâmetros são preenchidos automaticamente

### Configuração Manual

**Parâmetros de Algoritmo (NSGA-II):**

- **Tamanho da População**: 10-200
  - Número de soluções por geração
  - Maior = mais diversidade, mais lento

- **Número de Gerações**: 5-100
  - Iterações do algoritmo evolutivo
  - Maior = melhor convergência, mais tempo

- **Taxa de Mutação**: 0.0-1.0
  - Probabilidade de mutação genética
  - Padrão: 0.1-0.2

**Parâmetros de Simulação:**

- **Semente de Cenário**: Número inteiro
  - Reprodutibilidade do cenário
  - Mesma semente = mesmo cenário

- **Semente de Simulação**: Número inteiro
  - Reprodutibilidade da simulação
  - Afeta comportamento de indivíduos

- **Iterações Máximas**: 100-2000
  - Limite de passos da simulação
  - Maior = permite evacuações mais lentas

- **Gerar Imagens**: Checkbox
  - Ativa/desativa geração de frames
  - Necessário para visualizações posteriores

- **Modo Verboso**: Checkbox
  - Exibe logs detalhados
  - Útil para debug

### Salvar Configuração

1. Configure todos os parâmetros
2. Adicione descrição (opcional)
3. Clique em "Salvar Configuração"
4. Configuração ficará disponível em execuções futuras

## 🚀 Execução de Simulações

### Otimização NSGA-II

Executa otimização multiobjetivo para encontrar melhores configurações de portas.

**Variantes Disponíveis:**

1. **NSGA-II Pymoo** - Implementação baseada na biblioteca pymoo
2. **NSGA-II Cached** - Implementação customizada com cache de avaliações

**Passos:**

1. **Preparar**
   - Mapa com possíveis locais de portas
   - Arquivo de indivíduos (feito na UI ou por JSON)
   - Configuração carregada (preset ou manual)

2. **Executar Otimização**
   - Clique em "Executar Simulação/Otimização"
   - Processo pode demorar (minutos a horas)
   - Progresso exibido por geração

3. **Salvar sem Executar** (Opcional)
   - Botão "Salvar sem Executar"
   - Salva configuração para execução posterior
   - Status: Não Executada

4. **Resultados**
   - Fronteira de Pareto gerada
   - Conjunto de soluções ótimas
   - Salvamento automático no banco de dados

**Interpretação da Fronteira de Pareto:**
- Cada ponto = uma configuração ótima de portas
- Não há solução "melhor" absoluta
- Trade-offs entre 3 objetivos:
  - **Número de portas**: Minimizar (custo de construção)
  - **Iterações**: Minimizar (tempo de evacuação)
  - **Distância total**: Minimizar (eficiência de rotas)

### Força Bruta

Testa todas as combinações possíveis de portas.

**Limitações:**
- Apenas mapas pequenos (≤ 10 possíveis portas)
- Tempo exponencial: 2^n combinações
- Garante solução ótima global

**Uso:**
1. Selecione "Força Bruta" em Parâmetros
2. Configure e salve
3. Execute normalmente em Simulação
4. Aguarde conclusão (pode ser MUITO lento)

## 📊 Análise de Resultados

### Página Resultados

**Tabela de Simulações:**
- Lista todas as simulações salvas no sistema
- Colunas: Nome, Algoritmo, Mapa, Status (Executada/Não Executada)
- Badge visual indica status de execução
- Botão "Visualizar" para ver detalhes

**Informações Exibidas:**
- Nome da simulação
- Algoritmo utilizado (NSGA-II Pymoo, NSGA-II Cached, Força Bruta)
- Mapa associado
- Status de execução

**Ações Disponíveis:**
- **Visualizar**: Abre página da simulação caso você queira executar novamente
- Identificação visual de simulações executadas vs. não executadas

### Página Detalhes

Mostra informações detalhadas sobre um mapa específico e suas simulações associadas.

**Tabela de Simulações do Mapa:**
- Lista todas as simulações feitas ou preparadas neste mapa
- Colunas: Nome, Status, Algoritmo
- Badge visual de status:
  - ✅ Verde: Simulação executada
  - ⚠️ Amarelo: Não executada (salva para execução posterior)

**Status de Execução:**
- **SIM** (Executada): Simulação foi executada e tem resultados
- **NÃO** (Não Executada): Configuração salva, aguardando execução

## 💾 Gestão de Dados

### Banco de Dados

O sistema usa SQLite para armazenar:
- **Simulações**: Histórico completo
- **Mapas**: Todos os mapas criados
- **Resultados**: Métricas e configurações
- **Configurações**: Presets salvos

**Localização:** `database/simulacoes.db`

### Estrutura de Arquivos

```
uploads/
├── nsga_ii/          # Resultados NSGA-II
├── forca_bruta/      # Resultados Força Bruta
└── results/          # Exportações

simulador_heuristica/
├── input/            # Arquivos de entrada (temporários)
└── output/           # Resultados de simulações
    ├── <experiment>/ # Por experimento
    └── nsga_eval_*/  # Avaliações NSGA-II

temp_nsga/            # Dados temporários de otimização
logs/                 # Logs de execução
```

## ❓ Solução de Problemas

### Simulação Não Executa

**Verifique:**
- [ ] Mapa e indivíduos foram selecionados
- [ ] Configuração está carregada
- [ ] Não há erros no console/logs
- [ ] Dependências estão instaladas

**Soluções:**
1. Recarregue a página
2. Verifique logs em `logs/`
3. Execute simulador via CLI para debug
4. Verifique permissões de escrita

### Otimização Muito Lenta

**Causas comuns:**
- População muito grande (>100)
- Muitas gerações (>50)
- Mapa grande com muitas portas possíveis
- Iterações máximas muito altas

**Soluções:**
1. Use preset "Teste Rápido" inicialmente
2. Reduza tamanho da população
3. Reduza número de gerações
4. Simplifique o mapa

### Erros de Importação

**Mapa não aceito:**
- Verifique dimensões (5x5 a 100x100)
- Confira cores exatas RGB
- Garanta pelo menos uma porta
- Salve em PNG sem compressão

**Indivíduos inválidos:**
- Formato JSON correto
- Posições dentro do mapa
- Posições em células navegáveis

### Resultados Inesperados

**Fronteira de Pareto vazia:**
- População muito pequena
- Poucas gerações
- Problema sem soluções viáveis

**Todas evacuações falham:**
- Sem portas suficientes
- Portas bloqueadas
- Iterações máximas muito baixas
- Mapa sem caminho válido para saídas

## 💡 Dicas e Boas Práticas

### Criação de Mapas

✅ **Faça:**
- Comece com mapas pequenos (10x10 a 20x20)
- Teste com 2-4 portas possíveis
- Garanta corredores de pelo menos 2 células
- Use áreas abertas para aglomerações

❌ **Evite:**
- Mapas muito complexos inicialmente
- Portas em cantos isolados
- Corredores de 1 célula (gargalos severos)
- Muitas portas sem necessidade

### Configuração

✅ **Faça:**
- Comece com presets
- Ajuste incrementalmente
- Salve configurações que funcionam
- Documente experimentos

❌ **Evite:**
- Configurações extremas sem necessidade
- Mudanças drásticas simultâneas
- Ignorar avisos de validação

### Otimização

✅ **Faça:**
- Comece com preset "Teste Rápido"
- Use poucos indivíduos inicialmente (20-50)
- Monitore progresso das gerações
- Salve configurações antes de executar
- Use "Salvar sem Executar" para preparar múltiplas simulações

❌ **Evite:**
- Começar com configurações muito pesadas
- Executar overnight sem validação prévia
- Ignorar avisos de tempo de execução estimado
- Mudar muitos parâmetros simultaneamente

---

**Versão:** 1.0  
**Atualizado:** Outubro 2024
