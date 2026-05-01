import pygame 
from random import randint
import os



#Game Settings
SCREEN_SIZEX = 2000
SCREEN_SIZEY = 2000 
STARTFUEL = 100
GRAVITY = 0.3
THRUSTPOWER = 0.7
FULLTANK = 2000
BASEBULLETSPEED = 20
TURNSPEED = 2
ASTROIDNUM =6

#Control Schemes
WASD_E = 1  # WASD and E
ARROW_RSHIFT = 2  # Arrow keys and Right Shift



#Setup
objectplaceattempts = 10000
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZEX, SCREEN_SIZEY))
font = pygame.font.SysFont(None, 36)
bigfont = pygame.font.SysFont(None, 72)


#Images 
image_dir = os.path.join(os.path.dirname(__file__), "..", "images")
shipimage = pygame.image.load(os.path.join(image_dir, "ship.png"))  
ship2image = pygame.image.load(os.path.join(image_dir, "starbarge.png"))
astroid_image = pygame.image.load(os.path.join(image_dir, "astro.png"))
landingpad_image = pygame.image.load(os.path.join(image_dir, "landingpad.png"))
explosion_image = pygame.image.load(os.path.join(image_dir, "explosion.png"))
bullet_image = pygame.image.load(os.path.join(image_dir, "bullet.png"))


# Cache asteroid image for efficiency
MIN_DISTANCE = 400
MIN_DISTANCE_LANDINGPAD = 500


