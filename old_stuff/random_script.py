import numpy as np
import matplotlib.pyplot as plt
import random

# Parameters
NUM_POIS = 15  # Number of Points of Interest
VEHICLE_RANGE = 200  # Maximum distance the vehicle can travel
POP_SIZE = 100  # Population size for GA
NUM_GENERATIONS = 200  # Number of generations
MUTATION_RATE = 0.1

# Generate random POIs with priority levels
np.random.seed(42)
pois = np.random.rand(NUM_POIS, 2) * 100
priorities = np.random.randint(1, 5, NUM_POIS)  # Priority 1-4 (4 is highest)
depot = np.array([50, 50])  # Fixed start and end position

# Distance calculation
def distance(p1, p2):
    return np.linalg.norm(p1 - p2)

def total_distance(route):
    dist = distance(depot, pois[route[0]])
    for i in range(len(route) - 1):
        dist += distance(pois[route[i]], pois[route[i+1]])
    dist += distance(pois[route[-1]], depot)
    return dist

# Fitness function (higher priority POIs get more weight)
def fitness(route):
    dist = total_distance(route)
    priority_score = sum(priorities[route])
    if dist > VEHICLE_RANGE:
        return 1 / (dist * 10)  # Penalize exceeding range
    return priority_score / dist

# Genetic Algorithm functions
def create_population():
    return [random.sample(range(NUM_POIS), NUM_POIS) for _ in range(POP_SIZE)]

def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [-1] * size
    child[start:end] = parent1[start:end]
    remaining = [p for p in parent2 if p not in child]
    idx = 0
    for i in range(size):
        if child[i] == -1:
            child[i] = remaining[idx]
            idx += 1
    return child

def mutate(route):
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route

def select_parents(population):
    sorted_pop = sorted(population, key=lambda r: fitness(r), reverse=True)
    return sorted_pop[:POP_SIZE // 2]

def evolve_population(population):
    parents = select_parents(population)
    new_population = parents.copy()
    while len(new_population) < POP_SIZE:
        p1, p2 = random.sample(parents, 2)
        child = mutate(crossover(p1, p2))
        new_population.append(child)
    return new_population

# Visualization
def plot_route(route, generation):
    plt.clf()
    plt.scatter(pois[:, 0], pois[:, 1], c=priorities, cmap='coolwarm', s=100, label='POIs')
    plt.scatter(*depot, c='black', marker='s', s=150, label='Depot')
    route_points = [depot] + [pois[i] for i in route] + [depot]
    plt.plot(*zip(*route_points), marker='o', linestyle='-', color='blue')
    plt.title(f'Generation {generation}')
    plt.legend()
    plt.pause(0.1)

def main():
    population = create_population()
    best_route = max(population, key=fitness)
    for gen in range(NUM_GENERATIONS):
        population = evolve_population(population)
        best_route = max(population, key=fitness)
        if gen % 10 == 0:
            plot_route(best_route, gen)
    plt.show()

if __name__ == '__main__':
    main()
