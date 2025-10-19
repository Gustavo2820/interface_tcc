from sim_ca_simulator import Simulator
from sim_ca_scenario import Scenario

from itertools import product
from copy import copy

class BruteForce:

    def __init__(self, instance):
        scen = Scenario(instance.experiment)
        self.exits = scen.doors_configurations
        self.instance = instance


    def pareto(self):
        n = len(self.exits)
        combinations = list(product([True, False], repeat=n))

        combs = [combinations[0]]
        objs = [self.decode(combinations[0])]
        todascombs = copy(combinations)
        todosobs = copy(objs)

        for combination in combinations[1:]:
            obj = self.decode(combination)
            todosobs.append(obj)

            i = 0
            menor = True
            while (i < len(combs)):
                menor = menor and (obj[0] < objs[i][0] or obj[1] < objs[i][1] or obj[2] < objs[i][2])

                if (obj[0] < objs[i][0] and obj[1] < objs[i][1] and obj[2] < objs[i][2]
                    or obj[0] == objs[i][0] and obj[1] < objs[i][1] and obj[2] < objs[i][2]
                    or obj[0] < objs[i][0] and obj[1] == objs[i][1] and obj[2] < objs[i][2]
                    or obj[0] < objs[i][0] and obj[1] < objs[i][1] and obj[2] == objs[i][2]
                    or obj[0] == objs[i][0] and obj[1] == objs[i][1] and obj[2] < objs[i][2]
                    or obj[0] == objs[i][0] and obj[1] < objs[i][1] and obj[2] == objs[i][2]
                    or obj[0] < objs[i][0] and obj[1] == objs[i][1] and obj[2] == objs[i][2]
                ):
                    combs.pop(i)
                    objs.pop(i)
                    i -= 1

                i += 1

            if menor:
                combs.append(combination)
                objs.append(obj)

        print(f"Todos combinations: {todascombs}, Tam:{len(todascombs)}")
        print(f"Todos objs: {todosobs}, Tam:{len(todosobs)}")
        print(f"Combinations final: {combs}, Tam:{len(combs)}")
        print(f"Objs final: {objs}, Tam:{len(objs)}")



    def decode(self, gene):
        doors = []
        for i in range(len(gene)):
            if gene[i]:
                doors.append(self.exits[i])

        iters = []
        distances = []
        scen = Scenario(self.instance.experiment, doors, self.instance.draw,
                            self.instance.scenario_seed[0], self.instance.simulation_seed)
        simulator = Simulator(scen)
        iterations, qtdDistance = simulator.simulate()
        print(f"Portas: {len(doors)}, Iter: {iterations}, Dist: {qtdDistance}")
        iters.append(iterations)
        distances.append(qtdDistance)

        i=0
        for current_seed in self.instance.scenario_seed[1:]:
            i += 1
            scen.scenario_reset(current_seed, self.instance.simulation_seed)
            simulator = Simulator(scen)
            iterations, qtdDistance = simulator.simulate()
            print(f"Portas: {len(doors)}, Iter: {iterations}, Dist: {qtdDistance}")
            iters.append(iterations)
            distances.append(qtdDistance)

        soma = sum(iters)
        distance = sum(distances)
        soma = soma / len(iters)
        distance = distance / len(distances)

        print(f"Final decode - Portas: {len(doors)}, Iters: {soma}, Distance: {distance}")
        return len(doors), soma, distance