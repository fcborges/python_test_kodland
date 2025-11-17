import pgzrun
from pgzero.actor import Actor
from pygame import Rect
import random

WIDTH = 800
HEIGHT = 600

game_state = "menu"
sound_on = True

# Botões do menu
buttons = {
    "start": Rect(300, 200, 200, 50),
    "toggle_sound": Rect(300, 270, 200, 50),
    "exit": Rect(300, 340, 200, 50)
}

# ---------------- CLASSES ---------------- #

class Hero:
    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.x = grid_x * 64
        self.y = grid_y * 64
        self.target_x = self.x
        self.target_y = self.y
        self.speed = 4
        self.direction = "down"
        self.anim_index = 0
        self.anim_timer = 0
        self.idle_images = {
            "down": [Actor("hero_idle_down1"), Actor("hero_idle_down2")],
            "up": [Actor("hero_idle_down1"), Actor("hero_idle_down2")],
            "left": [Actor("hero_idle_down1"), Actor("hero_idle_down2")],
            "right": [Actor("hero_idle_down1"), Actor("hero_idle_down2")]
        }
        self.walk_images = {
            "down": [Actor("hero_walk_down1"), Actor("hero_walk_down2")],
            "up": [Actor("hero_walk_down1"), Actor("hero_walk_down2")],
            "left": [Actor("hero_walk_down1"), Actor("hero_walk_down2")],
            "right": [Actor("hero_walk_down1"), Actor("hero_walk_down2")]
        }
        self.moving = False

    def update(self):
        if self.moving:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            if abs(dx) > self.speed:
                self.x += self.speed if dx > 0 else -self.speed
            else:
                self.x = self.target_x
            if abs(dy) > self.speed:
                self.y += self.speed if dy > 0 else -self.speed
            else:
                self.y = self.target_y
            if self.x == self.target_x and self.y == self.target_y:
                self.moving = False

        self.anim_timer += 1
        if self.anim_timer >= 10:
            self.anim_index = (self.anim_index + 1) % 2
            self.anim_timer = 0

    def draw(self):
        if self.moving:
            img = self.walk_images[self.direction][self.anim_index]
        else:
            img = self.idle_images[self.direction][self.anim_index]
        img.pos = (self.x, self.y)
        img.draw()

    def move(self, dx, dy, game_map):
        if not self.moving:
            new_x = self.grid_x + dx
            new_y = self.grid_y + dy
            if not game_map.is_blocked(new_x, new_y):
                self.grid_x = new_x
                self.grid_y = new_y
                self.target_x = self.grid_x * 64
                self.target_y = self.grid_y * 64
                self.moving = True
                if dx > 0:
                    self.direction = "right"
                elif dx < 0:
                    self.direction = "left"
                elif dy > 0:
                    self.direction = "down"
                elif dy < 0:
                    self.direction = "up"


class Enemy:
    def __init__(self, path_cells, direction="left"):
        self.path = path_cells
        self.path_index = 0
        self.grid_x, self.grid_y = self.path[self.path_index]
        self.x = self.grid_x * 64
        self.y = self.grid_y * 64
        self.target_x = self.x
        self.target_y = self.y
        self.speed = 2
        self.direction = direction
        self.anim_index = 0
        self.anim_timer = 0
        self.idle_images = {
            "left": [Actor("enemy_idle_left1"), Actor("enemy_idle_left1")],
            "right": [Actor("enemy_idle_left1"), Actor("enemy_idle_left1")]
        }
        self.walk_images = {
            "left": [Actor("enemy_idle_left1"), Actor("enemy_idle_left1")],
            "right": [Actor("enemy_idle_left1"), Actor("enemy_idle_left1")]
        }
        self.moving = False

    def update(self):
        if not self.moving:
            self.path_index = (self.path_index + 1) % len(self.path)
            self.grid_x, self.grid_y = self.path[self.path_index]
            self.target_x = self.grid_x * 64
            self.target_y = self.grid_y * 64
            self.moving = True
            self.direction = "right" if self.target_x > self.x else "left"

        if self.moving:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            if abs(dx) > self.speed:
                self.x += self.speed if dx > 0 else -self.speed
            else:
                self.x = self.target_x
            if abs(dy) > self.speed:
                self.y += self.speed if dy > 0 else -self.speed
            else:
                self.y = self.target_y
            if self.x == self.target_x and self.y == self.target_y:
                self.moving = False

        self.anim_timer += 1
        if self.anim_timer >= 10:
            self.anim_index = (self.anim_index + 1) % 2
            self.anim_timer = 0

    def draw(self):
        if self.moving:
            img = self.walk_images[self.direction][self.anim_index]
        else:
            img = self.idle_images[self.direction][self.anim_index]
        img.pos = (self.x, self.y)
        img.draw()

    def collides_with(self, hero):
        return abs(self.x - hero.x) < 40 and abs(self.y - hero.y) < 40


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.wall_image = Actor("wall")
        self.floor_image = Actor("floor")
        self.generate_walls()

    def generate_walls(self):
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
                    self.grid[y][x] = 1
                elif random.random() < 0.1:
                    self.grid[y][x] = 1

    def is_blocked(self, grid_x, grid_y):
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            return self.grid[grid_y][grid_x] == 1
        return True

    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                img = self.wall_image if self.grid[y][x] == 1 else self.floor_image
                img.pos = (x * 64 + 32, y * 64 + 32)
                img.draw()

# ---------------- INSTÂNCIAS ---------------- #

game_map = GameMap(12, 9)
hero = Hero(5, 5)
enemies = [
    Enemy([(2, 2), (4, 2)]),
    Enemy([(6, 4), (6, 6)])
]

# ---------------- LOOP PRINCIPAL ---------------- #

def update():
    global game_state
    if game_state == "playing":
        hero.update()
        for enemy in enemies:
            enemy.update()
            if enemy.collides_with(hero):
                game_state = "game_over"
        if keyboard.left:
            hero.move(-1, 0, game_map)
        elif keyboard.right:
            hero.move(1, 0, game_map)
        elif keyboard.up:
            hero.move(0, -1, game_map)
        elif keyboard.down:
            hero.move(0, 1, game_map)

def draw():
    screen.clear()

    if game_state == "menu":
        screen.draw.text("Start Game", center=buttons["start"].center, color="white")
        screen.draw.text("Toggle Sound", center=buttons["toggle_sound"].center, color="white")
        screen.draw.text("Exit", center=buttons["exit"].center, color="white")
        for rect in buttons.values():
            screen.draw.rect(rect, "white")

    elif game_state == "playing":
        game_map.draw()
        hero.draw()
        for enemy in enemies:
            enemy.draw()

    elif game_state == "game_over":
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")

def on_mouse_down(pos):
    global game_state, sound_on

    if game_state == "menu":
        if buttons["start"].collidepoint(pos):
            game_state = "playing"
        elif buttons["toggle_sound"].collidepoint(pos):
            sound_on = not sound_on
        elif buttons["exit"].collidepoint(pos):
            exit()
