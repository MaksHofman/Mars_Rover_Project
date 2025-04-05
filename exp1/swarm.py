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
    
    #to sie moze przydac przy mutacjach ale funkcja zostalo napisana tak o 
    def check_if_poi_is_used_already(self, poi):
        is_in_chromosome = False
        for i in self.chromosome:
            for j in i.pois_list:
                if j == poi:
                    is_in_chromosome = True
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
    
    #to trzeba zmienic jeszcze
    def mate(self, par2, dynamic_mutacion:bool, stagnation: bool): 
        child_chromosome = []
        for gp1, gp2 in zip(self.chromosome, par2.chromosome):  
            prob = random.random()
            if dynamic_mutacion == True and stagnation == True: #tu trzeba jakis rate moze dodac lub inaczej to rozkminic
                if prob < 0.45: 
                    child_chromosome.append(gp1)  
                elif prob < 0.70: 
                    child_chromosome.append(gp2) 
                else: 
                    child_chromosome.append(self.mutated_genes(self.pois)) 
            else: # to jest defoult 10% mustacji
                if prob < 0.45:  
                    child_chromosome.append(gp1)  
                elif prob < 0.70:  
                    child_chromosome.append(gp2) 
                else: 
                    child_chromosome.append(self.mutated_genes(self.pois))
        return Rover(position=Position(0,0), pois_list=child_chromosome,  genes=par2.genes) 
    
    #to trzeba zmienic jeszcze
    def cal_fitness(self):
        time = 0
        fitness_score = 0
        for rovers in self.chromosome:
            pass # srednia cal fitness kazdego rovera moze ?
        return fitness_score

