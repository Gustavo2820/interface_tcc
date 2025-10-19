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
    default=200
)

parser.add_argument(
    '--mut_prob', type=float, help='Probabilidade de mutação em cada geração',
    default=.1
)

# parser.add_argument(
    # '--cross_prob', type=float, help='Probabilidade de mutação em cada geração',
    # default=.1
# )

parser.add_argument(
    '--max_gen', type=int, help='Numero de gerações para o NSGA-II',
    # default=300
    default=50
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
    args = parser.parse_args()
    instance = read_instance(args.experiment)

    # seeds1 = [1,2,3,4,5,6]
    # seeds2 = [7,8,9,10,11,12]
    # seeds3 = [13,14,15,16,17,18]
    # seeds4 = [19,20,21,22,23,24]
    # seeds5 = [25,26,27,28,29,30]
    for seed_escolhida in seeds:
        random.seed(seed_escolhida)
        np.random.seed(seed_escolhida)
        factory = Factory(instance)
        results = None

        results = nsgaii(factory, selector, args.pop_size, args.mut_prob,
                            args.max_gen)
        
        uncoded = [factory.uncode(x.gene) for x in results]
        save_result(results, uncoded, f'res{seed_escolhida}.json')
