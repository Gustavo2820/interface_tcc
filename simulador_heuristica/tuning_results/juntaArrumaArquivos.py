import os

def consolidate_files(input_folder, output_file):
    # Navega pelos arquivos no diretório
    with open(output_file, 'w') as outfile:
        outfile.write("pop_size,crossover,crossover_prob,mutation,mutation_prob,F1,F2,F3\n")
        for filename in os.listdir(input_folder):
            if filename.endswith(".txt"):  # Processa apenas arquivos CSV
                filepath = os.path.join(input_folder, filename)
                with open(filepath, 'r') as infile:
                    next(infile)
                    for line in infile:
                        if not "[0.0, 200.0, 0.0]" in line:
                            line = line.replace("None", "0.0")
                            line = line.replace("[", "")
                            line = line.replace("]", "")
                            line = line.replace("]", "")
                            line = line.replace("HalfUniformCrossover", "HUX")
                            line = line.replace("TwoPointCrossover", "TPX")
                            line = line.replace("UniformCrossover", "UX")
                            line = line.replace("SinglePointCrossover", "SPX")
                            line = line.replace("BitflipMutation", "BFM")
                            line = line.replace("InversionMutation", "IM")
                            outfile.write(line)

# Caminho do diretório com os arquivos e o arquivo de saída
input_folder = os.getcwd()  # Substitua pelo caminho do diretório
output_file = "arquivo_consolidado.csv"  # Nome do arquivo de saída

consolidate_files(input_folder, output_file)
