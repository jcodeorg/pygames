'''
基本の移動ゲーム）
🐱 Scratch 版（よくある構成）
Scratch ではこんなブロックで作ります：
- 「ずっと」
- 「右向き矢印が押された → x座標を10ずつ変える」
- 「左向き矢印が押された → x座標を-10ずつ変える」
- 「上向き矢印が押された → y座標を10ずつ変える」
- 「下向き矢印が押された → y座標を-10ずつ変える」
Scratch は y軸が上向きなので、上矢印で y が増える。
'''
import pygame

pygame.init()

# 画面
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Rect move sample")

# プレイヤー（四角形）
player_rect = pygame.Rect(400, 300, 50, 50)  # x, y, width, height
player_color = (0, 128, 255)

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)  # 60FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # キー入力
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    if keys[pygame.K_UP]:
        player_rect.y -= 5   # 上はマイナス
    if keys[pygame.K_DOWN]:
        player_rect.y += 5

    # 背景（黒で塗りつぶし）
    screen.fill((0, 0, 0))  # 黒背景

    # プレイヤー（四角形）を描画
    pygame.draw.rect(screen, player_color, player_rect)

    pygame.display.update()

pygame.quit()