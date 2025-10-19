#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificação de dependências do projeto
Verifica se todas as dependências necessárias estão instaladas
"""

import sys
import importlib

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    
    # Dependências obrigatórias
    required_packages = {
        'numpy': 'Computação numérica',
        'matplotlib': 'Visualização de dados', 
        'PIL': 'Processamento de imagens (Pillow)',
        'pymoo': 'Algoritmos evolutivos'
    }
    
    missing_packages = []
    installed_packages = []
    
    print("Verificando dependências...")
    print("-" * 50)
    
    for package, description in required_packages.items():
        try:
            if package == 'PIL':
                # Pillow é importado como PIL
                importlib.import_module('PIL')
                package_name = 'Pillow'
            else:
                importlib.import_module(package)
                package_name = package
                
            installed_packages.append((package_name, description))
            print(f"✅ {package_name:<15} - {description}")
            
        except ImportError:
            missing_packages.append((package, description))
            print(f"❌ {package:<15} - {description} (AUSENTE)")
    
    print("-" * 50)
    
    if missing_packages:
        print(f"\n❌ {len(missing_packages)} dependência(s) ausente(s):")
        for package, description in missing_packages:
            print(f"   - {package}: {description}")
        
        print(f"\n💡 Para instalar as dependências ausentes:")
        print(f"   pip install -r requirements.txt")
        print(f"\n   Ou instale individualmente:")
        for package, _ in missing_packages:
            if package == 'PIL':
                print(f"   pip install Pillow")
            else:
                print(f"   pip install {package}")
        
        return False
    else:
        print(f"\n✅ Todas as {len(installed_packages)} dependências estão instaladas!")
        return True

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    print(f"Python version: {sys.version}")
    
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ é necessário")
        return False
    else:
        print("✅ Versão do Python compatível")
        return True

if __name__ == "__main__":
    print("=" * 60)
    print("VERIFICAÇÃO DE DEPENDÊNCIAS - SIMULADOR DE HEURÍSTICA")
    print("=" * 60)
    
    python_ok = check_python_version()
    deps_ok = check_dependencies()
    
    print("\n" + "=" * 60)
    
    if python_ok and deps_ok:
        print("🎉 Sistema pronto para execução!")
        sys.exit(0)
    else:
        print("⚠️  Corrija os problemas acima antes de executar o projeto")
        sys.exit(1)

