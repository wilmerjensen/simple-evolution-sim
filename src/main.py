import sys
import pygame

import environment
import creatures

GRID_SIZE_X = 50
GRID_SIZE_Y = 50
BLOCK_SIZE = 25

RIGHT_PANEL_SIZE = (GRID_SIZE_X * BLOCK_SIZE) * 0.35

WINDOW_WIDTH = GRID_SIZE_X * BLOCK_SIZE + RIGHT_PANEL_SIZE
WINDOW_HEIGHT = GRID_SIZE_Y * BLOCK_SIZE
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_TITLE = "Evolution Simulation"
WINDOW = pygame.display.set_mode(WINDOW_SIZE)

POPULATION = 10
TICKS_PER_SECOND = 1


def main():

    pygame.init()
    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()
    running = True

    grid = environment.Grid(WINDOW, GRID_SIZE_X, GRID_SIZE_Y, BLOCK_SIZE)
    creature_list = creatures.Creature.generate_creatures(grid, POPULATION)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click()

        for c in creature_list:
            c.move()

        grid.draw_grid()

        pygame.display.update()
        clock.tick(TICKS_PER_SECOND)

    pygame.quit()

def mouse_click():
    print(pygame.mouse.get_pos())

if __name__ == "__main__":
    main()