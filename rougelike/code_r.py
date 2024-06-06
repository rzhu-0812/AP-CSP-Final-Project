import pgzrun
import math
import time

# Constants
WIDTH = 1200
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

# Actors
player = Actor("player_placeholder")
tiles = [Actor("tile", pos=((j * 100) + 50, (i * 100) + 50)) for i in range(int(HEIGHT / 100)) for j in range(int(WIDTH / 100))]
big_tiles = [Actor("big_tile", pos=((i * 300) + 150, (j * 300) + 150)) for i in range(3) for j in range(2)]

# Classes
class Enemy:
    def __init__(self, enemy_type, sprite, distance_per_move, resting_time, health, damage):
        self.enemy_type = enemy_type
        self.sprite = sprite
        self.distance_per_move = distance_per_move
        self.resting_time = resting_time
        self.health = health
        self.damage = damage
        self.spawn_at_center()

    def spawn_at_center(self):
        self.sprite.pos = (CENTER_X, CENTER_Y)

class Spell:
    spell_cooldowns = {
        "spell_placeholder": 0.1
    }

    def __init__(self, sprite, speed, spell_range, delete, spell_type, spell_damage):
        self.sprite = sprite
        self.speed = speed
        self.spell_range = spell_range
        self.delete = delete
        self.spell_type = spell_type
        self.spell_damage = spell_damage
        self.cooldown = Spell.spell_cooldowns.get(spell_type)

# Game state
last_spell_cast_time = 0
on_field_enemies = []

# Functions
def create_and_target_spell(mouse_pos, x, y, spell_type):
    spell = Spell(Actor(spell_type), 10, 500, False, spell_type, 1)
    spell.sprite.pos = (x, y)
    spell.targetx, spell.targety = mouse_pos
    spell.angle = math.atan2(spell.targety - spell.sprite.y, spell.targetx - spell.sprite.x)
    spell.direction_x = math.cos(spell.angle) * spell.speed
    spell.direction_y = math.sin(spell.angle) * spell.speed
    spells.append(spell)

def enemy_movement():
    for enemy in on_field_enemies:
        angle = math.atan2(player.y - enemy.sprite.y, player.x - enemy.sprite.x)
        speed_factor = 0.3
        enemy.sprite.move_ip(math.cos(angle) * enemy.distance_per_move * speed_factor,
                             math.sin(angle) * enemy.distance_per_move * speed_factor)

def enemy_behavior():
    global on_field_enemies
    on_field_enemies = [enemy for enemy in on_field_enemies if enemy.health > 0]

def player_movement():
    if keyboard.W or keyboard.up:
        player.y = max(player.y - 2, 0 + 38)
    elif keyboard.S or keyboard.down:
        player.y = min(player.y + 2, HEIGHT - 38)
    if keyboard.A or keyboard.left:
        player.x = max(player.x - 2, 0 + 38)
    elif keyboard.D or keyboard.right:
        player.x = min(player.x + 2, WIDTH - 38)

def spell_behavior():
    global spells
    spells = [spell for spell in spells if spell.spell_range > 0]
    for spell in spells:
        spell.sprite.x += spell.direction_x
        spell.sprite.y += spell.direction_y
        spell.spell_range -= spell.speed

        if spell.spell_type == "spell_placeholder":
            for enemy in on_field_enemies:
                if spell.sprite.colliderect(enemy.sprite):
                    enemy.health -= spell.spell_damage
                    if enemy.health <= 0:
                        on_field_enemies.remove(enemy)
                    if spell in spells:
                        spells.remove(spell)

# Main game loop
def draw():
    screen.clear()
    for tile in tiles:
        tile.draw()
    player.draw()
    for enemy in on_field_enemies:
        enemy.sprite.draw()
    for spell in spells:
        spell.sprite.draw()

def on_mouse_down(pos):
    global last_spell_cast_time

    current_time = time.time()
    equipped_spell_cooldown = Spell.spell_cooldowns.get(equipped_spell)
    if current_time - last_spell_cast_time >= equipped_spell_cooldown:
        create_and_target_spell(pos, player.x, player.y, equipped_spell)
        last_spell_cast_time = current_time

def update():
    player_movement()
    enemy_movement()
    spell_behavior()

# Game start
enemy_constants = {
    "Normal": {"distance_per_move": 2, "resting_time": 0, "health": 5, "damage": 1},
    "Fast": {"distance_per_move": 5, "resting_time": 20, "health": 3, "damage": 1}
}
enemy_actors = {
    "Normal": Actor("enemy_placeholder"),
    "Fast": Actor("enemy_placeholder")
}

enemies = ["Normal", "Normal", "Fast"]
for enemy in enemies:
    on_field_enemies.append(Enemy(enemy, enemy_actors.get(enemy), **enemy_constants[enemy]))


spells = []
equipped_spell = "spell_placeholder"

clock.schedule_interval(update, 1.0 / 60.0)
pgzrun.go()
