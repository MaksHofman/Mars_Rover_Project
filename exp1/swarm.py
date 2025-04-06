import random
from poi import Position, Poi
from rover import Rover


class Swarm:
    def __init__(self, start_position: Position, chromosome: list, pois:list, amout_of_rovers:int): 
        self.start_position = start_position
        self.chromosome = chromosome
        self.rovers_count = amout_of_rovers #czesc genotypu
        self.pois = pois #czesc genotypu
        self.fitness, self.time = self.cal_fitness() 
    

    @classmethod
    def poi_in_list_already(cls, list, poi):
        is_in_list = False
        for i in list:
            if i == poi:
                is_in_list = True
        return is_in_list
    
    @classmethod
    def parent_gen_checking(cls, already_poi_list, parent_gene):
        for i in reversed(range(len(parent_gene.pois_list))):
            if Swarm.poi_in_list_already(already_poi_list, parent_gene.pois_list[i]):
                parent_gene.pois_list.pop(i)
            else:
                already_poi_list.append(parent_gene.pois_list[i])
        return already_poi_list, parent_gene
    
    @classmethod
    def check_if_rover_is_used_already(cls, chromosome, rover):
        is_in_chromosome = False
        for i in chromosome:
            if i.pois_list == rover.pois_list: #tu blad
                is_in_chromosome == True
        return is_in_chromosome


    @classmethod
    def create_gnome(cls, pois, amout_of_rovers, position): #trzeba sprawdzic funkcje pod kontem modulo != 0 bo smierdzi mi cos ta logika
        modulo = len(pois) % amout_of_rovers 
        gens = []
        random.shuffle(pois)
        pois_for_rover = len(pois) // amout_of_rovers  
        slices = [pois[i*pois_for_rover:(i+1)*pois_for_rover] for i in range(amout_of_rovers)]
        if modulo == 0:
            for i in range(amout_of_rovers):  
                gens.append(Rover(position, slices[i]))
        else:
            extra_pois = pois[amout_of_rovers * pois_for_rover:]  
            for i in range(modulo):
                random_rover = random.randint(0, amout_of_rovers - 1)
                slices[random_rover].append(extra_pois[i])
            for i in range(amout_of_rovers):
                gens.append(Rover(position, slices[i]))
        return gens 
    
    @classmethod
    def _creat_single_rover_poi_combo(cls, pois, amout_of_rovers, position):
        random.shuffle(pois)
        pois_for_rover = len(pois) // amout_of_rovers
        slices = [pois[i*pois_for_rover:(i+1)*pois_for_rover] for i in range(amout_of_rovers)]
        return Rover(position, slices[random.randint(0, len(slices) -1)])


    @classmethod
    def mutated_genes(cls, pois, rover_count, position, child_chromosome):
        rover = 0
        is_unique = True
        while is_unique == True:
            rover = Swarm._creat_single_rover_poi_combo(pois, rover_count, position)
            is_unique = Swarm.check_if_rover_is_used_already(child_chromosome, rover)
        if rover != 0:
            return rover

    def mate(self, par2, dynamic_mutacion: bool, stagnation: bool):  #
        child_chromosome = []
        used_poi_list = []
        for gp1, gp2 in zip(self.chromosome, par2.chromosome):  
            prob = random.random()
            if dynamic_mutacion == True and stagnation == True: #narazie to pominiemy
                if prob < 0.45: 
                    used_poi_list, parent_gene = Swarm.parent_gen_checking(used_poi_list, gp1)
                    child_chromosome.append(parent_gene)  
                elif prob < 0.70: 
                    used_poi_list, parent_gene = Swarm.parent_gen_checking(used_poi_list, gp2)
                    child_chromosome.append(parent_gene)  
                else: 
                    child_chromosome.append(Swarm.mutated_genes(gp1.pois_list, gp1.rovers_count, gp1.start_position, child_chromosome))
            else: # to jest defoult 10% mustacji
                if prob < 0.45: 
                    used_poi_list, parent_gene = Swarm.parent_gen_checking(used_poi_list, gp1)
                    child_chromosome.append(parent_gene)  
                elif prob < 0.70: 
                    used_poi_list, parent_gene = Swarm.parent_gen_checking(used_poi_list, gp2)
                    child_chromosome.append(parent_gene)  
                else: 
                    child_chromosome.append(Swarm.mutated_genes(self.pois, self.rovers_count, self.start_position, child_chromosome)) #to troche podejrzane
        return Swarm(self.start_position, child_chromosome, self.pois, self.rovers_count) 

    def cal_fitness(self):
        time = 0
        fitness_score = 0
        for rovers in self.chromosome:
            fitness_score += rovers.fitness
            time += rovers.time
        return fitness_score / self.rovers_count, time

