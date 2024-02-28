import pygame
import random

# class CreatureColors:

#     colors = {
#         "red": (255, 0, 0),
#         "green": (0, 255, 0),
#         "blue": (0, 0, 255),
#         "purple": (200, 0, 200),
#         "yellow": (150, 200, 0)
#     }

#     def get_color_rgb(color):
#         return CreatureColors.colors[color]
    
#     def get_random_color():
#         return random.choice(list(CreatureColors.colors.keys))

class Creature:

    def __init__(self, block, num_synapses = 5):

        from environment import Grid
        from environment import Block
        import brain

        self.block: Block = block
        self.grid: Grid = self.block.grid
        self.vision_range = 5
        self.set_random_color()

        self.num_synapses = num_synapses
        self.brain = brain.Brain(self, self.num_synapses)

        self.block.add_creature(self)

    def draw(self):
        if self.block is self.grid.window.selected_block:
            pygame.draw.circle(self.grid.window.display, self.color, self.block.rect.center, self.block.size / 2, 0)
            pygame.draw.rect(self.grid.window.display, (200, 0, 0), self.block.rect, 1)
        else:
            pygame.draw.circle(self.grid.window.display, self.color, self.block.rect.center, self.block.size / 2, 0)

    def action(self):
        self.brain.action()

    # def move_random(self):
    #     move_prefs = self.get_random_move_prefs()
    #     for m in move_prefs:
    #         if self.move_is_possible(m):
    #             self.block.remove_creature()
    #             self.block = self.block.get_adjacent_block(m)
    #             self.block.add_creature(self)
    #             break
        
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
        # max_vision_left = max(self.get_position_x() - self.vision_range, 0)
        # max_vision_right = min(self.get_position_x() + self.vision_range, self.grid.size_x - 1)
        # max_vision_up = max(self.get_position_y() - self.vision_range, 0)
        # max_vision_down = min(self.get_position_y() + self.vision_range, self.grid.size_y - 1)

        max_vision_left = max(self.block.pos_x - self.vision_range, 0)
        max_vision_right = min(self.block.pos_x + self.vision_range, self.grid.size_x - 1)
        max_vision_up = max(self.block.pos_y - self.vision_range, 0)
        max_vision_down = min(self.block.pos_y + self.vision_range, self.grid.size_y - 1)

        for x in range(max_vision_left, max_vision_right + 1):
            for y in range(max_vision_up, max_vision_down + 1):
                #if self.grid.get_block(x, y).is_occupied():
                if self.grid.blocks[x][y].creature != None:
                    count += 1

        # remove one because above loop includes own block
        count -= 1 
        return count
    
    def generate_creatures(grid, amount, num_synapses=5):
        creatures = []
        for i in range(amount):
            block = grid.get_random_block()
            if block != None:
                creatures.append(Creature(block, num_synapses))
        return creatures
    
    def set_random_color(self):
        self.color = (random.randint(25, 225), random.randint(25, 225), random.randint(25, 225))

    