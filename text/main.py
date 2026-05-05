import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Click to change text")

# 日本語フォントを取得する関数
def get_jp_font(size):
    available_fonts = set(pygame.font.get_fonts())
    preferred_fonts = ["meiryo", "notosansjp", "notosanscjkjp"]

    for font_name in preferred_fonts:
        if font_name in available_fonts:
            print(f"Using font: {font_name}")
            return pygame.font.SysFont(font_name, size)

    print("日本語フォントが見つからなかったため、デフォルトフォントを使用します。")
    return pygame.font.SysFont(None, size)

font = get_jp_font(24)

# ボタンの Rect（画面中央）
button_rect = pygame.Rect(0, 0, 300, 100)
button_rect.center = (400, 300)
button_color = (200, 200, 255)

# 切り替える文字のリスト
messages = [
    "文字をクリックしてね",
    "1回クリックされた！",
    "2回クリックされた！",
    "3回クリックされた！",
    "またクリックしてね"
]

msg_index = 0  # 現在のメッセージ番号

# 最初の文字
text = font.render(messages[msg_index], True, (0, 0, 0))
text_rect = text.get_rect(center=button_rect.center)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # マウスクリック
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                # 次のメッセージへ
                msg_index = (msg_index + 1) % len(messages)

                # 新しい文字をレンダリング
                text = font.render(messages[msg_index], True, (0, 0, 0))
                text_rect = text.get_rect(center=button_rect.center)

    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, button_color, button_rect)
    screen.blit(text, text_rect)

    pygame.display.update()

pygame.quit()