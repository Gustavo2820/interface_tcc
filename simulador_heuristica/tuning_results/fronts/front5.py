import pandas as pd
import numpy as np

def dominates(p1, p2):
    """Verifica se p1 domina p2 (minimização)."""
    return all(x <= y for x, y in zip(p1, p2)) and any(x < y for x, y in zip(p1, p2))

def fast_non_dominated_sort(points, max_fronts=11):
    """Classificação de Pareto do NSGA-II com limite de fronteiras."""
    fronts = []
    S = [[] for _ in range(len(points))]
    n = [0] * len(points)
    rank = [0] * len(points)

    for p in range(len(points)):
        for q in range(len(points)):
            if dominates(points[p], points[q]):
                S[p].append(q)
            elif dominates(points[q], points[p]):
                n[p] += 1
        if n[p] == 0:
            rank[p] = 0
            if len(fronts) == 0:
                fronts.append([])
            fronts[0].append(p)

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

def generate_frontier_csv(df, output_csv_path):
    """Gera um CSV com a configuração paramétrica, quantidade de pontos em cada fronteira, soma ponderada e normalização."""
    df['config'] = df.apply(lambda row: f"{row['pop_size']},{row['crossover']},{row['crossover_prob']},{row['mutation']},{row['mutation_prob']}", axis=1)
    
    unique_configs = df['config'].unique()
    points = df[['F1', 'F2', 'F3']].values
    pareto_fronts, _ = fast_non_dominated_sort(points, max_fronts=11)
    
    config_counts = {config: [0] * 11 for config in unique_configs}
    
    for i, front in enumerate(pareto_fronts):
        for index in front:
            config = df.iloc[index]['config']
            config_counts[config][i] += 1
    
    # Criar dataframe do CSV
    output_df = pd.DataFrame.from_dict(config_counts, orient='index', columns=[f'qt{i+1}' for i in range(11)])
    output_df.insert(0, 'config', output_df.index)
    output_df.reset_index(drop=True, inplace=True)
    
    # Calcular a soma das quantidades
    output_df['soma_qt'] = output_df[[f'qt{i+1}' for i in range(11)]].sum(axis=1)
    
    # Calcular a soma ponderada
    output_df['soma_ponderada'] = output_df.apply(lambda row: sum(row[f'qt{i+1}'] * (12 - (i+1)) for i in range(11)), axis=1)
    
    # Calcular a normalização
    output_df['normalizacao'] = output_df['soma_ponderada'] / output_df['soma_qt']
    
    output_df.to_csv(output_csv_path, index=False)

# Caminho do arquivo
file_path = "/home/odraude/Documentos/simulador/tuning_results/fronts"

df = pd.read_csv(file_path + '/arquivo_consolidado.csv')
output_csv_path = file_path + '/fronteira_pontos.csv'

generate_frontier_csv(df, output_csv_path)
