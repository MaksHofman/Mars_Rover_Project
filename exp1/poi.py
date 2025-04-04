from math import sqrt
import random

class Position:
    def __init__(self, x_position, y_position):
        self.x = x_position
        self.y = y_position
    def __str__(self):
        return f"X: {self.x}, Y: {self.y}"
    
    @classmethod
    def check_distance(cls, start_point, end_point):
        return sqrt((start_point.x - end_point.x) ** 2 + (start_point.y - end_point.y) ** 2)


def random_time_duration_gen(hour_max: int, min_max: int) -> float:
    return random.randint(0, hour_max) + random.randint(0, min_max) / 60.0

def random_position_gen(x_max:int , y_max: int) -> Position:
    return Position(random.randint(0, x_max), random.randint(0, y_max))

class Poi:
    def __init__(self, poi_number: int, time_of_task: float, position: Position, priority_level: int):
        self.poi_number = poi_number
        self.time_of_task = time_of_task
        self.position = position
        self.priority_level = priority_level
    
    def __str__(self):
        return f"Poi nr: {self.poi_number} czas: {self.time_of_task}, position: {self.position}, priority: {self.priority_level}"

    
    @classmethod
    def gen_random_list_of_pois(cls, amount :int, max_time_for_task_hour:int, max_x:int, max_y:int, max_priority: int) -> list:
        output = []
        for i in range(amount):
            output.append(Poi(i,random_time_duration_gen(max_time_for_task_hour,59), random_position_gen(max_x, max_y), random.randint(1, max_priority)))
        return output
    
    