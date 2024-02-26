import pygame

class Window:

    def __init__(self, title = None, display: pygame.Surface = None, grid_size = (64, 64), block_size = 16) -> None:
        self.title = title

        self.grid_size = grid_size
        self.grid_size_x = grid_size[0]
        self.grid_size_y = grid_size[1]
        self.block_size = block_size

        self.grid_width = self.grid_size_x * self.block_size
        self.grid_height = self.grid_size_y * self.block_size

        self.right_panel_size = (self.grid_width) * 0.35

        self.width = self.grid_width + self.right_panel_size
        self.height = self.grid_height
        self.size = (self.width, self.height)

        self.grid = None
        self.selected_block = None

        self.display = display

    def create_display(self):
        self.display = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)

    def set_title(self, title):
        self.title = title
        pygame.display.set_caption(self.title)