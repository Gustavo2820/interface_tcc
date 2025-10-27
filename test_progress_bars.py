#!/usr/bin/env python3
"""
Script de teste para validar as barras de progresso nos algoritmos NSGA-II.

Este script verifica:
1. Importação correta dos módulos
2. Existência das classes/funções de callback
3. Assinatura correta dos métodos
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

print("=" * 70)
print("TESTE DE BARRAS DE PROGRESSO - NSGA-II")
print("=" * 70)

# Test 1: Import pymoo callback
print("\n[1] Testando importação do callback do pymoo...")
try:
    from pymoo.core.callback import Callback
    print("   ✓ Callback importado com sucesso")
except ImportError as e:
    print(f"   ✗ Erro ao importar Callback: {e}")
    sys.exit(1)

# Test 2: Import nsga_integration
print("\n[2] Testando importação do nsga_integration...")
try:
    from interface.services import nsga_integration
    print("   ✓ nsga_integration importado com sucesso")
except ImportError as e:
    print(f"   ✗ Erro ao importar nsga_integration: {e}")
    sys.exit(1)

# Test 3: Check StreamlitProgressCallback class
print("\n[3] Verificando classe StreamlitProgressCallback...")
try:
    assert hasattr(nsga_integration, 'StreamlitProgressCallback')
    callback_class = nsga_integration.StreamlitProgressCallback
    print(f"   ✓ Classe encontrada: {callback_class}")
    
    # Check if it's a subclass of Callback
    assert issubclass(callback_class, Callback)
    print("   ✓ É subclasse de pymoo.core.callback.Callback")
    
    # Check __init__ signature
    import inspect
    init_sig = inspect.signature(callback_class.__init__)
    assert 'max_generations' in init_sig.parameters
    assert 'progress_bar' in init_sig.parameters
    assert 'status_text' in init_sig.parameters
    print("   ✓ __init__ aceita parâmetros: max_generations, progress_bar, status_text")
    
    # Check notify method
    assert hasattr(callback_class, 'notify')
    notify_sig = inspect.signature(callback_class.notify)
    assert 'algorithm' in notify_sig.parameters
    print("   ✓ Método notify(algorithm) está presente")
    
except (AssertionError, AttributeError) as e:
    print(f"   ✗ Erro na verificação: {e}")
    sys.exit(1)

# Test 4: Import cached NSGA integration
print("\n[4] Testando importação do nsga_cached_integration...")
try:
    from interface.services import nsga_cached_integration
    print("   ✓ nsga_cached_integration importado com sucesso")
except ImportError as e:
    print(f"   ✗ Erro ao importar nsga_cached_integration: {e}")
    sys.exit(1)

# Test 5: Import unified mh_ga_nsgaii
print("\n[5] Testando importação do mh_ga_nsgaii...")
try:
    unified_path = project_root / "simulador_heuristica" / "unified"
    sys.path.insert(0, str(unified_path))
    
    import mh_ga_nsgaii
    print("   ✓ mh_ga_nsgaii importado com sucesso")
except ImportError as e:
    print(f"   ✗ Erro ao importar mh_ga_nsgaii: {e}")
    sys.exit(1)

# Test 6: Check nsgaii function signature
print("\n[6] Verificando assinatura da função nsgaii...")
try:
    import inspect
    nsgaii_sig = inspect.signature(mh_ga_nsgaii.nsgaii)
    params = list(nsgaii_sig.parameters.keys())
    
    print(f"   Parâmetros: {params}")
    
    assert 'factory' in params
    assert 'selector' in params
    assert 'population_size' in params
    assert 'mutation_probability' in params
    assert 'max_generations' in params
    assert 'progress_callback' in params
    print("   ✓ Todos os parâmetros presentes")
    
    # Check if progress_callback has default value
    callback_param = nsgaii_sig.parameters['progress_callback']
    assert callback_param.default is None
    print("   ✓ progress_callback tem default=None (retrocompatível)")
    
except (AssertionError, AttributeError) as e:
    print(f"   ✗ Erro na verificação: {e}")
    sys.exit(1)

# Test 7: Check NSGAIntegration.run_optimization uses callback
print("\n[7] Verificando uso do callback em NSGAIntegration...")
try:
    import inspect
    source = inspect.getsource(nsga_integration.NSGAIntegration.run_optimization)
    
    assert 'StreamlitProgressCallback' in source
    print("   ✓ StreamlitProgressCallback é instanciado")
    
    assert 'callback=' in source
    print("   ✓ Callback passado para minimize()")
    
    assert '.empty()' in source
    print("   ✓ Limpeza da UI implementada")
    
except (AssertionError, AttributeError) as e:
    print(f"   ✗ Erro na verificação: {e}")
    sys.exit(1)

# Test 8: Check CachedNSGAIntegration.run_optimization uses callback
print("\n[8] Verificando uso do callback em CachedNSGAIntegration...")
try:
    import inspect
    source = inspect.getsource(nsga_cached_integration.CachedNSGAIntegration.run_optimization)
    
    assert 'progress_callback' in source
    print("   ✓ progress_callback é definido")
    
    assert 'st.progress' in source
    print("   ✓ Barra de progresso criada")
    
    assert 'progress_callback=' in source or 'progress_callback)' in source
    print("   ✓ Callback passado para cached_nsgaii()")
    
    assert '.empty()' in source
    print("   ✓ Limpeza da UI implementada")
    
except (AssertionError, AttributeError) as e:
    print(f"   ✗ Erro na verificação: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ TODOS OS TESTES PASSARAM!")
print("=" * 70)
print("\nImplementação validada:")
print("  1. ✓ Pymoo callback importado corretamente")
print("  2. ✓ StreamlitProgressCallback implementado")
print("  3. ✓ NSGA-II pymoo usa callback")
print("  4. ✓ mh_ga_nsgaii aceita progress_callback")
print("  5. ✓ NSGA-II cached usa callback")
print("  6. ✓ Limpeza de UI implementada em ambos")
print("\nPróximo passo: Testar no Streamlit com otimização real")
print("  Execute: streamlit run interface/App.py")
