import pygame
import random

class Creature:

    def __init__(self, block):

        from environment import Grid
        from environment import Block

        self.block: Block = block
        self.grid: Grid = self.block.grid
        #self.color = self.get_random_color()
        self.set_random_color()

        self.block.add_creature(self)

    def draw(self):
        pygame.draw.circle(self.grid.window, self.color, self.block.rect.center, self.block.size / 2, 0)

    def move(self):
        move_prefs = self.determine_move_preferences()
        for m in move_prefs:
            if self.move_is_possible(m):
                self.block.remove_creature()
                self.block = self.block.get_adjacent_block(m)
                self.block.add_creature(self)
                break

    def determine_move_preferences(self):
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
    
    def generate_creatures(grid, amount):
        creatures = []
        for i in range(amount):
            block = grid.get_random_block()
            if block != None:
                creatures.append(Creature(block))
        return creatures
    
    def set_random_color(self):
        self.color = (random.randint(25, 225), random.randint(25, 225), random.randint(25, 225))