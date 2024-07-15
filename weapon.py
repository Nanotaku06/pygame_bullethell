import pygame
import math
import projectile as prj

class Weapon:
    def __init__(self, player, range_x=20, range_y = 40, base_dmg = 1, base_speed = 0):
        self.projectile_list = []
        self.base_dmg = base_dmg
        self.base_speed = base_speed
        self.player = player
        self.range_x = range_x
        self.range_y = range_y
        self.weaponRect = pygame.Rect(player.playerRect.x, player.playerRect.y, range_x, range_y)
        self.w_surface = pygame.Surface((self.weaponRect.w, self.weaponRect.h))
        self.w_surface.fill(color=(0, 100, 0))

    def shoot(self, mouse_pos):
        x_value = mouse_pos[0]
        y_value = mouse_pos[1]

        proj = prj.playerProjectile(self, x_value, y_value)
        self.projectile_list.append(proj)

    def update_projectiles(self, screen, proj):
        for i in self.projectile_list:
            screen.blit(proj, (i.rect.x, i.rect.y))

            i.rect = i.rect.move(i.dir_x * i.speed, i.dir_y * i.speed)

    def update_weapon(self, screen, cursor_pos, sprite):
        x_value = cursor_pos[0]
        y_value = cursor_pos[1]

        ad = y_value - self.weaponRect.y
        op = x_value - self.weaponRect.x
        hipo = math.sqrt(ad*ad+op*op)

        sprite = pygame.transform.rotate(sprite,-math.degrees(math.asin(op/hipo)))
        screen.blit(sprite, (((self.player.playerRect.x + self.player.playerRect.w/2  - self.weaponRect.w + op*50/800)), ((self.player.playerRect.y + self.player.playerRect.w/2 -self.weaponRect.h + ad*50/800))))











class MeleeWeapon(Weapon):
    def __init__(self,player, range_x=20, range_y = 40, base_dmg = 1, base_speed = 0):
        Weapon.__init__(player, base_dmg, base_speed)
        self.player = player
        self.range_x = range_x
        self.range_y = range_y
        self.weaponRect = pygame.Rect(player.playerRect.x, player.playerRect.y, range_x, range_y)



