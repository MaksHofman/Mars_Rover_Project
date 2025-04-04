from rover import Rover
from poi import Position, Poi

GENES = [] # do usunieciea

def TOP_GA(ilosc_poi, ilosc_roverow, czy_mutacja_zmiena, ilosc_populacji, wielkosc_rejonu):
    Amout_of_pois = 50
    POPULATION_SIZE = 1000
    Max_time_for_task_in_poi = 3
    Max_X_bound = 100
    Max_Y_bound = 100
    Max_piority = 5
    global GENES
    GENES = Poi.gen_random_list_of_pois(Amout_of_pois, Max_time_for_task_in_poi, Max_X_bound, Max_Y_bound, Max_piority)
    Last_best_fitness = 0
    og_loop_counter = 100
    loop_after_peak = og_loop_counter
    generation = 1
    found = False
    population = [] 
    best_fitness = 0



def main():
    print("start")
    Amout_of_pois = 50
    POPULATION_SIZE = 1000
    Max_time_for_task_in_poi = 3
    Max_X_bound = 100
    Max_Y_bound = 100
    Max_piority = 5
    global GENES
    GENES = Poi.gen_random_list_of_pois(Amout_of_pois, Max_time_for_task_in_poi, Max_X_bound, Max_Y_bound, Max_piority)
    Last_best_fitness = 0
    og_loop_counter = 100
    loop_after_peak = og_loop_counter
    generation = 1
    found = False
    population = [] 
    best_fitness = 0

    for _ in range(POPULATION_SIZE): 
                gnome = Rover_individual.create_gnome(GENES) 
                population.append(Rover_individual(Position(0,0), gnome, GENES)) 
  
    while not loop_after_peak == 0: 
        population = sorted(population, key=lambda x: x.fitness, reverse=True)
  
        if population[0].fitness >= best_fitness:  
            Last_best_fitness = best_fitness
            best_fitness = population[0].fitness

        if Last_best_fitness != best_fitness and found == True:
             found = False
             loop_after_peak = og_loop_counter

        if Last_best_fitness == best_fitness and found == True:
             loop_after_peak -= 1

        if Last_best_fitness == best_fitness and found != True:
            found = True
            loop_after_peak -= 1
  
        new_generation = [] # od tego punktu nie dziala (nowe generacje sie zle tworza(sa takie same))
   
        s = int((10*POPULATION_SIZE)/100) 
        new_generation.extend(population[:s]) 
   
        s = int((90*POPULATION_SIZE)/100) 
        for _ in range(s): 
            parent1 = random.choice(population[:50]) 
            parent2 = random.choice(population[:50]) 
            child = parent1.mate(parent2) 
            new_generation.append(child) 

        
        population = new_generation 
  
        #print(f"Generation: {generation} String: {population[0].chromosome} Fitness: {population[0].fitness}") # trzeba to na wizualizacje zmienic
        print(f"Best time{best_fitness}, Last Time = {Last_best_fitness}, Geratiuon {generation}")
      
        generation += 1

      
   # print(f"Generation: {generation} String: {population[0].chromosome} Fitness: {population[0].fitness}") 



if __name__ == "__main__":
    main()

    