import projectile as prj
import pygame
import random
import math


class Enemy:
    def __init__(self, player, hp=100,speed=3,dmg_mult=1, x=250, y=100, w=50,h=50, atk_speed=1, atk_opportunity = 0, move_opportunity = 0, type = "fire"):
        self.projectile_list = []
        randx = random.randint(0,500)

        self.hp = hp
        self.speed = speed
        self.dmg_mult = dmg_mult
        self.enemyRect = pygame.Rect(x+randx,y,w,h)
        self.atk_speed = atk_speed
        self.p_pos = player
        self.rand_x = 0
        self.rand_y = 0
        self.attacking = False
        self.atk_clock = 0
        self.atk_opportunity = atk_opportunity+ random.randint(-10,20)
        self.move_opportunity = move_opportunity
        self.type= type

    def pick_dir(self):
        self.rand_x = random.random()*2-1
        self.rand_y = random.random()*2-1


    def move(self, walls):
        if (self.enemyRect.x<=10 and self.rand_x<0) or (self.enemyRect.x>=790 and self.rand_x>0):
            self.rand_x*=-1
        if (self.enemyRect.y<=10 and self.rand_y<0) or (self.enemyRect.y>=740 and self.rand_y>0):
            self.rand_y*=-1

        self.enemyRect = self.enemyRect.move(self.rand_x * self.speed, self.rand_y * self.speed)

   

class FireEnemy(Enemy):
    def __init__(self, player, hp=100,speed=3,dmg_mult=1, x=250, y=100, w=50,h=50, atk_speed=1.5,  atk_opportunity = 0, move_opportunity = 0):
        Enemy.__init__(self,player,hp,speed,dmg_mult,x,y,w,h,atk_speed)
        self.type = "fire"

    def update_projectiles(self, screen, proj):
        for i in self.projectile_list:
            screen.blit(proj, (i.rect.x, i.rect.y))


            i.rect = i.rect.move(i.dir_x * i.speed, i.dir_y * i.speed)    
    def atk1(self):
        self.attacking=True
        proj = prj.Projectile(self, self.p_pos.playerRect.x, self.p_pos.playerRect.y)
        self.projectile_list.append(proj)
        self.attacking = False

    def atk2(self):
        self.attacking = True
        for i in range(3):
            rndNum = random.randint(-30, 30)
            proj = prj.Projectile(self, self.p_pos.playerRect.x, self.p_pos.playerRect.y, rndNum)
            self.projectile_list.append(proj)
        self.attacking = False    




class WaterEnemy(Enemy):
    def __init__(self, player, hp=100,speed=3,dmg_mult=1, x=250, y=100, w=50,h=50, atk_speed=0.5,  atk_opportunity = 0, move_opportunity = 0):
        Enemy.__init__(self,player,hp,speed,dmg_mult,x,y,w,h,atk_speed)
        self.type = "water"

    def update_projectiles(self, screen, proj):
        for i in self.projectile_list:
            if (i.rect.x>1000 or i.rect.x<-200 or i.rect.y>1000 or i.rect.y<-200):
                self.projectile_list.remove(i)
                
            screen.blit(proj, (i.rect.x, i.rect.y))
            i.rect = i.rect.move(i.dir_x * i.speed, i.dir_y * i.speed)       
    def atk1(self):
        self.attacking=True
        for i in range(12):
            proj = prj.Projectile(self, self.p_pos.playerRect.x, self.p_pos.playerRect.y)
            proj.dir_x = math.cos(30*i)
            proj.dir_y = math.sin(30*i)
            self.projectile_list.append(proj)
        self.attacking = False
    
    def atk2(self,screen, ink):
        
        self.attacking=True
        proy_h = 800

        if self.atk_clock == 1:
            print("jet start")
            self.enemyRect.y = 0 + random.randint(10,40)
            self.enemyRect.x = self.p_pos.playerRect.x
        
        if self.atk_clock<=120 and self.atk_clock>0:
            self.enemyRect.x = self.p_pos.playerRect.x

        if self.atk_clock==140:
            self.jet = prj.jet(self, self.p_pos.playerRect.x, self.p_pos.playerRect.y,0,25,20,30,0)
            self.projectile_list.append(self.jet)
            squirt = pygame.mixer.Sound("./music/squirt.mp3")
            squirt.play()


        if self.atk_clock >142 and self.atk_clock <200:
                    anim_rect = pygame.Rect(self.enemyRect.x,self.enemyRect.y+self.enemyRect.h, 50, 32)
                    self.jet.rect.h +=30
                    jet_surface = pygame.Surface((self.jet.rect.w,self.jet.rect.h))
                    jet_surface.fill((0,0,0))
                    screen.blit(jet_surface,(self.jet.rect.x,self.jet.rect.y))
                    screen.blit(ink, (self.jet.rect.x-12, self.jet.rect.y))


        if self.atk_clock>=200:

                print("jet end")
                self.attacking = False
                self.atk_clock = -1
                if self.jet in self.projectile_list:
                    self.projectile_list.remove(self.jet)


        self.atk_clock += 1
