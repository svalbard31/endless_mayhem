import pygame as pygame
from abc import ABC, abstractmethod
class Object(pygame.sprite.Sprite, ABC):
    def __init__(self, image, x, y,name):
        super().__init__()
        self.name = name
        if image is not None:
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        else:
            # Placeholder for subclasses that load images differently
            self.image = None
            self.rect = None
    @abstractmethod
    def draw(self, surface):
        pass
    def update(self, *args, **kwargs):
        pass

class landingpad(Object):
    def __init__(self, image_path, x, y):
        super().__init__(image_path, x, y,"landingpad")
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class astroid(Object):    
    def __init__(self, image, x, y):
        super().__init__(None, x, y,"astroid")
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self, surface):
        surface.blit(self.image, self.rect) 


