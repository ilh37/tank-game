# Utility functions
import pygame, math, random

##
## Constants
##

FPS = 30
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 900

# Player tank
PLAYER_TANK = None

# Color constants
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (204,204,0)
BLACK = (0,0,0)

# All movement is reduced by this factor so that speeds can be stored exactly as
# ints but units move at reasonable speeds
SPEED_FACTOR = 0.2

##
## Basic mathematical functions
##

# Bounds value between min_value and max_value if it is too low or too high
def clip(value,min_value,max_value):
    return max(min(value, max_value), min_value)

##
## Logic functions
##

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

# List of objects to be spawned
SPAWN_GAME_OBJECTS = []

def spawn(obj):
    SPAWN_GAME_OBJECTS.append(obj)

def get_spawn_objects():
    global SPAWN_GAME_OBJECTS
    spawn = SPAWN_GAME_OBJECTS
    SPAWN_GAME_OBJECTS = []
    return spawn

##
## Drawing functions
##

# Given an object, draws an HP bar over it
def draw_hp_bar(obj, display_surf):
    obj_rect = obj.image.get_rect()
    obj_rect.center = obj.rect.center
    color = RED
    if 10 * obj.hp > 6 * obj.max_hp:
        color = GREEN
    elif 10 * obj.hp > 3 * obj.max_hp:
        color = YELLOW

    hp_rect = pygame.rect.Rect(obj_rect.left-2,obj_rect.top-15,(obj_rect.width+4)*(obj.hp/obj.max_hp),8)
    pygame.draw.rect(display_surf,color,hp_rect)

# Rotate an image while keeping its center and size
def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
