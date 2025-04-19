from rover import Rover
from poi import Position, Poi
from swarm import Swarm
import random, time

"""
To do:
Poprawic selekcje osobnikow(zrobic na te 2 standardowe sposoby)
Napisac sensowne experymenty
"""


def TOP_GA_TRAIN(amount_of_pois, amount_of_rovers, population_size, max_itter_eneabled, scalleble_mmutation_eneabled): #trzeba jeszcze zmienic pod nowy swarm / rower
    Amout_of_pois = amount_of_pois
    POPULATION_SIZE = population_size
    Max_time_for_task_in_poi = 3
    Max_X_bound = 1000
    Max_Y_bound = 1000
    Max_piority = 5
    max_itter = 10000
    global poi_list
    poi_list = Poi.gen_random_list_of_pois(Amout_of_pois, Max_time_for_task_in_poi, Max_X_bound, Max_Y_bound, Max_piority)
    Last_best_fitness = 0
    og_loop_counter = 100
    loop_after_peak = og_loop_counter
    generation = 1
    found = False
    population = [] 
    best_fitness = 0
    best_individual =0
    for _ in range(POPULATION_SIZE): 
                chrom = Swarm.create_gnome(poi_list, amount_of_rovers,36000, Position(0,0)) 
                population.append(Swarm(Position(0,0),chrom, poi_list, amount_of_rovers, 36000 )) 
    while not loop_after_peak == 0: 
        population = sorted(population, key=lambda x: x.fitness, reverse=True)
        if population[0].fitness >= best_fitness:  
            Last_best_fitness = best_fitness
            best_fitness = population[0].fitness
            best_individual = population[0]

        if Last_best_fitness != best_fitness and found == True:
             found = False
             loop_after_peak = og_loop_counter

        if Last_best_fitness == best_fitness and found == True:
             loop_after_peak -= 1

        if Last_best_fitness == best_fitness and found != True:
            found = True
            loop_after_peak -= 1
        
        if max_itter == generation and max_itter_eneabled:
            loop_after_peak = 0
  
        new_generation = [] # od tego punktu nie dziala (nowe generacje sie zle tworza(sa takie same))

        s = int((10*POPULATION_SIZE)/100) 
        new_generation.extend(population[:s]) 
   
        s = int((90*POPULATION_SIZE)/100) 
        for _ in range(s): 
            parent1 = random.choice(population[:50]) 
            parent2 = random.choice(population[:50])
            child = parent1.mate(parent2, len(parent1.gens[1]) // 10) 
            new_generation.append(child) 


        
        population = new_generation 
  
        print(f"Generation: {generation} String: Fitness: {population[0].fitness}") # trzeba to na wizualizacje zmienic
        #print(f"Best fitness = {best_fitness}, Last fitness = {Last_best_fitness}, Geratiuon {generation}, found = {found}, gen till end = {loop_after_peak}")
      
        generation += 1
    return best_individual

def exp1():
    start_time_50poi = time.time()
    poi50 = TOP_GA_TRAIN(50, 5, 1000, False, True)
    end_time50poi = time.time()
    deltaTime50poi = end_time50poi - start_time_50poi

    print(f"Dla 50 = {deltaTime50poi}")

    start_time_100poi = time.time()
    TOP_GA_TRAIN(100,5,1000, False, True)
    end_time100poi = time.time()
    deltaTime100poi = end_time100poi - start_time_100poi
    print(f"Dla 100 = {deltaTime100poi}")

    start_time_200poi = time.time()
    TOP_GA_TRAIN(200,10,1000, False, True)
    end_time200poi = time.time()
    deltaTime200poi = end_time200poi - start_time_200poi
    print(f"Dla 200 = {deltaTime200poi}")

    start_time_500poi = time.time()
    TOP_GA_TRAIN(500,15,1000, False, True)
    end_time500poi = time.time()
    deltaTime500poi = end_time500poi - start_time_500poi

    print(f"Dla 50 = {deltaTime50poi},Dla 100 = {deltaTime100poi},Dla 200 = {deltaTime200poi},Dla 500 = {deltaTime500poi}")

if __name__ == "__main__":
    print("start")
    start_time_500poi = time.time()
    to = TOP_GA_TRAIN(300,15,1000, False, True)
    end_time500poi = time.time()
    deltaTime500poi = end_time500poi - start_time_500poi 
    start_time_200poi = time.time()   
    tp = TOP_GA_TRAIN(1000,26,1000, False, True)
    end_time200poi = time.time()
    deltaTime200poi = end_time200poi - start_time_200poi
    print(f"fitness = {to.fitness / (to.rovers_count * len(to.pois))}, time = {to.time}, time of calkulation = {deltaTime500poi}")
    print(f"fitness = {tp.fitness  / (tp.rovers_count * len(tp.pois))}, time = {tp.time}, time of calkulation = {deltaTime200poi}")
    #exp1()
    """
    wynik z dzieleniem fitnesa w swarmie
    poi = 100, rovers = 15
    fitness = 0.0005376554174759646, time = 36198.300638991976
    poi = 400, rovers = 15
    fitness = 0.0002465110292173232, time = 190960.97825291305

    wyniki z dzielenie fitnesa poza swarmem 
    fitness = 0.0004867869413201165, time = 34314.27292433864
    fitness = 0.0002543448049218352, time = 196358.501228254
    wiec parametr fitness/ poi * rover niema wplywu na dzialanie 


    Dla 50 = 24.47069001197815,Dla 100 = 95.65448904037476,Dla 200 = 136.53235054016113,Dla 500 = 2985.691530942917 wyniki dal poi roznych ( 1/10 * poi = rover)
    """