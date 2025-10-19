# Exemplos de Integração (snippets e fluxos)

Estes exemplos demonstram como integrar a interface (uploads) ao simulador, preservando lógica e formatos atuais. Use-os como referência para implementar utilitários externos ou camadas de orquestração.

## 1) Preparar a pasta de experimento a partir de uploads
```python
from pathlib import Path
import shutil

def prepare_experiment_from_uploads(experiment_name: str, map_file_path: Path, individuals_file_path: Path) -> Path:
    base = Path("simulador_heuristica")
    in_dir = base / "input" / experiment_name
    in_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(map_file_path, in_dir / "map.txt")
    shutil.copy2(individuals_file_path, in_dir / "individuals.json")
    return in_dir
```

## 2) Rodar o simulador via CLI (subprocesso)
```python
import subprocess, sys

def run_simulator_cli(experiment_name: str, draw: bool = False, scenario_seed: int | None = None, simulation_seed: int | None = None):
    cmd = [sys.executable, "-m", "simulador_heuristica.simulator.main", "-e", experiment_name]
    if draw:
        cmd.append("-d")
    if scenario_seed is not None:
        cmd += ["-m", str(scenario_seed)]
    if simulation_seed is not None:
        cmd += ["-s", str(simulation_seed)]
    subprocess.run(cmd, check=True)
```

## 3) Ler resultados do simulador
```python
from pathlib import Path

def read_results(experiment_name: str) -> dict:
    out_dir = Path("simulador_heuristica") / "output" / experiment_name
    report_html = next(out_dir.glob("*.html"), None)
    frames = sorted(out_dir.glob("*.png"))
    return {"report": report_html, "frames": frames}
```

## 4) Fluxo completo de simulação (sem otimização)
```python
from datetime import datetime

exp = datetime.now().strftime("exp_%Y%m%d_%H%M%S")
# map_file_path e individuals_file_path são caminhos de arquivos enviados pela interface
prepare_experiment_from_uploads(exp, map_file_path, individuals_file_path)
run_simulator_cli(exp, draw=False)
results = read_results(exp)
# results["report"] pode ser exibido na interface; frames podem ser animados
```

## 5) Esboço de avaliação dentro de NSGA-II
```python
# Dentro da sua ChromosomeFactory:
# - decode(gene): traduz gene para arranjo de portas no map.txt
# - build(...):
#   1) gerar map.txt/individuals.json para um experimento temporário
#   2) run_simulator_cli(exp)
#   3) ler métricas do output e montar obj = [tempo, distancia]
#   4) retornar Chromosome(generation, gene, obj)
```

## 7) Criação de Mapas com Editor Pixel Art

### Criar mapa a partir de template
```python
from interface.services.map_creation_integration import map_creation_service

# Criar sala simples
map_data = map_creation_service.create_map_from_template('room', 20, 20)

# Criar corredor
map_data = map_creation_service.create_map_from_template('corridor', 15, 30)

# Criar mapa vazio
map_data = map_creation_service.create_map_from_template('empty', 25, 25)
```

### Converter imagem PNG em mapas
```python
# Validar imagem primeiro
is_valid, message = map_creation_service.validate_map_image('meu_mapa.png')

if is_valid:
    # Converter imagem
    files = map_creation_service.convert_image_to_maps('meu_mapa.png', 'output')
    
    # Arquivos gerados: output.map, output_fogo.map, output_vento.map
    for key, filename in files.items():
        print(f"Arquivo {key}: {filename}")
else:
    print(f"Imagem inválida: {message}")
```

### Obter estatísticas do mapa
```python
# Calcular estatísticas
stats = map_creation_service.get_map_statistics(map_data)

print(f"Paredes: {stats['Parede']} pixels ({stats['Parede_percent']}%)")
print(f"Espaço vazio: {stats['Espaço vazio']} pixels ({stats['Espaço vazio_percent']}%)")
print(f"Saídas: {stats['Porta/Saída']} pixels")
```

### Salvar mapa no diretório
```python
# Salvar mapa criado
saved_path = map_creation_service.save_map_to_directory(map_data, 'meu_mapa')
print(f"Mapa salvo em: {saved_path}")
```

## 8) Fluxos de Uso do Editor de Mapas

### Fluxo A: Criação de mapa personalizado
```
[Configurar dimensões] → [Selecionar template] → [Editor pixel art] → [Preview] → [Salvar/Download]
```

### Fluxo B: Conversão de imagem existente
```
[Upload PNG] → [Validação] → [Conversão] → [Download arquivos .map]
```

### Fluxo C: Integração com simulação
```
[Criar mapa] → [Salvar no diretório] → [Usar em simulação] → [Analisar resultados]
```
