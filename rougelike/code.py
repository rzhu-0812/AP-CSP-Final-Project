import pgzrun
import math
import time
import random

WIDTH = 1200
HEIGHT = 600
CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2

last_spell_cast_time = 0
cooldown = 0.1


tiles = [Actor("tile", pos=((j * 100) + 50, (i * 100) + 50)) for i in range(int(HEIGHT / 100)) for j in range(int(WIDTH / 100))]
big_tiles = [Actor("big_tile", pos=((i * 300) + 150, (j * 300) + 150)) for i in range(3) for j in range(2)]

enemy_constants = {
    "Placeholder": {"distance_per_move": 4, "resting_time": 1, "vision": 200, "health": 3, "damage": 1}
}

class Enemy:
    def __init__(self, enemy_type, sprite, distance_per_move, resting_time, vision, health, damage):
        self.enemy_type = enemy_type
        self.sprite = sprite
        self.distance_per_move = distance_per_move
        self.resting_time = resting_time
        self.vision = vision
        self.health = health
        self.damage = damage
        self.spawn_at_alter()

    def spawn_at_alter(self):
        self.sprite.pos = (CENTER_X, CENTER_Y)


player = Actor("player_placeholder")

#equippable_spells = []
equipped_spell = "spell_placeholder"

"""
spell_types = {
    spell_placeholder, "spell_placeholder"
    }
"""

class Spell:
    global equipped_spell
    def __init__(self, sprite, speed, spell_range, delete, spell_type, spell_damage):
        self.sprite = Actor(equipped_spell)
        self.speed = speed
        self.spell_range = spell_range
        self.delete = delete
        self.spell_type = equipped_spell
        self.spell_damage = spell_damage

        

on_field_enemies = [Enemy("Placeholder", Actor("enemy_placeholder"), **enemy_constants["Placeholder"]) for _ in range(1)]

#enemy = Enemy("Placeholder", Actor("enemy_placeholder", **enemy_constants["Placeholder"]))
#on_field_enemies.append(enemy)

placeholder_enemy = 1
orc = 1
goblin = 3
bat = 2
assasin = 5
vampire = 10

level_strength = 87
wave_number = 1

unchanging_types_of_enemies = [placeholder_enemy, orc, goblin, bat, assasin]
changing_types_of_enemies = [placeholder_enemy, orc, goblin, bat, assasin]
selected_enemies_for_next_level = []

def select_enemies_for_next_level():
    global level_strength
    while level_strength > 0:
        for enemy in changing_types_of_enemies:
            if enemy > level_strength:
                changing_types_of_enemies.remove(enemy)
        print(changing_types_of_enemies)
        for enemy in changing_types_of_enemies:
            x = random.randint(0, len(changing_types_of_enemies) - 1)
            print(x)
            selected_enemies_for_next_level.append(changing_types_of_enemies[x])
            level_strength -= changing_types_of_enemies[x]

    print(level_strength)
    print(selected_enemies_for_next_level)
        

def reset_for_next_wave():
    changing_types_of_enemies.clear()
    changing_types_of_enemies = unchanging_types_of_enemies
    wave_number += 1
    level_strength = wave_number

spells = []

equipped_spell = "spell_placeholder"

def create_and_target_spell(mouse_pos, x, y):
    spell = Spell(Actor("spell_placeholder"), 10, 500, False, equipped_spell, 2)
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
        enemy.sprite.x += math.cos(angle) * enemy.distance_per_move * speed_factor
        enemy.sprite.y += math.sin(angle) * enemy.distance_per_move * speed_factor
        
def enemy_behavior():
    for enemy in on_field_enemies:
        if enemy.health <= 0:
            on_field_enemies.delete(enemy)

def player_movement():
    global player
    
    if keyboard.W or keyboard.up:
        player.y = max(player.y - 5, 0 + 38)
    elif keyboard.S or keyboard.down:
        player.y = min(player.y + 5, HEIGHT - 38)
    if keyboard.A or keyboard.left:
        player.x = max(player.x - 5, 0 + 38)
    elif keyboard.D or keyboard.right:
        player.x = min(player.x + 5, WIDTH - 38)

    if keyboard.space:
        select_enemies_for_next_level()

def spell_behavior():
    for spell in spells:
        if spell.spell_range <= 0:
            spells.remove(spell)
        else:
            spell.sprite.x += spell.direction_x
            spell.sprite.y += spell.direction_y
            spell.spell_range -= spell.speed

        if spell.spell_type == "spell_placeholder":
            for enemy in on_field_enemies:
                if spell.sprite.colliderect(enemy.sprite):
                    spells.remove(spell)
                    enemy.health -= spell.spell_damage

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
    if current_time - last_spell_cast_time >= cooldown:
        create_and_target_spell(pos, player.x, player.y)
        last_spell_cast_time = current_time

def update():
    player_movement()
    enemy_movement()
    spell_behavior()

pgzrun.go()
