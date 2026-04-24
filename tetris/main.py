import pygame
import random
from enum import Enum

pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 20
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
]

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[0, 1, 0], [1, 1, 1]],  # T
]

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

FALL_INTERVAL = 500  # ミリ秒ごとに1セル落下（大きいほどゆっくり）

class Game:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.score = 0
        self.game_over = False
        self.fall_timer = 0

    def is_collision(self, piece, x, y):
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[row])):
                if piece.shape[row][col]:
                    grid_x = x + col
                    grid_y = y + row
                    if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y >= GRID_HEIGHT:
                        return True
                    if grid_y >= 0 and self.grid[grid_y][grid_x]:
                        return True
        return False

    def place_piece(self, piece):
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[row])):
                if piece.shape[row][col]:
                    grid_y = piece.y + row
                    grid_x = piece.x + col
                    if grid_y >= 0:
                        self.grid[grid_y][grid_x] = piece.color

    def clear_lines(self):
        lines_to_clear = [i for i in range(GRID_HEIGHT) if all(self.grid[i])]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [0] * GRID_WIDTH)
        self.score += len(lines_to_clear) * 100

    def update(self, dt):
        self.fall_timer += dt
        if self.fall_timer < FALL_INTERVAL:
            return
        self.fall_timer = 0
        piece = self.current_piece
        if not self.is_collision(piece, piece.x, piece.y + 1):
            piece.y += 1
        else:
            self.place_piece(piece)
            self.clear_lines()
            self.current_piece = Tetromino()
            if self.is_collision(self.current_piece, self.current_piece.x, self.current_piece.y):
                self.game_over = True

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not self.is_collision(self.current_piece, self.current_piece.x - 1, self.current_piece.y):
                        self.current_piece.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not self.is_collision(self.current_piece, self.current_piece.x + 1, self.current_piece.y):
                        self.current_piece.x += 1
                elif event.key == pygame.K_DOWN:
                    if not self.is_collision(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                        self.current_piece.y += 1
                elif event.key == pygame.K_UP:
                    original_shape = self.current_piece.shape
                    self.current_piece.rotate()
                    if self.is_collision(self.current_piece, self.current_piece.x, self.current_piece.y):
                        self.current_piece.shape = original_shape
        return True

    def draw(self, screen):
        screen.fill(BLACK)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    pygame.draw.rect(screen, self.grid[y][x], 
                                   (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, GRAY, 
                               (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        piece = self.current_piece
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[row])):
                if piece.shape[row][col]:
                    pygame.draw.rect(screen, piece.color,
                                   ((piece.x + col) * CELL_SIZE, (piece.y + row) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = Game()

    while not game.game_over:
        dt = clock.tick(FPS)
        if not game.handle_input():
            break
        game.update(dt)
        game.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()