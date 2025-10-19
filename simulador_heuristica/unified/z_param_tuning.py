from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem
from pymoo.optimize import minimize

from pymoo.operators.sampling.rnd import BinaryRandomSampling
from pymoo.operators.crossover.pntx import TwoPointCrossover, SinglePointCrossover
from pymoo.operators.crossover.ux import UniformCrossover
from pymoo.operators.crossover.hux import HalfUniformCrossover
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.operators.mutation.inversion import InversionMutation

import numpy as np
import os

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

crossover_methods = [
    (UniformCrossover, {"prob": [0.5, 0.7, 1.0]}),
    (SinglePointCrossover, {"prob": [0.7, 0.9, 1.0]}),
    (TwoPointCrossover, {"prob": [0.7, 0.9, 1.0]}),
    (HalfUniformCrossover, {}),
]
mutation_methods = [
    (BitflipMutation, {"prob": [0.01, 0.05, 0.1]}),
    (InversionMutation, {"prob": [0.01, 0.05, 0.1]})
]
population_sizes = [50, 100, 200]

instance = read_instance("tuning_cult_experiment")
problem = ScenarioOptimizationProblem(instance)

# Arquivo para salvar os resultados
output_file = "tuning_results.txt"

# Loop de tuning
with open(output_file, "w") as file:
    # Cabeçalho do arquivo
    file.write("pop_size,crossover,crossover_prob,mutation,mutation_prob,F\n")

    for population_size in population_sizes:
        for crossover_cls, crossover_params in crossover_methods:
            for mutation_cls, mutation_params in mutation_methods:
                # Gera combinações de parâmetros
                crossover_probs = crossover_params.get("prob", [None])
                mutation_probs = mutation_params.get("prob", [None])

                for crossover_prob in crossover_probs:
                    for mutation_prob in mutation_probs:
                        # Define os operadores com os parâmetros
                        crossover_operator = crossover_cls(prob=crossover_prob) if crossover_prob else crossover_cls()
                        mutation_operator = mutation_cls(prob=mutation_prob) if mutation_prob else mutation_cls()

                        # Cria o algoritmo NSGA-II
                        algorithm = NSGA2(
                            pop_size=population_size,
                            sampling=BinaryRandomSampling(),
                            crossover=crossover_operator,
                            mutation=mutation_operator
                        )

                        # Avalia a configuração
                        print(f"Running: pop_size={population_size}, crossover={crossover_cls.__name__}, "
                              f"crossover_prob={crossover_prob}, mutation={mutation_cls.__name__}, mutation_prob={mutation_prob}")
                        res = minimize(
                            problem,
                            algorithm,
                            termination=('n_gen', 100),
                            seed=42,
                            verbose=False
                        )

                        # Salva os resultados no arquivo
                        for obj_values in res.F:
                            file.write(
                                f"{population_size},{crossover_cls.__name__},{crossover_prob},"
                                f"{mutation_cls.__name__},{mutation_prob},{list(obj_values)}\n"
                            )

                        file.flush()
                        os.fsync()