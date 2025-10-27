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
    preset_dir.mkdir(parents=True, exist_ok=True)

    import json
    from datetime import datetime
    import copy

    template_path = preset_dir / "Teste_Rapido.json"

    # If a template preset exists, load it, otherwise create a sensible default
    if template_path.exists():
        try:
            with open(template_path, 'r') as f:
                template = json.load(f)
            print(f"✓ Preset base carregado: {template_path.name}")
        except Exception as e:
            print(f"⚠️ Falha ao ler {template_path}: {e}")
            template = None
    else:
        # create a default lightweight template similar to previous behaviour
        template = {
            "preset_name": "Teste Rápido",
            "description": "Configuração leve para testes rápidos e desenvolvimento",
            "simulation_params": {
                "scenario_seed": 42,
                "simulation_seed": 123,
                "max_iterations": 800,
                "draw_mode": False,
                "verbose": False
            },
            "nsga_config": {
                "population_size": 10,
                "generations": 5,
                "crossover_rate": 0.8,
                "mutation_rate": 0.1,
                "use_three_objectives": True
            },
            "bruteforce_config": {
                "max_doors": 10
            },
            "created_at": datetime.now().isoformat(),
            "version": "1.0"
        }
        # write the template to disk
        try:
            with open(template_path, 'w') as f:
                json.dump(template, f, indent=2, ensure_ascii=False)
            print(f"✓ Preset base criado: {template_path.name}")
        except Exception as e:
            print(f"✗ Falha ao criar {template_path}: {e}")

    # Build derived presets from the template
    presets_to_create = []

    # Production preset
    prod = copy.deepcopy(template)
    prod["preset_name"] = "Produção Média"
    prod["description"] = "Configuração balanceada para uso geral"
    # adjust NSGA parameters if present
    if "nsga_config" in prod:
        prod["nsga_config"].update({
            "population_size": 50,
            "generations": 30,
            "mutation_rate": prod["nsga_config"].get("mutation_rate", 0.15)
        })
    # adjust simulation params
    if "simulation_params" in prod:
        prod["simulation_params"].update({
            "max_iterations": max(prod["simulation_params"].get("max_iterations", 1000), 1000),
            "draw_mode": True,
            "verbose": False
        })
    prod["created_at"] = datetime.now().isoformat()
    presets_to_create.append(("Producao_Media.json", prod))

    # Research preset
    research = copy.deepcopy(template)
    research["preset_name"] = "Pesquisa Pesada"
    research["description"] = "Configuração completa para pesquisa"
    if "nsga_config" in research:
        research["nsga_config"].update({
            "population_size": 100,
            "generations": 50,
            "mutation_rate": research["nsga_config"].get("mutation_rate", 0.1)
        })
    if "simulation_params" in research:
        research["simulation_params"].update({
            "max_iterations": max(research["simulation_params"].get("max_iterations", 1500), 1500),
            "draw_mode": True,
            "verbose": True
        })
    research["created_at"] = datetime.now().isoformat()
    presets_to_create.append(("Pesquisa_Pesada.json", research))

    # Write derived presets
    for filename, config in presets_to_create:
        config_file = preset_dir / filename
        if not config_file.exists():
            try:
                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                print(f"✓ Preset criado: {filename}")
            except Exception as e:
                print(f"✗ Falha ao criar {filename}: {e}")
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
        print("   - docs/DEVELOPMENT.md (guia do desenvolvedor - APIs e integrações)")
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
