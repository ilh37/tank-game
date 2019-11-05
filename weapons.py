import pygame
from baseobjects import *
from projectiles import *

class Weapon:
    image = pygame.image.load('images/object.png')
    
    def __init__(self,parent,length):
        self.parent = parent
        self.length = length

    def update(self):
        pass

    def shoot(self):
        pass

    def draw(self):
        pass

class Minigun(Weapon):
    image = pygame.image.load('images/turret.png')
    
    def __init__(self,parent):
        super().__init__(parent,40)
    
    def draw(self, display_surf,offset):
        x = self.parent.location()[0]+offset[0]
        y = self.parent.location()[1]+offset[1]
        shooter = self.image
        display_surf.blit(rot_center(shooter,self.parent.getTurretAngle()),(x-self.length,y-self.length))

    def shoot(self):
        spawn_x = self.parent.location()[0] + self.length * math.sin(math.radians(self.parent.getTurretAngle()))
        spawn_y = self.parent.location()[1] + self.length * math.cos(math.radians(self.parent.getTurretAngle()))
        spawn(Bullet((spawn_x,spawn_y),self.parent.getTurretAngle()))
