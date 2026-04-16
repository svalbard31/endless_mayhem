import pygame 
from objects import astroid,landingpad
from random import randint
import os




SCREEN_SIZEX = 2000
SCREEN_SIZEY = 2000 
STARTFUEL = 100
GRAVITY = 0.2
THRUSTPOWER = 0.7
FULLTANK = 2000
BASEBULLETSPEED = 16
TURNSPEED = 3
ASTROIDNUM = 5

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZEX, SCREEN_SIZEY))
font = pygame.font.SysFont(None, 36)


#Images 
image_dir = os.path.join(os.path.dirname(__file__), "..", "images")
shipimage = pygame.image.load(os.path.join(image_dir, "ship.png"))  
astroid_image = pygame.image.load(os.path.join(image_dir, "astro.png"))
landingpad_image = pygame.image.load(os.path.join(image_dir, "landingpad.png"))
explosion_image = pygame.image.load(os.path.join(image_dir, "explosion.png"))



# Cache asteroid image for efficiency
MIN_DISTANCE = 400
MIN_DISTANCE_LANDINGPAD = 500


def distance_between(x1, y1, x2, y2):
    """Calculate Euclidean distance between two points"""
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

# Place the landing pad
landingpadrect = landingpad_image.get_rect()
landingpad1 = landingpad(landingpad_image, SCREEN_SIZEX//2-landingpadrect.width//2, SCREEN_SIZEY//2-landingpadrect.height//2)
landingpad_group = pygame.sprite.RenderUpdates()
landingpad_group.add(landingpad1)
astroid_group = pygame.sprite.RenderUpdates()


for _ in range(ASTROIDNUM):
    placed = False
    attempts = 0
    while not placed and attempts < 50:  # Max 50 attempts per asteroid
        x = randint(30, SCREEN_SIZEX-200)
        y = randint(30, SCREEN_SIZEY-200)
        attempts += 1
        
        # Check distance to landing pad
        if distance_between(x, y, landingpad1.rect.centerx, landingpad1.rect.centery) < MIN_DISTANCE_LANDINGPAD:
            continue
        
        # Check distance to other asteroids
        safe = True
        for astro in astroid_group:
            if distance_between(x, y, astro.rect.centerx, astro.rect.centery) < MIN_DISTANCE:
                safe = False
                break
        
        if safe:
            astroid_group.add(astroid(astroid_image, x, y))
            placed = True

shippostion = (SCREEN_SIZEX//4, SCREEN_SIZEY//4)
# Find safe ship position
placed = False
attempts = 0

while not placed and attempts < 50:
    attempts += 1
    # Check distance to landing pad
    if distance_between(shippostion[0], shippostion[1], landingpad1.rect.centerx, landingpad1.rect.centery) >= MIN_DISTANCE:
        # Check distance to all asteroids
        safe = True
        for astro in astroid_group:
            if distance_between(shippostion[0], shippostion[1], astro.rect.centerx, astro.rect.centery) < MIN_DISTANCE:
                safe = False
                break
        
        if safe:
            placed = True
            break
    
    # Try new position
    shippostion = (randint(30, SCREEN_SIZEX-200), randint(30, SCREEN_SIZEY-200))


