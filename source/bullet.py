from objects import Object
from config import screen,BASEBULLETSPEED
from copy import copy
from math import cos, sin, radians

import pygame
class Bullet(Object):
    def __init__(self, image_path, x, y,angle,speed):
        super().__init__(image_path, x, y, "bullet")
        self.angle = angle
        self.speed = copy(speed)
        self.destroyed = False
        self.rotated_image = pygame.transform.rotate(self.image, self.angle + 90)
    def update(self):
        speed = self.speed
        self.rect.x += (abs(speed[0])+BASEBULLETSPEED )* cos(radians(self.angle))
        self.rect.y -= (abs(speed[1])+BASEBULLETSPEED) * sin(radians(self.angle))  
    def pixel_perfect_collision(self, other):
        return pygame.sprite.collide_mask(self, other)  
    def handle_collision(self, other):
        self.kill()  # Remove bullet from game
        self.destroyed = True
        if other.name == "ship":
                other.destroy()  
    def draw(self, surface):
        if not self.destroyed:
            surface.blit(self.rotated_image, self.rect)