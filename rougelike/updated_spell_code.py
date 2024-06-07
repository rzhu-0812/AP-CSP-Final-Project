import pgzrun
import math
import time

from pgzhelper import Actor

# Constants
WIDTH = 1200
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

# Actors
tiles = [Actor("tile", pos=((j * 100) + 50, (i * 100) + 50)) for i in range(int(HEIGHT / 100)) for j in range(int(WIDTH / 100))]
big_tiles = [Actor("big_tile", pos=((i * 300) + 150, (j * 300) + 150)) for i in range(3) for j in range(2)]

# Spells
spell_constants = {
    "spell_1": {
        "speed": 10,
        "range": 400,
        "cooldown": 0.75,
        "damage": 1
    },
    "spell_2": {
        "speed": 5,
        "range": 600,
        "cooldown": 1,
        "damage": 0.75
    },
    "spell_3": {
        "speed": 3,
        "range": 10000,
        "cooldown": 1.25,
        "damage": 0.5
    }
}

# Classes
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
        
class Enemy:
    def __init__(self, enemy_type, sprite, distance_per_move, health, damage, attack_cooldown):
        self.enemy_type = enemy_type
        self.sprite = sprite
        self.distance_per_move = distance_per_move
        self.health = health
        self.damage = damage
        self.attack_cooldown = attack_cooldown
        self.last_attack_time = 0
        self.spawn_at_center()

    def spawn_at_center(self):
        self.sprite.pos = (CENTER_X, CENTER_Y)
    
    def can_attack(self):
        current_time = time.time()
        return current_time - self.last_attack_time >= self.attack_cooldown

    def attack(self):
        if self.can_attack():
            player.take_damage(self.damage)
            self.last_attack_time = time.time()

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

        if self.spell_type == "spell_1":
            for enemy in on_field_enemies:
                if self.sprite.colliderect(enemy.sprite):
                    enemy.health -= self.damage
                    if enemy.health <= 0:
                        on_field_enemies.remove(enemy)
                    spells.remove(self)
        
        if self.spell_type == "spell_2":
            for enemy in on_field_enemies:
                if self.sprite.colliderect(enemy.sprite) and enemy not in self.enemies_hit:
                    enemy.health -= self.damage
                    self.enemies_hit.add(enemy)
                    if enemy.health <= 0:
                        on_field_enemies.remove(enemy)

class Spell_3(Spell):
    def __init__(self, sprite, spell_type):
        super().__init__(sprite, spell_type)
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

# Game state
last_spell_cast_time = 0
on_field_enemies = []

def enemy_movement():
    for enemy in on_field_enemies:
        angle = math.atan2(player.sprite.y - enemy.sprite.y, player.sprite.x - enemy.sprite.x)
        speed_factor = 0.3
        enemy.sprite.move_ip(math.cos(angle) * enemy.distance_per_move * speed_factor,
                             math.sin(angle) * enemy.distance_per_move * speed_factor)

def enemy_behavior():
    global on_field_enemies
    on_field_enemies = [enemy for enemy in on_field_enemies if enemy.health > 0]

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
    screen.draw.text(f"Health: {player.health}", (WIDTH - 90, 20), color="black")

def on_mouse_down(pos):
    global last_spell_cast_time

    current_time = time.time()
    equipped_spell_cooldown = spell_constants[equipped_spell]["cooldown"]
    if current_time - last_spell_cast_time >= equipped_spell_cooldown:
        if equipped_spell == "spell_3":
            spell = Spell_3(Actor(equipped_spell), equipped_spell)
        else:
            spell = Spell(Actor(equipped_spell), equipped_spell)
        spell.sprite.pos = (player.sprite.x, player.sprite.y)
        spell.targetx, spell.targety = pos
        spell.angle = math.atan2(spell.targety - spell.sprite.y, spell.targetx - spell.sprite.x)
        spell.direction_x = math.cos(spell.angle) * spell.speed
        spell.direction_y = math.sin(spell.angle) * spell.speed
        spells.append(spell)
        last_spell_cast_time = current_time

def update():
    player.player_movement()
    enemy_movement()
    for enemy in on_field_enemies:
        if player.sprite.colliderect(enemy.sprite):
            if enemy.can_attack():
                enemy.attack()
    for spell in spells:
        if isinstance(spell, Spell_3):
            spell.move()
        else:
            spell.move()

# Game start
enemy_constants = {
    "orc": {"distance_per_move": 2, "health": 5, "damage": 1, "attack_cooldown": 1},
    "goblin": {"distance_per_move": 6, "health": 3, "damage": 1, "attack_cooldown": 1},
    "bat": {"distance_per_move": 5,  "health": 3, "damage": 1, "attack_cooldown": 1},
    "assasin": {"distance_per_move": 3, "health": 4, "damage": 2, "attack_cooldown": 1},
    "vampire": {"distance_per_move": 1, "health": 10, "damage": 2, "attack_cooldown": 1}
}
enemy_actors = {
    "orc": Actor("orc_enemy_placeholder"),
    "goblin": Actor("goblin_enemy_placeholder"),
    "bat": Actor("bat_enemy_placeholder"),
    "assasin": Actor("assasin_enemy_placeholder"),
    "vampire": Actor("vampire_enemy_placeholder")
}

enemies = ["bat"]
for enemy in enemies:
    on_field_enemies.append(Enemy(enemy, enemy_actors.get(enemy), **enemy_constants[enemy]))

player = Player()

spells = []
equipped_spell = "spell_3"

clock.schedule_interval(update, 1.0 / 60.0) # type: ignore
pgzrun.go()
