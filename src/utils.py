import math

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