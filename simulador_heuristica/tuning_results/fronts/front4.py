import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

def dominates(p1, p2):
    """Verifica se p1 domina p2 (minimização)."""
    return all(x <= y for x, y in zip(p1, p2)) and any(x < y for x, y in zip(p1, p2))

def fast_non_dominated_sort(points, max_fronts=11):
    """Implementação do algoritmo de classificação de Pareto do NSGA-II com limite de fronteiras."""
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

    # Determina as demais fronteiras até o limite estabelecido
    i = 0
    while len(fronts[i]) > 0 and i < max_fronts - 1:
        next_front = []
        for p in fronts[i]:
            for q in S[p]:
                n[q] -= 1
                if n[q] == 0:
                    rank[q] = i + 1
                    next_front.append(q)
        i += 1
        fronts.append(next_front)

    return fronts[:max_fronts], rank  # Retorna no máximo 11 fronteiras

def smooth_curve(x, y, num_points=200):
    """Cria uma curva suavizada entre os pontos utilizando interpolação cúbica."""
    # Remove duplicatas de F1 e ajusta os valores correspondentes de F2
    unique_x, unique_idx = np.unique(x, return_index=True)
    unique_y = y[unique_idx]
    
    # Se restar menos de 3 pontos após a remoção, não faz interpolação
    if len(unique_x) < 3:
        return unique_x, unique_y

    x_new = np.linspace(min(unique_x), max(unique_x), num_points)
    spline = make_interp_spline(unique_x, unique_y, k=3)  # Interpolação cúbica
    y_smooth = spline(x_new)
    return x_new, y_smooth

def plot_pareto_fronts(df, output_path):
    """Plota as 11 fronteiras de Pareto baseadas em F1 e F2, com curvas suavizadas."""
    points = df[['F1', 'F3']].values  # Apenas as duas primeiras funções objetivo
    pareto_fronts, _ = fast_non_dominated_sort(points, max_fronts=11)

    plt.figure(figsize=(12, 8))
    colors = [
        'red', 'blue', 'green', 'purple', 'orange', 'brown', 
        'pink', 'gray', 'olive', 'cyan', 'magenta'
    ]

    # Plota cada uma das 11 fronteiras com curvas suaves
    for i, front in enumerate(pareto_fronts):
        if not front: 
            continue  # Evita erro se uma fronteira estiver vazia
        front_points = np.array(sorted(points[front], key=lambda x: x[0]))  # Ordena por F1
        x_smooth, y_smooth = smooth_curve(front_points[:, 0], front_points[:, 1])

        plt.plot(x_smooth, y_smooth, linestyle='-', label=f'Fronteira {i+1}', color=colors[i % len(colors)])

    plt.xlabel("F1")
    plt.ylabel("F2")
    plt.title("Fronteiras de Pareto (NSGA-II) - 11 Fronteiras")
    plt.legend()
    plt.grid()

    # Salvando o gráfico
    filename = f"{output_path}/fronteiras_pareto_11_F1_F3.png"
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()

# Caminho do arquivo
file_path = "/home/odraude/Documentos/simulador/tuning_results/fronts"

# Carregar os dados
df = pd.read_csv(file_path + '/arquivo_consolidado.csv')

# Gerar gráfico das 11 fronteiras de Pareto com curvas suavizadas
plot_pareto_fronts(df, file_path)
