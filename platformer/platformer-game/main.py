import random
from pgzero.builtins import Rect
import pgzrun

WIDTH = 800
HEIGHT = 400

GRAVITY = 0.6
JUMP_STRENGTH = -12
player_speed = 3
enemy_speed = 2.5

player = Rect((100, 300), (30, 30))
player_vy = 0
on_ground = False
jump_pressed_last_frame = False

platforms = [Rect((0, 350), (300, 20))]
coins = []
enemies = []
bullets = []  # Enemy killer

scroll_x = 0
score = 0
game_started = False

def spawn_platforms():
    global platforms, coins
    last_platform = platforms[-1]

    max_jump_height = 120
    max_gap = 90
    min_gap = 60

    for i in range(5):
        gap = random.randint(min_gap, max_gap)
        new_x = last_platform.x + last_platform.width + gap

        min_y = max(150, last_platform.y - max_jump_height)
        max_y = min(HEIGHT - 50, last_platform.y + 50)
        new_y = random.randint(min_y, max_y)

        platform = Rect((new_x, new_y), (random.randint(80, 120), 20))
        platforms.append(platform)

        if random.random() < 0.7:
            coin = Rect((platform.centerx - 10, platform.y - 20), (20, 20))
            coins.append(coin)

        last_platform = platform

def spawn_enemy():
    y = random.randint(50, HEIGHT - 100)
    x = scroll_x + WIDTH + random.randint(0, 300)
    enemy = Rect((x, y), (30, 30))
    enemies.append(enemy)

spawn_platforms()

def update():
    global player_vy, on_ground, scroll_x, score, game_started
    global jump_pressed_last_frame

    if not game_started:
        return

    prev_y = player.y

    if keyboard.right:
        player.x += player_speed
        scroll_x += player_speed
    if keyboard.left:
        player.x -= player_speed
        scroll_x -= player_speed

    player_vy += GRAVITY
    player.y += player_vy
    on_ground = False

    for plat in platforms:
        if (
            player.colliderect(plat)
            and player_vy > 0
            and prev_y + player.height <= plat.top + 5
        ):
            player.bottom = plat.top
            player_vy = 0
            on_ground = True

    if keyboard.up and on_ground and not jump_pressed_last_frame:
        player_vy = JUMP_STRENGTH
        on_ground = False

    jump_pressed_last_frame = keyboard.up

    # Atualizacao de inimigos
    for enemy in enemies[:]:
        enemy.x -= enemy_speed
        if enemy.x < scroll_x - 100:
            enemies.remove(enemy)
        if player.colliderect(enemy):
            reset_game()

    # Atualizacao de tiros
    for bullet in bullets[:]:
        bullet.x += 6
        if bullet.x > scroll_x + WIDTH:
            bullets.remove(bullet)
        else:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    break

    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            score += 1

    if platforms[-1].x - scroll_x < WIDTH:
        spawn_platforms()

    if random.random() < 0.02:
        spawn_enemy()

    if player.y > HEIGHT:
        reset_game()

def on_key_down(key):
    if key == keys.SPACE:
        bullet = Rect((player.right, player.centery - 15), (10, 40))  # 4 bolinhas nos tiros
        bullets.append(bullet)

def reset_game():
    global player, player_vy, score, platforms, coins, enemies, bullets, scroll_x
    player = Rect((100, 300), (30, 30))
    player_vy = 0
    score = 0
    platforms = [Rect((0, 350), (300, 20))]
    coins = []
    enemies = []
    bullets = []
    scroll_x = 0
    spawn_platforms()

def draw_menu():
    screen.clear()
    screen.fill((135, 206, 250))

    screen.draw.text("PLATFORMER GAME", center=(WIDTH//2, HEIGHT//4), fontsize=50, color="black")

    start_button = Rect((WIDTH//2 - 75, HEIGHT//2 - 25), (150, 50))
    screen.draw.filled_rect(start_button, (0, 128, 0))
    screen.draw.text("Iniciar", center=(WIDTH//2, HEIGHT//2), fontsize=30, color="white")

    quit_button = Rect((WIDTH//2 - 75, HEIGHT//2 + 50), (150, 50))
    screen.draw.filled_rect(quit_button, (255, 0, 0))
    screen.draw.text("Sair", center=(WIDTH//2, HEIGHT//2 + 75), fontsize=30, color="white")

def draw_game_buttons():
    menu_button = Rect((WIDTH - 160, 10), (70, 30))
    quit_button = Rect((WIDTH - 80, 10), (70, 30))

    screen.draw.filled_rect(menu_button, (100, 100, 255))
    screen.draw.text("Menu", center=menu_button.center, fontsize=20, color="white")

    screen.draw.filled_rect(quit_button, (255, 0, 0))
    screen.draw.text("Sair", center=quit_button.center, fontsize=20, color="white")

def on_mouse_down(pos):
    global game_started
    if not game_started:
        start_button = Rect((WIDTH//2 - 75, HEIGHT//2 - 25), (150, 50))
        quit_button = Rect((WIDTH//2 - 75, HEIGHT//2 + 50), (150, 50))

        if start_button.collidepoint(pos):
            game_started = True
            reset_game()
        elif quit_button.collidepoint(pos):
            quit()
    else:
        menu_button = Rect((WIDTH - 160, 10), (70, 30))
        quit_button = Rect((WIDTH - 80, 10), (70, 30))

        if menu_button.collidepoint(pos):
            game_started = False
        elif quit_button.collidepoint(pos):
            quit()

def draw():
    if not game_started:
        draw_menu()
        return

    screen.clear()
    screen.fill((135, 206, 250))

    for plat in platforms:
        screen.draw.filled_rect(Rect((plat.x - scroll_x, plat.y), plat.size), (100, 100, 100))

    for coin in coins:
        screen.draw.filled_circle((coin.centerx - scroll_x, coin.centery), 10, (255, 255, 0))  # Moeda redonda

    for enemy in enemies:
        screen.draw.filled_rect(Rect((enemy.x - scroll_x, enemy.y), enemy.size), (0, 128, 0))  # Inimigo verde escuro

    for bullet in bullets:
        bx = bullet.x - scroll_x + 5
        by = bullet.y
        for i in range(4):
            screen.draw.filled_circle((bx, by + i * 10), 5, (0, 0, 0))

    screen.draw.filled_rect(Rect((player.x - scroll_x, player.y), player.size), (255, 105, 180))  # Ator rosa
    screen.draw.text(f"Moedas: {score}", topleft=(10, 10), fontsize=30, color="black")

    draw_game_buttons()

pgzrun.go()
