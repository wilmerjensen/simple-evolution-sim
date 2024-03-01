import pygame
import random
import copy
import config

class Creature:

    def __init__(self, grid, block = None, brain = None):

        from environment import Grid
        from environment import Block
        from brain import Brain

        self.grid: Grid = grid
        self.vision_range = 5
        self.set_random_color()

        if brain != None:
            self.brain = brain
        else:
            self.brain = Brain(self)

        if block != None:
            self.block: Block = block
        else:
            self.block = self.grid.get_random_block()

        self.block.add_creature(self)

    def draw(self):
        if self.block is self.grid.window.selected_block:
            pygame.draw.circle(self.grid.window.display, self.color, self.block.rect.center, self.block.size / 2, 0)
            pygame.draw.rect(self.grid.window.display, (200, 0, 0), self.block.rect, 1)
        else:
            pygame.draw.circle(self.grid.window.display, self.color, self.block.rect.center, self.block.size / 2, 0)

    def action(self):
        self.brain.action()

    def create_offspring(self):
        new_brain = copy.deepcopy(self.brain)
        if random.random() >= config.MUTATION_RATE:
            new_brain.remove_random_synapse()
            new_brain.add_synapse()
        return Creature(self.grid, brain = new_brain)

    def move_random(self):
        self.move(random.choice(["right", "left", "up", "down"]))

    def move(self, direction):
        if self.move_is_possible(direction):
            new_block = self.block.get_adjacent_block(direction)
            if self == self.grid.window.selected_creature:
                self.grid.window.selected_block = new_block

            self.block.remove_creature()
            self.block = new_block
            self.block.add_creature(self)

    def get_random_move_prefs(self):
        move_prefs = ["right", "left", "up", "down"]
        random.shuffle(move_prefs)
        return move_prefs

    def move_is_possible(self, move):
        grid = self.block.grid
        pos_x, pos_y = self.get_position()
        if move == "right":
            if pos_x == self.grid.size_x - 1 or self.block.get_adjacent_block(move).is_occupied():
                return False
        elif move == "left":
            if pos_x == 0 or self.block.get_adjacent_block(move).is_occupied():
                return False
        elif move == "down":
            if pos_y == self.grid.size_y - 1 or self.block.get_adjacent_block(move).is_occupied():
                return False
        elif move == "up":
            if pos_y == 0 or self.block.get_adjacent_block(move).is_occupied():
                return False
        return True

    def get_position(self):
        return self.block.pos_x, self.block.pos_y
    
    def get_position_x(self):
        return self.block.pos_x
    
    def get_position_y(self):
        return self.block.pos_y
    
    def get_vision_area(self):
        max_vision_left = max(self.block.pos_x - self.vision_range, 0)
        max_vision_right = min(self.block.pos_x + self.vision_range, self.grid.size_x - 1)
        max_vision_up = max(self.block.pos_y - self.vision_range, 0)
        max_vision_down = min(self.block.pos_y + self.vision_range, self.grid.size_y - 1)
        return max_vision_left, max_vision_right, max_vision_up, max_vision_down
    
    def get_population_within_vision(self):
        count = 0

        max_vision_left = max(self.block.pos_x - self.vision_range, 0)
        max_vision_right = min(self.block.pos_x + self.vision_range, self.grid.size_x - 1)
        max_vision_up = max(self.block.pos_y - self.vision_range, 0)
        max_vision_down = min(self.block.pos_y + self.vision_range, self.grid.size_y - 1)

        for x in range(max_vision_left, max_vision_right + 1):
            for y in range(max_vision_up, max_vision_down + 1):
                if self.grid.blocks[x][y].creature != None:
                    count += 1

        # remove one because above loop includes own block
        count -= 1 
        return count
    
    def set_random_color(self):
        self.color = (random.randint(25, 225), random.randint(25, 225), random.randint(25, 225))


def generate_creatures(grid, amount):
    creatures = []
    for i in range(amount):
        block = grid.get_random_block()
        if block != None:
            creatures.append(Creature(grid))
    return creatures
    
def trigger_creature_actions(creature_list):
    for c in creature_list:
        c: Creature
        c.action()

def draw_creatures(creature_list):
    for c in creature_list:
        c: Creature
        c.draw()