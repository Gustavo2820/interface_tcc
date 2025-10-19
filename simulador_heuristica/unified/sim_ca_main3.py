# -*- coding:utf-8 -*-

import argparse
import json
import random
import numpy as np

from mh_ga_instance import read_instance
from mh_ga_factory import Factory, selector
from mh_ga_nsgaii import nsgaii

parser = argparse.ArgumentParser(description='Simulator')

parser.add_argument('-e', action="store", dest='experiment', type=str, required=True, help="Experiment Folder.")

parser.add_argument(
    '--pop_size', type=int, help='Quantidade de indivíduos em cada geração',
    default=10
)

parser.add_argument(
    '--mut_prob', type=float, help='Probabilidade de mutação em cada geração',
    default=.4
)

parser.add_argument(
    '--max_gen', type=int, help='Numero de gerações para o NSGA-II',
    default=300
)

parser.add_argument(
    '-o', '--out', default='results',
    help='Nome da pasta onde os arquivos de estatística serão salvos'
)

parser.add_argument(
    '--seed', type=int, help='Semente para o gerador de numeros aleatórios', default=75
)

#def save_result(result, instance, filename):
def save_result(result, uncoded, filename):

    with open(filename, 'w+') as outfile:
        solution = []
        for i in range(len(result)):
            solution.append(
                {
                    'qtd_doors': result[i].obj[0],
                    'iterations': result[i].obj[1],
                    'distance': result[i].obj[2],
                    'gene': result[i].gene.configuration,
                    'generation': result[i].generation,
                    'configuration': uncoded[i]
                }
            )
        

        json.dump(solution, outfile, indent=2)

if __name__ == "__main__":
    try:
        args = parser.parse_args()

        random.seed(args.seed)
        np.random.seed(args.seed)
        
        # Verificar se experimento existe
        instance = read_instance(args.experiment)

        factory = Factory(instance)
        results = None

        print(f"Iniciando NSGA-II com {args.pop_size} indivíduos por {args.max_gen} gerações...")
        results = nsgaii(factory, selector, args.pop_size, args.mut_prob,
                             args.max_gen)
        
        uncoded = [factory.uncode(x.gene) for x in results]
        save_result(results, uncoded, 'res.json')
        print(f"Otimização concluída. {len(results)} soluções salvas em res.json")
        
    except FileNotFoundError as e:
        print(f"Erro: Experimento '{args.experiment}' não encontrado.")
        print(f"Verifique se o diretório input/{args.experiment}/ existe.")
        exit(1)
    except ValueError as e:
        print(f"Erro de parâmetros: {e}")
        exit(1)
    except MemoryError as e:
        print(f"Erro de memória: {e}")
        print("Tente reduzir --pop_size ou --max_gen")
        exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        exit(1)
