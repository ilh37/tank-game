import pygame, sys, math
from pygame.locals import *

# Global constants
FPS = 60 # frames per second
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

# Color constants
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (204,204,0)

# Represents position of mouse (updated in mouseMotion)
MOUSE = [0,0]

# Display surface
DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Player tank
PLAYER_TANK = None

# List of other objects
GAME_OBJECTS = []

# Images to load
TURRET_IMG = pygame.image.load('turret.png')

# Game loop
def main():
    global PLAYER_TANK
    PLAYER_TANK = Tank()

    GAME_OBJECTS.append(Crate((700,500)))
    
    pygame.display.set_caption('Tanks!')
    pygame.init()
    draw()
    while True:
        # Handle all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                keyDown(event)
            elif event.type == pygame.MOUSEMOTION:
                mouseMotion(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
            draw()

# Handle user input
def keyDown(event):
    print('You pressed a key!')

# Update position of mouse
def mouseMotion(event):
    mouse_pos = pygame.mouse.get_pos()
    MOUSE[0] = mouse_pos[0]
    MOUSE[1] = mouse_pos[1]

def getTurretAngle():
    return math.degrees(math.atan2(MOUSE[0]-960,MOUSE[1]-540))

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def draw():
    DISPLAY_SURF.fill(WHITE)

    PLAYER_TANK.draw(DISPLAY_SURF)
    for obj in GAME_OBJECTS:
        obj.draw(DISPLAY_SURF)
    pygame.display.update()

class GameObject:
    def __init__(self, location):
        self.location = location # a pair of (x,y) coordinates
    
    def draw(self,display_surf):
        pass

class Projectile(GameObject):
    pass

class Weapon:
    pass

class Unit(GameObject):
    def __init__(self, location, hp, energy=0, armor=0, weapon = None):
        self.location = location
        self.hp = hp
        self.energy = energy
        self.weapons = weapon
        self.armor = 0
        self.is_dead = False

    def damage(self, amount, ignore_armor=False):
        if ignore_armor:
            self.hp -= amount
        else:
            self.hp -= (amount - self.armor)
        if self.hp <= 0:
            die()

    def die():
        self.is_dead = True

class Crate(Unit):
    def __init__(self,location):
        super().__init__(hp=50,location=location)

    def draw(self,display_surf):
        pygame.draw.circle(display_surf, YELLOW, self.location, 20)

class Tank(Unit):
    def __init__(self):
        super().__init__(location=(960,540), hp=100)
    
    def draw(self,display_surf):
        x = self.location[0]
        y = self.location[1]
        # Draw "base"
        pygame.draw.rect(DISPLAY_SURF, GREEN, (x-20,y-20,40,40))
        # Draw "shooter"
        shooter = TURRET_IMG
        DISPLAY_SURF.blit(rot_center(shooter,getTurretAngle()+180),(x-40,y-40))

if __name__ == '__main__':
    main()
