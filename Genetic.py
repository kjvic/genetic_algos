# idea cred goes to http://www.ai-junkie.com/ga/intro/gat1.html
# author: krista victorsen
# email: kjvic at umich dot edu

from random import random

def bitstring_of_len(n):
    """Returns a boolean bitstring of length n, i.e. a list of ints in [0,1]"""
    temp = []
    for _ in range(n):
        temp.append(int(random() < 0.5))
    return temp

class RouletteWheel(object):
    def __init__(self, fitness_scores):
        """
        Transforms a list of probabilities (fitness_scores) in [0,1] into a 
        list of thresholds to be used in conjunction with random.random().
        """
        self.scalar = sum(fitness_scores)
        running_sum = 0
        self.upperbounds = []
        for f_score in fitness_scores:
            running_sum += f_score/self.scalar
            self.upperbounds.append(running_sum)

    def spin(self):
        """
        Pulls a random number in [0,1) from random.random(), and returns the
        integer index of the item with the smallest fitness score that was 
        greater than that random number.
        """
        fate = random()
        for i, item in enumerate(self.upperbounds):
            if fate < item:
                return i
        return -1 # somelist[-1] == somelist.last()
            
class Genetic(object):
    def __init__(self, fitness, chromosome_len, population_size,
                 crossover_rate=0.6, mutation_rate=0.1,
                 initial_population=None, epsilon=0):
        """
        This class implements a generic genetic algorithm.
        Ya pass it a fitness function, a chromosome_len (i.e. how many
        bits to track for each "chromosome" in the genetic algo), and a 
        population_size --and optionally, crossover_rate, mutation_rate, 
        a list containing members of the initial_population, and an error
        threshold--, and it spits out a solution.

        Note: fitness scores as assigned by the fitness function must be 
        in [0, 1]
        """
        self.fitness = fitness
        self.chromosome_len = chromosome_len
        self.crossover_rate = crossover_rate
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.fitness_scores = []
        self.epsilon = epsilon
        if not initial_population:
            self.population = []
            for _ in range(population_size):
                self.population.append(bitstring_of_len(chromosome_len))
        else:
            self.population = initial_population
            
    def sol_found(self):
        """
        Returns true if any fitness score is within a given threshold (epsilon)
        of the solution.
        """
        if self.fitness_scores:
            return max(self.fitness_scores) >= (1-self.epsilon)
        else:
            return False
    
    def find_sol(self):
        """Keeps requesting new generations until solution is found"""
        while not self.sol_found():
            _ = self.generation()
        print "SOLUTION FOUND!"
        # print _

    def generation(self):
        """Simulates one generation of the genetic algorithm"""
        print "\nStarting next generation..."
        print "===================================================="
        self.assign_fitness_scores()
        self.population = self.regenerate_population()
        return self.population

    def assign_fitness_scores(self):
        """For each chromosome in the population, assign a fitness score"""
        self.fitness_scores = []
        for chromosome in self.population:
            self.fitness_scores.append(self.fitness(chromosome))

    def regenerate_population(self):
        """
        Generate the population for the next generation of the simulation.
        1. Pick two parents to mate. (Fitter parents are more likely to mate)
        2. Add their babies to the new_population
        Repeat 1&2 until the new_population is as big as the current population
        """
        roulette = RouletteWheel(self.fitness_scores)
        new_population = []
        while len(new_population) < self.population_size:
            victim1 = self.population[roulette.spin()]
            victim2 = self.population[roulette.spin()]
            baby1, baby2 = self.mate(victim1, victim2)
            new_population.append(baby1)
            new_population.append(baby2)
        return new_population
            
    def mate(self, victim1, victim2):
        """
        To mate the two victimes...
        1. Copy the two parents into two baby chromosomes
        2. (Possibly) swap the babys' genomes after a certain point
        3. (Possibly) apply any mutations to each baby's genome
        """
        baby1 = victim1
        baby2 = victim2
        # Any gene crossovers?
        # (randomly swaps baby1 and baby2's guts, after some random_loc)
        if random() < self.crossover_rate:
            randloc = int(random() * self.chromosome_len)
            for i in range(randloc, self.chromosome_len):
                temp = baby1[i]
                baby1[i] = baby2[i]
                baby2[i] = temp
        # Any mutations?
        baby1 = self.mutate(baby1)
        baby2 = self.mutate(baby2)
        return baby1, baby2
    
    def mutate(self, baby):
        """
        Steps through baby's guts. Flips bits when randomly selected,
        according to the mutation_rate assigned for this simulation
        """
        for i in range(len(baby)):
            if random() < self.mutation_rate:
                baby[i] = not baby[i]
        return baby

##################################################
# end of class Genetic
##################################################

if __name__ == "__main__":
    print "No, you're *supposed* to run 'python main.py'"
