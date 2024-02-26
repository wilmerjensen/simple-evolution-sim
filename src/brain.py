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
        if self.type is NeuronInputType.LocationX:
            return NeuronInput.normalize_input(self.creature.get_position_x(), 0, self.creature.grid.size_x)
        elif self.type is NeuronInputType.LocationY:
            return NeuronInput.normalize_input(self.creature.get_position_y(), 0, self.creature.grid.size_y)
        elif self.type is NeuronInputType.PopulationDensityClose:
            return NeuronInput.normalize_input(self.creature.get_population_within_vision(), 0, (self.creature.vision_range * self.creature.vision_range) - 1)
        elif self.type is NeuronInputType.Random:
            return random.uniform(-1.0, 1.0)
        return 0

    def normalize_input(value, min, max):
        return (value - min) / (max - min) * 2 - 1

class NeuronOutput:

    from creatures import Creature

    def __init__(self, brain: "Brain", type: NeuronInputType) -> None:
        self.creature = brain.creature
        self.type = type
        self.activation_value = 0

    def activation(self) -> bool:
        cutoff = random.random()
        if self.activation_value > cutoff:
            self.call_output_function()
            return True
        return False

    def call_output_function(self):
        if self.type is NeuronOutputType.MoveRight:
            self.creature.move("right")
        elif self.type is NeuronOutputType.MoveLeft:
            self.creature.move("left")
        elif self.type is NeuronOutputType.MoveUp:
            self.creature.move("up")
        elif self.type is NeuronOutputType.MoveDown:
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
        self.output.activation_value += input_value

        # cutoff = random.random()
        # if input_value > cutoff:
        #     self.output.call_output_function()

class Brain:

    from creatures import Creature

    def __init__(self, creature: Creature, num_synapses):
        self.creature = creature
        self.num_synapses = num_synapses
        self.inputs = []
        self.outputs = []
        self.synapses = []

        self.generate()

    def action(self):
        self.reset_activation_values()
        self.stimulate_synapses()
        self.call_output_activations()

    def reset_activation_values(self):
        for output in self.outputs:
            output.activation_value = 0

    def stimulate_synapses(self):
        for synapse in self.synapses:
            synapse.stimulate()

    def call_output_activations(self):
        for output in self.outputs:
            fired = output.activation()
            if fired == True:
                break

    def generate(self):
        for i in range(self.num_synapses):
            self.add_synapse()

    def add_synapse(self):
        input_type = random.choice(list(NeuronInputType))
        output_type = random.choice(list(NeuronOutputType))

        if self.find_input_type(input_type) >= 0:
            input = self.inputs[self.find_input_type(input_type)]
        else:
            input = NeuronInput(self, input_type)
            self.inputs.append(input)

        if self.find_output_type(output_type) >= 0:
            output = self.outputs[self.find_output_type(output_type)]
        else:
            output = NeuronOutput(self, output_type)
            self.outputs.append(output)

        synapse = Synapse(self, input, output)
        self.synapses.append(synapse)

    def find_input_type(self, type: NeuronInputType):
        for i, inputs in enumerate(self.inputs):
            if inputs.type is type:
                return i
        return -1

    def find_output_type(self, type: NeuronOutputType):
        for i, output in enumerate(self.outputs):
            if output.type is type:
                return i
        return -1