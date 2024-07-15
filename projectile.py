import math
import pygame
import enemy_class as en

class Projectile:
    def __init__(self,enemyOrigin, p_pos_x, p_pos_y,offset=0, w=16,h=16,base_dmg=10, speed=5, rect=pygame.Rect(10,10,0,0)):
        self.w = w
        self.h = h
        self.base_dmg = base_dmg
        self.speed = speed
        self.rect = pygame.Rect(enemyOrigin.enemyRect.x,enemyOrigin.enemyRect.y,w,h)
        self.offset = offset

        ad = p_pos_x - self.rect.x
        op = p_pos_y - self.rect.y

        hipo = math.sqrt(math.pow(op, 2) + math.pow(ad, 2))

        sin = op / hipo
        cos = ad / hipo

        self.dir_x = math.cos(math.acos(cos) + math.radians(offset))
        self.dir_y = math.sin(math.asin(sin) + math.radians(offset))


class playerProjectile(Projectile):
    def __init__(self, weaponOrigin, p_pos_x, p_pos_y, offset=0, w=16, h=16, base_dmg=10, speed=10,rect=pygame.Rect(10, 10, 0, 0)):
        self.w = w
        self.h = h
        self.base_dmg = base_dmg
        self.speed = speed
        self.rect = pygame.Rect(weaponOrigin.weaponRect.x, weaponOrigin.weaponRect.y, w, h)
        self.offset = offset

        ad = p_pos_x - self.rect.x
        op = p_pos_y - self.rect.y

        hipo = math.sqrt(math.pow(op, 2) + math.pow(ad, 2))

        sin = op / hipo
        cos = ad / hipo

        self.dir_x = math.cos(math.acos(cos) + offset)
        self.dir_y = math.sin(math.asin(sin) + offset)

class jet(Projectile):
    def __init__(self,enemyOrigin, p_pos_x, p_pos_y,offset=0, w=10,h=10,base_dmg=10, speed=5, rect=pygame.Rect(10,10,0,0)):
        self.w = w

        self.base_dmg = base_dmg
        self.speed = speed
        self.offset = offset
        self.dir_x = 0
        self.dir_y = 0
        self.rect = pygame.Rect(enemyOrigin.enemyRect.x-(self.w/2) + enemyOrigin.enemyRect.w/2,enemyOrigin.enemyRect.y + enemyOrigin.enemyRect.h,w,h)