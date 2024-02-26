import random
from enum import Enum

class NeuronInput(Enum):
    LocationX = 1
    LocationY = 2
    PopulationDensityClose = 3
    Random = 4

    from creatures import Creature

    def get_value(self, creature: Creature):
        if self is NeuronInput.LocationX:
            return NeuronInput.normalize_input(creature.get_position_x, 0, creature.grid.size_x)
        elif self is NeuronInput.LocationY:
            return NeuronInput.normalize_input(creature.get_position_y, 0, creature.grid.size_y)
        elif self is NeuronInput.PopulationDensityClose:
            return NeuronInput.normalize_input(creature.get_population_within_vision, 0, (creature.vision_range * creature.vision_range) - 1)
        elif self is NeuronInput.Random:
            return random.uniform(-1.0, 1.0)
        return 0

    def normalize_input(value, min, max):
        return (value - min) / (max - min) * 2 - 1

class NeuronOutput(Enum):
    MoveRight = 1
    MoveLeft = 2
    MoveUp = 3
    MoveDown = 4

    from creatures import Creature

    def call_output_function(self, creature: Creature):
        if self is NeuronOutput.MoveRight:
            creature.move("right")
        elif self is NeuronOutput.MoveLeft:
            creature.move("left")
        elif self is NeuronOutput.MoveUp:
            creature.move("up")
        elif self is NeuronOutput.MoveDown:
            creature.move("down")
        return

class Synapse:

    from creatures import Creature

    def __init__(self, creature: Creature, input: NeuronInput, output: NeuronOutput):
        self.creature = creature
        self.input = input
        self.output = output
        self.weight = random.uniform(-4.0, 4.0)

    def stimulate(self):
        input_value = self.input.get_value(self.creature)
        cutoff = random.random()
        print(input_value, cutoff)
        if input_value > cutoff:
            print("FIRE")
            self.output.call_output_function(self.creature)