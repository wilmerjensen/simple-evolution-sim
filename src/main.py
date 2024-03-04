import sys
import pygame
import config

from simulation import SimulationState

def main():

    pygame.init()
    clock = pygame.time.Clock()
    running = True
    
    simulation_state = SimulationState()

    kill_start_x = ((config.GRID_SIZE_X * config.BLOCK_SIZE) / 100) * 5
    kill_start_y = 0
    kill_width = ((config.GRID_SIZE_X * config.BLOCK_SIZE) / 100) * 90
    kill_height = config.GRID_SIZE_Y * config.BLOCK_SIZE
    simulation_state.window.grid.add_kill_zone((kill_start_x, kill_start_y), (kill_width, kill_height))

    while running:

        for event in pygame.event.get():
            event_handler(event, simulation_state)

        simulation_state.update()
        pygame.display.update()

        clock.tick(config.MAX_FPS)
        simulation_state.window.current_fps = int(clock.get_fps())

    pygame.quit()

def event_handler(event, simulation):
    if event.type == pygame.QUIT:
        sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        simulation.on_click(event.pos)
    if event.type == pygame.KEYDOWN:
        simulation.on_key_press(event.key)


if __name__ == "__main__":
    main()