import random
from poi import Position, Poi

class Rover:
    def __init__(self, position: Position, pois_list: list, skipped: int, max_time): 
        self.start_position = position
        self.position = self.start_position
        self.pois_list = pois_list
        self.skipped = skipped
        self.max_time = max_time
        self.fitness, self.time = self.cal_fitness(max_time) 

    def add_1_to_skipped(self):
        self.skipped = self.skipped + 1

    def __eq__(self, other):
        return isinstance(other, Rover) and self.pois_list == other.pois_list 
    
    def cal_path_cost(self, end_point, hour_per_distance_unit):
        return Position.check_distance(self.position, end_point) * hour_per_distance_unit

    def cal_fitness(self, max_time): # to do zmienienia
        time = 0
        fitness_score = 0
        for poi in self.pois_list:
            time += (self.cal_path_cost(poi.position, 0.16) + poi.time_of_task) #tu oblicznamy czas dla kazdego poia + czas dojechania tam
            self.position = poi.position #tu zmnieniamy pozycje lazika
            fitness_score += (poi.priority_level/(time))
        if time > max_time:
            fitness_score - 50# Kara za nie wyrobienie sie w czasie
        fitness_score = fitness_score - (self.skipped * (fitness_score / len(self.pois_list))* 3)
        return fitness_score, time
    

