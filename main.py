from string import ascii_letters as letters
from random import choice, random
from colorama import Fore, Style

ALPHABET = letters + ' '
MUTATION_RATE = 0.1
POPULATION_SIZE = 10


def fitness_function(target, population):
    distance = 0
    possibilities = {}
    for element in population:
        for k, j in zip(target, element):
            if k != j:
                distance += 1
        possibilities[''.join(element)] = distance
        distance = 0
    return possibilities


def get_possibilities(fitness):
    try:
        si = [i / float(sum(fitness.values())) for i in fitness.values()]
        possibilities = [sum(si[:i + 1]) for i in range(len(si))]
    except ZeroDivisionError:
        pass
    return possibilities


def roulette_wheel_selection(population, possibilities):
    chosen = []
    for i in range(POPULATION_SIZE):
        number = random()
        for j, element in enumerate(population):
            if number <= possibilities[j]:
                chosen.append(element)
                break
    return chosen


def mate(chosen, target):
    parent1 = chosen[:int(POPULATION_SIZE / 2)]
    parent2 = chosen[int(POPULATION_SIZE / 2):]
    child1 = [[0 for _ in range(len(target))] for _ in range(int(POPULATION_SIZE / 2))]
    child2 = [[0 for _ in range(len(target))] for _ in range(int(POPULATION_SIZE / 2))]
    for i in range(int(POPULATION_SIZE / 2)):
        mate_point = round(random() + 1)
        child1[i][:mate_point] = parent1[i][:mate_point]
        child1[i][mate_point:] = parent2[i][mate_point:]
        child2[i][:mate_point] = parent2[i][:mate_point]
        child2[i][mate_point:] = parent1[i][mate_point:]
    return child1 + child2


def mutate(population):
    for i in range(POPULATION_SIZE):
        for j in range(len(population[0])):
            if MUTATION_RATE > random():
                population[i][j] = choice(ALPHABET)
    return population


def colorize(best_fitness, target):
    colorized_text = ''
    for i, j in zip(best_fitness, target):
        if i != j:
            colorized_text += Fore.RED + i
        else:
            colorized_text += Fore.GREEN + i
    return colorized_text + Style.RESET_ALL


def main(target, population):
    iterations = 0
    best_fitness = ''
    while target != list(best_fitness):
        fitness = fitness_function(target=target, population=population)
        best_distance = min(fitness.values())
        best_fitness = min(fitness, key=fitness.get)
        possibilities = get_possibilities(fitness=fitness)
        chosen = roulette_wheel_selection(population=population, possibilities=possibilities)
        population = mate(chosen=chosen, target=target)
        population = mutate(population=population)
        fitness = fitness_function(target=target, population=population)
        worst_fitness = max(fitness, key=fitness.get)
        worst_fitness_index = population.index(list(worst_fitness))
        population[worst_fitness_index] = list(best_fitness)
        colorized_text = colorize(best_fitness=best_fitness, target=target)
        iterations += 1
        print("Iterations: {} - {} - Distance: {} ".format(iterations, colorized_text, best_distance))


if __name__ == '__main__':
    target = list(input("Enter target word: "))
    population = [[choice(ALPHABET) for _ in range(len(target))] for _ in range(POPULATION_SIZE)]
    main(target=target, population=population)
