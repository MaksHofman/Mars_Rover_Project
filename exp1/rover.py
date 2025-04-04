import random
from poi import Position, Poi

class Rover:
    def __init__(self, position: Position, chromosome: list, genes:list): 
        self.position = position
        self.chromosome = chromosome
        self.genes = genes
        self.fitness, self.time = self.cal_fitness() 
  
    @classmethod
    def mutated_genes(cls, genes):
        gene = random.choice(genes) # Trzeba dodac pusta mutacje
        return gene 
    
    @classmethod
    def create_gnome(cls, genes):
        gnome_len = len(genes) 
        return [cls.mutated_genes(genes) for _ in range(gnome_len)] 
    
    def cal_path_cost(self, end_point, hour_per_distance_unit):
        return Position.check_distance(self.position, end_point) * hour_per_distance_unit

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
                    child_chromosome.append(self.mutated_genes(self.genes)) 
            else: # to jest defoult 10% mustacji
                if prob < 0.45:  
                    child_chromosome.append(gp1)  
                elif prob < 0.70:  
                    child_chromosome.append(gp2) 
                else: 
                    child_chromosome.append(self.mutated_genes(self.genes))
        return Rover(position=Position(0,0), chromosome=child_chromosome,  genes=par2.genes) 
  
    def cal_fitness(self):
        time = 0
        fitness_score = 0
        for poi in self.chromosome:
            time += (self.cal_path_cost(poi.position, 1.0) + poi.time_of_task) #tu oblicznamy czas dla kazdego poia + czas dojechania tam
            self.position = poi.position #tu zmnieniamy pozycje lazika
            fitness_score += poi.priority_level/(time)
        return fitness_score

