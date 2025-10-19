# -*- coding:utf-8 -*-

import argparse

from mh_ga_instance import read_instance
from h_brute_force import BruteForce

parser = argparse.ArgumentParser(description='Simulator')

parser.add_argument('-e', action="store", dest='experiment', type=str, required=True, help="Experiment Folder.")


#Rodar com nohup e direcionar para arquivo especifico
if __name__ == "__main__":
    instance = read_instance("cult_experiment")
    b = BruteForce(instance)
    b.pareto()

