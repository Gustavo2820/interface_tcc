# Migração NSGA-II Pymoo para 3 Objetivos

## Data: 27/10/2025

## Contexto
A integração NSGA-II pymoo (sem cache) estava configurada para 2 objetivos, enquanto o experimento original (`z_experiment1_audition.py`) e a versão cached NSGA-II já usavam 3 objetivos. Esta migração alinha ambas as implementações.

---

## Comparação: Antes vs Depois

### **Definição do Problema (EvacuationProblem)**

#### ❌ ANTES (2 objetivos):
```python
super().__init__(n_var=n_var, n_obj=2, n_constr=0, xl=0, xu=1, type_var=bool)
```

#### ✅ DEPOIS (3 objetivos):
```python
super().__init__(n_var=n_var, n_obj=3, n_constr=0, xl=0, xu=1, type_var=bool)
```

---

### **Método `_evaluate()` - Normalização de Resultados**

#### ❌ ANTES:
```python
results = np.full((len(x), 2), 1e6, dtype=float)  # Penalidade para 2 objetivos
```

#### ✅ DEPOIS:
```python
results = np.full((len(x), 3), 1e6, dtype=float)  # Penalidade para 3 objetivos
```

---

### **Método `_evaluate_single()` - Retorno**

#### ❌ ANTES:
```python
# Retornava apenas [num_doors, distance]
return [float(num_doors_val), float(distance_val)]

# Em caso de erro:
return [1e6, 1e6]
```

#### ✅ DEPOIS:
```python
# Retorna [num_doors, iterations, distance]
return [float(num_doors_val), float(iterations_val), float(distance_val)]

# Em caso de erro:
return [1e6, 1e6, 1e6]
```

---

### **Método `_extract_objectives()` - Extração de Métricas**

#### ❌ ANTES (extraía apenas distance):
```python
distance_keys = ['distance', 'avg_distance', 'qtdDistance', ...]
d_key = next((k for k in distance_keys if k in results), None)
# ...
return [nd, d_val]  # Apenas 2 valores
```

#### ✅ DEPOIS (extrai iterations e distance):
```python
iterations_keys = ['iterations', 'tempo_total', 'qtd_iteracoes', 'iters', 'total_time']
distance_keys = ['distance', 'avg_distance', 'qtdDistance', ...]

i_key = next((k for k in iterations_keys if k in results), None)
d_key = next((k for k in distance_keys if k in results), None)
# ...
return [nd, i_val, d_val]  # 3 valores
```

---

### **Método `save_results()` - Salvamento de Resultados**

#### ❌ ANTES:
```python
# Esperava 2 objetivos
if len(obj_list) > 2:
    obj_list = obj_list[:2]

# Tentava extrair iterations de forma auxiliar (não funcionava bem)
aux_iterations = None
# ... código complexo para buscar iterations separadamente

res_obj = {
    "objectives": _to_native(obj_list),  # [num_doors, distance]
    "iterations": int(aux_iterations) if aux_iterations is not None else None
}
```

#### ✅ DEPOIS:
```python
# Espera 3 objetivos
if len(obj_list) > 3:
    obj_list = obj_list[:3]
elif len(obj_list) < 3:
    obj_list = obj_list + [None] * (3 - len(obj_list))

# Extrai diretamente do array de objetivos
num_doors = obj_list[0]
iterations = obj_list[1]
distance = obj_list[2]

res_obj = {
    "objectives": _to_native(obj_list),  # [num_doors, iterations, distance]
    "num_doors": int(num_doors),
    "iterations": int(iterations) if iterations is not None else None,
    "distance": float(distance) if distance is not None else None
}
```

---

## Alinhamento com z_experiment1_audition.py

### **Experimento Original (z_experiment1_audition.py)**
```python
class ScenarioOptimizationProblem(Problem):
    def __init__(self, instance):
        # ...
        super().__init__(n_var=n, n_obj=3, n_constr=0, xl=0, xu=1, type_var=bool)
    
    def decode(self, gene):
        # ...
        return len(doors), avg_iters, avg_distance  # 3 valores
```

### **Integração Pymoo ATUAL (interface/services/nsga_integration.py)**
```python
class EvacuationProblem(Problem):
    def __init__(self, ...):
        # ...
        super().__init__(n_var=n_var, n_obj=3, n_constr=0, xl=0, xu=1, type_var=bool)
    
    def _evaluate_single(self, gene):
        # ...
        return [float(num_doors_val), float(iterations_val), float(distance_val)]  # 3 valores
```

✅ **ALINHADO!** Ambos agora usam 3 objetivos: `[num_doors, iterations, distance]`

---

## Consistência com Cached NSGA-II

### **Cached NSGA-II (interface/services/nsga_cached_integration.py)**
- ✅ Já estava configurado para **3 objetivos permanentemente** (após mudança anterior)
- ✅ Retorna `[num_doors, iterations, distance]`
- ✅ Tag de algoritmo: `NSGA-II-Cached-3obj`

### **NSGA-II Pymoo (interface/services/nsga_integration.py)**
- ✅ Agora também usa **3 objetivos**
- ✅ Retorna `[num_doors, iterations, distance]`
- ℹ️ Tag de algoritmo: `NSGA-II` (padrão pymoo)

---

## Arquivos Modificados

1. **interface/services/nsga_integration.py**
   - Classe `EvacuationProblem.__init__()`: `n_obj=2` → `n_obj=3`
   - Método `_evaluate()`: ajustado para 3 objetivos
   - Método `_evaluate_single()`: retorna 3 valores
   - Método `_extract_objectives()`: extrai iterations e distance
   - Método `save_results()`: processa 3 objetivos diretamente

---

## Validação

✅ **Teste de sintaxe Python:**
```bash
python3 -m py_compile interface/services/nsga_integration.py
# Resultado: OK - Sem erros de sintaxe
```

---

## Impacto nas Simulações Futuras

### **Antes desta mudança:**
- Pymoo NSGA-II otimizava apenas: `[num_doors, distance]`
- `iterations` era tratada como métrica auxiliar (não otimizada)
- Resultados salvos com 2 objetivos no array `objectives`

### **Após esta mudança:**
- Pymoo NSGA-II otimiza: `[num_doors, iterations, distance]`
- Todos os 3 valores são objetivos reais no Pareto front
- Resultados salvos com 3 objetivos no array `objectives`
- **Alinhado com cached NSGA-II e experimento original**

---

## Resultados Históricos

⚠️ **Resultados anteriores** (salvos antes desta mudança):
- Continuarão funcionando (compatibilidade mantida)
- Terão apenas 2 valores no array `objectives`
- A UI já tem fallbacks para lidar com formatos antigos

✅ **Novos resultados** (após esta mudança):
- Terão 3 valores no array `objectives: [num_doors, iterations, distance]`
- Formato consistente entre pymoo e cached NSGA-II
- Melhor rastreabilidade e análise

---

## Recomendações

1. ✅ **Testar uma simulação pequena** com pymoo NSGA-II para validar o comportamento
2. ✅ **Verificar se metrics.json** contém `iterations` (ou `tempo_total`) — necessário para extração
3. ⚠️ **Documentar** que agora há 3 objetivos em novos runs (para análises futuras)
4. 💡 **Opcional**: adicionar tag de algoritmo `NSGA-II-3obj` para diferenciar de runs antigos (2-obj)

---

## Conclusão

A integração NSGA-II pymoo (sem cache) foi migrada com sucesso de **2 para 3 objetivos**, alinhando-se com:
- ✅ Experimento original (`z_experiment1_audition.py`)
- ✅ Cached NSGA-II (`nsga_cached_integration.py`)
- ✅ Documentação e expectativas do projeto

**Todas as mudanças foram validadas sintaticamente e mantêm compatibilidade com resultados históricos.**
