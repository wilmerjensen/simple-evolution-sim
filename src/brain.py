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
            self.input_value = Brain.normalize_value(self.creature.block.pos_x, 0, self.creature.grid.size_x)
        elif self.type is NeuronInputType.LocationY:
            self.input_value = Brain.normalize_value(self.creature.block.pos_y, 0, self.creature.grid.size_y)
        elif self.type is NeuronInputType.PopulationDensityClose:
            self.input_value = Brain.normalize_value(self.creature.get_population_within_vision(), 0, (self.creature.vision_range * self.creature.vision_range) - 1)
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
        #self.inputs = []
        #self.outputs = []
        self.inputs = [NeuronInput(self, type) for type in NeuronInputType]
        self.outputs = [NeuronOutput(self, type) for type in NeuronOutputType]

        self.synapses: list[Synapse] = []

        self.generate()

    def action(self):
        self.reset_output_neurons()
        self.calculate_inputs()
        self.stimulate_synapses()
        self.calculate_outputs()
        self.call_output_activations()

    def reset_output_neurons(self):
        for output in self.outputs:
            output.input_unweighted = 0
            output.input_value = 0
            output.activation_value = 0

    def stimulate_synapses(self):
        for synapse in self.synapses:
            synapse.stimulate()
            
        self.synapses = sorted(self.synapses, key=lambda x: x.output.input_value, reverse=True)
        self.outputs = sorted(self.outputs, key=lambda x: x.input_value, reverse=True)

    def calculate_inputs(self):
        for input in self.inputs:
            if self.input_has_synapse(input):
                input.calculate_input_value()

    def calculate_outputs(self):
        for output in self.outputs:
            output.calculate_activation_value()

    def input_has_synapse(self, input):
        for synapse in self.synapses:
            if input.type == synapse.input.type:
                return True
        return False

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
        synapse = Synapse(self, random.choice(self.inputs), random.choice(self.outputs))
        self.synapses.append(synapse)

    def remove_random_synapse(self):
        self.synapses.remove(random.choice(self.synapses))
    
    def normalize_value(value, min, max):
        if max - min == 0:
            return 0
        return (value - min) / (max - min) * 2 - 1
    