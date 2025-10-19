from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem
from pymoo.optimize import minimize

from pymoo.operators.sampling.rnd import BinaryRandomSampling
from pymoo.operators.crossover.hux import HalfUniformCrossover
from pymoo.operators.mutation.bitflip import BitflipMutation

import numpy as np

from sim_ca_simulator import Simulator
from sim_ca_scenario import Scenario
from mh_ga_instance import read_instance

class ScenarioOptimizationProblem(Problem):
    def __init__(self, instance):
        self.instance = instance
        scen = Scenario(instance.experiment)
        self.exits = scen.doors_configurations
        n = len(self.exits)
        
        # Definimos um problema com 3 objetivos e 'n' variáveis binárias
        super().__init__(n_var=n, n_obj=3, n_constr=0, xl=0, xu=1, type_var=bool)
    
    def _evaluate(self, x, out, *args, **kwargs):
        results = np.apply_along_axis(self.decode, 1, x)
        out["F"] = results

    def decode(self, gene):
        doors = [self.exits[i] for i in range(len(gene)) if gene[i]]
        
        iters = []
        distances = []
        scen = Scenario(self.instance.experiment, doors, self.instance.draw,
                        self.instance.scenario_seed[0], self.instance.simulation_seed)
        simulator = Simulator(scen)
        
        iterations, qtdDistance = simulator.simulate()
        iters.append(iterations)
        distances.append(qtdDistance)

        for current_seed in self.instance.scenario_seed[1:]:
            scen.scenario_reset(current_seed, self.instance.simulation_seed)
            simulator = Simulator(scen)
            iterations, qtdDistance = simulator.simulate()
            iters.append(iterations)
            distances.append(qtdDistance)

        avg_iters = sum(iters) / len(iters)
        avg_distance = sum(distances) / len(distances)
        
        return len(doors), avg_iters, avg_distance


np.set_printoptions(precision=6, suppress=True)


instance = read_instance("balada_experiment")
problem = ScenarioOptimizationProblem(instance)

# Arquivo para salvar os resultados
output_file = "balada_results"
# seeds1 = [1,2,3,4,5,6,7,8,9,10]
# seeds2 = [11,12,13,14,15,16,17,18,19,20]
# seeds3 = [21,22,23,24,25,26,27,28,29,30]

for seed_escolhida in seeds:
    # Loop de tuning
    with open(output_file + '_s' + str(seed_escolhida) + '.txt', "w") as file:
        # Cabeçalho do arquivo
        file.write("seed, F\n")

        # Cria o algoritmo NSGA-II
        algorithm = NSGA2(
            pop_size=200,
            sampling=BinaryRandomSampling(),
            crossover=HalfUniformCrossover(),
            mutation=BitflipMutation(prob=0.1)
        )
        res = minimize(
            problem,
            algorithm,
            termination=('n_gen', 50),
            seed=seed_escolhida,
            verbose=False
        )

        # Salva os resultados no arquivo
        for obj_values in res.F:
            file.write(f"{seed_escolhida},{list(obj_values)}\n")

        file.flush()
