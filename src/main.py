import sys
import pygame

import window
import environment
import creatures

GRID_SIZE_X = 100
GRID_SIZE_Y = 100
BLOCK_SIZE = 12

POPULATION = 200
SYNAPSES = 8

TICKS_PER_SECOND = 30
TICKS_PER_GENERATION = 300

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)

def main():

    pygame.init()

    game_window = window.Window(title="Evolution Simulation", grid_size=(GRID_SIZE_X, GRID_SIZE_Y), block_size=BLOCK_SIZE)
    game_window.create_display()

    running = True
    clock = pygame.time.Clock()

    game_window.grid = environment.Grid(game_window, game_window.grid_size_x, game_window.grid_size_x, game_window.block_size)
    game_window.grid.add_kill_zone((0,0), ((GRID_SIZE_X * BLOCK_SIZE) / 10, GRID_SIZE_Y * BLOCK_SIZE))


    creature_list = creatures.Creature.generate_creatures(game_window.grid, POPULATION, SYNAPSES)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_window.on_click(event.pos)
            if event.type == pygame.KEYDOWN:
                game_window.on_key_press(event.key)

        if game_window.paused == False:
            for c in creature_list:
                c.action()
                
        game_window.draw()

        pygame.display.update()
        clock.tick(TICKS_PER_SECOND)

    pygame.quit()



if __name__ == "__main__":
    main()