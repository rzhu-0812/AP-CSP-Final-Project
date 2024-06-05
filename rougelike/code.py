import pgzrun
import math
import time
import random

WIDTH = 1200
HEIGHT = 800
CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2

last_spell_cast_time = 0
cooldown = 0.1

tiles = [Actor("tile", pos=((j * 100) + 50, (i * 100) + 50)) for i in range(int(HEIGHT / 100)) for j in range(int(WIDTH / 100))]
big_tiles = [Actor("big_tile", pos=((i * 300) + 150, (j * 300) + 150)) for i in range(3) for j in range(2)]

enemy_constants = {
    "Placeholder": {"distance_per_move": 4, "resting_time": 1, "vision": 200}
}

class Enemy:
    def __init__(self, type, sprite, distance_per_move, resting_time, vision):
        self.type = type
        self.sprite = sprite
        self.distance_per_move = distance_per_move
        self.resting_time = resting_time
        self.vision = vision
        self.spawn_random_position()

    def spawn_random_position(self):
        while True:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            if math.sqrt((x - player.x) ** 2 + (y - player.y) ** 2) > 100: 
                self.sprite.pos = (x, y)
                break

player = Actor("player_placeholder")

class Spell:
    def __init__(self, sprite, speed, spell_range):
        self.sprite = sprite
        self.speed = speed
        self.spell_range = spell_range

enemies = [Enemy("Placeholder", Actor("enemy_placeholder"), **enemy_constants["Placeholder"]) for _ in range(5)]

spells = []

equipped_spell = "spell_placeholder"

def create_and_target_spell(mouse_pos, x, y):
    spell = Spell(Actor("spell_placeholder"), 10, 500)
    spell.sprite.pos = (x, y)
    spell.targetx, spell.targety = mouse_pos
    spell.angle = math.atan2(spell.targety - spell.sprite.y, spell.targetx - spell.sprite.x)
    spell.direction_x = math.cos(spell.angle) * spell.speed
    spell.direction_y = math.sin(spell.angle) * spell.speed
    spells.append(spell)

def enemy_movement():
    for enemy in enemies:
        angle = math.atan2(player.y - enemy.sprite.y, player.x - enemy.sprite.x)
        speed_factor = 0.3
        enemy.sprite.x += math.cos(angle) * enemy.distance_per_move * speed_factor
        enemy.sprite.y += math.sin(angle) * enemy.distance_per_move * speed_factor

def player_movement():
    global player
    
    if keyboard.W or keyboard.up:
        player.y = max(player.y - 5, 0 + 38)
    elif keyboard.S or keyboard.down:
        player.y = min(player.y + 5, HEIGHT - 38)
    elif keyboard.A or keyboard.left:
        player.x = max(player.x - 5, 0 + 38)
    elif keyboard.D or keyboard.right:
        player.x = min(player.x + 5, WIDTH - 38)

def spell_behavior():
    for spell in spells:
        if spell.spell_range <= 0:
            spells.remove(spell)
        else:
            spell.sprite.x += spell.direction_x
            spell.sprite.y += spell.direction_y
            spell.spell_range -= spell.speed

def draw():
    screen.clear()
    for tile in tiles:
        tile.draw()
    player.draw()
    for enemy in enemies:
        enemy.sprite.draw()
    for spell in spells:
        spell.sprite.draw()

def on_mouse_down(pos):
    global last_spell_cast_time

    current_time = time.time()
    if current_time - last_spell_cast_time >= cooldown:
        create_and_target_spell(pos, player.x, player.y)
        last_spell_cast_time = current_time

def update():
    player_movement()
    enemy_movement()
    spell_behavior()

pgzrun.go()
