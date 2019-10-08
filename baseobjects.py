import pygame
from utils import *

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

