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
        self.type = type
        self.input_value = 0

    def calculate_input_value(self, creature: Creature):
        if self.type is NeuronInputType.LocationX:
            self.input_value = utils.normalize_value(creature.block.pos_x, 0, creature.grid.size_x)
        elif self.type is NeuronInputType.LocationY:
            self.input_value = utils.normalize_value(creature.block.pos_y, 0, creature.grid.size_y)
        elif self.type is NeuronInputType.PopulationDensityClose:
            max_creatures_in_vision = ((creature.vision_range * 2) + 1) * ((creature.vision_range * 2) + 1) - 1
            self.input_value = utils.normalize_value(creature.get_population_within_vision(), 0, max_creatures_in_vision)
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
        self.type = type
        self.input_value = 0

    def activation(self, creature: Creature) -> bool:
        cutoff = random.random()
        activation = math.tanh(self.input_value)
        if activation > cutoff:
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
        weighted_input = self.input.input_value * self.weight
        self.output.input_value += weighted_input

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
        self.stimulate_synapses()
        self.call_output_activations()

    def reset_output_neurons(self):
        for output in self.outputs:
            output.input_value = 0

    def stimulate_synapses(self):
        handled_inputs = set()
        for synapse in self.synapses:
            if synapse.input not in handled_inputs:
                synapse.input.calculate_input_value(self.creature)
                handled_inputs.add(synapse.input)
            synapse.stimulate()
        self.outputs = sorted(self.outputs, key=lambda x: x.input_value, reverse=True)

    def call_output_activations(self):
        for output in self.outputs:
            if output.input_value <= 0:
                # outputs are ordered by input_value, if we get here no other outputs will trigger either
                break 
            fired = output.activation(self.creature)
            if fired == True:
                break 

    def input_has_synapse(self, input: NeuronInput):
        for synapse in self.synapses:
            if input.type == synapse.input.type:
                return True
        return False
    
    def output_has_synapse(self, output: NeuronOutput):
        for synapse in self.synapses:
            if output.type == synapse.output.type:
                return True
        return False 

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
    


