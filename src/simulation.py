import pygame
import config
import creatures
import window

from creatures import Creature

class SimulationState:

    def __init__(self) -> None:

        self.window = window.Window()
        self.creatures = creatures.generate_creatures(self.window.grid, config.POPULATION)

        self.num_generations = config.NUMBER_OF_GENERATIONS
        self.steps_per_generation = config.STEPS_PER_GENERATION

        self.paused = False

        self.generation_count = 0
        self.step_count = 0

    def step(self):
        if self.paused == False:
            self.step_count += 1
            creatures.trigger_creature_actions(self.creatures)

        self.window.draw()
        creatures.draw_creatures(self.creatures)

        if self.step_count == self.steps_per_generation:
            self.new_generation()


    def new_generation(self):
        self.generation_count += 1
        self.step_count = 0
        self.kill_creatures_in_kill_zones()
        print(f"New Generation: {self.generation_count}")
        if config.PAUSE_ON_NEW_GENERATION:
            self.paused = True

    def on_click(self, pos):
        for x in range(self.window.grid_size_x):
            for y in range(self.window.grid_size_y):
                block = self.window.grid.get_block(x, y)
                if block.rect.collidepoint(pos):
                    self.window.select_block(block)
        return

    def on_key_press(self, key):
        if key == pygame.K_SPACE:
            self.toggle_pause()
        if key == pygame.K_RIGHT:
            if self.window.selected_block != None and self.window.selected_block.pos_x < self.window.grid_size_x - 1:
                self.window.select_block(self.window.selected_block.get_adjacent_block("right"))
        if key == pygame.K_LEFT:
            if self.window.selected_block != None and self.window.selected_block.pos_x > 0:
                self.window.select_block(self.window.selected_block.get_adjacent_block("left"))
        if key == pygame.K_UP:
            if self.window.selected_block != None and self.window.selected_block.pos_y > 0:
                self.window.select_block(self.window.selected_block.get_adjacent_block("up"))
        if key == pygame.K_DOWN:
            if self.window.selected_block != None and self.window.selected_block.pos_y < self.window.grid_size_y - 1:
                self.window.select_block(self.window.selected_block.get_adjacent_block("down"))
        return
    
    def toggle_pause(self):
        self.paused = not self.paused
        return
    
    def kill_creatures_in_kill_zones(self):
        for c in self.creatures[:]:
            c: Creature
            for kz in self.window.grid.kill_zones:
                if c.block.rect.colliderect(kz):
                    c.block.remove_creature()
                    self.creatures.remove(c)
                    del c

        self.window.draw()
        creatures.draw_creatures(self.creatures)
        pygame.display.update()