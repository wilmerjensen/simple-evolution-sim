import pygame
import random
#import creatures

class Grid:

    def __init__(self, window, size_x, size_y, block_size, color_bg = (255, 255, 255), color_lines = (200, 200, 200)):
        self.window = window
        self.size_x = size_x
        self.size_y = size_y
        self.block_size = block_size
        self.color_bg = color_bg
        self.color_lines = color_lines

        # --> generate block instances ans store them in 2D list
        self.blocks = self.__create_blocks__()
        
    def __create_blocks__(self):
        blocks = []
        for x in range(0, self.size_x):
            col = []
            for y in range(0, self.size_y):
                col.append(Block(self, x, y, self.block_size))
            blocks.append(col)
        return blocks

    def draw_grid(self):
        self.window.fill(self.color_bg)
        for x in range(self.size_x):
            for y in range(self.size_y):
                self.blocks[x][y].draw()

    def get_block(self, x, y) -> "Block":
        return self.blocks[x][y]

    def get_random_block(self):
        max_tries = 100
        for i in range(max_tries):
            x = random.randint(0, self.size_x - 1)
            y = random.randint(0, self.size_y - 1)
            block = self.blocks[x][y]
            if block.is_occupied() == False:
                return block
        return None
    
class Block:

    def __init__(self, grid: Grid, x, y, size, creature=None):
        from creatures import Creature
        self.grid = grid
        self.pos_x = x
        self.pos_y = y
        self.size = size
        self.rect = pygame.Rect(self.pos_x * self.size, self.pos_y * self.size, self.size, self.size)
        self.creature: Creature = creature

    def add_creature(self, creature):
        self.creature = creature

    def remove_creature(self):
        self.creature = None

    def is_occupied(self):
        return self.creature != None

    def get_position(self):
        return self.pos_x, self.pos_y

    def get_adjacent_block(self, direction):
        if direction == "right":
            return self.grid.get_block(self.pos_x + 1, self.pos_y)
        elif direction == "left":
            return self.grid.get_block(self.pos_x - 1, self.pos_y)
        elif direction == "down":
            return self.grid.get_block(self.pos_x, self.pos_y + 1)
        elif direction == "up":
            return self.grid.get_block(self.pos_x, self.pos_y - 1)
        return None

    def draw(self):
        if self.creature != None:
            self.creature.draw()
        else:
            pygame.draw.rect(self.grid.window, self.grid.color_lines, self.rect, 1)