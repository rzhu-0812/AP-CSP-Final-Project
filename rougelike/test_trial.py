import pgzrun
import math
import time
import random
import pygame

# Constants
WIDTH = 1200
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

player = Actor("player_placeholder")
def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]
class Enemy:
    summon_cooldowns = {
        "orc": 1.0,
        "goblin": 0.3,
        "bat": 0.6,
        "assasin": 0.9,
        "vampire": 1.5
    }
    def __init__(self, enemy_type, sprite, distance_per_move, health, damage):
        self.enemy_type = enemy_type
        self.sprite = sprite
        self.distance_per_move = distance_per_move
        self.health = health
        self.damage = damage
        self.spawn_at_center()


    def spawn_at_center(self):
        self.sprite.x = CENTER_X + random.randint(-400, 400)
        self.sprite.y = CENTER_Y

def player_movement():
    if keyboard.W or keyboard.up:
        player.y = max(player.y - 2, 0 + 38)
    elif keyboard.S or keyboard.down:
        player.y = min(player.y + 2, HEIGHT - 38)
    if keyboard.A or keyboard.left:
        player.x = max(player.x - 2, 0 + 38)
    elif keyboard.D or keyboard.right:
        player.x = min(player.x + 2, WIDTH - 38)

def enemy_movement():
    global speed_factor
    for enemy in on_field_enemies:
        angle = math.atan2(player.y - enemy.sprite.y, player.x - enemy.sprite.x)
        enemy.sprite.move_ip(math.cos(angle) * enemy.distance_per_move * speed_factor,
                             math.sin(angle) * enemy.distance_per_move * speed_factor)
        
# Main game loop
def draw():
    counter = 0
    screen.clear()
    for tile in tiles:
        tile.draw()
    player.draw()
    for enemy in on_field_enemies:
        enemy.sprite.draw()
        
def update():
    events = pygame.event.get()
    player_movement()
    enemy_movement()


# Game start
enemy_constants = {
    "orc": {"distance_per_move": 2, "health": 5, "damage": 1},
    "goblin": {"distance_per_move": 6, "health": 3, "damage": 1},
    "bat": {"distance_per_move": 5,  "health": 3, "damage": 1},
    "assasin": {"distance_per_move": 3, "health": 4, "damage": 2},
    "vampire": {"distance_per_move": 1, "health": 10, "damage": 2}
}
enemy_actors = {
    "orc": Actor("orc_enemy_placeholder"),
    "goblin": Actor("goblin_enemy_placeholder"),
    "bat": Actor("bat_enemy_placeholder"),
    "assasin": Actor("assasin_enemy_placeholder"),
    "vampire": Actor("vampire_enemy_placeholder")
}

on_field_enemies = []
enemies = ["orc", "orc", "orc", "orc", "orc"]
for enemy in enemies:
    on_field_enemies.append(Enemy(namestr(enemy, globals()), enemy_actors.get(namestr(enemy, globals()), **enemy_constants[enemy] ) ) )

clock.schedule_interval(update, 1.0 / 15.0)
pgzrun.go()
