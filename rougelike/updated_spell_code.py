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
        self.sprite = Actor("player_placeholder")
        self.sprite.pos = (38, 38)
        self.health = 3
    
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

# Enemy Class  
class Enemy:
    def __init__(self, enemy_type, player):
        constants = enemy_constants[enemy_type]
        self.enemy_type = enemy_type
        self.sprite = constants["actor"]
        self.distance_per_move = constants["distance_per_move"]
        self.health = constants["health"]
        self.damage = constants["damage"]
        self.attack_cooldown = constants["attack_cooldown"]
        self.last_attack_time = 0
        self.random_spawn()
        self.player = player

    def random_spawn(self):
        min_distance = 200
        while True:
            self.sprite.x = random.randint(40, WIDTH - 40)
            self.sprite.y = random.randint(40, HEIGHT - 40)
            if self.distance_to_player() > min_distance:
                break

    def distance_to_player(self):
        return math.sqrt((self.sprite.x - player.sprite.x) ** 2 + (self.sprite.y - player.sprite.y) ** 2)
    
    def can_attack(self):
        current_time = time.time()
        return current_time - self.last_attack_time >= self.attack_cooldown

    def attack(self):
        if self.can_attack():
            player.take_damage(self.damage)
            self.last_attack_time = time.time()
    
    def enemy_movement(self):
        angle = math.atan2(player.sprite.y - self.sprite.y, player.sprite.x - self.sprite.x)
        speed_factor = 0.3
        self.sprite.move_ip(math.cos(angle) * self.distance_per_move * speed_factor,
                             math.sin(angle) * self.distance_per_move * speed_factor)

    @classmethod 
    # A classmethod is a method bound to a class, but not an instance of a class. It takes in cls (class) instead of self as parameter.
    def update_enemies(cls):
        for enemy in on_field_enemies:
            enemy.enemy_movement()
            if player.sprite.colliderect(enemy.sprite):
                if enemy.can_attack():
                    enemy.attack()
        on_field_enemies[:] = [enemy for enemy in on_field_enemies if enemy.health > 0]

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
            if self.sprite.colliderect(enemy.sprite):
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
            if self.sprite.colliderect(enemy.sprite) and enemy not in self.enemies_hit:
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
            if self.sprite.colliderect(enemy.sprite) and (self.previous_enemy is None or enemy != self.previous_enemy):
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
        enemy_center_x = enemy.sprite.x + enemy.sprite.width / 2
        enemy_center_y = enemy.sprite.y + enemy.sprite.height / 2
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
            if self.sprite.colliderect(enemy.sprite) and enemy not in self.enemies_hit:
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
                distance = math.sqrt((enemy.sprite.x - current_enemy.sprite.x)**2 + (enemy.sprite.y - current_enemy.sprite.y)**2)
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
        
        if closest_enemy:
            self.angle = math.atan2(closest_enemy.sprite.y - self.sprite.y, closest_enemy.sprite.x - self.sprite.x)
            self.direction_x = math.cos(self.angle) * self.speed
            self.direction_y = math.sin(self.angle) * self.speed

# Game state
last_spell_cast_time = 0
on_field_enemies = []

# Main game loop
def draw():
    screen.clear() # type: ignore
    for tile in tiles:
        tile.draw()
    player.sprite.draw()
    for enemy in on_field_enemies:
        enemy.sprite.draw()
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

def update():
    player.player_movement()
    Enemy.update_enemies()
    for spell in spells:
        spell.move()

player = Player()

enemies = ["orc", "goblin", "bat", "assasin", "vampire"]
for enemy in enemies:
    on_field_enemies.append(Enemy(enemy, player))

spells = []
equipped_spell = "chain_shot"

clock.schedule_interval(update, 1.0 / 60.0) # type: ignore
pgzrun.go()