import pygame as pygame
from abc import ABC, abstractmethod
from random import randint
from config import SCREEN_SIZEX, SCREEN_SIZEY,MIN_DISTANCE, objectplaceattempts

def distance_between(x1, y1, x2, y2):
    """Calculate Euclidean distance between two points"""
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

class Object(pygame.sprite.Sprite, ABC):
    def __init__(self, image, objects_group, name):
        super().__init__()
        self.name = name
        self.image = image
        self.rect = self.image.get_rect()

    @abstractmethod
    def draw(self, surface):
        pass
    def update(self, *args, **kwargs):
        pass

    def place(self, objects_group):
        placed = False
        attempts = 0
        while not placed and attempts < objectplaceattempts:  
            x = randint(30, SCREEN_SIZEX-200)
            y = randint(30, SCREEN_SIZEY-200)
            safe = True
            for object in objects_group:
                if distance_between(x, y, object.rect.centerx, object.rect.centery) < MIN_DISTANCE:
                    safe = False
                    break
            if safe:
                objects_group.add(self)
                placed = True
            attempts += 1

        if not placed:
            return False 
        if placed:
            self.rect.x = x
            self.rect.y = y
            return True



class landingpad(Object):
    def __init__(self, image_path, objects_group):
        super().__init__(image_path, objects_group, "landingpad")
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class astroid(Object):    
    def __init__(self, image, objects_group):
        super().__init__(image, objects_group, "astroid")
        self.image = image
        self.rect = self.image.get_rect()
    def draw(self, surface):
        surface.blit(self.image, self.rect) 


