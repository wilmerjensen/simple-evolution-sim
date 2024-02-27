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

TICKS_PER_SECOND = 60
TICKS_PER_GENERATION = 300
GENERATION_TICK_COUNT = 0
GENERATION_COUNT = 0

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

    generation_tick_count = 0
    generation_count = 0

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

        generation_tick_count += 1
        if generation_tick_count == TICKS_PER_GENERATION:
            print("New Generation!")
            generation_tick_count = 0
            generation_count += 1
            kill_creatures_in_kill_zones(game_window.grid, creature_list)
            game_window.draw()
            pygame.display.update()
            clock.tick(TICKS_PER_SECOND)
            pygame.time.wait(2000)

    pygame.quit()


def kill_creatures_in_kill_zones(grid: environment.Grid, creature_list: list):
    for c in creature_list:
        c: creatures.Creature
        for kz in grid.kill_zones:
            if c.block.rect.colliderect(kz):
                c.block.remove_creature()
                creature_list.remove(c)
                del c

if __name__ == "__main__":
    main()