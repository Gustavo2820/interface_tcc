
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


def plot_two_occurrences(occurrence_1, occurrence_2):
    # Extraindo os valores de F1, F2 e F3
    f1_1, f2_1, f3_1 = np.array(occurrence_1).T  # Transposta para dividir os valores em colunas
    f1_2, f2_2, f3_2 = np.array(occurrence_2).T  # Transposta para dividir os valores em colunas

    # Plotando as duas linhas
    plt.plot(f1_1, f2_1, 'o-', label="Ocorrência 1 (F1 vs F2)")
    plt.plot(f1_2, f2_2, 'x-', label="Ocorrência 2 (F1 vs F2)")
    
    # Adicionando título e rótulos aos eixos
    plt.title("Comparação entre duas ocorrências (F1 vs F2)")
    plt.xlabel("F1")
    plt.ylabel("F2")
    
    # Adicionando uma legenda
    plt.legend()
    
    # Exibindo o gráfico
    plt.show()


# Caminho para o arquivo
file_path = "/home/odraude/Documentos/simulador/tuning_results/plots/arquivo_consolidado.csv"

# Carregar os dados
data = load_data(file_path)

# Exibir uma amostra do dicionário
for key, value in list(data.items())[:2]:  # Mostrar apenas os dois primeiros itens
    print(f"{key}: {value}")

plot_two_occurrences(list(data.values())[0], list(data.values())[1])
