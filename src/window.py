import pygame

class Window:

    import environment

    def __init__(self, title = None, display: pygame.Surface = None, grid_size = (64, 64), block_size = 16) -> None:
        # from environment import Grid
        import environment
        self.title = title

        self.grid_size = grid_size
        self.grid_size_x = grid_size[0]
        self.grid_size_y = grid_size[1]
        self.block_size = block_size

        self.grid_width = self.grid_size_x * self.block_size
        self.grid_height = self.grid_size_y * self.block_size

        self.right_panel_size = (self.grid_width) * 0.65
        self.right_panel_lines = 30

        self.width = self.grid_width + self.right_panel_size
        self.height = self.grid_height
        self.size = (self.width, self.height)

        self.font = pygame.font.Font('freesansbold.ttf', 20)
        
        self.texts = []
        self.text_rects = []
        for i in range(self.right_panel_lines):
            self.texts.append("")
            self.text_rects.append(pygame.Rect(self.grid_width, (self.height / self.right_panel_lines) * i, self.right_panel_size, self.height / self.right_panel_lines))

        self.grid: environment.Grid = None
        self.selected_block = None
        self.selected_creature = None

        self.display = display
        self.paused = False

        return

    def draw(self):
        self.grid.draw_grid()
        self.draw_right_panel()
        return

    def draw_right_panel(self):
        self.set_right_panel_text()
        for i, rect in enumerate(self.text_rects):
            text = self.font.render(self.texts[i], True, (0, 0, 0), (255, 255, 255))
            self.display.blit(text, rect)
            pygame.draw.rect(self.display, (225, 225, 225), rect, 1)
        return

        # for text in self.texts:
        #     self.display.blit(self.font.render(text, True, (0, 0, 0), (255, 255, 255)))
        #     pygame.draw.rect(self.display, (255, 255, 255), textrect, 1)

        # game_window.display.blit(text, textrect)
        # pygame.draw.rect(game_window.display, white, textrect, 1)

    def on_click(self, pos):
        for x in range(self.grid_size_x):
            for y in range(self.grid_size_y):
                block = self.grid.get_block(x, y)
                if block.rect.collidepoint(pos):
                    self.selected_block = block
                    if block.creature != None:
                        self.selected_creature = block.creature
                    else:
                        self.selected_creature = None
                    self.set_right_panel_text()
                    break
        return

    
    def on_key_press(self, key):
        if key == pygame.K_SPACE:
            self.toggle_pause()
        return

    def toggle_pause(self):
        self.paused = not self.paused
        return

    def create_display(self):
        self.display = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        return

    def set_title(self, title):
        self.title = title
        pygame.display.set_caption(self.title)
        return
    
    def set_right_panel_text(self):
        for i in range(len(self.texts)):
            self.texts[i] = ""
        if self.selected_block == None:
            return

        self.texts[0] = f"Block: [{self.selected_block.pos_x}, {self.selected_block.pos_y}]"
        self.texts[1] = ""

        if self.selected_creature != None:
            self.texts[2] = "CREATURE BRAIN:"
            for i in range(self.selected_creature.brain.num_synapses):
                synapse = self.selected_creature.brain.synapses[i]
                self.texts[i + i + 3] = f"{synapse.input.type.name} -> {synapse.output.type.name} (w: {round(synapse.weight, 4)})"
                #self.texts[i + i + 4] = f"input: {round(synapse.output.input_value, 4)} | activation: {round(synapse.output.activation_value, 4)}"
                self.texts[i + i + 4] = f"input raw: {round(synapse.output.input_unweighted, 4)} | input weighted: {round(synapse.output.input_value, 4)} | activation: {round(max(synapse.output.activation_value, 0) * 100, 4)} %"

        return

        # self.text = self.font.render('Test', True, black, white)
        # game_window.display.blit(text, textrect)
        # pygame.draw.rect(game_window.display, white, textrect, 1) 