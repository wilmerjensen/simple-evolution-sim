import random
import math
from enum import Enum

class NeuronInputType(Enum):
    LocationX = 1
    LocationY = 2
    PopulationDensityClose = 3
    Random = 4
    BlockedRight = 5
    BlockedLeft = 6
    BlockedUp = 7
    BlockedDown = 8


class NeuronOutputType(Enum):
    MoveRight = 1
    MoveLeft = 2
    MoveUp = 3
    MoveDown = 4
    MoveRandom = 5

class NeuronInput:

    from creatures import Creature

    def __init__(self, brain: "Brain", type: NeuronInputType) -> None:
        self.creature = brain.creature
        self.type = type
        self.input_value = 0

    def calculate_input_value(self):
        if self.type is NeuronInputType.LocationX:
            self.input_value = Brain.normalize_value(self.creature.get_position_x(), 0, self.creature.grid.size_x)
        elif self.type is NeuronInputType.LocationY:
            self.input_value = Brain.normalize_value(self.creature.get_position_y(), 0, self.creature.grid.size_y)
        elif self.type is NeuronInputType.PopulationDensityClose:
            self.input_value = Brain.normalize_value(self.creature.get_population_within_vision(), 0, (self.creature.vision_range * self.creature.vision_range) - 1)
            #return random.uniform(-1.0, 1.0)
        elif self.type is NeuronInputType.Random:
            self.input_value = random.uniform(-1.0, 1.0)
        elif self.type is NeuronInputType.BlockedRight:
            self.input_value = -1 if self.creature.move_is_possible("right") else 1
        elif self.type is NeuronInputType.BlockedLeft:
            self.input_value = -1 if self.creature.move_is_possible("left") else 1
        elif self.type is NeuronInputType.BlockedUp:
            self.input_value = -1 if self.creature.move_is_possible("up") else 1
        elif self.type is NeuronInputType.BlockedDown:
            self.input_value = -1 if self.creature.move_is_possible("down") else 1

class NeuronOutput:

    from creatures import Creature

    def __init__(self, brain: "Brain", type: NeuronInputType) -> None:
        self.creature = brain.creature
        self.type = type
        self.input_value = 0
        self.activation_value = 0

    def calculate_activation_value(self):
        self.activation_value = math.tanh(self.input_value)

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
        elif self.type is NeuronOutputType.MoveRandom:
            self.creature.move_random()
        return

class Synapse:

    from creatures import Creature

    def __init__(self, brain: "Brain", input: NeuronInput, output: NeuronOutput):
        self.creature = brain.creature
        self.input = input
        self.output = output
        self.weight = random.uniform(-4.0, 4.0)

    def stimulate(self):
        self.output.input_value += self.input.input_value * self.weight

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
        self.reset_output_neurons()
        self.stimulate_synapses()
        self.call_output_activations()

    def reset_output_neurons(self):
        for output in self.outputs:
            output.input_unweighted = 0
            output.input_value = 0
            output.activation_value = 0

    def stimulate_synapses(self):
        for input in self.inputs:
            input: NeuronInput
            input.calculate_input_value()
        for synapse in self.synapses:
            synapse: Synapse
            synapse.stimulate()
        for output in self.outputs:
            output: NeuronOutput
            output.calculate_activation_value()
        self.synapses = sorted(self.synapses, key=lambda x: x.output.input_value, reverse=True)
        self.outputs = sorted(self.outputs, key=lambda x: x.input_value, reverse=True)

    def call_output_activations(self):
        for output in self.outputs:
            output: NeuronOutput
            fired = output.activation()
            if fired == True:
                break

    def generate(self):
        for i in range(self.num_synapses):
            self.add_synapse()

    def get_synapses(self, input_type: NeuronInputType = None, output_type: NeuronOutputType = None):
        synapse_list = []
        for s in self.synapses:
            s: Synapse
            synapse_is_match = True
            if input_type != None and s.input.type != input_type:
                synapse_is_match = False
            if output_type != None and s.output.type != output_type:
                synapse_is_match = False
            if synapse_is_match == True:
                synapse_list.append(s)
        return synapse_list

    def get_available_output_types(self, input_type):
        synapses_with_same_input = self.get_synapses(input_type)

        taken_output_types = []
        for s in synapses_with_same_input:
            s: Synapse
            taken_output_types.append(s.output.type)

        available_outputs = list(filter(lambda x: x not in taken_output_types, list(NeuronOutputType)))
        return available_outputs

    def add_synapse(self):
        available_inputs = list(NeuronInputType)
        available_outputs = []

        while len(available_inputs) > 0:
            input_type = random.choice(available_inputs)
            available_outputs = self.get_available_output_types(input_type)
            if len(available_outputs) == 0:
                available_inputs.remove(input_type)
            else:
                break

        output_type = random.choice(available_outputs)

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
    
    def normalize_value(value, min, max):
        if max - min == 0:
            return 0
        return (value - min) / (max - min) * 2 - 1