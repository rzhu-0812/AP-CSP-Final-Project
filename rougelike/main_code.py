import pgzrun
import math
import random
import time

from pgzhelper import Actor
from pgzhelper import *

# Constants
WIDTH = 1200
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
TILE_SIZE = 100

SPELL_ICON_SIZE = 50
SELECTED_SPELL_SCALE = 2.0

game_state = "Shop"
spell_changed = True

# Actors
tiles = [Actor("tile", pos=((j * TILE_SIZE) + 50, (i * TILE_SIZE) + 50)) for i in range(int(HEIGHT / TILE_SIZE)) for j in range(int(WIDTH / 100))]
enemies_in_next_round = Actor("enemies_in_next_round")
enemies_in_next_round.pos = (200, 300)

spell_shop = Actor("spells")
spell_shop.pos = (800, 500)
owned_spells = ['direct_shot']

coin = Actor("coin")
coin.pos = (WIDTH - 99, 65)
coin.scale = 1.75

full_heart = "full_heart"
half_heart = "half_heart"
empty_heart = "empty_heart"

direct_shot_sprite = Actor("direct_shot")
direct_shot_sprite.pos = (615, 500)
direct_owned = True

penetrating_shot_sprite = Actor("penetrating_shot")
penetrating_shot_sprite.pos = (710, 500)
penetrating_owned = False

bounce_shot_sprite = Actor("bounce_shot")
bounce_shot_sprite.pos = (805, 500)
bounce_owned = False

chain_shot_sprite = Actor("chain_shot")
chain_shot_sprite.pos = (900, 500)
chain_owned = False

freeze_shot_sprite = Actor("freeze_shot")
freeze_shot_sprite.pos = (995, 500)
freeze_owned = False

spells = []
spell_types = ["direct_shot", "penetrating_shot", "bounce_shot", "chain_shot", "freeze_shot"]
equipped_spell = "direct_shot"
selected_spell_index = spell_types.index(equipped_spell)

# Constants // Heres where you add monsters and spells
spell_constants = {
    "direct_shot": {
        "speed": 10,
        "range": 400,
        "cooldown": 0.75,
        "damage": 1
    },
    "penetrating_shot": {
        "speed": 5,
        "range": 250,
        "cooldown": 1,
        "damage": 1
    },
    "bounce_shot": {
        "speed": 3,
        "range": 10000,
        "cooldown": 1,
        "damage": 0.5
    },
    "chain_shot": {
        "speed": 3,
        "range": 5000,
        "cooldown": 1.5,
        "damage": 1
    },
    "freeze_shot": {
        "speed": 3,
        "range": 500,
        "cooldown": 0.5,
        "damage": 0.5
    }
}

enemy_constants = {
    "orc": {
        "actor": Actor("orc_enemy_placeholder"),  
        "distance_per_move": 2, 
        "health": 5, 
        "damage": 1, 
        "attack_cooldown": 5
    },
    "goblin": {
        "actor": Actor("goblin_enemy_placeholder"),
        "distance_per_move": 6, 
        "health": 3, 
        "damage": 1, 
        "attack_cooldown": 5
    },
    "bat": {
        "actor": Actor("bat_enemy_placeholder"),
        "distance_per_move": 5,  
        "health": 3, 
        "damage": 1, 
        "attack_cooldown": 5
    },
    "assasin": {
        "actor": Actor("assasin_enemy_placeholder"),
        "distance_per_move": 3, 
        "health": 4, 
        "damage": 2, 
        "attack_cooldown": 10
    },
    "vampire": {
        "actor": Actor("vampire_enemy_placeholder"),
        "distance_per_move": 1, 
        "health": 10, 
        "damage": 2, 
        "attack_cooldown": 10
    }
}

# Player Class
class Player:
    def __init__(self):
        self.sprite = Actor("player")
        self.sprite.pos = (38, 38)
        self.health = 6
        self.coins = 0
    
    def player_movement(self):
        if keyboard.W or keyboard.up: # type: ignore
            self.sprite.y = max(self.sprite.y - 2, 0 + 38)
        elif keyboard.S or keyboard.down: # type: ignore
            self.sprite.y = min(self.sprite.y + 2, HEIGHT - 38)
        if keyboard.A or keyboard.left: # type: ignore
            self.sprite.x = max(self.sprite.x - 2, 0 + 38)
        elif keyboard.D or keyboard.right: # type: ignore
            self.sprite.x = min(self.sprite.x + 2, WIDTH - 38)
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print("You Died")
            quit()

def create_enemy(enemy_type):
    if enemy_type == "orc":
        enemy = Actor("orc_enemy")
        enemy.type = "orc"
        enemy.distance_per_move = 2
        enemy.health = 7
        enemy.damage = 1
        enemy.attack_cooldown = 2
        enemy.is_frozen = False
        enemy.last_freeze_time = 0
        enemy.freeze_duration = 3
        enemy.pos = (monster_gate.x + random.randint(-50, 50), monster_gate.y + random.randint(-50, 50) )
        return(enemy)
    if enemy_type == "goblin":
        enemy = Actor("goblin_enemy")
        enemy.type = "goblin"
        enemy.distance_per_move = 6
        enemy.health = 3
        enemy.damage = 1
        enemy.attack_cooldown = 2
        enemy.is_frozen = False
        enemy.last_freeze_time = 0
        enemy.freeze_duration = 3
        enemy.pos = (monster_gate.x + random.randint(-50, 50), monster_gate.y + random.randint(-50, 50) )
        return(enemy)
    if enemy_type == "bat":
        enemy = Actor("bat_enemy")
        enemy.type = "bat"
        enemy.distance_per_move = 4
        enemy.health = 3
        enemy.damage = 1
        enemy.attack_cooldown = 2
        enemy.is_frozen = False
        enemy.last_freeze_time = 0
        enemy.freeze_duration = 3
        enemy.pos = (monster_gate.x + random.randint(-50, 50), monster_gate.y + random.randint(-50, 50) )
        return(enemy)
    if enemy_type == "assasin":
        enemy = Actor("assasin_enemy")
        enemy.type = "assasin"
        enemy.distance_per_move = 3
        enemy.health = 4
        enemy.damage = 5
        enemy.attack_cooldown = 2
        enemy.is_frozen = False
        enemy.last_freeze_time = 0
        enemy.freeze_duration = 3
        enemy.pos = (monster_gate.x + random.randint(-50, 50), monster_gate.y + random.randint(-50, 50 ) )
        return(enemy)
    if enemy_type == "vampire":
        enemy = Actor("vampire_enemy")
        enemy.type = "vampire"
        enemy.distance_per_move = 1
        enemy.health = 10
        enemy.damage = 2
        enemy.attack_cooldown = 2
        enemy.is_frozen = False
        enemy.last_freeze_time = 0
        enemy.freeze_duration = 3
        enemy.pos = (monster_gate.x + random.randint(-50, 50), monster_gate.y + random.randint(-50, 50) )
        return(enemy)
    if enemy_type == "necromancer":
        enemy = Actor("necromancer_enemy_placeholder")
        enemy.type = "necromancer"
        enemy.distance_per_move = 1
        enemy.health = 15
        enemy.damage = 0
        enemy.attack_cooldown = 0
        enemy.ability_delay = 500
        enemy.is_frozen = False
        enemy.last_freeze_time = 0
        enemy.freeze_duration = 3
        enemy.pos = (monster_gate.x + random.randint(-50, 50), monster_gate.y + random.randint(-50, 50) )
        return(enemy)

def assassinate(enemy, health):
    if enemy.type == "assasin":
        if health <= 3:
             enemy.distance_per_move = 6
        else:
            enemy.distance_per_move = 3
        
    
def vampire_bat_summon(vampire_x, vampire_y):
    summon_amount = random.randint(0, 3)
    for _ in range(summon_amount):
        enemy = Actor("bat_enemy")
        enemy.type = "bat"
        enemy.distance_per_move = 5
        enemy.health = 3
        enemy.damage = 1
        enemy.attack_cooldown = 2
        enemy.is_frozen = False
        enemy.last_freeze_time = 0
        enemy.freeze_duration = 3
        enemy.pos = (vampire_x + random.randint(-50, 50), vampire_y + random.randint(-50, 50))
        on_field_enemies.append(enemy)

def necromancer_skeleton_summon(necromancer_x, necromancer_y):
    summon_amount = random.randint(2, 6)
    for _ in range(summon_amount):
        enemy = Actor("skeleton_enemy_placeholder")
        enemy.type = "skeleton"
        enemy.distance_per_move = 3
        enemy.health = 1
        enemy.damage = 1
        enemy.attack_cooldown = 2
        enemy.is_frozen = False
        enemy.last_freeze_time = 0
        enemy.freeze_duration = 3
        enemy.pos = (necromancer_x + random.randint(-50, 50), necromancer_y + random.randint(-50, 50))
        on_field_enemies.append(enemy)


# Spell Classes
class Spell:
    def __init__(self, sprite, spell_type):
        constants = spell_constants[spell_type]
        self.spell_type = spell_type
        self.sprite = sprite
        self.speed = constants["speed"]
        self.range = constants["range"]
        self.cooldown = constants["cooldown"]
        self.damage = constants["damage"]
        self.enemies_hit = set()
    
    def move(self):
        self.sprite.x += self.direction_x
        self.sprite.y += self.direction_y
        self.range -= self.speed

        if self.range <= 0:
            spells.remove(self)
            return
    
    def initialize_spell(self, player_pos, target_pos):
        self.sprite.pos = player_pos
        self.targetx, self.targety = target_pos
        self.angle = math.atan2(self.targety - self.sprite.y, self.targetx - self.sprite.x)
        self.direction_x = math.cos(self.angle) * self.speed
        self.direction_y = math.sin(self.angle) * self.speed

class DirectShot(Spell):
    def __init__(self, sprite):
        super().__init__(sprite, "direct_shot")
    
    def move(self):
        super().move()
        for enemy in on_field_enemies:
            if self.sprite.colliderect(enemy):
                if enemy.type == "vampire":
                        vampire_bat_summon(enemy.x, enemy.y)
                        enemy.pos = (CENTER_X + random.randint(-500, 500), CENTER_Y + random.randint(-200, 200))
                enemy.health -= self.damage
                if enemy.health <= 0:
                    on_field_enemies.remove(enemy)
                if self in spells:
                    spells.remove(self)

class PenetratingShot(Spell):
    def __init__(self, sprite):
        super().__init__(sprite, "penetrating_shot")
    
    def move(self):
        super().move()
        for enemy in on_field_enemies:
            if self.sprite.colliderect(enemy) and enemy not in self.enemies_hit:
                if enemy.type == "vampire":
                        vampire_bat_summon(enemy.x, enemy.y)
                        enemy.pos = (CENTER_X + random.randint(-500, 500), CENTER_Y + random.randint(-200, 200))
                enemy.health -= self.damage
                self.enemies_hit.add(enemy)
                if enemy.health <= 0:
                    on_field_enemies.remove(enemy)

class BounceShot(Spell):
    def __init__(self, sprite):
        super().__init__(sprite, "bounce_shot")
        self.direction_x = 1
        self.direction_y = 0
        self.bounce_limit = 8
        self.bounces = 0
        self.previous_enemy = None
    
    def move(self):
        self.sprite.x += self.direction_x * self.speed
        self.sprite.y += self.direction_y * self.speed
        self.range -= self.speed

        if self.range <= 0 or self.bounces >= self.bounce_limit:
            spells.remove(self)
            return

        hit_enemy = None
        for enemy in on_field_enemies:
            if self.sprite.colliderect(enemy) and (self.previous_enemy is None or enemy != self.previous_enemy):
                hit_enemy = enemy
                break
        
        if hit_enemy:
            if enemy.type == "vampire":
                        vampire_bat_summon(enemy.x, enemy.y)
                        enemy.pos = (CENTER_X + random.randint(-500, 500), CENTER_Y + random.randint(-200, 200))
            hit_enemy.health -= self.damage
            if hit_enemy.health <= 0:
                on_field_enemies.remove(hit_enemy)
            self.enemies_hit.add(hit_enemy)
            self.bounce_off_enemy(hit_enemy)
            self.bounces += 1
            self.previous_enemy = hit_enemy
        else:
            self.previous_enemy = None

        if self.sprite.left <= 0 or self.sprite.right >= WIDTH:
            self.direction_x *= -1
        if self.sprite.top <= 0 or self.sprite.bottom >= HEIGHT:
            self.direction_y *= -1

    def bounce_off_enemy(self, enemy):
        # Calculate new direction based on the position of the enemy
        enemy_center_x = enemy.x + enemy.width / 2
        enemy_center_y = enemy.y + enemy.height / 2
        spell_center_x = self.sprite.x + self.sprite.width / 2
        spell_center_y = self.sprite.y + self.sprite.height / 2

        if enemy_center_x > spell_center_x:
            self.direction_x = -self.speed  # Change direction to left
        elif enemy_center_x < spell_center_x:
            self.direction_x = self.speed  # Change direction to right

        if enemy_center_y > spell_center_y:
            self.direction_y = -self.speed  # Change direction to up
        elif enemy_center_y < spell_center_y:
            self.direction_y = self.speed  # Change direction to down

class ChainShot(Spell):
    def __init__(self, sprite):
        super().__init__(sprite, "chain_shot")
        self.chain_limit = 5
        self.chains = 0
    
    def move(self):
        self.sprite.x += self.direction_x * self.speed
        self.sprite.y += self.direction_y * self.speed
        self.range -= self.speed

        if self.range <= 0 or self.chains >= self.chain_limit:
            spells.remove(self)
            return

        for enemy in on_field_enemies:
            if self.sprite.colliderect(enemy) and enemy not in self.enemies_hit:
                if enemy.type == "vampire":
                        vampire_bat_summon(enemy.x, enemy.y)
                        enemy.pos = (CENTER_X + random.randint(-500, 500), CENTER_Y + random.randint(-200, 200))
                enemy.health -= self.damage
                self.enemies_hit.add(enemy)
                self.chains += 1
                if enemy.health <= 0:
                    on_field_enemies.remove(enemy)
                self.target_next_enemy(enemy)
                break
    
    def target_next_enemy(self, current_enemy):
        closest_enemy = None
        min_distance = float("inf")
        for enemy in on_field_enemies:
            if enemy != current_enemy and enemy not in self.enemies_hit:
                distance = math.sqrt((enemy.x - current_enemy.x)**2 + (enemy.y - current_enemy.y)**2)
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
        
        if closest_enemy:
            self.angle = math.atan2(closest_enemy.y - self.sprite.y, closest_enemy.x - self.sprite.x)
            self.direction_x = math.cos(self.angle) * self.speed
            self.direction_y = math.sin(self.angle) * self.speed

class FreezeShot(Spell):
    def __init__(self, sprite):
        super().__init__(sprite, "freeze_shot")

    def move(self):
        self.sprite.x += self.direction_x * self.speed
        self.sprite.y += self.direction_y * self.speed
        self.range -= self.speed

        if self.range <= 0:
            spells.remove(self)
            return
        
        for enemy in on_field_enemies:
            if self.sprite.colliderect(enemy):
                if enemy.type == "vampire":
                        vampire_bat_summon(enemy.x, enemy.y)
                        enemy.pos = (CENTER_X + random.randint(-500, 500), CENTER_Y + random.randint(-200, 200))
                if not enemy.is_frozen:
                    self.freeze(enemy)
                enemy.health -= self.damage
                if enemy.health <= 0:
                    on_field_enemies.remove(enemy)
                if self in spells:
                    spells.remove(self)

    def freeze(self, enemy):
        if not enemy.is_frozen:
            enemy.distance_per_move /= 3
            enemy.is_frozen = True
            enemy.last_freeze_time = time.time()

# Game state
last_spell_cast_time = 0
last_attack_time = 0
on_field_enemies = []

# Functions
def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

orc = 2
num_orcs = 0
num_orcs_sprite = Actor("orc_enemy")
num_orcs_sprite.scale = 0.75
num_orcs_sprite.pos = (125, 190)
num_orcs_box = Rect(220, 165, 100, 50)
goblin = 3
num_goblins = 0
num_goblins_sprite = Actor("goblin_enemy")
num_goblins_sprite.scale = 0.75
num_goblins_sprite.pos = (116, 250)
num_goblins_box = Rect(220, 228, 100, 50)
bat = 1
num_bats = 0
num_bats_sprite = Actor("bat_enemy")
num_bats_sprite.scale = 0.75
num_bats_sprite.pos = (116, 310)
num_bats_box = Rect(220, 291, 100, 50)
assasin = 5
num_assasins = 0
num_assasins_sprite = Actor("assasin_enemy")
num_assasins_sprite.scale = 0.75
num_assasins_sprite.pos = (116, 370)
num_assasins_box = Rect(220, 348, 100, 50)
vampire = 15
num_vampires = 0
num_vampires_sprite = Actor("vampire_enemy")
num_vampires_sprite.scale = 0.75
num_vampires_sprite.pos = (116, 430)
num_vampires_box = Rect(220, 405, 100, 50)
necromancer = 10
num_necromancers = 0
num_necromancers_sprite = Actor("necromancer_enemy_placeholder")
num_necromancers_sprite.scale = 0.75
num_necromancers_sprite.pos = (116, 490)
num_necromancers_box = Rect(220, 461, 100, 50)
speed_factor = 0.3

monster_gate = Actor("monster_gate")
monster_gate.x = random.randint(-400, 400) + CENTER_X
monster_gate.y = random.randint(-200, 200) + CENTER_Y
monster_gate.spawn_time = 50

unchanging_types_of_enemies = [orc, goblin, bat, assasin, vampire, necromancer]
changing_types_of_enemies = [orc, goblin, bat, assasin, vampire, necromancer]


level_strength = -1
wave_number = -1

selected_enemies_for_next_level = []


def select_enemies_for_next_level():

    global level_strength
    global changing_types_of_enemies
    global num_orcs, num_goblins, num_bats, num_assasins, num_vampires, num_necromancers
    done = False
    while not done:
        for enemy in changing_types_of_enemies:
            if enemy > abs(level_strength):
                changing_types_of_enemies.remove(enemy)

        if len(changing_types_of_enemies) > 0:

            if max(changing_types_of_enemies) <= abs(level_strength):
                done = True

        else:
            done = True

    while abs(level_strength) > 0:
        if level_strength > 0:
            level_strength = 0
        if level_strength == 0:
            break

        x = random.randint(0, len(changing_types_of_enemies) - 1)

        if changing_types_of_enemies[x] <= abs(level_strength):
            selected_enemies_for_next_level.append(changing_types_of_enemies[x])
            level_strength += changing_types_of_enemies[x]

    for enemy in selected_enemies_for_next_level:
        if enemy == orc:
            num_orcs += 1
        elif enemy == goblin:
            num_goblins += 1
        elif enemy == bat:
            num_bats += 1
        elif enemy == assasin:
            num_assasins += 1
        elif enemy == vampire:
            num_vampires += 1
        elif enemy == necromancer:
            num_necromancers += 1

    #print(len(selected_enemies_for_next_level))
    
def reset_for_next_wave():
    global changing_types_of_enemies
    global unchanging_types_of_enemies
    global wave_number
    global level_strength
    global num_orcs, num_goblins, num_bats, num_assasins, num_vampires, num_necromancers
    monster_gate.x = random.randint(-400, 400) + CENTER_X
    monster_gate.y = random.randint(-200, 200) + CENTER_Y
    changing_types_of_enemies.clear()
    changing_types_of_enemies = [orc, goblin, bat, assasin, vampire, necromancer]
    selected_enemies_for_next_level.clear()
    wave_number -= 1
    level_strength = wave_number
    num_orcs = 0
    num_goblins = 0
    num_bats = 0
    num_assasins = 0
    num_vampires = 0
    num_necromancers = 0

summoning_next_wave = False
summon_cooldown = 500
def summon_next_wave():
    global game_state
    global summon_cooldown
    for enemy in selected_enemies_for_next_level:
        if monster_gate.spawn_time <= 0:
            monster_gate.spawn_time = random.randint(50, 200)
            if enemy == orc:
                on_field_enemies.append(create_enemy("orc"))
                selected_enemies_for_next_level.remove(enemy)
            elif enemy == goblin:
                on_field_enemies.append(create_enemy("goblin"))
                selected_enemies_for_next_level.remove(enemy)
            elif enemy == bat:
                on_field_enemies.append(create_enemy("bat"))
                selected_enemies_for_next_level.remove(enemy)
                #print("hello")
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
            monster_gate.spawn_time -= 1

def enemy_movement():
    global speed_factor
    for enemy in on_field_enemies:
        angle = math.atan2(player.sprite.y - enemy.y, player.sprite.x - enemy.x)
        enemy.move_ip(math.cos(angle) * enemy.distance_per_move * speed_factor,
                             math.sin(angle) * enemy.distance_per_move * speed_factor)

def enemy_behavior():
    global on_field_enemies
    for enemy in on_field_enemies:
        assassinate(enemy, player.health)
        if enemy.type == "necromancer":
            if enemy.ability_delay <= 0:
                necromancer_skeleton_summon(enemy.x, enemy.y)
                enemy.ability_delay = 500
            else:
                enemy.ability_delay -= 1
        if enemy.colliderect(player.sprite):
            if can_attack(enemy):
                attack(enemy)
    on_field_enemies = [enemy for enemy in on_field_enemies if enemy.health > 0]

def can_attack(enemy):
        current_time = time.time()
        return current_time - last_attack_time >= enemy.attack_cooldown

def attack(enemy):
    global last_attack_time
    if can_attack(enemy):
        player.take_damage(enemy.damage)
        last_attack_time = time.time()

def selected_spell():
    global selected_spell_index

    match selected_spell_index:
        case 0:
            direct_shot_sprite.scale = SELECTED_SPELL_SCALE
        case 1:
            penetrating_shot_sprite.scale = SELECTED_SPELL_SCALE
        case 2:
            bounce_shot_sprite.scale = SELECTED_SPELL_SCALE
        case 3:
            chain_shot_sprite.scale = SELECTED_SPELL_SCALE
        case 4:
            freeze_shot_sprite.scale = SELECTED_SPELL_SCALE

def reset_spell_scale():
    direct_shot_sprite.scale = 1
    penetrating_shot_sprite.scale = 1
    bounce_shot_sprite.scale = 1
    chain_shot_sprite.scale = 1
    freeze_shot_sprite.scale = 1

def draw_spell():
    global equipped_spell

    formatted_spell_name = equipped_spell.replace("_", " ")

    screen.draw.text(f"{formatted_spell_name} equipped", (720, 440), color="black")

    direct_shot_sprite.draw()
    penetrating_shot_sprite.draw()
    bounce_shot_sprite.draw()
    chain_shot_sprite.draw()
    freeze_shot_sprite.draw()

    screen.draw.text(f"owned", (720, 440), color="black")

def player_hearts():
    hearts = []
    player_health = player.health

    while player_health > 0:
        if player_health - 2 >= 0:
            player_health -= 2
            hearts.append(full_heart)
        elif player_health - 1 >= 0:
            player_health -= 1
            hearts.append(half_heart)
    
    while len(hearts) < 3:
        hearts.append(empty_heart)

    x_offset = 20
    hearts.reverse()
    for i, heart_img in enumerate(hearts):
        heart = Actor(heart_img)
        heart.pos = (WIDTH - (x_offset + i * 40), 20)
        heart.scale = 2
        heart.draw()

def purchase_spells(spell):
    global penetrating_owned, bounce_owned, chain_owned, freeze_owned

    if spell == "penetrating_shot" and player.coins >= 30:
        penetrating_owned = True
        player.coins -= 30
    elif spell == "bounce_shot" and player.coins >= 35:
        bounce_owned = True
        player.coins -= 35
    elif spell == "chain_shot" and player.coins >= 60:
        chain_owned = True
        player.coins -= 60
    elif spell == "bounce_shot" and player.coins >= 100:
        bounce_owned = True
        player.coins -= 100


# Main game loop
def draw():
    global game_state
    global num_orcs, num_goblins, num_bats, num_assasins, num_vampires, num_assasins
    global spell_changed
    screen.clear() # type: ignore

    if game_state == "Fight":
        for tile in tiles:
            tile.draw()
        monster_gate.draw()
        player.sprite.draw()
        for enemy in on_field_enemies:
            enemy.draw()
        for spell in spells:
            spell.sprite.draw()

    if game_state == "Shop":
        screen.fill("dark green")
        enemies_in_next_round.draw()
        num_orcs_sprite.draw()
        #screen.draw.rect(num_orcs_box, color = "black")
        screen.draw.textbox(str(num_orcs), num_orcs_box, color = ("black") )
        num_goblins_sprite.draw()
        #screen.draw.rect(num_goblins_box, color = "black")
        screen.draw.textbox(str(num_goblins), num_goblins_box, color = ("black") )
        num_bats_sprite.draw()
        #screen.draw.rect(num_bats_box, color = "black")
        screen.draw.textbox(str(num_bats), num_bats_box, color = ("black") )
        num_assasins_sprite.draw()
        #screen.draw.rect(num_assasins_box, color = "black")
        screen.draw.textbox(str(num_assasins), num_assasins_box, color = ("black") )
        num_vampires_sprite.draw()
        #screen.draw.rect(num_vampires_box, color = "black")
        screen.draw.textbox(str(num_vampires), num_vampires_box, color = ("black") )
        num_necromancers_sprite.draw()
        #screen.draw.rect(num_necromancers_box, color = "black")
        screen.draw.textbox(str(num_necromancers), num_necromancers_box, color = ("black") )

        spell_shop.draw()
        if spell_changed:
            reset_spell_scale()
            selected_spell()
            spell_changed = False 
        draw_spell()
    player_hearts()
    coin.draw()
    screen.draw.text(f"{player.coins}", (WIDTH - 60, 53), color="black", fontsize=45) # type: ignore

def on_mouse_down(pos):
    global last_spell_cast_time, spell_changed, equipped_spell, selected_spell_index

    if game_state == "Fight":
        current_time = time.time()
        equipped_spell_cooldown = spell_constants[equipped_spell]["cooldown"]
        if current_time - last_spell_cast_time >= equipped_spell_cooldown:
            if equipped_spell == "direct_shot":
                spell = DirectShot(Actor("direct_shot", pos=(player.sprite.x, player.sprite.y)))
            elif equipped_spell == "penetrating_shot":
                spell = PenetratingShot(Actor("penetrating_shot", pos=(player.sprite.x, player.sprite.y)))
            elif equipped_spell == "bounce_shot":
                spell = BounceShot(Actor("bounce_shot", pos=(player.sprite.x, player.sprite.y)))
            elif equipped_spell == "chain_shot":
                spell = ChainShot(Actor("chain_shot", pos=(player.sprite.x, player.sprite.y)))
            elif equipped_spell == "freeze_shot":
                spell = FreezeShot(Actor("freeze_shot", pos=(player.sprite.x, player.sprite.y)))
            spell.initialize_spell((player.sprite.x, player.sprite.y), pos)
            spells.append(spell)
            last_spell_cast_time = current_time
    if game_state == "Shop":
        if direct_shot_sprite.collidepoint(pos):
            equipped_spell = "direct_shot"
            spell_changed = True
        elif penetrating_shot_sprite.collidepoint(pos):
            if penetrating_owned:
                equipped_spell = "penetrating_shot"
                spell_changed = True
            else:
                purchase_spells("penetrating_shot")
        elif bounce_shot_sprite.collidepoint(pos):
            if bounce_owned:
                equipped_spell = "bounce_shot"
                spell_changed = True
            else:
                purchase_spells("bounce_shot")
        elif chain_shot_sprite.collidepoint(pos):
            if penetrating_owned:
                equipped_spell = "chain_shot"
                spell_changed = True
            else:
                purchase_spells("chain_shot")
        elif freeze_shot_sprite.collidepoint(pos):
            if freeze_owned:
                equipped_spell = "freeze_shot"
                spell_changed = True
            else:
                purchase_spells("freeze_shot")

        selected_spell_index = spell_types.index(equipped_spell)

        print(equipped_spell)

def on_key_up(key):
    global game_state, summoning_next_wave
    if game_state == "Shop":
        if key == keys.SPACE:
            game_state = "Fight"
            summoning_next_wave = True

           
def update():
    global game_state, summoning_next_wave

    player.player_movement()
    enemy_movement()
    for spell in spells:
        spell.move()
    if game_state == "Fight":
        if len(selected_enemies_for_next_level) > 0:
            if summoning_next_wave == True:
                summon_next_wave()

        else:
            summoning_next_wave = False
            if len(on_field_enemies) <= 0:
                game_state = "Shop"
                player.coins += abs(wave_number)
                reset_for_next_wave()
                select_enemies_for_next_level()

        enemy_behavior()
        
        current_time = time.time()
        for enemy in on_field_enemies:
            if enemy.is_frozen and current_time - enemy.last_freeze_time >= enemy.freeze_duration:
                enemy.distance_per_move *= 3
                enemy.is_frozen = False
                enemy.last_freeze_time = current_time
                 
    elif game_state == "Shop":
        spells.clear()

player = Player()

select_enemies_for_next_level()

clock.schedule_interval(update, 1.0 / 60.0) # type: ignore
pgzrun.go()
