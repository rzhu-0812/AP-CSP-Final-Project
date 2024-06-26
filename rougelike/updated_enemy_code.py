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

game_state = "Shop"


# Actors
player = Actor("player_placeholder")
tiles = [Actor("tile", pos=((j * 100) + 50, (i * 100) + 50)) for i in range(int(HEIGHT / 100)) for j in range(int(WIDTH / 100))]
big_tiles = [Actor("big_tile", pos=((i * 300) + 150, (j * 300) + 150)) for i in range(3) for j in range(2)]

# Classes

"""
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



class Vampire(Enemy):
    def __init__(self, enemy_type, sprite, distance_per_move, health, damage):
        self.enemy_type = enemy_type
        self.sprite = sprite
        self.distance_per_move = distance_per_move
        self.health - health
        self.damage = damage
        self.teleport()
    def teleport():
        #for spell in spells():
            #if vampire.sprite.colliderect(spell):
        vampire.x = random.randint(200, 1000)
        vampire.y = random.randint(200, 400)
"""
def create_enemy(enemy_type):
    if enemy_type == "orc":
        enemy = Actor("orc_enemy")
        enemy.type = "orc"
        enemy.distance_per_move = 2
        enemy.health = 7
        enemy.damage = 1
        enemy.pos = (CENTER_X + random.randint(-400, 400), CENTER_Y)
        return(enemy)
    if enemy_type == "goblin":
        enemy = Actor("goblin_enemy")
        enemy.type = "goblin"
        enemy.distance_per_move = 6
        enemy.health = 3
        enemy.damage = 1
        enemy.pos = (CENTER_X + random.randint(-400, 400), CENTER_Y)
        return(enemy)
    if enemy_type == "bat":
        enemy = Actor("bat_enemy")
        enemy.type = "bat"
        enemy.distance_per_move = 4
        enemy.health = 3
        enemy.damage = 1
        enemy.pos = (CENTER_X + random.randint(-400, 400), CENTER_Y)
        return(enemy)
    if enemy_type == "assasin":
        enemy = Actor("assasin_enemy")
        enemy.type = "assasin"
        enemy.distance_per_move = 3
        enemy.health = 4
        enemy.damage = 5
        enemy.pos = (CENTER_X + random.randint(-400, 400), CENTER_Y)
        return(enemy)
    if enemy_type == "vampire":
        enemy = Actor("vampire_enemy")
        enemy.type = "vampire"
        enemy.distance_per_move = 1
        enemy.health = 10
        enemy.damage = 2
        enemy.pos = (CENTER_X + random.randint(-400, 400), CENTER_Y)
        return(enemy)
    if enemy_type == "necromancer":
        enemy = Actor("necromancer_enemy_placeholder")
        enemy.type = "necromancer"
        enemy.distance_per_move = 1
        enemy.health = 15
        enemy.damage = 0
        enemy.ability_delay = 500
        enemy.pos = (CENTER_X + random.randint(-400, 400), CENTER_Y)
        return(enemy)
    
def vampire_bat_summon(vampire_x, vampire_y):
    summon_amount = random.randint(0, 3)
    for i in range(summon_amount):
        enemy = Actor("bat_enemy")
        enemy.type = "bat"
        enemy.distance_per_move = 5
        enemy.health = 3
        enemy.damage = 1
        enemy.pos = (vampire_x + random.randint(-50, 50), vampire_y + random.randint(-50, 50))
        on_field_enemies.append(enemy)


def vampire_special():
    """
    for enemy in on_field_enemies:
        for spell in spells:
            if spell.sprite.colliderect(enemy):
                if enemy.type == "vampire":
                """
    vampire_bat_summon(enemy.x, enemy.y)
    enemy.pos = (CENTER_X + random.randint(-500, 500), CENTER_Y + random.randint(-200, 200))

def necromancer_skeleton_summon(necromancer_x, necromancer_y):
    summon_amount = random.randint(2, 6)
    for i in range(summon_amount):
        enemy = Actor("skeleton_enemy_placeholder")
        enemy.type = "skeleton"
        enemy.distance_per_move = 3
        enemy.health = 1
        enemy.damage = 1
        enemy.pos = (necromancer_x + random.randint(-50, 50), necromancer_y + random.randint(-50, 50))
        on_field_enemies.append(enemy)
                        
        

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
def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

#on_field_enemies = [Enemy("Placeholder", Actor("enemy_placeholder"), **enemy_constants["Placeholder"]) for _ in range(1)]

#enemy = Enemy("Placeholder", Actor("enemy_placeholder", **enemy_constants["Placeholder"]))
#on_field_enemies.append(enemy)

orc = 2
goblin = 3
bat = 1
assasin = 5
vampire = 15
necromancer = 30
speed_factor = 0.3

unchanging_types_of_enemies = [orc, goblin, bat, assasin, vampire]
changing_types_of_enemies = [orc, goblin, bat, assasin, vampire]
#print(changing_types_of_enemies)

level_strength = -1
wave_number = -1
"""
for i in changing_types_of_enemies:
    if i <= level_strength:
        print(i)
"""
selected_enemies_for_next_level = []
#select_enemies_for_next_level_counter = 0

def select_enemies_for_next_level():
    #counter = 0
    global level_strength
    global changing_types_of_enemies
    #print(level_strength)
    done = False
    while not done:
        for enemy in changing_types_of_enemies:
            #print (enemy)
            if enemy > abs(level_strength):
                changing_types_of_enemies.remove(enemy)
                #if enemy in changing_types_of_enemies:
                    
                   # print(namestr(enemy, globals()))

        if len(changing_types_of_enemies) > 0:

            if max(changing_types_of_enemies) <= abs(level_strength):
                done = True

        else:
            done = True

            

    #print(changing_types_of_enemies)

    while abs(level_strength) > 0:
        #for enemy in changing_types_of_enemies:
        #print(level_strength)
        if level_strength > 0:
            level_strength = 0
        if level_strength == 0:
            break
        x = random.randint(0, len(changing_types_of_enemies) - 1)
        #print(x)
        #print(max(changing_types_of_enemies))
        if changing_types_of_enemies[x] <= abs(level_strength):
            #print(changing_types_of_enemies[x])
            #print(namestr(changing_types_of_enemies[x], globals()))
            selected_enemies_for_next_level.append(changing_types_of_enemies[x])
            #print(selected_enemies_for_next_level)
            #print("hello")
            level_strength += changing_types_of_enemies[x]
            

    #print(level_strength)
    for selected_enemy_for_next_level in selected_enemies_for_next_level:
        print(namestr(selected_enemy_for_next_level, globals()))
        #pass
    #print(selected_enemies_for_next_level)
    
def reset_for_next_wave():
    global changing_types_of_enemies
    global unchanging_types_of_enemies
    global wave_number
    global level_strength
    changing_types_of_enemies.clear()
    changing_types_of_enemies = [orc, goblin, bat, assasin, vampire, necromancer]
    selected_enemies_for_next_level.clear()
    #print(unchanging_types_of_enemies)
    #print(changing_types_of_enemies)
    wave_number -= 1
    level_strength = wave_number
    #print(level_strength)
    #print(random.randint(0, len(changing_types_of_enemies) - 1))


summon_cooldown = 500
def summon_next_wave():
    global game_state
    global summon_cooldown
    game_state = "Fight"
    while len(selected_enemies_for_next_level) > 0:
        for enemy in selected_enemies_for_next_level:
            #pass
            if summon_cooldown <= 0:
                #print(namestr(enemy, globals()))
                summon_cooldown = 50000
                if enemy == orc:
                    on_field_enemies.append(create_enemy("orc"))
                    selected_enemies_for_next_level.remove(enemy)
                elif enemy == goblin:
                    on_field_enemies.append(create_enemy("goblin"))
                    selected_enemies_for_next_level.remove(enemy)
                elif enemy == bat:
                    on_field_enemies.append(create_enemy("bat"))
                    selected_enemies_for_next_level.remove(enemy)
                elif enemy == assasin:
                    on_field_enemies.append(create_enemy("assasin"))
                    selected_enemies_for_next_level.remove(enemy)
                elif enemy == vampire:
                    on_field_enemies.append(create_enemy("vampire"))
                    selected_enemies_for_next_level.remove(enemy)
                elif enemy == necromancer:
                    on_field_enemies.append(create_enemy("necromancer"))
                    selected_enemies_for_next_level.remove(enemy)                    
                    
            else:
                summon_cooldown -= 1
    #print(on_field_enemies)
"""
    for enemy in on_field_enemies:
        #print(namestr(enemy, globals()))
        if enemy.type == "orc":
            enemy.x = random.randint(-400, 400) + CENTER_X
            #counter += 1
            #print("hello")
            #print(enemy.sprite.x)

    #print(counter)
            #print(summon_cooldown)

"""
#for enemy in selected_enemies_for_next_level:

    #print(type(namestr(enemy, globals())))
def create_and_target_spell(mouse_pos, x, y, spell_type):
    spell = Spell(Actor(spell_type), 10, 500, False, spell_type, 1)
    spell.sprite.pos = (x, y)
    spell.targetx, spell.targety = mouse_pos
    spell.angle = math.atan2(spell.targety - spell.sprite.y, spell.targetx - spell.sprite.x)
    spell.direction_x = math.cos(spell.angle) * spell.speed
    spell.direction_y = math.sin(spell.angle) * spell.speed
    spells.append(spell)

def enemy_movement():
    global speed_factor
    for enemy in on_field_enemies:
        angle = math.atan2(player.y - enemy.y, player.x - enemy.x)
        enemy.move_ip(math.cos(angle) * enemy.distance_per_move * speed_factor,
                             math.sin(angle) * enemy.distance_per_move * speed_factor)

def enemy_behavior():
    global on_field_enemies
    on_field_enemies = [enemy for enemy in on_field_enemies if enemy.health > 0]
    #if enemy == Vampire:
        #enemy.teleport()

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
                if spell.sprite.colliderect(enemy):
                    if enemy.type == "vampire":
                        vampire_bat_summon(enemy.x, enemy.y)
                        enemy.pos = (CENTER_X + random.randint(-500, 500), CENTER_Y + random.randint(-200, 200))
                    enemy.health -= spell.spell_damage
                    if enemy.health <= 0:
                        on_field_enemies.remove(enemy)
                        enemy = object()
                    if spell in spells:
                        spells.remove(spell)

# Main game loop
def draw():
    global game_state
    counter = 0
    screen.clear()

    if game_state == "Fight":
        for tile in tiles:
            tile.draw()
        player.draw()
        for enemy in on_field_enemies:
            enemy.draw()
            #print(counter)
        for spell in spells:
            spell.sprite.draw()

def on_mouse_down(pos):
    global last_spell_cast_time

    current_time = time.time()
    equipped_spell_cooldown = Spell.spell_cooldowns.get(equipped_spell)
    if current_time - last_spell_cast_time >= equipped_spell_cooldown:
        create_and_target_spell(pos, player.x, player.y, equipped_spell)
        last_spell_cast_time = current_time

def on_key_up(key):
    global game_state
    if game_state == "Shop":
        if key == keys.SPACE:
            select_enemies_for_next_level()
            summon_next_wave()
            reset_for_next_wave()
        #print(len(on_field_enemies))

def update():
    global game_state
    events = pygame.event.get()
    player_movement()
    enemy_movement()
    #vampire_special()
    spell_behavior()
    if game_state == "Fight":
        if len(on_field_enemies) <= 0:
            game_state = "Shop"

        for enemy in on_field_enemies:
            if enemy.type == "necromancer":
                if enemy.ability_delay <= 0:
                    necromancer_skeleton_summon(enemy.x, enemy.y)
                    enemy.ability_delay = 500
                else:
                    enemy.ability_delay -= 1


# Game start
enemy_constants = {
    "orc": {"distance_per_move": 2, "health": 7, "damage": 1},
    "goblin": {"distance_per_move": 6, "health": 3, "damage": 1},
    "bat": {"distance_per_move": 4,  "health": 3, "damage": 1},
    "assasin": {"distance_per_move": 3, "health": 4, "damage": 5},
    "vampire": {"distance_per_move": 1, "health": 10, "damage": 2},
    "necromancer": {"distance_per_move": 1, "health": 15, "damage": 1}
}
enemy_actors = {
    "orc": Actor("orc_enemy_placeholder"),
    "goblin": Actor("goblin_enemy_placeholder"),
    "bat": Actor("bat_enemy_placeholder"),
    "assasin": Actor("assasin_enemy_placeholder"),
    "vampire": Actor("vampire_enemy_placeholder")
}

enemies = ["orc", "orc", "orc", "orc", "orc"]#"bat", "goblin", "assasin", "vampire"]
#print(enemies[1])
#print(enemies)

"""
for enemy in enemies:
    #if enemy == "vampire":
    #on_field_enemies.append(Vampire(enemy, enemy_actors.get(enemy), **enemy_constants[enemy] ) )
    #else:
    on_field_enemies.append(Enemy(enemy, enemy_actors.get(enemy), **enemy_constants[enemy] ) )
    print(namestr(on_field_enemies, globals() ) )
    enemy = object()
    
for enemy in selected_enemies_for_next_level:
    on_field_enemies.append(Enemy(namestr(enemy, globals()), enemy_actors.get(namestr(enemy, globals()), **enemy_constants[enemy] ) ) )

"""
spells = []
equipped_spell = "spell_placeholder"

clock.schedule_interval(update, 1.0 / 15.0)
pgzrun.go()
