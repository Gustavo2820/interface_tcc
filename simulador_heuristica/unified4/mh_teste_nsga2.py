from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
# from pymoo.operators.sampling.  import BinaryRandomSampling
# from pymoo.operators.crossover. bin_two_point import TwoPointCrossover
# from pymoo.operators.mutation. bin_bitflip import BinaryBitflipMutation
# from pymoo.operators import get_sampling, get_crossover, get_mutation

from pymoo.operators.sampling.rnd import BinaryRandomSampling
from pymoo.operators.crossover.pntx import TwoPointCrossover
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


if __name__ == "__main__":
    
    # args = parser.parse_args()
    # instance = read_instance(args.experiment)
    instance = read_instance("cult_experiment")
    problem = ScenarioOptimizationProblem(instance)

    algorithm = NSGA2(pop_size=20,
                  sampling=BinaryRandomSampling(),
                  crossover=TwoPointCrossover(),
                  mutation=BitflipMutation(),
                  eliminate_duplicates=True)

    # prob: controla a chance de uma solução inteira ser mutada.
    # prob_var: controla a chance de cada variável individual (bit) ser invertida na solução.
    # mutation = BitflipMutation(prob=0.5, prob_var=0.3)


    np.set_printoptions(precision=6, suppress=True)

    # Rodando a otimização
    res = minimize(problem,
                algorithm,
                termination=('n_gen', 100),  # Define 100 gerações como critério de parada
                seed=1,
                verbose=True)

    # Resultados
    print("Soluções ótimas:")
    print(res.X)   # Configurações ótimas (combinações de portas)
    print("Objetivos ótimos:")
    print(res.F)   # Valores dos objetivos
