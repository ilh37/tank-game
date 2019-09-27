import pygame, sys, math, time, random
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
    PLAYER_TANK = PlayerTank((960,540))

    GAME_OBJECTS.append(Crate((700,500)))
    GAME_OBJECTS.append(Crate((800,400)))
    GAME_OBJECTS.append(DummyTank((600,300)))

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
                mouseButton(event)
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

def mouseButton(event):
    # Left mouse button
    if event.button == 1:
        PLAYER_TANK.shoot()

# Main method that updates the state of all objects
def update():
    global GAME_OBJECTS
    
    # Update all objects
    if not PLAYER_TANK.is_dead:
        PLAYER_TANK.update()
    for obj in GAME_OBJECTS:
        obj.update()

    if PLAYER_TANK.is_dead:
        all_objects = GAME_OBJECTS
    else:
        all_objects = GAME_OBJECTS + [PLAYER_TANK]
    # Deal with collisions
    for obj1 in all_objects:
        for obj2 in all_objects:
            if obj1 != obj2 and colliding(obj1,obj2):
                obj1.on_collide(obj2)
    
    # Clean up dead objects and add new objects
    GAME_OBJECTS = list(filter(lambda x: not x.is_dead, GAME_OBJECTS))
    GAME_OBJECTS.extend(SPAWN_GAME_OBJECTS)
    SPAWN_GAME_OBJECTS.clear()

# Main method that draws all objects
def draw():
    DISPLAY_SURF.fill(WHITE)
    if not PLAYER_TANK.is_dead:
        PLAYER_TANK.draw(DISPLAY_SURF)
    
    for obj in GAME_OBJECTS:
        obj.draw(DISPLAY_SURF)
    pygame.display.update()

# Creates a new object
def spawn(obj):
    SPAWN_GAME_OBJECTS.append(obj)

# Utility functions
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

def draw_hp_bar(obj, display_surf):
    obj_rect = obj.image.get_rect()
    obj_rect.center = obj.rect.center
    color = RED
    if obj.hp >= 0.6 * obj.max_hp:
        color = GREEN
    elif obj.hp >= 0.3 * obj.max_hp:
        color = YELLOW

    hp_rect = pygame.rect.Rect(obj_rect.left-2,obj_rect.top-15,(obj_rect.width+4)*(obj.hp/obj.max_hp),8)
    pygame.draw.rect(display_surf,color,hp_rect)

# Checks if two GameObjects collide
def colliding(obj1,obj2):
    # Quickly remove obvious cases: if bounding rects don't collide
    if not obj1.rect.colliderect(obj2.rect):
        return False
    # Then compare bitmasks
    mask1 = pygame.mask.from_surface(obj1.image,0)
    mask2 = pygame.mask.from_surface(obj2.image,0)
    
    dx = obj2.rect.topleft[0] - obj1.rect.topleft[0]
    dy = obj2.rect.topleft[1] - obj1.rect.topleft[1]
    return mask1.overlap_area(mask2,(dx,dy)) > 0

class GameObject(pygame.sprite.Sprite):
    image_template = pygame.image.load("images/object.png")
    
    def __init__(self, location):
        super().__init__()
        self.is_dead = False
        self.image = self.image_template
        self.rect = self.image.get_rect()
        self.real_location = location
        self.rect.center = (round(self.real_location[0]), round(self.real_location[1]))
    
    def draw(self,display_surf):
        display_surf.blit(self.image,self.rect.topleft)

    def update(self):
        pass

    def die(self):
        self.is_dead = True

    def on_collide(self,other_obj):
        pass
        
    def location(self):
        return self.real_location

    def set_location(self,x,y):
        self.real_location = (x,y)
        self.rect.center = (round(self.real_location[0]), round(self.real_location[1]))

class Weapon:
    def __init__(self,parent,length):
        self.parent = parent
        self.length = length

    def update(self):
        pass

    def shoot(self):
        pass

# Turret image
TURRET_IMG = pygame.image.load('images/turret.png')

class Minigun(Weapon):
    def __init__(self,parent):
        super().__init__(parent,40)
    
    def draw(self, display_surf):
        x = self.parent.location()[0]
        y = self.parent.location()[1]
        shooter = TURRET_IMG
        display_surf.blit(rot_center(shooter,self.parent.getTurretAngle()),(x-self.length,y-self.length))

    def shoot(self):
        spawn_x = self.parent.location()[0] + self.length * math.sin(math.radians(self.parent.getTurretAngle()))
        spawn_y = self.parent.location()[1] + self.length * math.cos(math.radians(self.parent.getTurretAngle()))
        spawn(Bullet((spawn_x,spawn_y),self.parent.getTurretAngle()))

class Projectile(GameObject):
    def __init__(self, location, speed, angle, duration):
        super().__init__(location)
        self.speed = speed
        self.angle = angle
        self.duration = duration
        self.life = 0
        
    def update(self):
        x = self.location()[0]
        y = self.location()[1]
        dx = SPEED_FACTOR * self.speed * math.sin(math.radians(self.angle))
        dy = SPEED_FACTOR * self.speed * math.cos(math.radians(self.angle))
        self.set_location(x+dx,y+dy)

        self.life += 1
        if self.life > self.duration:
            self.die()
        

class Bullet(Projectile):
    image_template = pygame.image.load("images/minigun-bullet.png")
    
    def __init__(self, location, angle):
        super().__init__(location=location,speed=30,angle=angle,duration=150)

    def on_collide(self,other_obj):
        if isinstance(other_obj,Unit):
            other_obj.damage(10)
            self.die()
        

class Unit(GameObject):
    def __init__(self, location, hp, energy=0, armor=0, weapon = None):
        super().__init__(location=location)
        self.hp = hp
        self.max_hp = hp
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
            self.die()
    def draw(self,display_surf):
        super().draw(display_surf)
        draw_hp_bar(self,display_surf)
    
    def die(self):
        self.is_dead = True

class Crate(Unit):
    image_template = pygame.image.load("images/crate.png")
    
    def __init__(self,location):
        super().__init__(hp=50,location=location)

class Tank(Unit):
    def __init__(self,location):
        super().__init__(location=location, hp=100, weapon=Minigun(self))
        self.dx = 0
        self.dy = 0
        self.maxSpeed = 15
        self.turret_angle = 0
    
    def draw(self,display_surf):
        super().draw(display_surf)
        # Draw "base"
        display_surf.blit(self.image,self.rect.topleft)
        # Draw "shooter"
        self.weapon.draw(display_surf)

    def update(self):
        super().update()
        self.weapon.update()
        
        x = self.location()[0]
        y = self.location()[1]
        self.set_location(x+(self.dx*SPEED_FACTOR),y+(self.dy*SPEED_FACTOR))
        if self.dx > 0:
            self.dx -= 1
            self.dx = clip(self.dx,-self.maxSpeed,self.maxSpeed)
        elif self.dx < 0:
            self.dx += 1
            self.dx = clip(self.dx,-self.maxSpeed,self.maxSpeed)
        if self.dy > 0:
            self.dy -= 1
            self.dy = clip(self.dy,-self.maxSpeed,self.maxSpeed)
        elif self.dy < 0:
            self.dy += 1
            self.dy = clip(self.dy,-self.maxSpeed,self.maxSpeed)

    def moveX(self,amount):
        self.dx += amount

    def moveY(self,amount):
        self.dy += amount

    def shoot(self):
        self.weapon.shoot()

    def getTurretAngle(self):
        return self.turret_angle

class PlayerTank(Tank):
    image_template = pygame.image.load("images/player-tank.png")
    
    def getTurretAngle(self):
        return math.degrees(math.atan2(MOUSE[0]-self.location()[0],MOUSE[1]-self.location()[1]))

class DummyTank(Tank):
    image_template = pygame.image.load("images/enemy-tank.png")

    def __init__(self,location):
        super().__init__(location)
        self.turret_turn = True # True if turning right
        self.turn_cooldown = 50
    
    def update(self):
        super().update()
        # Shoot bullets randomly
        if random.random() < 0.01:
            self.shoot()
        self.turn_cooldown -= 1
        if self.turn_cooldown <= 0:
            if random.random() < 0.5:
                self.turret_turn = True
            else:
                self.turret_turn = False
            self.turn_cooldown = round(100 * random.random())
        if self.turret_turn:
            self.turret_angle += 2
        else:
            self.turret_angle -= 2

if __name__ == '__main__':
    main()
