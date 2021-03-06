'''
Interact with genomes through species.
'''
import config
import random
import gene
import itertools as it
from genome import Genome


class NEAT:
    ''' Main. '''
    def __init__(self, inputs, outputs, simulation):
        god = Genome(inputs, outputs)
        self.simulation = simulation

        self.populate(god)
        for _ in range(config.GENERATIONS):
            self.simulate()
            self.speciate()
            self.replicate()

        genomes = list(it.chain.from_iterable(self.Species))
        genomes.sort(key=lambda genome: genome.fitness, reverse=True)
        # for genome in genomes:
        #     print(genome)

        best = genomes[0]
        print(best)
        best.setup()
        *result, = best.feed([0.5])
        print(result)

    def populate(self, god):
        self.Species = [[god]]
        for _ in range(config.POPULATION):
            clone = god.clone()
            clone.mutate(config.POPULATION)
            self.Species[0].append(clone)

    def simulate(self):
        for species in self.Species:
            for genome in species:
                genome.setup()
            self.simulation(species)

    def speciate(self):
        next_species = []
        randomized = sorted(it.chain.from_iterable(self.Species), key=lambda L: random.random())
        for genome in randomized:
            for i, species in enumerate(next_species):
                if species[0].compatable(genome):
                    next_species[i].append(genome)
                    break
            else:
                next_species.append([genome])

        self.Species = [species for species in next_species
                        if len(species) > config.species_size_threshold]

    def replicate(self):
        gene.Gene.reset()
        species_fitness = []
        for i, species in enumerate(self.Species):
            species.sort(key=lambda genome: genome.fitness, reverse=True)
            self.Species[i] = species[:len(species)//2]
            species_fitness.append(sum((genome.fitness for genome in species if genome.fitness >= 0)) / len(species))
        total_fitness = sum(species_fitness)

        for i, species in enumerate(self.Species):
            allowed_offspring = int(species_fitness[i] / total_fitness * config.POPULATION)
            offspring = [species[0]]
            # kid_per_genome = int(allowed_offspring / len(species))
            # for parent1 in species:
            #     for _ in range(kid_per_genome):
            #         if random.uniform(0, 1) < config.chance_mutate_no_crossover:
            #             kid = parent1.clone()
            #         else:
            #             if random.uniform(0, 1) < config.chance_interspecies_mate:
            #                 parent2 = random.choice(list(it.chain.from_iterable(self.Species)))
            #             else:
            #                 parent2 = random.choice(species)
            #             kid = parent1.crossover(parent2)

            #         kid.mutate(len(species))
            #         offspring.append(kid)

            # self.Species[i] = offspring


            for j in range(allowed_offspring):
                for _ in range(2):
                    if j >= len(species):
                        parent1 = random.choice(species)
                    else:
                        parent1 = species[j]

                    if random.uniform(0, 1) < config.chance_mutate_no_crossover:
                        kid = parent1.clone()
                    else:
                        if random.uniform(0, 1) < config.chance_interspecies_mate:
                            parent2 = random.choice(list(it.chain.from_iterable(self.Species)))
                        else:
                            parent2 = random.choice(species)
                        kid = parent1.crossover(parent2)

                    kid.mutate(len(species))
                    offspring.append(kid)

            self.Species[i] = offspring


if __name__ == '__main__':

    def run(species):
        for genome in species:
            num = 0.5
            result = sum(genome.feed([num]))
            # genome.fitness = 1 / abs(result - num)
            genome.fitness = len(genome.Genes)
        species.sort(key=lambda genome: genome.fitness, reverse=True)
        # print(species[0].fitness, species[-1].fitness)


    NEAT(1, 10, run)

