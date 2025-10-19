import numpy as np

from simulator.scenario import Scenario
# from simulator import *

# Representação do mapa

# No lugar de gerar o mapa inteiro, a heuristica vai trabalhar com "Peças", 
# pedaços sequenciais que há possibilidade de posicionar portas

# O objetivo da heurisca, é colocar portas validas nessas Peças.



# Geração de Vizinhos

# Geração de uma quantidade X de soluções válidas, na qual, uma será escolhida para ser a nova solução. 
# Essa escolha é feita por probabilidade, sendo que quanto mais fria a temperatura, mais chances de 
# escolher as melhores soluções

# Kirkpatrick, S., et al. “Optimization by Simulated Annealing.” <i>Science</i>, vol. 220, no. 4598, 1983, pp. 671–680. <i>JSTOR</i>, www.jstor.org/stable/1690046. Accessed 3 Sept. 2021.
# http://www2.stat.duke.edu/~scs/Courses/Stat376/Papers/TemperAnneal/KirkpatrickAnnealScience1983.pdf

# Decaimento Geometrico
def cooling_scheme(current_temperature):
    return (current_temperature * ALPHA)

# Criterio de aceitação de boltzman
def acceptance_criteria(current_solution, new_solution, current_temperature):
    return (np.exp(-(current_solution - new_solution) / current_temperature))

def roulette_whell():
    pass

def create_first_solution():
    pass

scen = Scenario("cult_experiment", True, 1, 2)
sim = Simulator(scen)
sim.simulate()



# current_solution = create_first_solution()
# best_solution = current_solution
# current_temperature = INITIAL_TEMPERATURE
# while (current_temperature > FINAL_TEMPERATURE):
#     neighborhood_solutions = create_neighborhood()
#     current_solution = find_new_solution(neighborhood_solutions, current_solution)
#     current_temperature = cooling_scheme(current_temperature)

# def find_new_solution(neighborhood_solutions, current_solution):
#     new_solution = current_solution
#     for solution in neighborhood_solutions:
#         if (solution > new_solution):
#             new_solution = solution
#     if (new_solution == current_solution):
#         temp_solution = roulette_whell(neighborhood_solutions)
#         if (acceptance_criteria(current_solution, temp_solution, current_temperature)):
#             new_solution = temp_solution
#         pass
#     return new_solution