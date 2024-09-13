import pygame

class Player:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.player_size = 10
        self.rect = pygame.Rect(self.x, self.y, self.player_size, self.player_size)
        self.color = (250, 120, 60)
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4

    @staticmethod
    def get_current_cell(x, y, grid_cells):
        for cell in grid_cells:
            if cell.x == x and cell.y == y:
                return cell

    def check_move(self, tile, grid_cells, thickness):
        current_cell_x, current_cell_y = self.x // tile, self.y // tile
        current_cell = self.get_current_cell(current_cell_x, current_cell_y, grid_cells)

        current_cell_abs_x, current_cell_abs_y = current_cell_x * tile, current_cell_y * tile

        if self.left_pressed:
            if current_cell.walls['left'] and self.x <= current_cell_abs_x + thickness:
                self.left_pressed = False
            else:
                self.x -= self.speed

        if self.right_pressed:
            if current_cell.walls['right'] and self.x + self.player_size >= current_cell_abs_x + tile - thickness:
                self.right_pressed = False
            else:
                self.x += self.speed

        if self.up_pressed:
            if current_cell.walls['top'] and self.y <= current_cell_abs_y + thickness:
                self.up_pressed = False
            else:
                self.y -= self.speed

        if self.down_pressed:
            if current_cell.walls['bottom'] and self.y + self.player_size >= current_cell_abs_y + tile - thickness:
                self.down_pressed = False
            else:
                self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
