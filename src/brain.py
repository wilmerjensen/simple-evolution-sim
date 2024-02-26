import random
from enum import Enum

class NeuronInputType(Enum):
    LocationX = 1
    LocationY = 2
    PopulationDensityClose = 3
    Random = 4

class NeuronOutputType(Enum):
    MoveRight = 1
    MoveLeft = 2
    MoveUp = 3
    MoveDown = 4

class NeuronInput:

    from creatures import Creature

    def __init__(self, brain: "Brain", type: NeuronInputType) -> None:
        self.creature = brain.creature
        self.type = type

    def get_value(self):
        if self.type is NeuronInput.LocationX:
            return NeuronInput.normalize_input(self.creature.get_position_x, 0, self.creature.grid.size_x)
        elif self.type is NeuronInput.LocationY:
            return NeuronInput.normalize_input(self.creature.get_position_y, 0, self.creature.grid.size_y)
        elif self.type is NeuronInput.PopulationDensityClose:
            return NeuronInput.normalize_input(self.creature.get_population_within_vision, 0, (self.creature.vision_range * self.creature.vision_range) - 1)
        elif self.type is NeuronInput.Random:
            return random.uniform(-1.0, 1.0)
        return 0

    def normalize_input(value, min, max):
        return (value - min) / (max - min) * 2 - 1

class NeuronOutput:

    from creatures import Creature

    def __init__(self, brain: "Brain", type: NeuronInputType) -> None:
        self.creature = brain.creature
        self.type = type

    def call_output_function(self):
        if self.type is NeuronOutput.MoveRight:
            self.creature.move("right")
        elif self.type is NeuronOutput.MoveLeft:
            self.creature.move("left")
        elif self.type is NeuronOutput.MoveUp:
            self.creature.move("up")
        elif self.type is NeuronOutput.MoveDown:
            self.creature.move("down")
        return

class Synapse:

    from creatures import Creature

    def __init__(self, brain: "Brain", input: NeuronInput, output: NeuronOutput):
        self.creature = brain.creature
        self.input = input
        self.output = output
        self.weight = random.uniform(-4.0, 4.0)

    def stimulate(self):
        input_value = self.input.get_value() * self.weight
        cutoff = random.random()
        if input_value > cutoff:
            self.output.call_output_function()

class Brain:

    from creatures import Creature

    def __init__(self, creature: Creature, num_synapses):
        self.creature = creature
        self.num_synapses = num_synapses
        self.inputs = []
        self.outputs = []
        self.synapses = []

        self.generate()

    def generate(self):
        for i in range(self.num_synapses):
            new_input = NeuronInput(self, random.choice(list(NeuronInputType)))
            new_output = NeuronOutput(self, random.choice(list(NeuronOutputType)))
            new_synapse = Synapse(self, new_input, new_output)
            self.inputs.append(new_input)
            self.outputs.append(new_output)
            self.synapses.append(new_synapse)