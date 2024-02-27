import pygame
import random
#import creatures

class Grid:

    def __init__(self, window, size_x, size_y, block_size, color_bg = (225, 225, 225), color_lines = (175, 175, 175)):
        from window import Window
        self.window: Window = window
        self.size_x = size_x
        self.size_y = size_y
        self.block_size = block_size
        self.color_bg = color_bg
        self.color_lines = color_lines
        self.kill_zones = []
        #self.kill_zone = pygame.Rect(0, 0, (self.size_x * self.block_size) / 10, self.size_y * self.block_size)

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

    def add_kill_zone(self, position_source, size):
        self.kill_zones.append(pygame.Rect(position_source, size))

    def draw_grid(self):
        self.window.display.fill(self.color_bg)
        for kz in self.kill_zones:
           pygame.draw.rect(self.window.display, (125, 50, 50), kz, 0)
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
            return
        
        border_color = self.grid.color_lines

        if self is self.grid.window.selected_block:
            border_color = (200, 0, 0)
            #pygame.draw.rect(self.grid.window.display, (200, 0, 0), self.rect, 1)
        else:
            for kz in self.grid.kill_zones:
                kz: pygame.Rect
                if kz.contains(self.rect):
                    border_color = (150, 100, 100)
                    #pygame.draw.rect(self.grid.window.display, (255, 255, 255), self.rect, 1)
                
                #pygame.draw.rect(self.grid.window.display, self.grid.color_lines, self.rect, 1)

        pygame.draw.rect(self.grid.window.display, border_color, self.rect, 1)