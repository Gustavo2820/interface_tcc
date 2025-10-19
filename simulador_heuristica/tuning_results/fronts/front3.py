import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def dominates(p1, p2):
    """Verifica se p1 domina p2 (minimização)."""
    return all(x <= y for x, y in zip(p1, p2)) and any(x < y for x, y in zip(p1, p2))

def fast_non_dominated_sort(points):
    """Implementação do algoritmo de classificação de Pareto do NSGA-II."""
    fronts = []
    S = [[] for _ in range(len(points))]
    n = [0] * len(points)
    rank = [0] * len(points)

    # Identifica dominação entre pontos
    for p in range(len(points)):
        for q in range(len(points)):
            if dominates(points[p], points[q]):
                S[p].append(q)
            elif dominates(points[q], points[p]):
                n[p] += 1
        
        # Se um ponto não é dominado, pertence à primeira fronteira
        if n[p] == 0:
            rank[p] = 0
            if len(fronts) == 0:
                fronts.append([])
            fronts[0].append(p)

    # Determina as demais fronteiras
    i = 0
    while len(fronts[i]) > 0:
        next_front = []
        for p in fronts[i]:
            for q in S[p]:
                n[q] -= 1
                if n[q] == 0:
                    rank[q] = i + 1
                    next_front.append(q)
        i += 1
        fronts.append(next_front)

    return fronts[:-1], rank

def plot_pareto_fronts(df, output_path):
    """Plota as fronteiras de Pareto baseadas em F1, F2 e F3 com curvas suaves."""
    points = df[['F1', 'F2', 'F3']].values
    pareto_fronts, _ = fast_non_dominated_sort(points)

    plt.figure(figsize=(10, 7))
    colors = [
        'red', 'blue', 'green', 'purple', 'orange', 'brown', 
        'pink', 'gray', 'olive', 'cyan', 'magenta'
    ]
    # colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']

    # Plota cada fronteira com curvas suaves
    for i, front in enumerate(pareto_fronts):
        front_points = np.array(sorted(points[front], key=lambda x: x[0]))  # Ordena por F1 para suavização
        plt.plot(front_points[:, 0], front_points[:, 1], marker='o', linestyle='-', label=f'Fronteira {i+1}', color=colors[i % len(colors)])

    plt.xlabel("F1")
    plt.ylabel("F2")
    plt.title("Fronteiras de Pareto (NSGA-II)")
    plt.legend()
    plt.grid()

    # Salvando o gráfico
    filename = f"{output_path}/fronteiras_pareto_curvas.png"
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()

# Caminho do arquivo
file_path = "/home/odraude/Documentos/simulador/tuning_results/fronts"

# Carregar os dados
df = pd.read_csv(file_path + '/arquivo_consolidado.csv')

# Gerar gráfico das fronteiras de Pareto com curvas
plot_pareto_fronts(df, file_path)
