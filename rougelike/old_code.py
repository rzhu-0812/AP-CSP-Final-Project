import pgzrun
import pygame
import random
import math
import time
from pgzhelper import *

WIDTH = 900
HEIGHT = 600
CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2
CENTER = (CENTER_X, CENTER_Y)

last_spell_cast_time = 0
cooldown = 0.1

tiles = []

for i in range(6):
    for j in range(9):
        tile = Actor("tile")
        tile.pos = ( (j * 100) + 50, (i * 100) + 50 )
        tiles.append(tile)

big_tiles = []

for i in range(3):
    for j in range(2):
        big_tile = Actor("big_tile")
        big_tile.pos = ( (i * 300) + 150, (j * 300) + 150 )
        big_tiles.append(big_tile)

enemy_placeholder_distance_per_move = 4
enemy_placeholder_resting_time = 1
enemy_placeholder_vision = 200
enemy_constants = [
    ["Placeholder", enemy_placeholder_distance_per_move, enemy_placeholder_resting_time, enemy_placeholder_vision]
    ]

class Enemy():
    type = ""
    x = CENTER_X
    y = CENTER_Y
    sprite = Actor("orc_enemy_placeholder")
    sprite.pos = (x, y)
    sprite_height = 0
    sprite_width = 0
    distance_per_move = 0
    mode = "Not Moving"
    movement_direction = ""
    resting_time = 0
    time_to_move = True
    vision = 0
    size = ""
    same_tile = False

"""
class Placeholder_Enemy(Enemy):
    sprite = Actor("enemy_placeholder")
    x = CENTER_X
    y = CENTER_Y
    sprite.pos = (x, y)
    sprite_height = 75
    sprite_width = 75
"""


"""
enemy = Enemy
#enemy.sprite = "enemy_placeholder"
enemy.type = "Placeholder"
enemy.sprite = Actor("orc_enemy_placeholder")
enemy.sprite.pos = (CENTER_X, CENTER_Y)
enemy.sprite_height = 75
enemy.sprite_width = 75
enemy.distance_per_move = enemy_constants[0][1]
enemy.resting_time = enemy_constants[0][2]
enemy.vision = enemy_constants[0][3]

enemies = [enemy]

"""
enemies = []
for i in range(3):
    enemy = Enemy
    #enemy.sprite = "enemy_placeholder"
    enemy.type = "Placeholder"
    enemy.sprite = Actor("orc_enemy_placeholder")
    enemy.sprite.pos = (CENTER_X + random.randint(-400, 400), CENTER_Y)
    enemy.sprite_height = 75
    enemy.sprite_width = 75
    enemy.distance_per_move = enemy_constants[0][1]
    enemy.resting_time = enemy_constants[0][2]
    enemy.vision = enemy_constants[0][3]
    enemies.append(enemy)

def enemy_movement():
    enemy_resting_time()
    for big_tile in big_tiles:
        for enemy in enemies:
            #print(enemy.movement_direction)
            if enemy.sprite.colliderect(player):
                pass

            elif enemy.mode == "Moving":
                if enemy.distance_per_move < 0:
                    enemy.distance_per_move = 0
                    
                if enemy.movement_direction == "UP":
                    #print("hello")
                    enemy.sprite.y -= enemy.distance_per_move/5
                    #print(enemy.distance_per_move/5)
                    enemy.distance_per_move -= (enemy_constants[0][1]/5)
                    #print(enemy.distance_per_move - enemy_constants[0][1]/5)

                elif enemy.movement_direction == "DOWN":
                    enemy.sprite.y += enemy.distance_per_move/5
                    #print(enemy.distance_per_move/5)
                    enemy.distance_per_move -= (enemy_constants[0][1]/5)
                    #print(enemy.distance_per_move - enemy_constants[0][1]/5)

                elif enemy.movement_direction == "RIGHT":
                    enemy.sprite.x += enemy.distance_per_move/5
                    enemy.distance_per_move -= (enemy_constants[0][1]/5)

                elif enemy.movement_direction == "LEFT":
                    enemy.sprite.x -= enemy.distance_per_move/5
                    enemy.distance_per_move -= (enemy_constants[0][1]/5)

                elif enemy.movement_direction == "UP/LEFT":
                    enemy.sprite.y -= enemy.distance_per_move/5
                    enemy.sprite.x -= enemy.distance_per_move/5
                    enemy.distance_per_move -= (enemy_constants[0][1]/5)

                elif enemy.movement_direction == "UP/RIGHT":
                    enemy.sprite.y -= enemy.distance_per_move/5
                    enemy.sprite.x += enemy.distance_per_move/5
                    enemy.distance_per_move -= (enemy_constants[0][1]/5)

                elif enemy.movement_direction == "DOWN/LEFT":
                    enemy.sprite.y += enemy.distance_per_move/5
                    enemy.sprite.x -= enemy.distance_per_move/5
                    enemy.distance_per_move -= (enemy_constants[0][1]/5)

                elif enemy.movement_direction == "DOWN/RIGHT":
                    enemy.sprite.y += enemy.distance_per_move/5
                    enemy.sprite.x += enemy.distance_per_move/5
                    enemy.distance_per_move -= (enemy_constants[0][1]/5)


                    

            elif enemy.mode == "Not Moving":
                if enemy.time_to_move == True:
                
                    if enemy.sprite.colliderect(big_tile) and player.colliderect(big_tile):

                        if enemy.sprite.y > player.y:

                            if enemy.sprite.y - player.y <= (enemy.vision) * 1.5 and enemy.sprite.y - player.y > enemy.sprite_height/2:
                                #print(enemy.sprite.y - player.y)
                                #print(enemy.sprite.x - player.x)
                                #print(player.x - enemy.sprite.x)
                                
                                if enemy.sprite.x > player.x:
                                    if enemy.sprite.x - player.x <= enemy.vision/3:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "UP"
                                        enemy.time_to_move = False

                                elif player.x > enemy.sprite.x:
                                    if player.x - enemy.sprite.x <= enemy.vision/3:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "UP"

                            

                        elif enemy.sprite.y < player.y:
                            
                            if player.y - enemy.sprite.y <= (enemy.vision) * 1.5 and player.y - enemy.sprite.y > enemy.sprite_height/2:
                                if enemy.sprite.x > player.x:
                                    
                                    if enemy.sprite.x - player.x <= enemy.vision/3:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "DOWN"
                                        enemy.time_to_move = False

                                elif player.x > enemy.sprite.x:
                                    if player.x - enemy.sprite.x <= enemy.vision/3:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "DOWN"

                        if enemy.sprite.x > player.x:
                            if enemy.sprite.x - player.x <= (enemy.vision) * 1.5 and enemy.sprite.x - player.x > enemy.sprite_width/2:

                                if enemy.sprite.y > player.y:
                                    if enemy.sprite.y - player.y <= enemy.vision/3:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "LEFT"
                                        enemy.time_to_move = False

                                elif player.y > enemy.sprite.y:
                                    if player.y - enemy.sprite.y <= enemy.vision/3:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "LEFT"

                        elif enemy.sprite.x < player.x:
                            if player.x - enemy.sprite.x <= (enemy.vision) * 1.5 and player.x - enemy.sprite.x > enemy.sprite_width/2:

                                if enemy.sprite.y > player.y:
                                    if enemy.sprite.y - player.y <= enemy.vision/3:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "RIGHT"
                                        enemy.time_to_move = False

                                elif player.y > enemy.sprite.y:
                                    if player.y - enemy.sprite.y <= enemy.vision/3:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "RIGHT"

                        if enemy.sprite.y > player.y:
                            if enemy.sprite.y - player.y <= (enemy.vision) * 1.5 and enemy.sprite.y - player.y > enemy.sprite_height/2:
                                if enemy.sprite.x > player.x:
                                    if enemy.sprite.x - player.x >= enemy.sprite_width/2 and enemy.sprite.x - player.x < enemy.vision * 1.5:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "UP/LEFT"
                                        enemy.time_to_move = False
                                elif enemy.sprite.x < player.x:
                                    if player.x - enemy.sprite.x >= enemy.sprite_width/2 and player.x - enemy.sprite.x < enemy.vision * 1.5:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "UP/RIGHT"

                        elif enemy.sprite.y < player.y:
                            if player.y - enemy.sprite.y <= (enemy.vision) * 1.5 and player.y - enemy.sprite.y > enemy.sprite_height/2:
                                if enemy.sprite.x > player.x:
                                    if enemy.sprite.x - player.x >= enemy.sprite_width/2 and enemy.sprite.x - player.x < enemy.vision * 1.5:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "DOWN/LEFT"
                                        enemy.time_to_move = False
                                elif enemy.sprite.x < player.x:
                                    if player.x - enemy.sprite.x >= enemy.sprite_width/2 and player.x - enemy.sprite.x < enemy.vision * 1.5:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "DOWN/RIGHT"

                            

"""
                                    elif enemy.sprite.x - player.x <= enemy.vision:
                                        if enemy.sprite.y - player.y > enemy.vision/2 and enemy.sprite.y - player.y <= enemy.vision:
                                            enemy.mode = "Moving"
                                            enemy.movement_direction = "LEFT"
                                            enemy.time_to_move = False

                                    elif enemy.sprite.x - player.x > enemy.vision/2 and enemy.sprite.x - player.x <= enemy.vision:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "UP/LEFT"
                                        enemy.time_to_move = False


                                        
                                elif enemy.sprite.x < player.x:
                                    if player.x - enemy.sprite.x <= enemy.vision/2:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "UP"
                                        enemy.time_to_move = False

                                    elif player.x - enemy.sprite.x > enemy.vision/2 and player.x - enemy.sprite.x <= enemy.vision:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "UP/RIGHT"
                                        enemy.time_to_move = False




                        if enemy.sprite.y < player.y:

                            if player.y - enemy.sprite.y <= enemy.vision:
                                #print(player.y - enemy.sprite.y)
                                #print(enemy.sprite.x - player.x)
                                #print(player.x - enemy.sprite.x)
                                
                                if enemy.sprite.x > player.x:
                                    if enemy.sprite.x - player.x <= enemy.vision/2:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "DOWN"
                                        enemy.time_to_move = False

                                    elif enemy.sprite.x - player.x > enemy.vision/2 and enemy.sprite.x - player.x <= enemy.vision:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "DOWN/LEFT"
                                        enemy.time_to_move = False

                                        
                                elif enemy.sprite.x < player.x:
                                    if player.x - enemy.sprite.x <= enemy.vision/2:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "DOWN"
                                        enemy.time_to_move = False

                                    elif player.x - enemy.sprite.x > enemy.vision/2 and player.x - enemy.sprite.x <= enemy.vision:
                                        enemy.mode = "Moving"
                                        enemy.movement_direction = "DOWN/RIGHT"
                                        enemy.time_to_move = False

                                        """

                            

def enemy_resting_time():
    for enemy in enemies:
       # print(enemy.resting_time)
        if enemy.distance_per_move <= 0:
            if enemy.mode == "Moving":
                enemy.mode = "Not Moving"
                if enemy.type == "Placeholder":
                    enemy.distance_per_move = enemy_constants[0][1]
                
        if enemy.mode == "Not Moving":
            if enemy.resting_time <= 0:
                    enemy.time_to_move = True

                    if enemy.type == "Placeholder":
                        enemy.resting_time = enemy_constants[0][2]
            else:
                enemy.resting_time -= 1
                            
                        

player = Actor("player_placeholder")

def player_movement():
    if keyboard.W or keyboard.up:
        if player.y > 0:
            player.y -= 5
    elif keyboard.S or keyboard.down:
        if player.y < 600:
            player.y += 5
    elif keyboard.A or keyboard.left:
        if player.x > 0:
            player.x -= 5
    elif keyboard.D or keyboard.right:
        if player.x < 900:
            player.x += 5

spells_stats = [
    ]

spells = []

equippable_spells = ["spell_placeholder"]
equipped_spell = equippable_spells[0]

class Spell():
    type = ""
    x = player.x
    y = player.y
    sprite = Actor("spell_placeholder")
    sprite.x = CENTER_X
    sprite.y = CENTER_Y
    sprite_height = 0
    sprite_width = 0
    speed = 10
    spell_range = 500
    size = ""
    targety = 0
    targetx = 0
    angle = math.atan2(targety - sprite.y, targetx - sprite.x)
    direction_x = math.cos(angle) * speed
    direction_y = math.sin(angle) * speed
    delete = False

def create_and_target_spell(mouse_pos, x, y):
        spell = Spell()
        #print(spell)
        spell.speed = 10
        if equipped_spell == equippable_spells[0]:
            spell.type = "Placeholder Spell"
            spell.sprite = Actor("spell_placeholder")
        spell.sprite.pos = (x, y)
        spell.targetx = mouse_pos[0]
        spell.targety = mouse_pos[1]
        spell.angle = math.atan2(spell.targety - spell.sprite.y, spell.targetx - spell.sprite.x)
        spell.direction_x = math.cos(spell.angle) * spell.speed
        spell.direction_y = math.sin(spell.angle) * spell.speed
        spell.spell_range = 500
        spells.append(spell)
        #print(spell)
        del spell

        
def spell_behavior():
    for spell in spells:
        #print(spell.sprite.pos)
        if spell.delete:
            spells.remove(spell)
            
        if spell.spell_range <= 0:
            spell.delete = True

        else:
            spell.sprite.x += spell.direction_x
            #print(spell.x)
            spell.sprite.y += spell.direction_y
            spell.spell_range -= spell.speed
        

def on_same_tile():
    for big_tile in big_tiles:
        for enemy in enemies:
            if player.colliderect(big_tile) and enemy.colliderect(big_tile):
                enemy.on_same_tile = True

def draw():
    screen.clear()
    
    for tile in tiles:
        tile.draw()

    #for big_tile in big_tiles:
        #big_tile.draw()

    player.draw()
    enemy.sprite.draw()

    for spell in spells:
        spell.sprite.draw()

def on_mouse_down(pos):
    global last_spell_cast_time

    current_time = time.time()
    if current_time - last_spell_cast_time >= cooldown:
        create_and_target_spell(pos, player.x, player.y)
        last_spell_cast_time = current_time
    #print(player.x)
    #print(player.y)

def update():
    player_movement()
    enemy_movement()
    spell_behavior()

pgzrun.go()
