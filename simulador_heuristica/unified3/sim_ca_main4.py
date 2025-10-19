# -*- coding:utf-8 -*-

import argparse
import json
import random
import numpy as np
import os

from mh_ga_instance import read_instance
from h_brute_force import BruteForce

parser = argparse.ArgumentParser(description='Simulator')

parser.add_argument('-e', action="store", dest='experiment', type=str, required=True, help="Experiment Folder.")

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
    # args = parser.parse_args()


    # instance = read_instance(args.experiment)
    instance = read_instance("cult_experiment")
    # factory = Factory(instance)
    b = BruteForce(instance)
    b.pareto()

