import pygame
from math import cos, sin, radians,sqrt
from objects import Object
from bullet import Bullet
from config import SCREEN_SIZEX,SCREEN_SIZEY, GRAVITY, THRUSTPOWER, FULLTANK,font,TURNSPEED,explosion_image
borders = [SCREEN_SIZEX,SCREEN_SIZEY]   
class Ship(Object):
    def __init__(self, image, x, y):
        super().__init__(image, x, y, "ship")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = [float(x), float(y)]
        self.angle = 90
        self.image_angle_offset = -90
        self.speed = [0, 0]
        self.acceleration = [0, 0]
        self.thrust_power = THRUSTPOWER
        self.drag = 0.96
        self.max_speed = 12
        self.grounded = False
        self.turnspeed = TURNSPEED
        self.destroyed = False
        self.fuel = FULLTANK
        self.landed = False
        self.bullet_group = pygame.sprite.RenderUpdates()   
        self.reload_time = 10
    
    def thrust(self):
        heading = self.angle
        thrustx = self.thrust_power * cos(radians(heading))
        thrusty = -self.thrust_power * sin(radians(heading))  # Negate for pygame Y-axis (down is positive)
        self.acceleration[0] += thrustx
        self.acceleration[1] += thrusty 
    
    def gravity(self):
        self.acceleration[1] += GRAVITY

    def turnleft(self):
        self.angle += self.turnspeed
        if self.angle > 360:
            diff = self.angle - 360
            self.angle = 0 + diff

    def turnright(self):
        self.angle -= 3
        if self.angle < 0:
            self.angle = 360 + self.angle
    
    def shoot(self):
        bullet = Bullet("bullet.png", self.rect.centerx+100*cos(radians(self.angle)), self.rect.centery-100*sin(radians(self.angle)), self.angle,self.speed)
        self.bullet_group.add(bullet)
    
    def clamp(self): 
        #This is managing the borders it also applys friction on the sides. 
        if self.rect.x <= 0:
            self.rect.x = 0
            if self.speed[0] < 0:
                self.speed[0] = 0
                self.speed[1] = 0
            if self.acceleration[0] < 0:
                self.acceleration[0] = 0
                self.acceleration[1] = 0
        if self.rect.x >= borders[0] - self.rect.width:
            self.rect.x = borders[0] - self.rect.width
            if self.speed[0] > 0:
                self.speed[0] = 0
            if self.acceleration[0] > 0:
                self.acceleration[0] = 0
        if self.rect.y <= 0:
            self.rect.y = 0
            if self.speed[1] < 0:
                self.speed[1] = 0
            if self.acceleration[1] < 0:
                self.acceleration[1] = 0
        if self.rect.y >= borders[1] - self.rect.height:
            self.grounded = True
            self.rect.y = borders[1] - self.rect.height
            if self.speed[1] > 0:
                self.speed[1] = 0
            if self.acceleration[1] > 0:
                self.acceleration[1] = 0
        else:
            self.grounded = False
        if self.grounded:
            self.speed[0] *= self.drag
            if abs(self.speed[0]) < 0.1:
                self.speed[0] = 0
        
    def handle_landing(self, landingpad):
        self.handle_collision(landingpad)  # Handle collision response first
        if self.rect.colliderect(landingpad.rect):
            # Check if landing conditions are met (e.g., low speed, correct angle)
            if self.rect.y <= landingpad.rect.y-0.1 and abs(self.speed[0]) < 1 and abs(self.speed[1]) < 1 and ((self.angle - 90) % 360 < 30 or (self.angle - 90) % 360 > 340):
                self.landed = True
                self.fuel = FULLTANK  # Refuel on landing
            else:
                self.destroy()
    def destroy(self):
        self.destroyed = True
        self.image = explosion_image
        self.rect = self.image.get_rect(center=self.rect.center)
    def update(self):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global run
                run = False

        for bullet in self.bullet_group:
            bullet.update()
            if bullet.rect.x < 0 or bullet.rect.x > borders[0] or bullet.rect.y < 0 or bullet.rect.y > borders[1]:
                bullet.kill()  # Remove bullet if it goes off-screen
        if self.destroyed:
            return
        # Get input
        keys = pygame.key.get_pressed()
        if self.fuel <= 0:
            self.fuel = 0
        else:
            # Handle rotation and thrust
            if not self.landed:
                if keys[pygame.K_LEFT]:
                    self.turnleft()
                    self.fuel -= 1
    
                if keys[pygame.K_RIGHT]:
                    self.turnright()
                    self.fuel -= 1  
            if self.reload_time > 0:
                self.reload_time -= 1

            if keys[pygame.K_SPACE]:
                if self.reload_time <= 0:
                    self.shoot()
                    self.reload_time = 10  # Reset reload time
            if keys[pygame.K_UP]:
                self.thrust()
                self.landed = False
                self.fuel -= 2  

        
        self.gravity()

        self.speed[0] += self.acceleration[0]
        self.speed[1] += self.acceleration[1]
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        
        self.clamp()

        # Apply boundaries
        self.pos[0] = float(self.rect.x)
        self.pos[1] = float(self.rect.y)
        
        # Reset acceleration each frame (gravity will reapply)
        self.acceleration[0] = 0
        self.acceleration[1] = 0

    def pixel_perfect_collision(self, other):
        return pygame.sprite.collide_mask(self, other)  
    def handle_collision(self, other):
        if other.name == "astroid":
            self.destroy()
        if self.rect.colliderect(other.rect):
            # Push ship away
            self.rect.x -= self.speed[0]
            self.rect.y -= self.speed[1]
            # Reverse velocity
            self.speed[0] *= -0.01 # Damping factor
            self.speed[1] *= -0.01

    def draw(self, surface):
        text = False
        if self.fuel <= 1000:
            text = font.render(f"Fuel: {self.fuel}", True, (255, 0, 0))
        if self.destroyed:
            text = font.render("Ship Destroyed!", True, (255, 0, 0))
        if text:
            surface.blit(text, (10, 10))
        for bullet in self.bullet_group:
            if not bullet.destroyed:
                bullet.draw(surface)
        draw_angle = self.angle + self.image_angle_offset
        rotated_image = pygame.transform.rotate(self.image, draw_angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, rotated_rect)

         