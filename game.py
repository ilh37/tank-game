import pygame, sys, math, time
from pygame.locals import *

# Global constants
FPS = 30 # frames per second
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

# Color constants
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (204,204,0)
BLACK = (0,0,0)

# Represents position of mouse (updated in mouseMotion)
MOUSE = [0,0]

# Display surface
DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Player tank
PLAYER_TANK = None

# List of other objects
GAME_OBJECTS = []

# List of objects to be spawned
SPAWN_GAME_OBJECTS = []

# All movement is reduced by this factor so that speeds can be stored exactly as
# ints but units move at reasonable speeds
SPEED_FACTOR = 0.2

# Game loop
def main():
    global PLAYER_TANK
    PLAYER_TANK = Tank()

    GAME_OBJECTS.append(Crate((700,500)))

    fpsClock = pygame.time.Clock()
    
    pygame.display.set_caption('Tanks!')
    pygame.init()
    draw()
    while True:
        # Handle all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mouseMotion(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseClick(event)
        keyPress()
        update()
        draw()
        fpsClock.tick(round(1000/FPS))

# Handle user input
def keyPress():
    keys = pygame.key.get_pressed()
    if(keys[pygame.K_d]):
        PLAYER_TANK.moveX(5)
    elif(keys[pygame.K_a]):
        PLAYER_TANK.moveX(-5)
    elif(keys[pygame.K_w]):
        PLAYER_TANK.moveY(-5)
    elif(keys[pygame.K_s]):
        PLAYER_TANK.moveY(5)

# Update position of mouse
def mouseMotion(event):
    mouse_pos = pygame.mouse.get_pos()
    MOUSE[0] = mouse_pos[0]
    MOUSE[1] = mouse_pos[1]

def mouseClick(event):
    PLAYER_TANK.shoot()

# Main method that updates the state of all objects
def update():
    PLAYER_TANK.update()
    for obj in GAME_OBJECTS:
        obj.update()
    GAME_OBJECTS.extend(SPAWN_GAME_OBJECTS)
    SPAWN_GAME_OBJECTS.clear()

# Main method that draws all objects
def draw():
    DISPLAY_SURF.fill(WHITE)
    PLAYER_TANK.draw(DISPLAY_SURF)
    
    for obj in GAME_OBJECTS:
        obj.draw(DISPLAY_SURF)
    pygame.display.update()

# Creates a new object
def spawn(obj):
    SPAWN_GAME_OBJECTS.append(obj)

# Utility functions
def time_ms():
    return int(round(time.time() * 1000))

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def clip(value,min_value,max_value):
    return max(min(value, max_value), min_value)

class GameObject:
    def __init__(self, location):
        self.location = location # a tuple of (x,y) coordinates
    
    def draw(self,display_surf):
        pass

    def update(self):
        pass

    def getLocation(self):
        return (round(self.location[0]),round(self.location[1]))

class Weapon:
    def __init__(self,parent):
        self.parent = parent

    def update(self):
        pass

    def getTurretAngle(self):
        return math.degrees(math.atan2(MOUSE[0]-self.parent.location[0],MOUSE[1]-self.parent.location[1]))

    def shoot(self):
        pass

# Turret image
TURRET_IMG = pygame.image.load('turret.png')

class Minigun(Weapon):
    def draw(self, display_surf):
        x = self.parent.location[0]
        y = self.parent.location[1]
        shooter = TURRET_IMG
        DISPLAY_SURF.blit(rot_center(shooter,self.getTurretAngle()),(x-40,y-40))

    def shoot(self):
        spawn(Bullet(self.parent.location,self.getTurretAngle()))

class Projectile(GameObject):
    def __init__(self, location, speed, angle, duration):
        self.location = location
        self.speed = speed
        self.angle = angle
        self.duration = duration
        self.spawnTime = 0 # FILL IN LATER
        
    def update(self):
        x = self.location[0]
        y = self.location[1]
        dx = SPEED_FACTOR * self.speed * math.sin(math.radians(self.angle))
        dy = SPEED_FACTOR * self.speed * math.cos(math.radians(self.angle))
        self.location = (x+dx,y+dy)

class Bullet(Projectile):
    def __init__(self, location, angle):
        super().__init__(location=location,speed=1,angle=angle,duration=1000)

    def draw(self,display_surf):
        pygame.draw.circle(display_surf,BLACK,self.getLocation(),5)
        

class Unit(GameObject):
    def __init__(self, location, hp, energy=0, armor=0, weapon = None):
        self.location = location
        self.hp = hp
        self.energy = energy
        self.weapon = weapon
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
        super().__init__(location=(960,540), hp=100, weapon=Minigun(self))
        self.dx = 0
        self.dy = 0
        self.maxSpeed = 10
    
    def draw(self,display_surf):
        x = self.location[0]
        y = self.location[1]
        # Draw "base"
        pygame.draw.rect(display_surf, GREEN, (x-20,y-20,40,40))
        # Draw "shooter"
        self.weapon.draw(display_surf)

    def update(self):
        self.weapon.update()
        
        x = self.location[0]
        y = self.location[1]
        self.location = (x+(self.dx*SPEED_FACTOR),y+(self.dy*SPEED_FACTOR))
        if self.dx > 0:
            self.dx -= 2
            self.dx = clip(self.dx,-self.maxSpeed,self.maxSpeed)
        elif self.dx < 0:
            self.dx += 2
            self.dx = clip(self.dx,-self.maxSpeed,self.maxSpeed)
        if self.dy > 0:
            self.dy -= 2
            self.dy = clip(self.dy,-self.maxSpeed,self.maxSpeed)
        elif self.dy < 0:
            self.dy += 2
            self.dy = clip(self.dy,-self.maxSpeed,self.maxSpeed)

    def moveX(self,amount):
        self.dx += amount

    def moveY(self,amount):
        self.dy += amount

    def shoot(self):
        self.weapon.shoot()

if __name__ == '__main__':
    main()
