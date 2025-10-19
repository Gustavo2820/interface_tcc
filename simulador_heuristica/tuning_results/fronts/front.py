
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Função para carregar os dados
def load_data(file_path):
    df = pd.read_csv(file_path)
    
    # Dicionário para armazenar os resultados
    result_dict = {}
    
    # Iterando sobre as linhas do dataframe
    for _, row in df.iterrows():
        # Montando a chave como a combinação dos parâmetros
        key = f"{row['pop_size']},{row['crossover']},{row['crossover_prob']},{row['mutation']},{row['mutation_prob']}"
        
        # Adicionando a lista [F1, F2, F3] ao dicionário
        if key not in result_dict:
            result_dict[key] = []
        
        result_dict[key].append([row['F1'], row['F2'], row['F3']])
        # Ordenando os vetores dentro de cada chave conforme F1
        for key in result_dict:
            result_dict[key] = sorted(result_dict[key], key=lambda x: x[0])  # x[0] é o valor de F1

    return result_dict


def fast_non_dominated_sort(solution_set):
    """Sort the chromosomes into non dominated fronts.

    In a multi objective optimization problem the solutions are given in a set,
    the solutions that belongs to this set are no better than each other since
    one cannot get better for a given objective function without getting worse
    in other. In a given population one solution dominates another solution
    olny and if only all of its objective values are better than the oter.
    Therefore in a multi objective genetic algorithm the non dominating
    solutions must be separated into sets and those sets sorted in order of
    dominance.

    Parameters
    ----------
    solution_set: set of chromosome
        An unordered set containing a population of individuals that must be
        sorted.

    Returns
    -------
    list of chromosome list
        Each chromosome list represents a non dominated front.
    """
    frontier = [set(), ]
    # p: [set of solutions dominated by p, number of solutions dominating p]
    dominated_by = {x: [set(), 0] for x in solution_set}
    for solution_p in solution_set:
        for solution_q in solution_set:
            if solution_p <= solution_q:
                dominated_by[solution_p][0].add(solution_q)
            elif solution_q <= solution_p:
                dominated_by[solution_p][1] += 1
        # if p is not dominated it belongs to the pareto frontier
        if dominated_by[solution_p][1] == 0:
            frontier[0].add(solution_p)
            solution_p.rank = 0
    i = 0
    while True:
        new_front = set()
        for solution_p in frontier[i]:
            for solution_q in dominated_by[solution_p][0]:
                dominated_by[solution_q][1] -= 1
                if dominated_by[solution_q][1] == 0:
                    solution_q.rank = i + 1
                    new_front.add(solution_q)
        # stops when there is no solution to be added in this front
        if not new_front:
            break
        frontier.append(new_front)
        i += 1
    return [[y for y in x] for x in frontier]

# Caminho para o arquivo
file_path = "/home/odraude/Documentos/simulador/tuning_results/plots"

# Carregar os dados
data = load_data(file_path + '/arquivo_consolidado.csv')

plot_all_occurrences(data, file_path)

# keys = list(data.keys())
# values = list(data.values())
# n = len(keys)
# for i in range(n):
#     for j in range(i + 1, n):
#         key1, value1 = keys[i], values[i]
#         key2, value2 = keys[j], values[j]
#         plot_two_occurrences(key1, value1, key2, value2, file_path)

