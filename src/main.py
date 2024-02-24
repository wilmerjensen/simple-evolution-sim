import sys
import pygame
import random

GRID_SIZE_X = 128
GRID_SIZE_Y = 128
BLOCK_SIZE = 8

WINDOW_WIDTH = GRID_SIZE_X * BLOCK_SIZE
WINDOW_HEIGHT = GRID_SIZE_Y * BLOCK_SIZE
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)

COLOR_BACKGROUND = (255, 255, 255)
COLOR_LINES = (200, 200, 200)

POPULATION = 250


def main():
    pygame.init()

    clock = pygame.time.Clock()
    running = True

    grid = Grid(GRID_SIZE_X, GRID_SIZE_Y, BLOCK_SIZE)
    creatures = Creature.generate_creatures(grid, POPULATION)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        WINDOW.fill(COLOR_BACKGROUND)

        for c in creatures:
            c.move()

        grid.draw_grid()

        pygame.display.update()
        clock.tick(5)

    pygame.quit()


def get_random_color():
    return (random.randint(25, 225), random.randint(25, 225), random.randint(25, 225))


class Grid:

    def __init__(self, size_x, size_y, block_size):
        self.size_x = size_x
        self.size_y = size_y
        self.block_size = block_size
        self.blocks = self.__create_blocks__()
        
    def __create_blocks__(self):
        blocks = []
        for x in range(0, self.size_x):
            col = []
            for y in range(0, self.size_y):
                col.append(Block(self, x, y))
            blocks.append(col)
        return blocks

    def draw_grid(self):
        for x in range(self.size_x):
            for y in range(self.size_y):
                self.blocks[x][y].draw()

    def get_block(self, x, y):
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

    def __init__(self, grid, x, y):
        self.grid = grid
        self.pos_x = x
        self.pos_y = y
        self.size = BLOCK_SIZE
        self.rect = pygame.Rect(self.pos_x * self.size, self.pos_y * self.size, self.size, self.size)
        self.creature = None

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
            pygame.draw.rect(WINDOW, COLOR_LINES, self.rect, 1)


class Creature:

    def __init__(self, block):
        self.block = block
        self.grid = self.block.grid
        self.color = get_random_color()

        self.block.add_creature(self)

    def draw(self):
        pygame.draw.circle(WINDOW, self.color, self.block.rect.center, BLOCK_SIZE / 2, 0)

    def move(self):
        move_prefs = self.determine_move_preferences()
        for m in move_prefs:
            if self.move_is_possible(m):
                #new_block = self.block.get_adjacent_block(m)
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
            if pos_x == GRID_SIZE_X - 1 or self.block.get_adjacent_block(move).is_occupied():
                return False
        elif move == "left":
            if pos_x == 0 or self.block.get_adjacent_block(move).is_occupied():
                return False
        elif move == "down":
            if pos_y == GRID_SIZE_Y - 1 or self.block.get_adjacent_block(move).is_occupied():
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
        


if __name__ == "__main__":
    main()