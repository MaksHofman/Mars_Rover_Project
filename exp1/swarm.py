import random
from poi import Position, Poi
from rover import Rover


class Swarm:
    def __init__(self, start_position: Position, chromosome: list, pois:list, amout_of_rovers:int): 
        self.start_position = start_position
        self.chromosome = chromosome
        self.gens = [amout_of_rovers, pois]
        self.fitness, self.time = self.cal_fitness() 
    

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
    def find_index_by_rover(cls, chromosome, rover):
        for i in range(len(chromosome)):
            if rover == chromosome[i]:
                return i
        
    def mutate(self, amount):
        prob = random.random()
        for i in range(amount):
            if prob < 0.3:
                chromosom = self.chromosome
                random.shuffle(chromosom)
                rover_1 = chromosom[0]
                rover_2 = chromosom[1]
                
                pass #normalna mutacja
            elif prob < 0.6:
                chromosom = self.chromosome
                random.shuffle(chromosom)    
                rover_to_save = chromosom[0]
                random.shuffle(chromosom[0].pois_list) 
                self.chromosome[Swarm.find_index_by_rover(self.chromosome, rover_to_save)] = chromosom[0]           
            else:
                chromosom = self.chromosome
                random.shuffle(chromosom) 
                rover_saved = chromosom[0]       
                chromosom[0].pois_list.pop(random.randint(0, len(chromosom[0].pois_list)-1))    
                chromosom[0].skipped += 1 
                self.chromosome[Swarm.find_index_by_rover(self.chromosome, rover_saved)] = chromosom[0] 

    def mate(self, par2, amount: int):
        child_chromosome = []
        used_poi_list = []
        for gp1, gp2 in zip(self.chromosome, par2.chromosome):  
            prob = random.random()
            if prob < 0.5: 
                used_poi_list, parent_gene = Swarm.parent_gen_checking(used_poi_list, gp1)
                child_chromosome.append(parent_gene)  
            else: 
                used_poi_list, parent_gene = Swarm.parent_gen_checking(used_poi_list, gp2)
                child_chromosome.append(parent_gene)  
        return Swarm(self.start_position, child_chromosome, self.pois, self.rovers_count).mutate(amount) 



    def cal_fitness(self):
        time = 0
        fitness_score = 0
        for rovers in self.chromosome:
            fitness_score += rovers.fitness
            time += rovers.time
        return fitness_score, time #(self.rovers_count * len(self.pois))

