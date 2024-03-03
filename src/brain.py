import random
import math
import config
import utils

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

    def __init__(self, type: NeuronInputType) -> None:
        #self.creature = brain.creature
        self.type = type
        self.input_value = 0

    def calculate_input_value(self, creature: Creature):
        #self.input_value = random.uniform(-1.0, 1.0)
        if self.type is NeuronInputType.LocationX:
            self.input_value = utils.normalize_value(creature.block.pos_x, 0, creature.grid.size_x)
        elif self.type is NeuronInputType.LocationY:
            self.input_value = utils.normalize_value(creature.block.pos_y, 0, creature.grid.size_y)
        elif self.type is NeuronInputType.PopulationDensityClose:
            self.input_value = utils.normalize_value(creature.get_population_within_vision(), 0, (creature.vision_range * creature.vision_range) - 1)
        elif self.type is NeuronInputType.Random:
            self.input_value = random.uniform(-1.0, 1.0)
        elif self.type is NeuronInputType.BlockedRight:
            self.input_value = -1 if creature.move_is_possible("right") else 1
        elif self.type is NeuronInputType.BlockedLeft:
            self.input_value = -1 if creature.move_is_possible("left") else 1
        elif self.type is NeuronInputType.BlockedUp:
            self.input_value = -1 if creature.move_is_possible("up") else 1
        elif self.type is NeuronInputType.BlockedDown:
            self.input_value = -1 if creature.move_is_possible("down") else 1

class NeuronOutput:

    from creatures import Creature

    def __init__(self, type: NeuronInputType) -> None:
        #self.brain = brain
        self.type = type
        self.input_value = 0
        self.activation_value = 0

    def calculate_activation_value(self):
        self.activation_value = math.tanh(self.input_value)

    def activation(self, creature: Creature) -> bool:
        cutoff = random.random()
        if self.activation_value > cutoff:
            self.call_output_function(creature)
            return True
        return False

    def call_output_function(self, creature: Creature):
        if self.type is NeuronOutputType.MoveRight:
            creature.move("right")
        elif self.type is NeuronOutputType.MoveLeft:
            creature.move("left")
        elif self.type is NeuronOutputType.MoveUp:
            creature.move("up")
        elif self.type is NeuronOutputType.MoveDown:
            creature.move("down")
        elif self.type is NeuronOutputType.MoveRandom:
            creature.move_random()
        return

class Synapse:

    def __init__(self, input: NeuronInput, output: NeuronOutput):
        self.input = input
        self.output = output
        self.weight = random.uniform(-4.0, 4.0)

    def stimulate(self):
        self.output.input_value += self.input.input_value * self.weight

class Brain:

    from creatures import Creature

    def __init__(self, creature: Creature, copy_of: "Brain" = None):
        self.creature = creature
        self.num_synapses = config.NUMBER_OF_SYNAPSES

        self.inputs = [NeuronInput(type) for type in NeuronInputType]
        self.outputs = [NeuronOutput(type) for type in NeuronOutputType]
        self.synapses: list[Synapse] = []
        
        if copy_of != None:
            for copy_synapse in copy_of.synapses:
                self.add_synapse(copy_synapse.input.type, copy_synapse.output.type)
        else:
            for i in range(self.num_synapses):
                self.add_synapse()

    def create_copy(self):
        brain_copy = Brain(self.creature, self)
        brain_copy.creature = None
        return brain_copy

    def action(self):
        self.reset_output_neurons()
        self.calculate_inputs()
        self.stimulate_synapses()
        self.calculate_outputs()
        self.call_output_activations()

    def reset_output_neurons(self):
        for output in self.outputs:
            output.input_value = 0
            output.activation_value = 0

    def stimulate_synapses(self):
        for synapse in self.synapses:
            synapse.stimulate()
        self.synapses = sorted(self.synapses, key=lambda x: x.output.input_value, reverse=True)

    def calculate_inputs(self):
        for input in self.inputs:
            if self.input_has_synapse(input):
                input.calculate_input_value(self.creature)

    def calculate_outputs(self):
        for output in self.outputs:
            output.calculate_activation_value()

    def input_has_synapse(self, input):
        for synapse in self.synapses:
            if input.type == synapse.input.type:
                return True
        return False

    def call_output_activations(self):
        for synapse in self.synapses:
            fired = synapse.output.activation(self.creature)
            if fired == True:
                break

    def generate(self):
        self.synapses: list[Synapse] = []
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

    def add_synapse(self, input_type = None, output_type = None):
        if input_type != None:
            input = self.get_neuron_input(input_type)
        else:
            input = random.choice(self.inputs)
        if output_type != None:
            output = self.get_neuron_output(output_type)
        else:
            output = random.choice(self.outputs)
        
        synapse = Synapse(input, output)
        self.synapses.append(synapse)

    def get_neuron_input(self, input_type):
        for input in self.inputs:
            if input.type == input_type:
                return input
        return None
    
    def get_neuron_output(self, output_type):
        for output in self.outputs:
            if output.type == output_type:
                return output
        return None

    def remove_random_synapse(self):
        self.synapses.remove(random.choice(self.synapses))
    


