import pgzrun
from pgzero.actor import Actor
from pygame import Rect
import random

WIDTH = 800
HEIGHT = 600

game_state = "menu"
sound_on = True
score = 0
errors = 0

# listas globais para armazenar os atores
coins = []
spawned_enemies = []   # <--- aqui você cria a lista de inimigos

buttons = {
    "start": Rect(300, 200, 200, 50),
    "toggle_sound": Rect(300, 270, 200, 50),
    "exit": Rect(300, 340, 200, 50)
}

# ---------------- FUNÇÕES ---------------- #

def spawn_coin():
    # cria moeda em posição aleatória
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    coin = Actor("coin")
    coin.pos = (x, y)
    coins.append(coin)

def draw():
    screen.clear()

    if game_state == "menu":
        screen.fill("black")

        # Botão Start
        screen.draw.text("Start Game", center=buttons["start"].center, color="white", fontsize=40)
        screen.draw.rect(buttons["start"], "white")

        # Botão Toggle Sound (cor muda conforme estado)
        toggle_color = "white" if sound_on else "red"
        screen.draw.text("Toggle Sound", center=buttons["toggle_sound"].center, color=toggle_color, fontsize=40)
        screen.draw.rect(buttons["toggle_sound"], toggle_color)

        # Botão Exit
        screen.draw.text("Exit", center=buttons["exit"].center, color="white", fontsize=40)
        screen.draw.rect(buttons["exit"], "white")

    elif game_state == "playing":
        bg = Actor("fundo")
        bg.pos = (WIDTH // 2, HEIGHT // 2)
        bg.draw()

        # moedas
        for coin in coins:
            coin.draw()

        # inimigos
        for enemy in spawned_enemies:
            enemy.draw()

        # HUD
        screen.draw.text(f"Score: {score}", (10, 10), color="white", fontsize=30)
        screen.draw.text(f"Errors: {errors}/4", (10, 40), color="red", fontsize=30)

    elif game_state == "game_over":
        screen.fill("black")
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")
        screen.draw.text(f"Final Score: {score}", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=40, color="white")


def on_mouse_down(pos):
    global game_state, sound_on, score, errors

    if game_state == "menu":
        if buttons["start"].collidepoint(pos):
            game_state = "playing"
            start_music()
            spawn_coin()
        elif buttons["toggle_sound"].collidepoint(pos):
            sound_on = not sound_on
            start_music()
        elif buttons["exit"].collidepoint(pos):
            exit()

    elif game_state == "playing":
        hit = False
        for coin in coins:
            if coin.collidepoint(pos):
                coins.remove(coin)
                score += 1
                hit = True
                if sound_on:
                    sounds.coin.play()
                spawn_coin()  # nova moeda

                # 👾 cria inimigo ao acertar a moeda
                enemy = Actor("enemy_idle_left1")
                enemy.pos = pos  # aparece na posição da moeda
                spawned_enemies.append(enemy)

                if sound_on:
                    sounds.hit.play()
                break

        if not hit:
            errors += 1
            if sound_on:
                sounds.hit.play()
            if errors >= 4:
                game_state = "game_over"


def start_music():
    if sound_on:
        music.play("background")
        music.set_volume(0.5)
    else:
        music.stop()

def update():
    pass

pgzrun.go()
