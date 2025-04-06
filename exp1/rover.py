import random
from poi import Position, Poi

class Rover:
    def __init__(self, position: Position, pois_list: list): 
        self.position = position
        self.pois_list = pois_list
        self.fitness, self.time = self.cal_fitness() 

    def cal_path_cost(self, end_point, hour_per_distance_unit):
        return Position.check_distance(self.position, end_point) * hour_per_distance_unit

    def cal_fitness(self):
        time = 0
        fitness_score = 0
        for poi in self.pois_list:
            time += (self.cal_path_cost(poi.position, 1.0) + poi.time_of_task) #tu oblicznamy czas dla kazdego poia + czas dojechania tam
            self.position = poi.position #tu zmnieniamy pozycje lazika
            fitness_score += poi.priority_level/(time)
        return fitness_score, time

