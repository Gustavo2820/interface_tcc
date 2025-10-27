#!/usr/bin/env python3
"""
Script de configuração da integração entre interface e simulador.

Este script configura o ambiente necessário para a integração,
criando diretórios, inicializando o banco de dados e verificando dependências.

Uso:
    python setup_integration.py
"""
import os
import sys
import subprocess
from pathlib import Path
import sqlite3

def create_directories():
    """Cria os diretórios necessários para a integração."""
    directories = [
        "uploads/algoritmo_genetico",
        "uploads/nsga_ii", 
        "uploads/forca_bruta",
        "uploads/results",
        "simulador_heuristica/input",
        "simulador_heuristica/output",
        "temp_simulation",
        "temp_nsga",
        "mapas",
        "logs",
        "presets"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Diretório criado: {directory}")

def initialize_database():
    """Inicializa o banco de dados SQLite."""
    try:
        # Executa o script de criação do banco
        db_script = Path("database/db.py")
        if db_script.exists():
            subprocess.run([sys.executable, str(db_script)], check=True)
            print("✓ Banco de dados inicializado")
        else:
            print("⚠️ Script de banco de dados não encontrado")
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao inicializar banco de dados: {e}")

def check_dependencies():
    """Verifica se as dependências estão instaladas."""
    required_packages = [
        ("streamlit", "streamlit"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("PIL", "Pillow"),
        ("pymoo", "pymoo")
    ]
    
    missing_packages = []
    
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
            print(f"✓ {package_name} instalado")
        except ImportError:
            missing_packages.append(package_name)
            print(f"✗ {package_name} não encontrado")
    
    if missing_packages:
        print(f"\n⚠️ Pacotes faltando: {', '.join(missing_packages)}")
        print("Execute: pip install " + " ".join(missing_packages))
        return False
    
    return True

def check_simulator_structure():
    """Verifica se a estrutura do simulador está correta."""
    required_files = [
        "simulador_heuristica/simulator/main.py",
        "simulador_heuristica/simulator/scenario.py",
        "simulador_heuristica/simulator/simulator.py",
        "simulador_heuristica/unified/mh_ga_nsgaii.py",
        "simulador_heuristica/unified/mh_ga_factory.py",
        "simulador_heuristica/unified/mh_ga_instance.py",
        "simulador_heuristica/unified/sim_ca_scenario.py",
        "simulador_heuristica/unified/sim_ca_simulator.py",
        "modulo_criacao_mapas/map_converter_utils.py",
        "modulo_criacao_mapas/map_converter.py",
        "interface/App.py",
        "interface/services/nsga_integration.py",
        "interface/services/simulator_integration.py"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"✗ {file_path} não encontrado")
    
    if missing_files:
        print(f"\n⚠️ Arquivos faltando: {len(missing_files)}")
        return False
    
    return True

def create_example_configs():
    """Cria arquivos de configuração de exemplo."""
    
    # Verifica se preset directory existe
    preset_dir = Path("presets")
    if not preset_dir.exists():
        preset_dir.mkdir(parents=True, exist_ok=True)
    
    # Configuração de teste rápido
    test_config = {
        "nsga_config": {
            "population_size": 20,
            "generations": 10,
            "mutation_rate": 0.2
        },
        "simulation_params": {
            "scenario_seed": [0],
            "simulation_seed": 0,
            "max_iterations": 500,
            "draw_mode": False,
            "verbose": False
        },
        "description": "Configuração rápida para testes"
    }
    
    # Configuração de produção média
    production_config = {
        "nsga_config": {
            "population_size": 50,
            "generations": 30,
            "mutation_rate": 0.15
        },
        "simulation_params": {
            "scenario_seed": [0],
            "simulation_seed": 0,
            "max_iterations": 1000,
            "draw_mode": True,
            "verbose": False
        },
        "description": "Configuração balanceada para uso geral"
    }
    
    # Configuração de pesquisa pesada
    research_config = {
        "nsga_config": {
            "population_size": 100,
            "generations": 50,
            "mutation_rate": 0.1
        },
        "simulation_params": {
            "scenario_seed": [0],
            "simulation_seed": 0,
            "max_iterations": 1500,
            "draw_mode": True,
            "verbose": True
        },
        "description": "Configuração completa para pesquisa"
    }
    
    configs = [
        ("Teste_Rapido.json", test_config),
        ("Producao_Media.json", production_config),
        ("Pesquisa_Pesada.json", research_config)
    ]
    
    import json
    for filename, config in configs:
        config_file = preset_dir / filename
        if not config_file.exists():
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✓ Preset criado: {filename}")
        else:
            print(f"○ Preset já existe: {filename}")

def main():
    """Função principal de configuração."""
    print("=" * 70)
    print("  CONFIGURAÇÃO DO SISTEMA DE SIMULAÇÃO E OTIMIZAÇÃO DE EVACUAÇÃO")
    print("=" * 70)
    print()
    
    # Cria diretórios
    print("📁 Criando diretórios...")
    create_directories()
    print()
    
    # Inicializa banco de dados
    print("🗄️ Inicializando banco de dados...")
    initialize_database()
    print()
    
    # Verifica dependências
    print("📦 Verificando dependências Python...")
    deps_ok = check_dependencies()
    print()
    
    # Verifica estrutura do simulador
    print("🔍 Verificando estrutura do projeto...")
    simulator_ok = check_simulator_structure()
    print()
    
    # Cria configurações de exemplo
    print("📝 Criando presets de configuração...")
    create_example_configs()
    print()
    
    # Resumo
    print("=" * 70)
    print("  RESUMO DA CONFIGURAÇÃO")
    print("=" * 70)
    print()
    
    if deps_ok and simulator_ok:
        print("✅ Sistema configurado com sucesso!")
        print()
        print("🚀 Para iniciar a interface web:")
        print("   streamlit run interface/App.py")
        print()
        print("🔧 Para executar o simulador diretamente (CLI):")
        print("   python -m simulador_heuristica.simulator.main -e <experiment>")
        print()
        print("📚 Documentação disponível em:")
        print("   - README.md (visão geral)")
        print("   - docs/USER_GUIDE.md (guia do usuário)")
        print("   - docs/ARCHITECTURE.md (arquitetura)")
        print("   - docs/API_REFERENCE.md (referência)")
    else:
        print("⚠️ Configuração incompleta. Verifique os erros acima.")
        print()
        if not deps_ok:
            print("  ❌ Instale as dependências faltantes:")
            print("     pip install -r requirements.txt")
        if not simulator_ok:
            print("  ❌ Verifique se todos os arquivos do projeto estão presentes")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()
