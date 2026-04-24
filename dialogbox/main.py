import pygame
import sys

pygame.init()

# 画面設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Screen Transition Demo")
clock = pygame.time.Clock()

# 色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
GREEN = (0, 150, 100)
GRAY = (200, 200, 200)
HOVER_COLOR = (100, 150, 255)

# フォント
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)

# ボタンクラス
class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.is_hovered = False

    def draw(self, surface):
        color = HOVER_COLOR if self.is_hovered else BLUE
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text_surf = font_medium.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()

# 画面クラス
class Screen:
    def __init__(self, name):
        self.name = name
        self.buttons = []

    def draw(self, surface):
        surface.fill(WHITE)
        title = font_large.render(self.name, True, BLACK)
        surface.blit(title, (50, 50))
        for button in self.buttons:
            button.draw(surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.check_hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.check_click(event.pos)

# 画面遷移管理
current_screen = None

def go_to_screen1():
    global current_screen
    current_screen = screen1

def go_to_screen2():
    global current_screen
    current_screen = screen2

def go_to_screen3():
    global current_screen
    current_screen = screen3

# スクリーン定義
screen1 = Screen("Screen 1")
screen1.buttons = [
    Button(300, 200, 200, 60, "Go to Screen 2", go_to_screen2),
    Button(300, 300, 200, 60, "Go to Screen 3", go_to_screen3),
]

screen2 = Screen("Screen 2")
screen2.buttons = [
    Button(300, 200, 200, 60, "Back to Screen 1", go_to_screen1),
    Button(300, 300, 200, 60, "Go to Screen 3", go_to_screen3),
]

screen3 = Screen("Screen 3")
screen3.buttons = [
    Button(300, 200, 200, 60, "Back to Screen 1", go_to_screen1),
    Button(300, 300, 200, 60, "Back to Screen 2", go_to_screen2),
]

current_screen = screen1

# メインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        current_screen.handle_event(event)

    current_screen.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()