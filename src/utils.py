import math
import random

def normalize_value(value, min, max):
        if max - min == 0:
            return 0
        return (value - min) / (max - min) * 2 - 1

def softmax(list):
    softmax_list = []
    exponential_total = 0
    for x in list:
        exponential_total += math.exp(x)
    for x in list: 
        softmax_list.append(math.exp(x) / exponential_total)
    return softmax_list

def get_random_color():
    return (random.randint(25, 225), random.randint(25, 225), random.randint(25, 225))

def get_color_mutation(color):
     return (color[0] + random.randint(-10, 10), color[1] + random.randint(-10, 10), color[2] + random.randint(-10, 10))