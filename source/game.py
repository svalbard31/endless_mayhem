from ship import Ship
from config import SCREEN_SIZEX,SCREEN_SIZEY, screen, font,shipimage,landingpad_group,astroid_group,shippostion
import pygame
borders = [SCREEN_SIZEX,SCREEN_SIZEY]

class Game:
    def __init__(self):
        ship = Ship(shipimage, shippostion[0], shippostion[1])
        objects_group = pygame.sprite.Group()
        self.ship = ship
        objects_group.add(ship)
        for astroid in astroid_group:
            objects_group.add(astroid)
        for landingpad in landingpad_group:
            objects_group.add(landingpad)
        self.astroid_group = astroid_group
        self.landingpad_group = landingpad_group
        self.objects_group = objects_group
        self.all_sprites = pygame.sprite.Group()
    def run(self):
        clock = pygame.time.Clock()
        run= True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            screen.fill((0, 0, 0))  # Clear screen each frame
            for astroid in self.astroid_group:
                if self.ship.rect.colliderect(astroid.rect):
                    if self.ship.pixel_perfect_collision(astroid):
                        self.ship.handle_collision(astroid)
            for landingpad in self.landingpad_group:
                if self.ship.rect.colliderect(landingpad.rect):
                 if self.ship.pixel_perfect_collision(landingpad):
                    self.ship.handle_landing(landingpad)
                    pass
            self.ship.update()
            if self.ship.destroyed:
                screen.fill((0, 0, 0))  # Clear screen
                timer = 0
                while timer < 120:  # Display "Ship Destroyed!" for 2 seconds
                    timer += 1
                    self.astroid_group.update()
                    self.astroid_group.draw(screen)
                    self.landingpad_group.draw(screen)
                    self.ship.draw(screen)
                    pygame.display.flip()

                self.ship = Ship(shipimage, shippostion[0], shippostion[1])  
                self.objects_group.add(self.ship)
            self.astroid_group.update()
            for bullet in self.ship.bullet_group:
                for object in self.objects_group:
                    if bullet.rect.colliderect(object.rect):
                        bullet.handle_collision(object)
            self.ship.draw(screen)
            dirty_rects = []
            dirty_rects.extend(self.ship.bullet_group.draw(screen))
            dirty_rects.extend(self.astroid_group.draw(screen))
            dirty_rects.extend(self.landingpad_group.draw(screen))
            pygame.display.flip()  # Full update to ensure text displays
            clock.tick(60)
game = Game()