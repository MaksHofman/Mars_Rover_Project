import random
from poi import Position, Poi
from rover import Rover
import copy

class Swarm:
    def __init__(self, start_position: Position, chromosome: list, pois:list, amout_of_rovers:int, max_time): 
        self.start_position = start_position
        self.chromosome = chromosome
        self.gens = [amout_of_rovers, pois, max_time]
        self.fitness, self.time = self.cal_fitness() 
      

    @classmethod
    def create_gnome(cls, pois, amout_of_rovers, max_time, position):
        modulo = len(pois) % amout_of_rovers 
        gens = []
        random.shuffle(pois)
        pois_for_rover = len(pois) // amout_of_rovers  
        slices = [pois[i*pois_for_rover:(i+1)*pois_for_rover] for i in range(amout_of_rovers)]
        if modulo == 0:
            for i in range(amout_of_rovers):  
                gens.append(Rover(position, slices[i], 0, max_time))
        else:
            extra_pois = pois[amout_of_rovers * pois_for_rover:]  
            for i in range(modulo):
                random_rover = random.randint(0, amout_of_rovers - 1)
                slices[random_rover].append(extra_pois[i])
            for i in range(amout_of_rovers):
                gens.append(Rover(position, slices[i], 0, max_time))
        return gens 
    
    @classmethod
    def find_index_by_rover(cls, chromosome, rover):
        for i in range(len(chromosome)):
            if rover == chromosome[i]:
                return i

    
    @classmethod
    def mutate(cls, chilld_chormosome, amount):
        for i in range(amount):
            prob = random.random()
            random.shuffle(chilld_chormosome) 
            if prob < 0.45:
                rand_poi_index_1 = random.randint(0, len(chilld_chormosome[0].pois_list)-1)
                rand_poi_index_2 = random.randint(0, len(chilld_chormosome[1].pois_list)-1)
                poi_1 = chilld_chormosome[0].pois_list.pop(rand_poi_index_1)
                poi_2 = chilld_chormosome[1].pois_list.pop(rand_poi_index_2-1)
                chilld_chormosome[0].pois_list.insert(rand_poi_index_1, poi_2)
                chilld_chormosome[1].pois_list.insert(rand_poi_index_2, poi_1)
                rov1 = chilld_chormosome.pop(0)
                rov2 = chilld_chormosome.pop(0)
                chilld_chormosome.insert(0, Rover(rov1.start_position, rov1.pois_list, rov1.skipped, rov1.max_time))
                chilld_chormosome.insert(1, Rover(rov2.start_position, rov2.pois_list, rov2.skipped, rov2.max_time))
              
            elif prob < 0.9:  
                random.shuffle(chilld_chormosome[0].pois_list)            
                rover = chilld_chormosome.pop(0)
                chilld_chormosome.insert(0, Rover(rover.start_position, rover.pois_list, rover.skipped, rover.max_time))
            elif prob >= 0.9:  
                if len(chilld_chormosome[0].pois_list) <= 2:
                    break
                chilld_chormosome[0].pois_list.pop(random.randint(0, len(chilld_chormosome[0].pois_list)-1))             
                chilld_chormosome[0].add_1_to_skipped()
                rover = chilld_chormosome.pop(0)
                chilld_chormosome.insert(0, Rover(rover.start_position, rover.pois_list, rover.skipped, rover.max_time))
        return chilld_chormosome

    def mate(self, par2, amount: int):
        child_chromosome = []
        
        for gp1, gp2 in zip(self.chromosome, par2.chromosome):  
            prob = random.random()
            if prob < 0.5: 
                child_chromosome.append(gp1)  
            else: 
                child_chromosome.append(gp2)  
        child_chromosome = Swarm.mutate(child_chromosome, amount)
        return Swarm(self.start_position, child_chromosome, self.gens[1], self.gens[0], self.gens[2]) # glupia jest tu kolejnosc [] ale boje sie kodu dotykac

    def cal_fitness(self):
        time = 0
        fitness_score = 0
        for rovers in self.chromosome:
            fitness_score += rovers.fitness
            time += rovers.time
        return fitness_score, time #(self.rovers_count * len(self.pois))

