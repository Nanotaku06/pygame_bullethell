import math

import pygame

class Player:
    def __init__(self, hp=100, speed=3, dmg_mult=1, x=250, y=250, w=50,h=50, atk_speed=1):
        self.hp = hp
        self.speed = speed
        self.dmg_mult = dmg_mult
        self.playerRect = pygame.Rect(x, y, w, h)
        self.atk_speed = atk_speed
        self.p_surface = pygame.Surface((self.playerRect.w, self.playerRect.h))
        self.p_surface.fill(color=(255, 0, 0))


