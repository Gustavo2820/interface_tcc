# TODOs e Refatoração

## Prioridades de Refatoração

###  ALTA PRIORIDADE (Crítico)

#### 1. Implementar Controle de Cache
- **Arquivo**: mh_ga_factory.py
- **Problema**: Cache pode ser invalidado sem controle
- **Solução**: Implementar sistema de versionamento do cache
- **Esforço**: 2-3 dias
- **Risco**: Alto - pode afetar performance

#### 2. Resolver Explosão Combinatória
- **Arquivo**: h_brute_force.py
- **Problema**: O(2^n) para muitos portas
- **Solução**: Implementar limite máximo de portas ou algoritmo híbrido
- **Esforço**: 1-2 dias
- **Risco**: Médio - pode limitar funcionalidade

#### 3. Implementar Thread Safety
- **Arquivos**: Todos os módulos sim_ca_*
- **Problema**: Módulos não são thread-safe
- **Solução**: Implementar locks ou usar multiprocessing
- **Esforço**: 3-4 dias
- **Risco**: Alto - pode quebrar funcionalidade existente

###  MÉDIA PRIORIDADE (Importante)

#### 4. Adicionar Type Hints
- **Arquivos**: Todos os arquivos Python
- **Problema**: Falta de tipagem estática
- **Solução**: Adicionar type hints em todas as funções
- **Esforço**: 2-3 dias
- **Risco**: Baixo - melhora manutenibilidade

#### 5. Implementar Logging Estruturado
- **Arquivo**: sim_ca_logs.py
- **Problema**: Logging básico sem estrutura
- **Solução**: Implementar logging com níveis e formatação
- **Esforço**: 1 dia
- **Risco**: Baixo - melhora debug

#### 6. Refatorar Funções Longas
- **Arquivos**: mh_ga_nsgaii.py, sim_ca_simulator.py
- **Problema**: Funções muito longas (>50 linhas)
- **Solução**: Quebrar em funções menores
- **Esforço**: 2 dias
- **Risco**: Médio - pode afetar lógica

#### 7. Implementar Validação de Entrada
- **Arquivos**: Todos os main*.py
- **Problema**: Falta validação de parâmetros
- **Solução**: Adicionar validação robusta
- **Esforço**: 1 dia
- **Risco**: Baixo - melhora robustez

###  BAIXA PRIORIDADE (Melhoria)

#### 8. Implementar Padrão Observer
- **Arquivo**: sim_ca_simulator.py
- **Problema**: Acoplamento alto com logs
- **Solução**: Implementar padrão Observer
- **Esforço**: 2 dias
- **Risco**: Médio - refatoração significativa

#### 9. Adicionar Documentação de Código
- **Arquivos**: Todos os arquivos Python
- **Problema**: Falta docstrings e comentários
- **Solução**: Adicionar docstrings no estilo Google
- **Esforço**: 3-4 dias
- **Risco**: Baixo - melhora manutenibilidade

#### 10. Implementar Testes Unitários
- **Arquivos**: Todos os módulos core
- **Problema**: Falta de testes automatizados
- **Solução**: Implementar testes unitários
- **Esforço**: 5-7 dias
- **Risco**: Baixo - melhora qualidade

## Melhorias de Código

### Nomes de Variáveis

#### Problemas Identificados
- combs  combinations
- objs  objectives
- iters  iterations
- qtdDistance  	otal_distance
- menor  is_dominated

#### Soluções Propostas
`python
# Antes
combs = [combinations[0]]
objs = [self.decode(combinations[0])]

# Depois
combinations = [combinations[0]]
objectives = [self.decode(combinations[0])]
`

### Funções Muito Longas

#### 1. mh_ga_nsgaii.py - Função 
sgaii
- **Problema**: 366 linhas, muito complexa
- **Solução**: Quebrar em funções menores:
  - initialize_population()
  - evaluate_population()
  - 
on_dominated_sort()
  - crowding_distance()
  - selection()
  - crossover()
  - mutation()

#### 2. sim_ca_simulator.py - Função simulate
- **Problema**: Loop principal muito longo
- **Solução**: Quebrar em funções menores:
  - initialize_simulation()
  - update_individuals()
  - check_termination()
  - inalize_simulation()

### Duplicação de Código

#### 1. Cálculo de Objetivos
- **Arquivos**: mh_ga_factory.py, h_brute_force.py, z_experiment*.py
- **Problema**: Código duplicado para cálculo de objetivos
- **Solução**: Criar classe ObjectiveCalculator

#### 2. Configuração de Experimentos
- **Arquivos**: Todos os main*.py
- **Problema**: Parsing de argumentos duplicado
- **Solução**: Criar classe ExperimentConfig

#### 3. Salvamento de Resultados
- **Arquivos**: Todos os main*.py
- **Problema**: Função save_result duplicada
- **Solução**: Criar classe ResultSaver

## Testes Unitários Prioritários

###  CRÍTICOS (Implementar Primeiro)

#### 1. Testes de NSGA-II
- **Arquivo**: 	est_mh_ga_nsgaii.py
- **Testes**:
  - Ordenação não-dominada
  - Cálculo de crowding distance
  - Seleção de indivíduos
  - Crossover e mutação
- **Cobertura**: 90%+

#### 2. Testes de Simulação
- **Arquivo**: 	est_sim_ca_simulator.py
- **Testes**:
  - Inicialização da simulação
  - Movimento de indivíduos
  - Verificação de evacuação
  - Cálculo de distâncias
- **Cobertura**: 85%+

#### 3. Testes de Força Bruta
- **Arquivo**: 	est_h_brute_force.py
- **Testes**:
  - Geração de combinações
  - Cálculo de Pareto
  - Decodificação de genes
- **Cobertura**: 80%+

###  IMPORTANTES (Implementar Segundo)

#### 4. Testes de Mapas
- **Arquivo**: 	est_sim_ca_maps.py
- **Testes**:
  - Carregamento de mapas
  - Cálculo de campos
  - Verificação de posições
- **Cobertura**: 75%+

#### 5. Testes de Indivíduos
- **Arquivo**: 	est_sim_ca_individual.py
- **Testes**:
  - Movimento de indivíduos
  - Cálculo de direções
  - Verificação de evacuação
- **Cobertura**: 80%+

###  DESEJÁVEIS (Implementar Terceiro)

#### 6. Testes de Integração
- **Arquivo**: 	est_integration.py
- **Testes**:
  - Fluxo completo main3
  - Fluxo completo main4
  - Fluxo completo z_experiment
- **Cobertura**: 70%+

## Riscos de Invalidação do Cache

### Problemas Identificados

#### 1. Cache Sem Controle de Versão
- **Arquivo**: mh_ga_factory.py
- **Problema**: Cache não é invalidado quando parâmetros mudam
- **Risco**: Resultados incorretos
- **Solução**: Implementar hash de parâmetros

#### 2. Múltiplas Instâncias
- **Arquivo**: mh_ga_factory.py
- **Problema**: Cache compartilhado entre instâncias
- **Risco**: Conflitos de dados
- **Solução**: Cache por instância

#### 3. Dependências Externas
- **Arquivo**: mh_ga_factory.py
- **Problema**: Cache não considera mudanças em arquivos
- **Risco**: Dados desatualizados
- **Solução**: Verificar timestamps de arquivos

### Soluções Propostas

#### 1. Sistema de Versionamento
`python
class CacheManager:
    def __init__(self):
        self.cache = {}
        self.versions = {}
    
    def get_cache_key(self, gene, parameters):
        return hash((gene, parameters))
    
    def is_valid(self, key, parameters):
        return key in self.cache and self.versions[key] == parameters
`

#### 2. Invalidação Automática
`python
def invalidate_cache(self, parameters):
    """Invalida cache quando parâmetros mudam."""
    if self.cache_version != parameters:
        self.cache.clear()
        self.cache_version = parameters
`

## Riscos de Explosão Combinatória

### Problemas Identificados

#### 1. Força Bruta O(2^n)
- **Arquivo**: h_brute_force.py
- **Problema**: 2^n combinações para n portas
- **Risco**: Memória insuficiente para n > 20
- **Solução**: Implementar limite máximo

#### 2. Sem Limite de Portas
- **Arquivo**: h_brute_force.py
- **Problema**: Não há verificação de limite
- **Risco**: Sistema pode travar
- **Solução**: Adicionar validação

#### 3. Sem Progresso
- **Arquivo**: h_brute_force.py
- **Problema**: Não há indicação de progresso
- **Risco**: Usuário não sabe se está funcionando
- **Solução**: Adicionar barra de progresso

### Soluções Propostas

#### 1. Limite Máximo de Portas
`python
MAX_DOORS = 20  # Limite máximo de portas

def pareto(self):
    if len(self.exits) > MAX_DOORS:
        raise ValueError(f"Máximo de {MAX_DOORS} portas permitido")
`

#### 2. Algoritmo Híbrido
`python
def pareto_hybrid(self):
    if len(self.exits) <= 15:
        return self.pareto_brute_force()
    else:
        return self.pareto_genetic_algorithm()
`

#### 3. Barra de Progresso
`python
from tqdm import tqdm

def pareto(self):
    combinations = list(product([True, False], repeat=len(self.exits)))
    for combination in tqdm(combinations, desc="Processando"):
        # Processar combinação
`

## Sugestões de Otimização

### 1. Paralelização
- **Implementar**: Multiprocessing para simulações
- **Arquivo**: mh_ga_factory.py
- **Ganho**: 2-4x mais rápido
- **Esforço**: 2-3 dias

### 2. Cache Inteligente
- **Implementar**: Cache com LRU e TTL
- **Arquivo**: mh_ga_factory.py
- **Ganho**: 50% menos recálculos
- **Esforço**: 1 dia

### 3. Vectorização
- **Implementar**: Usar numpy para operações vetoriais
- **Arquivo**: sim_ca_simulator.py
- **Ganho**: 30% mais rápido
- **Esforço**: 1-2 dias

### 4. Algoritmo Híbrido
- **Implementar**: Combinar força bruta com NSGA-II
- **Arquivo**: h_brute_force.py
- **Ganho**: Melhor qualidade de solução
- **Esforço**: 3-4 dias

### 5. Compressão de Dados
- **Implementar**: Compressão de resultados
- **Arquivo**: Todos os main*.py
- **Ganho**: 50% menos espaço em disco
- **Esforço**: 1 dia

## Cronograma de Implementação

### Semana 1
- [ ] Implementar controle de cache
- [ ] Adicionar type hints básicos
- [ ] Implementar validação de entrada

### Semana 2
- [ ] Resolver explosão combinatória
- [ ] Implementar logging estruturado
- [ ] Refatorar funções longas

### Semana 3
- [ ] Implementar testes unitários críticos
- [ ] Adicionar documentação de código
- [ ] Implementar thread safety

### Semana 4
- [ ] Implementar testes de integração
- [ ] Otimizações de performance
- [ ] Implementar padrão Observer

## Métricas de Sucesso

### Qualidade de Código
- [ ] Cobertura de testes > 80%
- [ ] Complexidade ciclomática < 10
- [ ] Duplicação de código < 5%

### Performance
- [ ] Tempo de execução reduzido em 30%
- [ ] Uso de memória reduzido em 20%
- [ ] Cache hit rate > 70%

### Manutenibilidade
- [ ] Documentação completa
- [ ] Type hints em 100% das funções
- [ ] Logs estruturados
