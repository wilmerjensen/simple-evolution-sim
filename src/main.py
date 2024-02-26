import sys
import pygame

import window
import environment
import creatures

GRID_SIZE_X = 50
GRID_SIZE_Y = 50
BLOCK_SIZE = 25

# RIGHT_PANEL_SIZE = (GRID_SIZE_X * BLOCK_SIZE) * 0.35
# WINDOW_WIDTH = GRID_SIZE_X * BLOCK_SIZE + RIGHT_PANEL_SIZE
# WINDOW_HEIGHT = GRID_SIZE_Y * BLOCK_SIZE
# WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
# WINDOW = pygame.display.set_mode(WINDOW_SIZE)

SELECTED_BLOCK = None

POPULATION = 10
TICKS_PER_SECOND = 1

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)

def main():

    pygame.init()

    game_window = window.Window(title="Evolution Simulation", grid_size=(GRID_SIZE_X, GRID_SIZE_Y), block_size=BLOCK_SIZE)
    game_window.create_display()

    clock = pygame.time.Clock()
    running = True

    grid = environment.Grid(game_window.display, game_window.grid_size_x, game_window.grid_size_x, game_window.block_size)
    creature_list = creatures.Creature.generate_creatures(grid, POPULATION)

    font = pygame.font.Font('freesansbold.ttf', 32)
    textrect = pygame.Rect(game_window.grid_width, 0, game_window.right_panel_size, game_window.height / 8)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click()

        for c in creature_list:
            c.move()

        grid.draw_grid()
        draw_selected_block()

        text = font.render('Test', True, black, white)
        game_window.display.blit(text, textrect)
        pygame.draw.rect(game_window.display, white, textrect, 1)

        pygame.display.update()
        clock.tick(TICKS_PER_SECOND)

    pygame.quit()

def draw_selected_block():
    if SELECTED_BLOCK == None:
        return
    pygame.draw.rect(SELECTED_BLOCK.grid.window, green, SELECTED_BLOCK.rect, 1)

def display_block_info(block):
    if block == None:
        return
    return  

def mouse_click():
    print(pygame.mouse.get_pos())
    

if __name__ == "__main__":
    main()