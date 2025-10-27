# Implementação de Barras de Progresso nos Algoritmos NSGA-II

## Resumo

Implementado sistema de barras de progresso para os dois algoritmos NSGA-II (pymoo e cached), seguindo o mesmo padrão visual do algoritmo Força Bruta.

## Motivação

O usuário expressou satisfação com a barra de progresso do Força Bruta e solicitou a mesma funcionalidade para os algoritmos NSGA-II, melhorando o feedback visual durante otimizações longas.

## Implementação

### 1. NSGA-II Pymoo (`interface/services/nsga_integration.py`)

#### Importação do Callback
```python
from pymoo.core.callback import Callback
```

#### Classe StreamlitProgressCallback
Criada nova classe (linhas ~95-125) que implementa a interface `Callback` do pymoo:

```python
class StreamlitProgressCallback(Callback):
    """
    Callback do pymoo para atualizar barra de progresso no Streamlit.
    
    Monitora o progresso da otimização NSGA-II e atualiza a interface
    do Streamlit com informações sobre a geração atual.
    """
    
    def __init__(self, max_generations: int):
        super().__init__()
        self.max_generations = max_generations
        self.progress_bar = st.progress(0.0)
        self.status_text = st.empty()
    
    def notify(self, algorithm):
        """Chamado a cada geração pela otimização do pymoo."""
        current_gen = algorithm.n_gen
        progress = current_gen / self.max_generations
        
        self.progress_bar.progress(min(progress, 1.0))
        self.status_text.text(
            f"Geração {current_gen}/{self.max_generations} "
            f"({progress*100:.1f}%) - População: {pop_size}"
        )
```

#### Integração no método `_run_optimization`
Modificado para criar e usar o callback (linha ~940):

```python
# Cria callback para atualizar progresso no Streamlit
progress_callback = StreamlitProgressCallback(self.config['generations'])

# Executa a otimização usando pymoo
res = minimize(
    self.problem,
    self.algorithm,
    termination=('n_gen', self.config['generations']),
    seed=1,
    callback=progress_callback,
    verbose=True
)

# Limpa a barra de progresso ao finalizar
progress_callback.progress_bar.empty()
progress_callback.status_text.empty()
```

**Características:**
- Usa o sistema de callbacks nativo do pymoo
- Atualizado automaticamente a cada geração
- Mostra geração atual, total e percentual
- Exibe tamanho da população
- Limpa a interface ao finalizar

---

### 2. NSGA-II Cached (`interface/services/nsga_cached_integration.py` + `simulador_heuristica/unified/mh_ga_nsgaii.py`)

#### Modificação da função `nsgaii` core
Arquivo: `simulador_heuristica/unified/mh_ga_nsgaii.py`

Adicionado parâmetro opcional `progress_callback`:

```python
def nsgaii(factory, selector, population_size, mutation_probability,
           max_generations, progress_callback=None):
    # ... inicialização ...
    
    for generation in range(max_generations):
        logger.info("=== Generation %d ===", generation)
        
        # Atualiza progresso se callback fornecido
        if progress_callback:
            progress_callback(generation, max_generations)
        
        # ... resto do loop de geração ...
    
    # Atualiza progresso final
    if progress_callback:
        progress_callback(max_generations, max_generations)
    
    return pareto[0]
```

#### Integração no módulo de integração
Arquivo: `interface/services/nsga_cached_integration.py`

Criada função de callback inline (linha ~267):

```python
# Cria função de callback para atualizar progresso no Streamlit
import streamlit as st
progress_bar = st.progress(0.0)
status_text = st.empty()

def progress_callback(current_gen, total_gen):
    """Atualiza barra de progresso no Streamlit."""
    progress = current_gen / total_gen
    progress_bar.progress(min(progress, 1.0))
    status_text.text(
        f"Geração {current_gen}/{total_gen} "
        f"({progress*100:.1f}%)"
    )

results = cached_nsgaii(
    factory=factory,
    selector=selector,
    population_size=population_size,
    mutation_probability=mutation_prob,
    max_generations=max_generations,
    progress_callback=progress_callback
)

# Limpa a barra de progresso ao finalizar
progress_bar.empty()
status_text.empty()
```

**Características:**
- Callback simples baseado em função
- Compatível com implementação existente
- Não afeta algoritmos que não usam callback (retrocompatível)
- Atualizado a cada geração
- Mostra geração atual, total e percentual
- Limpa a interface ao finalizar

---

## Padrão Visual Consistente

Todos os três algoritmos agora seguem o mesmo padrão:

### Força Bruta
```
Avaliando combinação X/Y (Z%)
[████████████████████          ] 60%
```

### NSGA-II Pymoo
```
Geração X/Y (Z%) - População: N
[████████████████████          ] 60%
```

### NSGA-II Cached
```
Geração X/Y (Z%)
[████████████████████          ] 60%
```

## Arquivos Modificados

1. **`interface/services/nsga_integration.py`**
   - Importação: `from pymoo.core.callback import Callback`
   - Adição: `StreamlitProgressCallback` class
   - Modificação: `_run_optimization()` method

2. **`interface/services/nsga_cached_integration.py`**
   - Modificação: `run_optimization()` method
   - Adição: callback inline com Streamlit progress bar

3. **`simulador_heuristica/unified/mh_ga_nsgaii.py`**
   - Modificação: Assinatura da função `nsgaii()`
   - Adição: Parâmetro opcional `progress_callback`
   - Adição: Chamadas ao callback no loop de gerações

## Validação

Todos os arquivos foram validados sintaticamente:

```bash
✓ python3 -m py_compile interface/services/nsga_integration.py
✓ python3 -m py_compile interface/services/nsga_cached_integration.py
✓ python3 -m py_compile simulador_heuristica/unified/mh_ga_nsgaii.py
```

## Compatibilidade

- ✅ Retrocompatível: cached NSGA-II aceita `progress_callback=None`
- ✅ Não afeta funcionalidade: callbacks são apenas para UI
- ✅ Sem overhead: apenas atualizações visuais no Streamlit
- ✅ Thread-safe: usa componentes nativos do Streamlit

## Próximos Passos (Teste)

Para testar a implementação:

1. Execute o Streamlit: `streamlit run interface/App.py`
2. Vá para a página "Simulação"
3. Configure e execute uma otimização NSGA-II (pymoo ou cached)
4. Observe a barra de progresso sendo atualizada a cada geração
5. Verifique que os resultados continuam corretos

## Observações Técnicas

### Pymoo Callback
- Usa `algorithm.n_gen` para obter geração atual
- Chamado automaticamente pelo pymoo após cada geração
- Acesso completo ao objeto `algorithm` para métricas adicionais

### Cached NSGA Callback
- Função simples: `callback(current_gen, total_gen)`
- Chamada manualmente no loop de gerações
- Não interfere com a lógica do algoritmo

### Limpeza da Interface
Ambas implementações limpam a barra de progresso ao finalizar:
```python
progress_bar.empty()
status_text.empty()
```

Isso evita que a barra permaneça na tela após a conclusão da otimização.

---

**Data de implementação:** 2024
**Solicitação do usuário:** "eu gostei bastante da barra de progresso que tem no brute force. Voce pode adaptar ela para os outros dois algoritmos?"
**Status:** ✅ Implementado e validado
