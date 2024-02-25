import random
from enum import Enum

class NeuronType(Enum):
    Input = 1
    Internal = 2
    Output = 3

class NeuronInput(Enum):
    LocationX = 1
    LocationY = 2
    PopulationDensityClose = 3

    from creatures import Creature

    def get_value(self, creature: Creature):
        if self is NeuronInput.LocationX:
            return NeuronInput.normalize_input(creature.get_position_x, 0, creature.grid.size_x)
        elif self is NeuronInput.LocationY:
            return NeuronInput.normalize_input(creature.get_position_y, 0, creature.grid.size_y)
        elif self is NeuronInput.PopulationDensityClose:
            return NeuronInput.normalize_input(creature.get_population_within_vision, 0, (creature.vision_range * creature.vision_range) - 1)
        return 0

    def normalize_input(value, min, max):
        return (value - min) / (max - min) * 2 - 1

class NeuronAction(Enum):
    MoveRight = 1
    MoveLeft = 2
    MoveUp = 3
    MoveDown = 4
    Mate = 5

class Synapse:
    
    def __init__(self, input, output, weight):
        self.input = input
        self.output = output
        self.weight = weight

