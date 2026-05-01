import pygame
from math import cos, sin, radians,sqrt
from objects import Object
from bullet import Bullet
from config import SCREEN_SIZEX,SCREEN_SIZEY, GRAVITY, THRUSTPOWER, FULLTANK,font,TURNSPEED,explosion_image,WASD_E,ARROW_RSHIFT,bullet_image
from player import Player

X = 0
Y = 1

borders = [SCREEN_SIZEX,SCREEN_SIZEY]   
class Ship(Object):
    '''Represents a player controlled ship
    Handles movement, shooting, collision and drawing of the ship.
    as well as the player's score and fuel.'''
    def __init__(self, image: pygame.Surface, objects_group: pygame.sprite.Group, player: Player, control_scheme=1):
        
        super().__init__(image, "ship")
        self.angle = 90
        self.pos = [float(self.rect.x), float(self.rect.y)]
        self.image_angle_offset = -90
        self.speed = [0, 0]
        self.acceleration = [0, 0]
        self.thrust_power = THRUSTPOWER
        self.drag = 0.95
        self.max_speed = 12
        self.grounded = False
        self.turnspeed = TURNSPEED
        self.destroyed = False
        self.fuel = FULLTANK
        self.landed = False
        self.bullet_group = pygame.sprite.RenderUpdates()   
        self.reload_time = 10
        self.control_scheme = control_scheme
        self.destroyed_timer = 120
        self.destroy_image = explosion_image
        self.objects_group = objects_group
        self.player = player

    def thrust(self):
        '''Apply thrust in the direction the ship is currently facing, consuming fuel.'''
        self.fuel -= 2
        self.landed = False
        heading = self.angle
        thrustx = self.thrust_power * cos(radians(heading))
        thrusty = -self.thrust_power * sin(radians(heading))  # Negate for pygame Y-axis (down is positive)
        self.acceleration[0] += thrustx
        self.acceleration[1] += thrusty 
    
    def gravity(self):
        '''Apply gravity'''
        self.acceleration[1] += GRAVITY

    def turnleft(self):
        '''Turn the ship left, consuming fuel.'''
        self.angle += self.turnspeed
        self.fuel -= 1
        if self.angle > 360:
            diff = self.angle - 360
            self.angle = 0 + diff

    def turnright(self):
        '''Turn the ship right, consuming fuel.'''
        self.angle -= self.turnspeed
        self.fuel -= 1
        if self.angle < 0:
            self.angle = 360 + self.angle
    
    def shoot(self):
        '''Fire a bullet, if the reload time has passed'''
        if self.reload_time > 0:
            return
        self.reload_time = 10
        bullet = Bullet(bullet_image, self.rect.centerx+100*cos(radians(self.angle)), self.rect.centery-100*sin(radians(self.angle)), self.angle,self.speed)
        self.bullet_group.add(bullet)
    
    def clamp(self): 
        '''Manage collisions with the borders of the game world, applying bounce'''
        if self.rect.x <= 0:
            self.rect.x = 0
            if self.speed[X] < 0:
                self.bounce(X, 1)
        if self.rect.x >= borders[0] - self.rect.width:
            self.rect.x = borders[0] - self.rect.width
            if self.speed[X] > 0:
                self.bounce(X, -1)
        if self.rect.y <= 0:    
            self.rect.y = 0
            if self.speed[Y] < 0:
                self.bounce(Y, 1 )
        if self.rect.y >= borders[1] - self.rect.height:
            self.grounded = True
            if self.speed[Y] > 0:
               self.bounce(Y, -1)  
        else:
            self.grounded = False
        if self.grounded:
            self.speed[X] *= self.drag
            if abs(self.speed[X]) < 0.1:
                self.speed[X] = 0
        
    def handle_landing(self, landingpad):
        '''Handle lands on the landing pad'''
        #Debuggin to check what is wrong with a landing 
        angle_delta = (self.angle - 90) % 360            
        can_land = (
            self.rect.y <= (landingpad.rect.y + 80)
            and abs(self.speed[X]) < 10
            and abs(self.speed[Y]) < 20
            and (angle_delta < 30 or angle_delta >= 330)
        )
        if can_land:
                self.landed = True
                self.speed[X] *=self.drag
                self.fuel = FULLTANK  # Refuel on landing
                if self.speed[Y] > 0:
                    self.speed[Y] = 0

        else:
            self.speed = [0, 0]
            self.destroy()

    def destroy(self):
        '''Destroy the ship if not alrea destroyed'''
        if not self.destroyed:
            self.player.add_score(-1)
            self.angle = 90
            self.speed = [0, 0]
            self.acceleration = [0, 0]
            self.fuel = FULLTANK
            self.destroyed = True

    def update(self):
        '''Update the ship, and bulllets fired by the ship. 
        Handles input and applies movement'''
        # Cool down shooting so holding shoot works at a fixed fire rate.
        if self.reload_time > 0:
            self.reload_time -= 1
        self.clamp()

        for bullet in self.bullet_group:
            bullet.update()
            if bullet.rect.x < 0 or bullet.rect.x > borders[0] or bullet.rect.y < 0 or bullet.rect.y > borders[1]:
                bullet.kill()  # Remove bullet if it goes off-screen
        if self.destroyed:
            if self.destroyed_timer >= 0:  # After displaying "Ship Destroyed!" for 2 seconds, reset the ship
                self.destroyed_timer -= 1
                return
            else:
                self.place(self.objects_group)  # Re-place the ship in the game
                self.destroyed_timer = 120
                self.destroyed = False
        # Get input
        keys = pygame.key.get_pressed()
        if self.fuel <= 0:
            self.fuel = 0
        else:
            # Handle rotation and thrust
            if self.control_scheme == WASD_E:
                if not self.landed:
                    if keys[pygame.K_a]:
                        self.turnleft()
                    if keys[pygame.K_d]:
                        self.turnright()
                if keys[pygame.K_w]:
                    self.thrust()
                if keys[pygame.K_e]:
                    self.shoot()
            elif self.control_scheme == ARROW_RSHIFT:
                if not self.landed:
                    if keys[pygame.K_LEFT]:
                        self.turnleft()
                    if keys[pygame.K_RIGHT]:
                        self.turnright()
                if keys[pygame.K_UP]:
                    self.thrust()
                if keys[pygame.K_RSHIFT]:
                    self.shoot()

        self.gravity()

        self.speed[0] += self.acceleration[0]
        self.speed[1] += self.acceleration[1]
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        

        # Apply boundaries
        self.pos[0] = float(self.rect.x)
        self.pos[1] = float(self.rect.y)

        # Forces are re-applied every frame; do not carry acceleration over.
        self.acceleration[0] = 0
        self.acceleration[1] = 0

    def bounce(self,Axis,direction,AXIS2=None,DIRECTION2=None):
        '''Bounces off an object, directions is roughly in the direction the collision.'''
        if AXIS2 and DIRECTION2:
            if AXIS2 == X:
                if self.speed[0] > 0.1 or self.speed[0] < -0.1:
                    self.speed[0] *= DIRECTION2 * 0.4  # Damping factor
                    self.rect.x -= self.speed[0]
            elif AXIS2 == Y:
                if self.speed[1] > 0.1 or self.speed[1] < -0.1:
                    self.speed[1] *= DIRECTION2 * 0.4  # Damping factor
                    self.rect.y += self.speed[1]
        if Axis == X:
            if self.speed[0] > 0.1 or self.speed[0] < -0.1:
                self.speed[0] *= direction * 0.4  # Damping factor
                self.rect.x -= self.speed[0]
        elif Axis == Y:
            if self.speed[1] > 0.1 or self.speed[1] < -0.1:
                self.speed[1] *= direction * 0.4  # Damping factor
                self.rect.y += self.speed[1]

    def pixel_perfect_collision(self, other):
        '''Check for pixel-perfect collision with another object.'''
        return pygame.sprite.collide_mask(self, other) 
     
    def handle_collision(self, other):
        '''Stops the ship from moving through objects, if the object is not a landing pad destroy the ship'''
        if not self.destroyed:
            
            if other.name == "landingpad":
                self.handle_landing(other)
            else:  
                self.speed = [0, 0] 
                self.destroy()

    def fuel_text(self):
        '''Return the fuel text to be displayed on the screen.'''
        return f"Fuel: {self.fuel}"
    
    def score_text(self):     
        '''Return the score text to be displayed on the screen.'''   
        return f"Score: {self.player.get_score()}"
    def speed_text(self):
        '''Return the speed text to be displayed on the screen.'''
        speed = sqrt(self.speed[X]**2 + self.speed[Y]**2)
        return f"Speedx: {int(self.speed[X])} Speedy: {int(self.speed[Y])} Total: {int(speed)}"

    def draw(self, surface):
        '''Displays the ship and associated text on the screen. 
        If ships is destoryed, displays and explosion instead.'''
        text = False
        text_fuel = font.render(self.fuel_text(), True, (255, 0, 0))
        text_score = font.render(self.score_text(), True, (255, 0, 0))
        text_speed = font.render(self.speed_text(), True, (255, 0, 0))
        if self.destroyed:
            surface.blit(self.destroy_image, self.rect)  
            return 
        if self.player.get_name() == "Player 1":
            surface.blit(text_fuel, (10, 10))
            surface.blit(text_score, (10, 40))
            surface.blit(text_speed, (10, 70))
        else:
            surface.blit(text_fuel, (SCREEN_SIZEX-text_fuel.get_width()-10,10))
            surface.blit(text_score, (SCREEN_SIZEX-text_score.get_width()-10,40))
            surface.blit(text_speed, (SCREEN_SIZEX-text_speed.get_width()-10,70))
        for bullet in self.bullet_group:
            if not bullet.destroyed:
                bullet.draw(surface)
        draw_angle = self.angle + self.image_angle_offset
        rotated_image = pygame.transform.rotate(self.image, draw_angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, rotated_rect)

         