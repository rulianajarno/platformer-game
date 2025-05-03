import random
from pgzero.builtins import Actor, Rect, keyboard, keys, mouse
import pgzrun

# Configurações
WIDTH = 800
HEIGHT = 600
GRAVITY = 0.6
JUMP_STRENGTH = -12
PLAYER_SPEED = 5
ENEMY_SPEED = 2.5
SCROLL_THRESHOLD = 400

# Estado
MENU = 0
PLAYING = 1
GAME_OVER = 2
game_state = MENU

# Música
music_playing = True
music_button = Rect(300, 450, 200, 50)

# Herói
player = Actor('stand', (100, 400))
player.vy = 0
player.on_ground = True
player.direction = 1
player.width = 30
player.height = 50
player.walk_frame = 0

# Inimigos
enemies = []
enemy_spawn_timer = 0

# Plataformas
platforms = [
    Rect(0, 550, 800, 50),
    Rect(250, 450, 200, 20),
    Rect(450, 350, 200, 20),
    Rect(650, 450, 200, 20),
    Rect(850, 350, 200, 20)
]

scroll_x = 0

def reset_game():
    global player, platforms, enemies, scroll_x, game_state
    player.pos = (100, 400)
    player.vy = 0
    player.on_ground = True
    platforms = [
        Rect(0, 550, 800, 50),
        Rect(250, 450, 200, 20),
        Rect(450, 350, 200, 20),
        Rect(650, 450, 200, 20),
        Rect(850, 350, 200, 20)
    ]
    enemies = []
    scroll_x = 0
    game_state = PLAYING

    if music_playing:
        music.play('background')

def spawn_enemy():
    spawn_x = scroll_x + WIDTH + 50
    spawn_y = HEIGHT - 100
    for plat in platforms:
        if plat.x <= spawn_x <= plat.x + plat.width:
            spawn_y = plat.y - 30
            break
    enemy = Actor('enemy_walk1', (spawn_x, spawn_y))
    enemy.speed = ENEMY_SPEED
    enemy.walk_frame = 0
    enemy.width = 40
    enemy.height = 60
    enemies.append(enemy)

def update_player():
    if keyboard.left:
        player.x -= PLAYER_SPEED
        player.direction = -1
        player.walk_frame += 0.2
        player.image = f'walk{int(player.walk_frame)%10+1}'
    elif keyboard.right:
        player.x += PLAYER_SPEED
        player.direction = 1
        player.walk_frame += 0.2
        player.image = f'walk{int(player.walk_frame)%10+1}'
    else:
        if player.on_ground:
            player.image = 'stand'
    player.flip_x = player.direction < 0
    player.vy += GRAVITY
    player.y += player.vy
    player.on_ground = False
    for platform in platforms:
        plat_x = platform.x - scroll_x
        if (player.x > plat_x and
            player.x < plat_x + platform.width and
            player.bottom < platform.y + platform.height and
            player.bottom + player.vy > platform.y):
            player.bottom = platform.y
            player.vy = 0
            player.on_ground = True
    if keyboard.up and player.on_ground:
        player.vy = JUMP_STRENGTH
        player.on_ground = False
        player.image = 'jump'

def update_enemies():
    global game_state
    for enemy in enemies[:]:
        enemy.x -= enemy.speed
        enemy.walk_frame += 0.2
        enemy.image = f'enemy_walk{int(enemy.walk_frame)%3+1}'
        enemy_rect = Rect(enemy.x - scroll_x, enemy.y, enemy.width, enemy.height)
        if Rect(player.x, player.y, player.width, player.height).colliderect(enemy_rect):
            if player.vy > 0 and player.bottom < enemy.y + 20:
                enemies.remove(enemy)
                player.vy = JUMP_STRENGTH / 2
            else:
                game_state = GAME_OVER
        if enemy.x < scroll_x - 50:
            enemies.remove(enemy)

def update_scroll():
    global scroll_x
    if player.x > SCROLL_THRESHOLD:
        scroll_x += player.x - SCROLL_THRESHOLD
        player.x = SCROLL_THRESHOLD

def update_platforms():
    if platforms[-1].x - scroll_x < WIDTH:
        last_plat = platforms[-1]
        new_x = last_plat.x + random.randint(200, 300)
        new_y = random.choice([350, 400, 450])
        if abs(new_y - last_plat.y) > 100:
            new_x = last_plat.x + 200
        platforms.append(Rect(new_x, new_y, 200, 20))
    if len(platforms) > 5 and platforms[0].x + platforms[0].width < scroll_x:
        platforms.pop(0)

def update():
    global enemy_spawn_timer, game_state
    if game_state != PLAYING:
        return
    update_player()
    update_scroll()
    update_platforms()
    update_enemies()
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= 90 and random.random() < 0.7:
        spawn_enemy()
        enemy_spawn_timer = 0
    if player.top > HEIGHT:
        game_state = GAME_OVER

def draw_menu():
    screen.clear()
    screen.fill((135, 206, 235))
    screen.draw.text("PLATFORMER", center=(WIDTH/2, 150), fontsize=70, color="black")
    start_btn = Rect(300, 250, 200, 50)
    quit_btn = Rect(300, 350, 200, 50)
    screen.draw.filled_rect(start_btn, (0, 200, 0))
    screen.draw.text("INICIAR", center=start_btn.center, fontsize=40, color="white")
    screen.draw.filled_rect(quit_btn, (200, 0, 0))
    screen.draw.text("SAIR", center=quit_btn.center, fontsize=40, color="white")

    # Botão de música
    screen.draw.filled_rect(music_button, (0, 0, 200))
    label = "MUSICA: ON" if music_playing else "MUSICA: OFF"
    screen.draw.text(label, center=music_button.center, fontsize=30, color="white")

def draw_game():
    screen.clear()
    screen.fill((135, 206, 235))
    for platform in platforms:
        screen.draw.filled_rect(
            Rect(platform.x - scroll_x, platform.y, platform.width, platform.height),
            (100, 100, 100)
        )
    for enemy in enemies:
        enemy.x -= scroll_x
        enemy.draw()
        enemy.x += scroll_x
    player.draw()

    # Botão de voltar ao menu
    menu_btn = Rect(10, 10, 120, 40)
    screen.draw.filled_rect(menu_btn, (0, 0, 200))
    screen.draw.text("MENU", center=menu_btn.center, fontsize=30, color="white")

def draw_game_over():
    screen.draw.text("GAME OVER", center=(WIDTH/2, 250), fontsize=70, color="red")
    screen.draw.text("Pressione R para reiniciar", center=(WIDTH/2, 350), fontsize=30, color="black")

def on_key_down(key):
    if game_state == PLAYING and key == keys.UP and player.on_ground:
        player.vy = JUMP_STRENGTH
        player.on_ground = False
    elif game_state == GAME_OVER and key == keys.R:
        reset_game()

def toggle_music():
    global music_playing
    music_playing = not music_playing
    if music_playing:
        music.play('background')
    else:
        music.stop()

def on_mouse_down(pos):
    global game_state
    if game_state == MENU:
        start_btn = Rect(300, 250, 200, 50)
        quit_btn = Rect(300, 350, 200, 50)
        if start_btn.collidepoint(pos):
            reset_game()
        elif quit_btn.collidepoint(pos):
            quit()
        elif music_button.collidepoint(pos):
            toggle_music()
    elif game_state == PLAYING:
        menu_btn = Rect(10, 10, 120, 40)
        if menu_btn.collidepoint(pos):
            game_state = MENU

def draw():
    if game_state == MENU:
        draw_menu()
    elif game_state == PLAYING:
        draw_game()
    elif game_state == GAME_OVER:
        draw_game()
        draw_game_over()
