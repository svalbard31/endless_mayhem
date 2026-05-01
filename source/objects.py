import pygame as pygame
from abc import ABC, abstractmethod
from random import randint
from config import SCREEN_SIZEX, SCREEN_SIZEY,MIN_DISTANCE, objectplaceattempts

def distance_between(x1, y1, x2, y2):
    """Calculate Euclidean distance between two points"""
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

class Object(pygame.sprite.Sprite, ABC):
    '''Base class for all game objects, handles basic properties and placement logic.'''
    def __init__(self, image: pygame.Surface, name: str):
        super().__init__()
        self.name = name
        self.image = image
        self.rect = self.image.get_rect()
    def draw(self, surface: pygame.Surface):
        '''Draw the object on the surface.'''
        surface.blit(self.image, self.rect)

    def place(self, objects_group: pygame.sprite.Group):
        '''
        Adds object to the game world, 
        Tries to find a postion, that works through random guessing, it fails after a certain number of attempts
        '''
        placed = False
        attempts = 0
        while not placed and attempts < objectplaceattempts:  
            x = randint(200, SCREEN_SIZEX-200)
            y = randint(200, SCREEN_SIZEY-200)
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
    '''Represents the landing pad, handles drawing of the landing pad.'''
    def __init__(self, image: pygame.Surface):
        super().__init__(image, "landingpad")

class astroid(Object):  
    '''Represents an asteroid, handles drawing of the asteroid.'''  
    def __init__(self, image: pygame.Surface):
        super().__init__(image, "astroid")
        self.image = image
        self.rect = self.image.get_rect()


