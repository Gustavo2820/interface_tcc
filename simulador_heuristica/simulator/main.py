# -*- coding:utf-8 -*-

import argparse
import cProfile as profile
import json
import pstats
import random
import os

from .crowd_map import CrowdMap
from .individual import Individual
from .dinamic_map import DinamicMap
from .simulator import Simulator
from .static_map import StaticMap
from .structure_map import StructureMap
from .wall_map import WallMap
from .scenario import Scenario

parser = argparse.ArgumentParser(description='Simulator')
parser.add_argument('-e', action="store", dest='experiment', type=str, required=True, help="Experiment Folder.")
parser.add_argument('-d', action="store_const", dest='draw', const=True, default=False, help="Enable Draw Mode.")
parser.add_argument('-m', action="store", dest='scenario_seed', type=int, required=False, help="Seed to generate the scenario.")
parser.add_argument('-s', action="store", dest='simulation_seed', type=int, required=False, help="Seed to guide the simulation.")

if __name__ == "__main__":
    args = parser.parse_args()

    # p = profile.Profile()
    # p.enable()

    if args.scenario_seed:
        random.seed(args.scenario_seed)

    sep = os.path.sep
    # Base paths on this file location to avoid dependence on process CWD
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + sep

    structure_map = StructureMap(args.experiment, root_path + "input" + sep + args.experiment + sep + "map.txt")
    structure_map.load_map()

    wall_map = WallMap(args.experiment, structure_map)
    wall_map.load_map()
    if (args.draw):
        wall_map.draw_map(root_path + "input" + sep + args.experiment)

    static_map = StaticMap(args.experiment, structure_map)
    static_map.load_map()
    if (args.draw):
        static_map.draw_map(root_path + "input" + sep + args.experiment)
  
    individuals = []
    with open(root_path + "input" + sep + args.experiment + sep + "individuals.json", 'r') as json_file:
        data = json.load(json_file)
        
        # Handle both formats: direct array or caracterizations object
        if isinstance(data, list):
            # Direct array format - each item is an individual
            for individual_data in data:
                # Convert color array to separate red, green, blue fields if needed
                if 'color' in individual_data and isinstance(individual_data['color'], list):
                    individual_data['red'] = individual_data['color'][0]
                    individual_data['green'] = individual_data['color'][1]
                    individual_data['blue'] = individual_data['color'][2]
                individuals.append(Individual(individual_data, individual_data.get('row', 0), individual_data.get('col', 0)))
        else:
            # Expected format with caracterizations
            for caracterization in data['caracterizations']:
                for _ in range(caracterization['amount']):
                    individuals.append(Individual(caracterization, 0, 0))

    if args.simulation_seed:
        random.seed(args.simulation_seed)      

    crowd_map = CrowdMap(args.experiment, structure_map)
    crowd_map.load_map(individuals)
    if (args.draw):
        crowd_map.draw_map(root_path + "output" + sep + args.experiment, 0)
    dinamic_map = DinamicMap(args.experiment, structure_map)
    dinamic_map.load_map()

    # SIMULATOR
    directory = root_path + "output" + sep + args.experiment
    scen = Scenario(args.experiment, args.draw, args.scenario_seed or 0, args.simulation_seed or 0)
    simulator = Simulator(scen)
    iterations, qtdDistance = simulator.simulate()

    print("qtd iteracoes " + str(iterations))
    print("qtd distancia " + str(qtdDistance))
    # p.disable()
    # pstats.Stats(p).sort_stats('cumulative').print_stats(30)
