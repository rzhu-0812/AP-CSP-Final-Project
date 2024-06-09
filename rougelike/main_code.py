import pgzrun
import math
import random
import time

from pgzhelper import Actor

# Constants
WIDTH = 1200
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
TILE_SIZE = 100

game_state = "Shop"

# Actors
tiles = [Actor("tile", pos=((j * TILE_SIZE) + 50, (i * TILE_SIZE) + 50)) for i in range(int(HEIGHT / TILE_SIZE)) for j in range(int(WIDTH / 100))]

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
        "range": 600,
        "cooldown": 1,
        "damage": 0.75
    },
    "bounce_shot": {
        "speed": 3,
        "range": 5000,
        "cooldown": 1.5,
        "damage": 0.5
    },
    "chain_shot": {
        "speed": 3,
        "range": 2000,
        "cooldown": 1.5,
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
        enemy.pos = (CENTER_X + random.randint(-400, 400), CENTER_Y)
        enemy.attack_cooldown = 2
        return(enemy)
    if enemy_type == "goblin":
        enemy = Actor("goblin_enemy")
        enemy.type = "goblin"
        enemy.distance_per_move = 6
        enemy.health = 3
        enemy.damage = 1
        enemy.pos = (CENTER_X + random.randint(-400, 400), CENTER_Y)
        enemy.attack_cooldown = 2
        return(enemy)
    if enemy_type == "bat":
        enemy = Actor("bat_enemy")
        enemy.type = "bat"
        enemy.distance_per_move = 4
        enemy.health = 3
        enemy.damage = 1
        enemy.pos = (CENTER_X + random.randint(-400, 400), CENTER_Y)
        enemy.attack_cooldown = 2
        return(enemy)
    if enemy_type == "assasin":
        enemy = Actor("assasin_enemy")
        enemy.type = "assasin"
        enemy.distance_per_move = 3
        enemy.health = 4
        enemy.damage = 5
        enemy.pos = (CENTER_X + random.randint(-400, 400), CENTER_Y)
        enemy.attack_cooldown = 2
        return(enemy)
    if enemy_type == "vampire":
        enemy = Actor("vampire_enemy")
        enemy.type = "vampire"
        enemy.distance_per_move = 1
        enemy.health = 10
        enemy.damage = 2
        enemy.pos = (CENTER_X + random.randint(-400, 400), CENTER_Y)
        enemy.attack_cooldown = 2
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
        enemy.attack_cooldown = 2
        on_field_enemies.append(enemy)
    
def vampire_bat_summon(vampire_x, vampire_y):
    summon_amount = random.randint(0, 3)
    for i in range(summon_amount):
        enemy = Actor("bat_enemy")
        enemy.type = "bat"
        enemy.distance_per_move = 5
        enemy.health = 3
        enemy.damage = 1
        enemy.pos = (vampire_x + random.randint(-50, 50), vampire_y + random.randint(-50, 50))
        enemy.attack_cooldown = 2
        on_field_enemies.append(enemy)


def vampire_special():
    vampire_bat_summon(enemy.x, enemy.y)
    enemy.pos = (CENTER_X + random.randint(-500, 500), CENTER_Y + random.randint(-200, 200))

# Spell Classes
class Spell:
    def __init__(self, sprite, spell_type):
        constants = spell_constants[spell_type]
        self.spell_type = spell_type
        self.sprite = sprites
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
                enemy.health -= self.damage
                self.enemies_hit.add(enemy)
                if enemy.health <= 0:
                    on_field_enemies.remove(enemy)

class BounceShot(Spell):
    def __init__(self, sprite):
        super().__init__(sprite, "bounce_shot")
        self.direction_x = 1
        self.direction_y = 0
        self.bounce_limit = 3
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
        self.chain_limit = 3
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

# Game state
last_spell_cast_time = 0
last_attack_time = 0
on_field_enemies = []

# Functions
def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

orc = 2
goblin = 3
bat = 1
assasin = 5
vampire = 15
speed_factor = 0.3

unchanging_types_of_enemies = [orc, goblin, bat, assasin, vampire]
changing_types_of_enemies = [orc, goblin, bat, assasin, vampire]


level_strength = -1
wave_number = -1

selected_enemies_for_next_level = []


def select_enemies_for_next_level():

    global level_strength
    global changing_types_of_enemies
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
    
def reset_for_next_wave():
    global changing_types_of_enemies
    global unchanging_types_of_enemies
    global wave_number
    global level_strength
    changing_types_of_enemies.clear()
    changing_types_of_enemies = [orc, goblin, bat, assasin, vampire]
    selected_enemies_for_next_level.clear()
    wave_number -= 1
    level_strength = wave_number


summon_cooldown = 500
def summon_next_wave():
    global game_state
    global summon_cooldown
    game_state = "Fight"
    while len(selected_enemies_for_next_level) > 0:
        for enemy in selected_enemies_for_next_level:
            if summon_cooldown <= 0:
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
                    
            else:
                summon_cooldown -= 1

def enemy_movement():
    global speed_factor
    for enemy in on_field_enemies:
        angle = math.atan2(player.sprite.y - enemy.y, player.sprite.x - enemy.x)
        enemy.move_ip(math.cos(angle) * enemy.distance_per_move * speed_factor,
                             math.sin(angle) * enemy.distance_per_move * speed_factor)

def enemy_behavior():
    global on_field_enemies
    for enemy in on_field_enemies:
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


# Main game loop
def draw():
    global game_state
    screen.clear() # type: ignore

    if game_state == "Fight":
        for tile in tiles:
            tile.draw()
        player.sprite.draw()
        for enemy in on_field_enemies:
            enemy.draw()
        for spell in spells:
            spell.sprite.draw()
        screen.draw.text(f"Health: {player.health}", (WIDTH - 90, 20), color="black") # type: ignore

def on_mouse_down(pos):
    global last_spell_cast_time

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
        spell.initialize_spell((player.sprite.x, player.sprite.y), pos)
        spells.append(spell)
        last_spell_cast_time = current_time

def on_key_up(key):
    global game_state
    if game_state == "Shop":
        if key == keys.SPACE:
            select_enemies_for_next_level()
            summon_next_wave()
            reset_for_next_wave()

def update():
    global game_state

    player.player_movement()
    enemy_movement()
    for spell in spells:
        spell.move()
    if game_state == "Fight":
        enemy_behavior()
        if len(on_field_enemies) <= 0:
            game_state = "Shop"

player = Player()

enemy_constants = {
    "orc": {"distance_per_move": 2, "health": 7, "damage": 1, "attack_cooldown": 2},
    "goblin": {"distance_per_move": 6, "health": 3, "damage": 1, "attack_cooldown": 2},
    "bat": {"distance_per_move": 4,  "health": 3, "damage": 1, "attack_cooldown": 2},
    "assasin": {"distance_per_move": 3, "health": 4, "damage": 5, "attack_cooldown": 2},
    "vampire": {"distance_per_move": 1, "health": 10, "damage": 2, "attack_cooldown": 2}
}
enemy_actors = {
    "orc": Actor("orc_enemy_placeholder"),
    "goblin": Actor("goblin_enemy_placeholder"),
    "bat": Actor("bat_enemy_placeholder"),
    "assasin": Actor("assasin_enemy_placeholder"),
    "vampire": Actor("vampire_enemy_placeholder")
}

enemy_attack_cooldown = {
    "orc": 2,
    "goblin": 2,
    "bat": 2,
    "assasin": 2,
    "vampire": 2
}

enemies = ["orc", "orc", "orc", "orc", "orc"]

spells = []
equipped_spell = "penetrating_shot"

clock.schedule_interval(update, 1.0 / 60.0) # type: ignore
pgzrun.go()