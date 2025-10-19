# Guia de Integração: Interface + Simulador Heurística

Este documento orienta como integrar a pasta `interface/` (Streamlit) com o núcleo de simulação em `simulador_heuristica/`, preservando a lógica, formatos de arquivos e comportamento atual.

- Público-alvo: novos desenvolvedores
- Não altera código existente; apenas descreve fluxos e pontos de contato

## Sumário
- Visão geral e papéis dos módulos
- Pontos de integração e fluxo de dados
- Como acionar o simulador a partir da interface (exemplos)
- Boas práticas de organização
- Referências (links para documentação existente)
- Documentos auxiliares: [steps.md](./steps.md), [examples.md](./examples.md)

---

## 1) Resumo dos Módulos e Responsabilidades

### Interface (`interface/`)
- `App.py`: ponto de entrada do Streamlit; define layout e navegação. Referência: [`docs/interface_docs/App.py.md`](../interface_docs/App.py.md)
- `pages/Algoritmo_Genetico.py`: upload de arquivos de parametrização para algoritmo genético simples. Salva em `uploads/algoritmo_genetico/`.
- `pages/NSGA_II.py`: upload de configuração do NSGA-II. Salva em `uploads/nsga_ii/`. Referência: [`docs/interface_docs/pages/NSGA_II.py.md`](../interface_docs/pages/NSGA_II.py.md)
- `pages/Forca_Bruta.py`: upload de arquivos para busca exaustiva. Salva em `uploads/forca_bruta/`.

Características comuns das páginas de parâmetros:
- Aceitam `.json`, `.csv`, `.txt`
- Persistem os uploads preservando o nome do arquivo

### Simulador (`simulador_heuristica/`)
- `simulator/main.py`: script CLI que constrói mapas, carrega indivíduos e roda `Simulator`. Entrada principal via argumentos `-e` (experimento), `-d` (desenho), `-m` e `-s` (seeds). Lê de `input/<experiment>/` e escreve em `output/<experiment>/`.
- `simulator/simulator.py`: classe `Simulator` que executa iterações, manipula mapas dinâmicos e gera logs/HTML de resultado.
- Estrutura de I/O padrão do simulador:
  - Entrada: `input/<experiment>/map.txt`, `input/<experiment>/individuals.json`
  - Saída: `output/<experiment>/` (mapas desenhados, HTML de relatório, métricas)
- NSGA-II (suporte de algoritmo multiobjetivo): implementação genérica em `unified/mh_ga_nsgaii.py` (fábrica e operadores devem ser fornecidos pela aplicação).

Referências:
- Guia do simulador: [`simulador_heuristica/README.md`](../../simulador_heuristica/README.md)
- Entradas exemplo: `simulador_heuristica/input/`
- Núcleo de simulação: [`simulador_heuristica/simulator/main.py`](../../simulador_heuristica/simulator/main.py), [`simulador_heuristica/simulator/simulator.py`](../../simulador_heuristica/simulator/simulator.py)
- NSGA-II genérico: [`simulador_heuristica/unified/mh_ga_nsgaii.py`](../../simulador_heuristica/unified/mh_ga_nsgaii.py)

---

## 2) Pontos de Integração Claros

### 2.1 Como a interface envia/recebe dados
- Uploads de parâmetros/arquivos feitos nas páginas `pages/*.py` são salvos em:
  - `uploads/algoritmo_genetico/`
  - `uploads/nsga_ii/`
  - `uploads/forca_bruta/`
- Para o simulador ler, é necessário disponibilizar arquivos nos diretórios esperados:
  - `simulador_heuristica/input/<experiment>/map.txt`
  - `simulador_heuristica/input/<experiment>/individuals.json`
- O simulador gera saídas em:
  - `simulador_heuristica/output/<experiment>/` (inclui HTML de relatório e quadros de mapas)

### 2.2 Funções/arquivos “pontos de contato”
- Interface → Sistema de arquivos: `st.file_uploader` grava em `uploads/…`
- Orquestração recomendada (utilitário externo ou função auxiliar nova, sem alterar os existentes):
  - Copiar/montar arquivos dos uploads para `simulador_heuristica/input/<experiment>/`
  - Invocar `simulador_heuristica/simulator/main.py` via CLI (subprocesso) ou importar e chamar a lógica equivalente
- Leitura de resultados: consumir arquivos gerados em `simulador_heuristica/output/<experiment>/` (HTML, imagens, métricas) para exibir na interface

---

## 3) Fluxos de Uso Recomendados

### Fluxo A: Simulação de cenário (sem otimização)
1. Na interface, disponibilize upload de `map.txt` e `individuals.json` (pode ser uma página dedicada a mapas/parâmetros).
2. Após uploads, copie-os para `simulador_heuristica/input/<experiment>/` (defina `<experiment>` como um nome único, p.ex. timestamp ou ID do projeto do usuário).
3. Execute o simulador para o `<experiment>`:
   - CLI: `python -m simulador_heuristica.simulator.main -e <experiment> [-d] [-m <seed>] [-s <seed>]`
4. Quando finalizar, leia `simulador_heuristica/output/<experiment>/` e exiba o HTML/estatísticas.

### Fluxo B: Otimização com NSGA-II
1. Na interface, receba um arquivo de parâmetros do NSGA-II em `uploads/nsga_ii/`.
2. Traduza os parâmetros (sem alterar formato) para construir uma "instância" do problema e uma `ChromosomeFactory` compatível (em um módulo seu, novo, fora do simulador).
3. Utilize `unified/mh_ga_nsgaii.py` para rodar o NSGA-II com sua fábrica e um seletor; para avaliar soluções, chame o simulador (Fluxo A) para cada gene quando necessário.
4. Colete o front de Pareto retornado e apresente opções/soluções ao usuário.

Diagrama textual do Fluxo B:
```
[Interface uploads NSGA-II params]
        ↓
[Parser de params] → [Factory/Selector (seu módulo)]
        ↓                           ↘
     [NSGA-II]  →→ (avaliação) →→  [Chamada do simulador p/ cada gene]
        ↓
[Front de Pareto] → [Exibição/Download]
```

---

## 4) Exemplos Práticos (pseudo-código)

Veja também: [examples.md](./examples.md)

### 4.1 Copiar uploads para a pasta de entrada do simulador
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

### 4.2 Disparar o simulador via subprocesso (CLI estável)
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

### 4.3 Consumir resultados gerados
```python
from pathlib import Path

def read_results(experiment_name: str) -> dict:
    out_dir = Path("simulador_heuristica") / "output" / experiment_name
    report_html = next(out_dir.glob("*.html"), None)
    frames = sorted(out_dir.glob("*.png"))
    return {"report": report_html, "frames": frames}
```

### 4.4 Loop de avaliação para NSGA-II (esboço)
```python
# Dentro da sua ChromosomeFactory.build(...):
# 1) decodificar gene → gerar/posicionar portas
# 2) escrever map.txt e individuals.json p/ experimento temporário
# 3) rodar simulador (run_simulator_cli)
# 4) ler resultados (tempo, distância) e retornar Chromosome(..., obj=[tempo, distancia])
```

Observação: mantenha os formatos atuais de `map.txt` e `individuals.json` exatamente como os exemplos da pasta `input/`.

---

## 5) Boas Práticas de Organização
- **Separação de responsabilidades**: mantenha adaptação/parse de parâmetros em um módulo à parte (p.ex., `interface/services/`), sem alterar `simulador_heuristica/`.
- **Nomes de experimentos únicos**: use timestamps/UUIDs para evitar colisões em `input/` e `output/`.
- **Idempotência**: copie arquivos de upload sem renomear campos internos; preserve o formato e a estrutura.
- **Limpeza opcional**: crie rotina (manual) para limpar pastas antigas de `output/`/`input/`, sem impactar execuções ativas.
- **Logs e erros**: capture return codes ao chamar o simulador; exiba mensagens amigáveis na interface.
- **Não alterar contratos**: não modifique nomes/formatos de arquivos esperados pelo simulador.

---

## 6) Diagramas Simples de Fluxo

### Execução direta de simulação
```
[Upload map.txt/individuals.json] → [Copiar p/ input/<exp>] → [Rodar simulador]
                                               ↓
                                      [output/<exp>/...] → [Exibir na interface]
```

### Integração NSGA-II
```
[Upload params NSGA-II] → [Factory/Selector (seu módulo)] → [NSGA-II]
                                         ↘ (para avaliar)
                                 [Preparar input/<exp> + rodar simulador]
```

---

## 7) Referências e Links Relativos
- Interface
  - `App.py`: [`docs/interface_docs/App.py.md`](../interface_docs/App.py.md)
  - `pages/NSGA_II.py`: [`docs/interface_docs/pages/NSGA_II.py.md`](../interface_docs/pages/NSGA_II.py.md)
- Simulador
  - Guia: [`simulador_heuristica/README.md`](../../simulador_heuristica/README.md)
  - Entrada/saída esperadas: exemplos em [`simulador_heuristica/input/`](../../simulador_heuristica/input/)
  - Execução: [`simulador_heuristica/simulator/main.py`](../../simulador_heuristica/simulator/main.py)
  - Núcleo: [`simulador_heuristica/simulator/simulator.py`](../../simulador_heuristica/simulator/simulator.py)
  - NSGA-II genérico: [`simulador_heuristica/unified/mh_ga_nsgaii.py`](../../simulador_heuristica/unified/mh_ga_nsgaii.py)

---

## 8) Checklist de Integração ✅

### Implementação Concluída
- ✅ Arquivos de upload disponíveis e copiados para `simulador_heuristica/input/<experiment>/`
- ✅ Execução do simulador concluída sem erros (CLI ou import)
- ✅ Resultados localizados em `simulador_heuristica/output/<experiment>/` e exibidos na interface
- ✅ Para NSGA-II: fábrica/avaliador usam o simulador sem alterar seus contratos
- ✅ Integração com banco de dados SQLite para persistência
- ✅ Interface de usuário aprimorada com feedback visual
- ✅ Validação de arquivos e tratamento de erros
- ✅ Script de configuração automática
- ✅ **NOVO**: Integração completa do módulo de criação de mapas
- ✅ **NOVO**: Editor de mapas pixel art integrado
- ✅ **NOVO**: Conversor de imagens PNG para arquivos .map
- ✅ **NOVO**: Templates pré-definidos e estatísticas de mapas

### Como Executar a Integração

1. **Configuração Inicial:**
   ```bash
   python setup_integration.py
   ```

2. **Executar Interface:**
   ```bash
   streamlit run interface/App.py
   ```

3. **Criar Mapas:**
   - Acesse a página "Criação de Mapas"
   - Use o editor pixel art ou converta imagens PNG
   - Configure templates e dimensões
   - Salve mapas para uso em simulações

4. **Navegar para Simulação:**
   - Acesse a página "Simulação" 
   - Selecione um mapa (criado ou existente)
   - Faça upload do arquivo de indivíduos
   - Configure parâmetros
   - Clique em "Executar Simulação"

5. **Executar NSGA-II:**
   - Acesse "Parâmetros" → "NSGA-II"
   - Faça upload da configuração
   - Faça upload do mapa e indivíduos
   - Configure parâmetros de otimização
   - Clique em "Executar Otimização NSGA-II"

### Arquivos Criados/Modificados

**Novos Módulos:**
- `interface/services/simulator_integration.py` - Integração com simulador
- `interface/services/nsga_integration.py` - Integração com NSGA-II
- `interface/services/map_creation_integration.py` - **NOVO**: Integração com módulo de criação de mapas
- `setup_integration.py` - Script de configuração

**Páginas Atualizadas:**
- `interface/pages/Simulação.py` - Integração completa
- `interface/pages/Resultados.py` - Dados do banco
- `interface/pages/NSGA_II.py` - Otimização multiobjetivo
- `interface/pages/Criacao_Mapas.py` - **NOVO**: Editor de mapas pixel art
- `interface/pages/Documentação.py` - **NOVO**: Documentação completa
- `interface/App.py` - Menu atualizado
- `interface/pages/Mapas.py` - Link para criação de mapas

**Documentação:**
- `docs/integration/implementation_log.md` - Log detalhado
- `docs/integration/steps.md` - Atualizado com implementação
- `docs/integration/map_creation_integration.md` - **NOVO**: Documentação da integração de mapas


