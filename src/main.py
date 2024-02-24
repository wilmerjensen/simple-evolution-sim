import sys
import pygame
import random

import environment
import creatures

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

    grid = environment.Grid(WINDOW, GRID_SIZE_X, GRID_SIZE_Y, BLOCK_SIZE, COLOR_BACKGROUND, COLOR_LINES)
    creature_list = creatures.Creature.generate_creatures(grid, POPULATION)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        #WINDOW.fill(COLOR_BACKGROUND)

        for c in creature_list:
            c.move()

        grid.draw_grid()

        pygame.display.update()
        clock.tick(5)

    pygame.quit()


if __name__ == "__main__":
    main()