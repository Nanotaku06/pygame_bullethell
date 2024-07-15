import pygame
from pygame.locals import *
import math
import random

#manage external resources
import player_class as pc
import enemy_class as ec

import projectile as prj
import weapon as wp
#game classes and functions

def move_projectile(projectileRect):
    return projectileRect.move(0,10)


running = True
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,800))
#text setup
titlefont = pygame.font.Font('freesansbold.ttf', 48)
font = pygame.font.Font('freesansbold.ttf', 24)
buttonfont = pygame.font.Font('freesansbold.ttf', 40)


#music setup
main_theme = pygame.mixer_music.load("./music/main_theme.mp3")
hit_sound = pygame.mixer.Sound("./music/hit_sound.mp3")
player_hit = pygame.mixer.Sound("./music/player_hit.mp3")
level_up = pygame.mixer.Sound("./music/level_up.mp3")
level_fail = pygame.mixer.Sound("./music/level_failed.mp3")

#sprites setup
ink = pygame.image.load("./sprites/ink.png").convert_alpha()
background_image = pygame.image.load("./sprites/brown_background.png").convert()
knight_sprite = pygame.image.load("./sprites/knight.png").convert_alpha()
gun = pygame.image.load("./sprites/gun.png").convert_alpha()
bullet = pygame.image.load("./sprites/bullet.png").convert_alpha()
blue_proj = pygame.image.load("./sprites/blue_proj.png").convert_alpha()
cursor = pygame.image.load("./sprites/cursor.png").convert_alpha()
red_proj = pygame.image.load("./sprites/red_proj.png").convert_alpha()

#initialize the game
while running:
    on_gameplay_loop = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            in_level = False
            dead = False
            on_gameplay_loop = False

    #background walls
    walls = []
    wall_screens = []
    topRect = pygame.Rect(0,0,800,20)
    walls.append(topRect)
    leftRect = pygame.Rect(0,0,20,800)
    walls.append(leftRect)
    rightRect = pygame.Rect(790,0,20,800)
    walls.append(rightRect)
    bottomRect = pygame.Rect(0,790,800,20)
    walls.append(bottomRect)

    for w in walls:
        wall_surface = pygame.Surface((w.w, w.h))
        wall_screens.append(wall_surface)

    #Player stufff
    player = pc.Player()
    alive = True
    weapon = wp.Weapon(player)
    kill_count = 0
    p_attack_opportunity=0
    player.hp = 100
    player.dmg_mult = 1
    level = 0

    pygame.mixer.music.play(-1,0,0)
#main loop
    while on_gameplay_loop:
        in_level = True
        # Enemy stuff
        level+=1
        level_up.play()
        enemy_list = []
        enemy_screens = []

        for i in range(2+math.floor(level*0.5)):
            random_enemy = random.randint(0,1)
            match(random_enemy):
                case 0:
                    enemy = ec.FireEnemy(player)
                    e_surface = (pygame.image.load("./sprites/fire_sprite_1.png"), pygame.image.load("./sprites/fire_sprite_2.png"))
                    enemy_screens.append(e_surface)
                case 1:
                    enemy = ec.WaterEnemy(player)
                    e_surface = (pygame.image.load("./sprites/octopus_sprite_1.png"), pygame.image.load("./sprites/octopus_sprite_2.png"))
                    enemy_screens.append(e_surface)
            
            enemy_list.append(enemy)
            

        sprite_opportunity = 0

        # projectile stuff

        projectile_types = []
        dir_x = 0
        dir_y = 0

        while in_level:
            for e in enemy_list:
                if(e.attacking == False):
                    e.atk_opportunity+=1 
                e.move_opportunity +=1
            sprite_opportunity +=1

            if(p_attack_opportunity<30):
                p_attack_opportunity+=1



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    in_level = False
                    dead = False
                    on_gameplay_loop = False
                if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                    running = False
                    in_level = False
                    dead = False
                    on_gameplay_loop = False
            

            if(player.hp<=0):
                alive = False

            x=0
            for e in enemy_list:
                if (e.hp<=0):
                    enemy_list.remove(e)
                    enemy_screens.remove(enemy_screens[x])
                    kill_count +=1
                x+=1    
                    

            #background
            screen.fill((255, 255, 255))
            screen.blit(background_image, (0,0))
            for w in range(len(wall_screens)):
                wall_screens[w].fill((0,0,0))
                screen.blit(wall_screens[w], (walls[w].x, walls[w].y))



            #HUD
            text = font.render("HP: " + str(player.hp), True, (255, 255, 255))
            textRect = text.get_rect()
            screen.blit(text, textRect)

            text = font.render("LVL: " + str(level), True, (255, 255, 255),(0,0,0))
            textRect = text.get_rect()
            textRect.y = 40
            screen.blit(text, textRect)




            if(alive):
                #movement
                keys = pygame.key.get_pressed()

                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()


                if keys[K_w]:
                    if(player.playerRect.y>10):
                        player.playerRect = player.playerRect.move(0, -player.speed)
                        weapon.weaponRect = weapon.weaponRect.move(0, -player.speed)
                if keys[K_a]:
                    if(player.playerRect.x > 10):
                        player.playerRect = player.playerRect.move(-player.speed, 0)
                        weapon.weaponRect = weapon.weaponRect.move(-player.speed, 0)
                if keys[K_s]:
                    if (player.playerRect.y < 740):
                        player.playerRect = player.playerRect.move(0, player.speed)
                        weapon.weaponRect = weapon.weaponRect.move(0, player.speed)
                if keys[K_d]:
                    if (player.playerRect.x < 740):
                        player.playerRect = player.playerRect.move(player.speed, 0)
                        weapon.weaponRect = weapon.weaponRect.move(player.speed, 0)

                if p_attack_opportunity>=30:
                    p_attack_opportunity=0
                    weapon.shoot(mouse_pos)

                # character assets
                screen.blit(knight_sprite, (player.playerRect.x, player.playerRect.y))
                weapon.update_weapon(screen, mouse_pos, gun)

                if(len(enemy_list)<=0):
                    in_level = False

                for e in enemy_list:
                    #text
                    text = font.render("HP: " + str(math.floor(e.hp)), True, (255, 0, 0))
                    textRect = text.get_rect()
                    textRect.center = (e.enemyRect.x, e.enemyRect.y - 50)
                    screen.blit(text, textRect)

                    #movement

                    match (e.type):
                        case "fire":
                            
                            e.move(walls)
                        case "water":
                            if e.attacking == True:
                                pass
                            else:
                                e.move(walls)
                            
                            pass

                    if(sprite_opportunity<15):    
                        for f in range(len(enemy_list)):
                            screen.blit(enemy_screens[f][0], (enemy_list[f].enemyRect.x, enemy_list[f].enemyRect.y))
                    elif(sprite_opportunity<30):    
                        for f in range(len(enemy_list)):
                            screen.blit(enemy_screens[f][1], (enemy_list[f].enemyRect.x, enemy_list[f].enemyRect.y))
                    if(sprite_opportunity>=30):
                        sprite_opportunity = 0                                    

                    #player damage >:3
                    for x in e.projectile_list:
                        hasCollided = pygame.Rect.colliderect(player.playerRect, x.rect)
                        if hasCollided:
                            player_hit.play()
                            player.hp-= x.base_dmg
                            e.projectile_list.remove(x)

                    #enemy damage
                    for x in weapon.projectile_list:
                        hasCollided = pygame.Rect.colliderect(e.enemyRect, x.rect)
                        if hasCollided:
                            hit_sound.play()
                            e.hp-= x.base_dmg*player.dmg_mult
                            weapon.projectile_list.remove(x)

                    #enemy attack  and move oportunities
                    if(e.move_opportunity%30==3):
                        if e.type ==  'water':
                            if(e.atk_clock>=1):
                                pass
                            else: 
                                e.pick_dir()
                        else:
                            e.pick_dir()    
                    
                    if(e.atk_opportunity*e.atk_speed%60==0 and e.atk_opportunity !=0):
                        e.atk_opportunity=0
                        match e.type:
                            case "fire":
                                randNum = random.randint(0, 1)
                                match(randNum):
                                    case 0:
                                        e.atk_clock=0
                                        e.atk1()
                                    case 1:
                                        e.atk_clock=0
                                        e.atk2()
                            case 'water':
                                if(not e.attacking):
                                    randNum = random.randint(0,5)
                                    if randNum > 2:
                                        e.atk_clock=1
                                    
                                    else:
                                        e.atk_clock=0
                                        e.atk1()
                        
                    if e.type ==  'water':
                        if(e.atk_clock>=140):
                            e.atk2(screen, ink) 
                        elif(e.atk_clock >=1):
                            e.atk2(screen, ink)
                            e.update_projectiles(screen, blue_proj)
                        else:
                            e.update_projectiles(screen, blue_proj)
                    else:
                        e.update_projectiles(screen, red_proj)        
                weapon.update_projectiles(screen, bullet)


            else:
                dead = True
                pygame.mixer.music.stop()
                level_fail.play()
                retry_surface = pygame.Surface((150, 50))
                retry_text = buttonfont.render("Retry", True, (255, 255, 255))
                retry_text_rect = retry_text.get_rect(center=(retry_surface.get_width()/2, retry_surface.get_height()/2))
                button_rect = pygame.Rect(150, 500, 150, 50)

                quit_surface = pygame.Surface((150, 50))
                quit_text = buttonfont.render("Quit", True, (255, 255, 255))
                quit_text_rect = quit_text.get_rect(center=(quit_surface.get_width() / 2, quit_surface.get_height() / 2))
                quit_button_rect = pygame.Rect(550, 500, 150, 50)

                while dead:
                    screen.fill((255, 255, 255))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            in_level = False
                            dead = False
                            on_gameplay_loop = False

                    if (level < 6):
                        text = titlefont.render("YOU'RE NOT A", True, (0, 0, 0))
                        textRect = text.get_rect()
                        screen.blit(text, (400 - textRect.w / 2, 200 - textRect.h / 2))
                        text = titlefont.render("BULLETHELL GOD", True, (0, 0, 0))
                        textRect = text.get_rect()
                        screen.blit(text, (400 - textRect.w / 2, 260 - textRect.h / 2))
                    else:
                        text = titlefont.render("GGs.", True, (0, 0, 0))
                        textRect = text.get_rect()
                        screen.blit(text, (400 - textRect.w / 2, 200 - textRect.h / 2))

                    text = font.render("enemies killed: " + str(kill_count), True, (0, 0, 0))
                    textRect = text.get_rect()
                    screen.blit(text, (100, 350 - textRect.h / 2))
                    text = font.render("max Level: " + str(level), True, (0, 0, 0))
                    textRect = text.get_rect()
                    screen.blit(text, (100, 400 - textRect.h / 2))


                    retry_surface.blit(retry_text, retry_text_rect)
                    quit_surface.blit(quit_text, quit_text_rect)
                    screen.blit(retry_surface, (button_rect.x, button_rect.y))
                    screen.blit(quit_surface, (quit_button_rect.x, quit_button_rect.y))
                    pygame.display.flip()

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if button_rect.collidepoint(event.pos):
                            dead = False
                            on_gameplay_loop = False
                            in_level = False
                        if quit_button_rect.collidepoint(event.pos):
                            running = False
                            in_level = False
                            dead = False
                            on_gameplay_loop = False

            # updating screen

            screen.blit(cursor, (mouse_pos[0]-cursor.get_width()/2 , mouse_pos[1]-cursor.get_width()/2))
            pygame.display.flip()
            clock.tick(60)

        player.hp+=10
        if(level%2==0):
            player.dmg_mult+=1.2
