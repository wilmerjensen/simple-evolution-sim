import pygame
import config

class Window:

    def __init__(self, simulation) -> None:
        from environment import Grid, Block
        from simulation import SimulationState
        from creatures import Creature

        self.simulation: SimulationState = simulation

        self.title = config.WINDOW_TITLE

        self.grid_size = (config.GRID_SIZE_X, config.GRID_SIZE_Y)
        self.grid_size_x = config.GRID_SIZE_X
        self.grid_size_y = config.GRID_SIZE_Y
        self.block_size = config.BLOCK_SIZE

        self.grid_width = self.grid_size_x * self.block_size
        self.grid_height = self.grid_size_y * self.block_size

        self.grid: Grid = Grid(self, self.grid_size_x, self.grid_size_x, self.block_size)

        self.right_panel_size = (self.grid_width) * 0.5
        self.right_panel_lines = 40

        self.width = self.grid_width + self.right_panel_size
        self.height = self.grid_height
        self.size = (self.width, self.height)

        self.font = pygame.font.Font('freesansbold.ttf', 18)
        
        self.texts = []
        self.text_rects = []
        for i in range(self.right_panel_lines):
            self.texts.append("")
            self.text_rects.append(pygame.Rect(self.grid_width, (self.height / self.right_panel_lines) * i, self.right_panel_size, self.height / self.right_panel_lines))

        self.selected_block: Block = None
        self.selected_creature: Creature = None

        self.create_display()
        self.current_fps = 0

        return

    def draw(self):
        self.grid.draw_grid()
        if self.selected_block != None:
            self.selected_block.draw((200, 0, 0))
        self.draw_right_panel()
        return

    def draw_right_panel(self):
        self.set_right_panel_text()
        for i, rect in enumerate(self.text_rects):
            text = self.font.render(self.texts[i], True, (0, 0, 0), (225, 225, 225))
            self.display.blit(text, rect)
            pygame.draw.rect(self.display, (175, 175, 175), rect, 1)
        return

    def select_block(self, block):
        self.selected_block = block
        if block.creature != None:
            self.selected_creature = block.creature
        else:
            self.selected_creature = None
        self.set_right_panel_text()

    def create_display(self):
        self.display = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)

    def set_title(self, title):
        self.title = title
        pygame.display.set_caption(self.title)
        return
    
    def set_right_panel_text(self):

        from math import tanh

        for i in range(len(self.texts)):
            self.texts[i] = ""

        self.texts[0] = f"FPS: {self.current_fps}"
        self.texts[1] = f"World size: {config.GRID_SIZE_X}x{config.GRID_SIZE_Y}"
        self.texts[2] = f"Population: {config.POPULATION}"
        self.texts[3] = f"Synapses: {config.NUMBER_OF_SYNAPSES}"
        self.texts[4] = f"Mutation rate: {config.MUTATION_RATE}"
        self.texts[5] = ""
        self.texts[6] = f"Generation: {self.simulation.generation_count}"
        self.texts[7] = f"Survival rate: {self.simulation.latest_survival_rate}%"
        self.texts[8] = ""

        if self.selected_block == None:
            return

        self.texts[9] = f"Block: [{self.selected_block.pos_x}, {self.selected_block.pos_y}]"

        if self.selected_creature != None:
            synapses = sorted(self.selected_creature.brain.synapses, key=lambda x: x.output.input_value, reverse=True)
            for i, synapse in enumerate(synapses):
                self.texts[10 + i] = f"{synapse.input.type.name} -> {synapse.output.type.name} (w: {round(synapse.weight, 4)}, a: {round(max(tanh(synapse.output.input_value), 0) * 100)}%)"

            self.texts[len(self.texts) - 1] = f"Creatures in vision: {self.selected_creature.get_population_within_vision()}"