from objects import Object
from config import screen,BASEBULLETSPEED
from copy import copy
from math import cos, sin, radians

import pygame
class Bullet(Object):
    '''Represents a bullet fired by a ship, handles movement, collision and drawing of the bullet.'''
    def __init__(self, image: pygame.Surface, x: float, y: float, angle: float, speed: list):
        super().__init__(image, "bullet")
        self.angle = angle
        self.speed = copy(speed)
        self.destroyed = False
        self.rotated_image = pygame.transform.rotate(self.image, self.angle + 90)
        self.pos = [x, y]
        self.place()
    def place(self):
        '''Add the bullet to the game and set its initial position.'''
        self.rect = self.rotated_image.get_rect()
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
    def update(self):
        '''Update the bullet's position based on its speed and angle.'''
        speed = self.speed
        self.rect.x += (abs(speed[0])+BASEBULLETSPEED ) * cos(radians(self.angle))
        self.rect.y -= (abs(speed[1])+BASEBULLETSPEED) * sin(radians(self.angle))  
    def pixel_perfect_collision(self, other: Object):
        '''Check for pixel-perfect collision with another object.'''
        return pygame.sprite.collide_mask(self, other)  
    def handle_collision(self, other: Object):
        ''' Handles collision, destroys the bullet, if its a non destroyed ship, destroy it and return 1, return 0'''
        if other.name == "ship":
                if other.destroyed:
                        return 0
                other.destroy()  
                self.kill()
                return 1 
        if self.pixel_perfect_collision(other):
            self.kill()  # Remove bullet from game
            self.destroyed = True
            return 0
    def draw(self, surface: pygame.Surface):
        '''Draw the bullet on the surface.'''
        if not self.destroyed:
            surface.blit(self.rotated_image, self.rect)