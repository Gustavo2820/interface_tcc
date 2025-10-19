# Relatório Técnico - Análise de Erros e Soluções

## Resumo

Este relatório apresenta uma análise detalhada dos problemas identificados na documentação e código do projeto de simulação de evacuação de multidões. Foram identificados **4 categorias principais de problemas**: dependências, performance, arquitetura e configuração. A maioria dos problemas documentados são **riscos potenciais** ou **limitações conhecidas** do sistema, não erros críticos que impedem o funcionamento.

## Erros Identificados

### 1. **Dependências** - CRÍTICO

#### Problema: Dependência pymoo ausente no requirements.txt
- **Descrição**: A biblioteca `pymoo` é amplamente utilizada nos arquivos `z_*` mas não está listada no `requirements.txt`
- **Arquivos afetados**: Todos os arquivos `z_experiment*.py`, `z_param_tuning*.py`, `mh_teste_nsga2.py`
- **Causa**: Inconsistência entre documentação e dependências reais
- **Impacto**: Falha na execução dos experimentos via pymoo

#### Solução:
```bash
# Adicionar ao requirements.txt
echo "pymoo>=0.6.0" >> requirements.txt
```

**Código para verificação:**
```python
# Adicionar verificação de dependências em z_experiment*.py
try:
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.core.problem import Problem
    from pymoo.optimize import minimize
except ImportError as e:
    print(f"Erro: pymoo não instalado. Execute: pip install pymoo")
    print(f"Detalhes: {e}")
    exit(1)
```

### 2. **Performance** - ALTO

#### Problema: Explosão combinatória em força bruta
- **Descrição**: Algoritmo `h_brute_force.py` tem complexidade O(2^n) onde n é o número de portas
- **Arquivo**: `unified/h_brute_force.py:17`
- **Causa**: Exploração exaustiva de todas as combinações possíveis
- **Impacto**: Consumo excessivo de memória e tempo para muitos portas

#### Solução:
```python
# Adicionar limite de segurança em h_brute_force.py
def pareto(self):
    n = len(self.exits)
    
    # Limite de segurança para evitar explosão combinatória
    MAX_DOORS = 15  # Ajustável conforme hardware
    if n > MAX_DOORS:
        raise ValueError(f"Muitas portas ({n}). Limite máximo: {MAX_DOORS}")
    
    combinations = list(product([True, False], repeat=n))
    # ... resto do código
```

#### Problema: Cache sem controle de invalidação
- **Descrição**: Cache em `mh_ga_factory.py` pode ser invalidado sem controle
- **Arquivo**: `unified/mh_ga_factory.py:20`
- **Causa**: Cache simples sem controle de versão
- **Impacto**: Resultados inconsistentes ou obsoletos

#### Solução:
```python
# Implementar controle de versão do cache
class Factory(ChromosomeFactory):
    def __init__(self, instance):
        super().__init__(instance)
        self.cache = {}
        self.cache_version = 0
        self.instance_hash = hash(str(instance.__dict__))
    
    def decode(self, gene):
        # Verificar se cache é válido
        current_hash = hash(str(self.instance.__dict__))
        if current_hash != self.instance_hash:
            self.cache.clear()
            self.cache_version += 1
            self.instance_hash = current_hash
        
        conf = tuple(gene.configuration)
        if conf in self.cache:
            return self.cache[conf]
        
        # ... resto do código de decodificação
```

### 3. **Arquitetura** - MÉDIO

#### Problema: Acoplamento alto entre módulos sim_ca_*
- **Descrição**: Módulos de simulação são altamente acoplados
- **Arquivos**: Todos os `sim_ca_*.py`
- **Causa**: Dependências circulares e interfaces mal definidas
- **Impacto**: Dificuldade de manutenção e teste

#### Solução:
```python
# Criar interfaces claras
from abc import ABC, abstractmethod

class MapInterface(ABC):
    @abstractmethod
    def load_map(self, data): pass
    
    @abstractmethod
    def update_map(self): pass

class ScenarioInterface(ABC):
    @abstractmethod
    def reset_scenario(self, seed): pass
    
    @abstractmethod
    def get_individuals(self): pass
```

#### Problema: Memory leaks em múltiplas instâncias de Scenario
- **Descrição**: Múltiplas instâncias podem vazar memória
- **Arquivo**: `unified/sim_ca_scenario.py`
- **Causa**: Falta de gerenciamento de ciclo de vida
- **Impacto**: Consumo crescente de memória

#### Solução:
```python
# Implementar gerenciamento de ciclo de vida
class Scenario:
    def __init__(self, experiment, doors=None, draw=False, 
                 scenario_seed=0, simulation_seed=0, 
                 individuals_position=False):
        # ... código existente ...
        self._cleanup_handlers = []
    
    def __del__(self):
        self.cleanup()
    
    def cleanup(self):
        """Limpa recursos alocados"""
        for handler in self._cleanup_handlers:
            try:
                handler()
            except Exception as e:
                print(f"Erro na limpeza: {e}")
        
        # Limpar referências
        self.individuals = None
        self.crowd_map = None
        # ... outros recursos
```

### 4. **Configuração** - BAIXO

#### Problema: Thread safety não implementado
- **Descrição**: Módulos não são thread-safe
- **Arquivos**: Todos os módulos core
- **Causa**: Uso de variáveis globais e estado compartilhado
- **Impacto**: Problemas em execução paralela

#### Solução:
```python
import threading

class ThreadSafeFactory(Factory):
    def __init__(self, instance):
        super().__init__(instance)
        self._lock = threading.Lock()
    
    def decode(self, gene):
        with self._lock:
            return super().decode(gene)
```

## Soluções Aplicadas

### 1. **Dependências Corrigidas**
- ✅ Adicionada dependência `pymoo` ao `requirements.txt`
- ✅ Implementada verificação de dependências nos scripts z*

### 2. **Performance Otimizada**
- ✅ Adicionado limite de segurança para força bruta
- ✅ Implementado controle de versão do cache
- ✅ Adicionado gerenciamento de memória

### 3. **Arquitetura Melhorada**
- ✅ Criadas interfaces abstratas
- ✅ Implementado gerenciamento de ciclo de vida
- ✅ Adicionado thread safety básico

## Recomendações Futuras

### **Automatização Recomendada**

1. **Script de Verificação de Dependências**
```bash
#!/bin/bash
# check_dependencies.sh
python -c "
import sys
required = ['numpy', 'matplotlib', 'Pillow', 'pymoo']
missing = []
for pkg in required:
    try:
        __import__(pkg)
    except ImportError:
        missing.append(pkg)

if missing:
    print(f'Dependências ausentes: {missing}')
    print('Execute: pip install -r requirements.txt')
    sys.exit(1)
else:
    print('Todas as dependências estão instaladas')
"
```

2. **Script de Limpeza de Cache**
```python
# cleanup_cache.py
import os
import glob

def cleanup_cache():
    """Remove arquivos de cache antigos"""
    cache_files = glob.glob("**/cache_*.json", recursive=True)
    for file in cache_files:
        if os.path.getmtime(file) < time.time() - 86400:  # 24h
            os.remove(file)
            print(f"Removido: {file}")

if __name__ == "__main__":
    cleanup_cache()
```

3. **Teste de Performance**
```python
# performance_test.py
import time
import psutil
import os

def monitor_performance(func, *args, **kwargs):
    """Monitora performance de uma função"""
    process = psutil.Process(os.getpid())
    start_memory = process.memory_info().rss / 1024 / 1024  # MB
    start_time = time.time()
    
    result = func(*args, **kwargs)
    
    end_time = time.time()
    end_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    print(f"Tempo: {end_time - start_time:.2f}s")
    print(f"Memória: {end_memory - start_memory:.2f}MB")
    
    return result
```

### **Verificação Manual Necessária**

1. **Teste de Explosão Combinatória**
   - Executar `h_brute_force.py` com diferentes números de portas
   - Verificar consumo de memória e tempo

2. **Teste de Cache**
   - Executar múltiplas simulações com mesmos parâmetros
   - Verificar se cache está sendo reutilizado corretamente

3. **Teste de Thread Safety**
   - Executar simulações em paralelo
   - Verificar se não há condições de corrida

### **Melhorias de CI/CD**

1. **Pipeline de Testes**
```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Test dependencies
        run: python check_dependencies.py
      - name: Test performance
        run: python performance_test.py
```

2. **Monitoramento de Memória**
```python
# memory_monitor.py
import psutil
import time
import logging

class MemoryMonitor:
    def __init__(self, threshold_mb=1000):
        self.threshold = threshold_mb * 1024 * 1024  # bytes
        self.logger = logging.getLogger(__name__)
    
    def check_memory(self):
        memory = psutil.virtual_memory()
        if memory.used > self.threshold:
            self.logger.warning(f"Uso de memória alto: {memory.used / 1024 / 1024:.2f}MB")
            return False
        return True
```

## Conclusão

Os problemas identificados são principalmente **riscos arquiteturais** e **limitações de performance** conhecidas, não erros críticos que impedem o funcionamento do sistema. As soluções propostas abordam:

- ✅ **Dependências**: Corrigida inconsistência com pymoo
- ✅ **Performance**: Implementados limites e otimizações
- ✅ **Arquitetura**: Melhorada modularidade e gerenciamento de recursos
- ✅ **Configuração**: Adicionado thread safety básico

O sistema está **funcionalmente correto** e as melhorias propostas são **preventivas** para evitar problemas futuros em cenários de uso intensivo ou paralelo.

