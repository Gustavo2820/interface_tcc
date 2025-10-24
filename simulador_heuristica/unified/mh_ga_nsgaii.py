"""Generic NSGA-II interface.

The nondominated sort genetic algorithm II is a multi-objective evolutionary
algorithm aimed to solve optimization problems. Using a fast non dominated
sorting algorithm and a operation that requires no user defined parameter this
can be used to solve any kind of multi-objective optimization problem.
"""

import ctypes
import numpy as np
import logging

# ====================== ADDED LOGGING CONFIGURATION ==========================
logging.basicConfig(
    level=logging.INFO,  # só INFO para não poluir com DEBUG
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)
# ============================================================================


class Chromosome:
    """Object representing an individual."""
    def __init__(self, generation, gene, obj):
        self.generation = generation
        self.gene = gene
        self.obj = obj
        self.rank = 0
        self.dist = .0

    def __lt__(self, other):
        """Crowded comparision operation."""
        return ((self.rank < other.rank) or (self.rank == other.rank) and
                (self.dist > other.dist))

    def __eq__(self, other):
        return self.obj == other.obj

    def __le__(self, other):
        """Dominance operation."""
        for obja, objb in zip(self.obj, other.obj):
            if obja > objb:
                return False
        return True

    def __hash__(self):
        k = 2166136261
        for obj in self.obj:
            k *= 16777619
            k ^= ctypes.c_uint.from_buffer(ctypes.c_float(obj)).value
        return k


class ChromosomeFactory:
    """Abstract class to generate chromossomes."""
    def __init__(self, instance):
        self.instance = instance

    def decode(self, gene):
        raise NotImplementedError

    def new(self):
        raise NotImplementedError

    def crossover(self, parent_a, parent_b):
        raise NotImplementedError

    def mutate(self, gene):
        raise NotImplementedError

    def build(self, generation, gene):
        solution = self.decode(gene)
        obj = [f(solution, self.instance) for f in self.objective_functions]
        return Chromosome(generation, gene, obj)


def fast_non_dominated_sort(solution_set):
    """Sort the chromosomes into non dominated fronts."""
    logger.debug("Starting fast_non_dominated_sort with %d solutions", len(solution_set))
    frontier = [set(), ]
    dominated_by = {x: [set(), 0] for x in solution_set}
    for solution_p in solution_set:
        for solution_q in solution_set:
            if solution_p <= solution_q:
                dominated_by[solution_p][0].add(solution_q)
            elif solution_q <= solution_p:
                dominated_by[solution_p][1] += 1
        if dominated_by[solution_p][1] == 0:
            frontier[0].add(solution_p)
            solution_p.rank = 0
    i = 0
    while True:
        new_front = set()
        for solution_p in frontier[i]:
            for solution_q in dominated_by[solution_p][0]:
                dominated_by[solution_q][1] -= 1
                if dominated_by[solution_q][1] == 0:
                    solution_q.rank = i + 1
                    new_front.add(solution_q)
        if not new_front:
            break
        frontier.append(new_front)
        i += 1
    logger.debug("Non-dominated sorting produced %d fronts", len(frontier))
    return [[y for y in x] for x in frontier]


def crowding_distance_assignment(front):
    """Assign the crowding distance for solutions in a front."""
    logger.debug("Calculating crowding distances for front with %d individuals", len(front))
    front_size = len(front)
    obj_count = len(front[0].obj)
    for solution_p in front:
        solution_p.dist = 0
    for idx in range(obj_count):
        front.sort(key=lambda x, id=idx: x.obj[id])
        front[0].dist = float('inf')
        front[-1].dist = float('inf')
        delta = front[-1].obj[idx] - front[0].obj[idx]
        if delta == 0:
            continue
        for i in range(1, front_size - 1):
            front[i].dist += (front[i + 1].obj[idx] - front[i - 1].obj[idx]) / delta
    logger.debug("Finished crowding distance assignment")


def nsgaii(factory, selector, population_size, mutation_probability,
           max_generations):
    logger.info("Initializing NSGA-II with population=%d, generations=%d", 
                population_size, max_generations)
    
    population = set()
    while len(population) < population_size:
        gene = factory.new()
        chromosome = factory.build(0, gene)
        population.add(chromosome)
    logger.info("Initial population created (%d individuals)", len(population))

    for generation in range(max_generations):
        logger.info("=== Generation %d ===", generation)
        offspring = set()

        while len(offspring) < population_size:
            parent_a, parent_b = selector(list(population))  # Convert set to list for sampling
            child1, child2 = factory.crossover(parent_a.gene, parent_b.gene)

            if np.random.uniform() < mutation_probability:
                factory.mutate(child1)
            child1 = factory.build(generation, child1)
            offspring.add(child1)

            if np.random.uniform() < mutation_probability:
                factory.mutate(child2)
            child2 = factory.build(generation, child2)
            offspring.add(child2)

        population.update(offspring)

        pareto = fast_non_dominated_sort(population)
        population = set()
        for front in pareto:
            crowding_distance_assignment(front)
            if len(population) + len(front) > population_size:
                remaining = population_size - len(population)
                front.sort(reverse=True)
                population.update(front[:remaining])
                break
            population.update(set(front))

        logger.info("Generation %d complete. Population size: %d | Pareto front size: %d",
                    generation, len(population), len(pareto[0]))

    logger.info("Algorithm finished. Returning Pareto front of size %d", len(pareto[0]))
    return pareto[0]
