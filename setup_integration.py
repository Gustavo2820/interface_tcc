#!/usr/bin/env python3
"""
Script de configuração da integração entre interface e simulador.

Este script configura o ambiente necessário para a integração,
criando diretórios, inicializando o banco de dados e verificando dependências.
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
        "simulador_heuristica/input",
        "simulador_heuristica/output",
        "temp_simulation",
        "temp_nsga",
        "mapas"
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
        "streamlit",
        "numpy",
        "pandas",
        "PIL"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} instalado")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} não encontrado")
    
    if missing_packages:
        print(f"\n⚠️ Pacotes faltando: {', '.join(missing_packages)}")
        print("Execute: pip install " + " ".join(missing_packages))
        return False
    
    return True

def check_simulator_structure():
    """Verifica se a estrutura do simulador está correta."""
    required_files = [
        "simulador_heuristica/simulator/main.py",
        "simulador_heuristica/simulator/simulator.py",
        "simulador_heuristica/unified/mh_ga_nsgaii.py",
        "modulo_criacao_mapas/map_converter_utils.py",
        "modulo_criacao_mapas/map_converter.py"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path} encontrado")
        else:
            missing_files.append(file_path)
            print(f"✗ {file_path} não encontrado")
    
    if missing_files:
        print(f"\n⚠️ Arquivos do simulador faltando: {missing_files}")
        return False
    
    return True

def create_example_configs():
    """Cria arquivos de configuração de exemplo."""
    
    # Configuração de exemplo para NSGA-II
    nsga_config = {
        "population_size": 20,
        "generations": 10,
        "crossover_rate": 0.8,
        "mutation_rate": 0.1,
        "description": "Configuração de exemplo para NSGA-II"
    }
    
    config_file = Path("uploads/nsga_ii/example_config.json")
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    import json
    with open(config_file, 'w') as f:
        json.dump(nsga_config, f, indent=2)
    
    print(f"✓ Arquivo de configuração de exemplo criado: {config_file}")

def main():
    """Função principal de configuração."""
    print("🚀 Configurando integração entre interface e simulador...\n")
    
    # Cria diretórios
    print("📁 Criando diretórios...")
    create_directories()
    print()
    
    # Inicializa banco de dados
    print("🗄️ Inicializando banco de dados...")
    initialize_database()
    print()
    
    # Verifica dependências
    print("📦 Verificando dependências...")
    deps_ok = check_dependencies()
    print()
    
    # Verifica estrutura do simulador
    print("🔍 Verificando estrutura do simulador...")
    simulator_ok = check_simulator_structure()
    print()
    
    # Cria configurações de exemplo
    print("📝 Criando configurações de exemplo...")
    create_example_configs()
    print()
    
    # Resumo
    print("=" * 50)
    print("📋 RESUMO DA CONFIGURAÇÃO")
    print("=" * 50)
    
    if deps_ok and simulator_ok:
        print("✅ Integração configurada com sucesso!")
        print("\nPara executar a interface:")
        print("  streamlit run interface/App.py")
        print("\nPara executar o simulador diretamente:")
        print("  python -m simulador_heuristica.simulator.main -e cult_experiment")
    else:
        print("⚠️ Configuração incompleta. Verifique os erros acima.")
        if not deps_ok:
            print("  - Instale as dependências faltantes")
        if not simulator_ok:
            print("  - Verifique se todos os arquivos do simulador estão presentes")
    
    print("\n📚 Documentação disponível em: docs/integration/")

if __name__ == "__main__":
    main()
