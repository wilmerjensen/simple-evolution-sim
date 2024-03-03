import pygame
import random
import config
import creatures
import window

from creatures import Creature

class SimulationState:

    def __init__(self) -> None:

        self.window = window.Window(self)
        self.creatures: list[Creature] = []

        self.num_generations = config.NUMBER_OF_GENERATIONS
        self.steps_per_generation = config.STEPS_PER_GENERATION

        self.generation_log = []
        self.latest_survival_rate = 0

        self.paused = False

        self.generation_count = 0
        self.step_count = 0

    def update(self):
        if self.paused == False:
            if self.step_count == 0:
                self.new_generation()
            self.step()

        self.window.draw()
        creatures.draw_creatures(self.creatures)

        if self.step_count == self.steps_per_generation:
            self.end_generation()

    def step(self):
        self.step_count += 1
        creatures.trigger_creature_actions(self.creatures)

    def end_generation(self):
        self.kill_creatures_in_kill_zones()
        creatures_survived = len(self.creatures)
        creatures_killed = config.POPULATION - creatures_survived
        self.latest_survival_rate = round((creatures_survived / config.POPULATION) * 100)
        print(f"Generation {self.generation_count} ended:")
        print(f"{creatures_killed} died")
        print(f"{self.latest_survival_rate}% survived")
        self.step_count = 0
        if config.PAUSE_ON_NEW_GENERATION:
            self.paused = True

    def new_generation(self):
        self.generation_count += 1
        if self.generation_count == 1:
            self.creatures = creatures.generate_creatures(self.window.grid, config.POPULATION)
        else:
            parents = self.creatures.copy()
            self.kill_all_creatures()
            self.creatures = creatures.generate_population_offspring(self.window.grid, config.POPULATION, parents)

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
    
    def kill_all_creatures(self):
        for c in self.creatures[:]:
            c: Creature
            c.block.remove_creature()
            self.creatures.remove(c)
            del c

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