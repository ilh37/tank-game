import pygame
from baseobjects import *
from weapons import *
from utils import *

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
    
    def draw(self,display_surf,offset=(0,0)):
        super().draw(display_surf, offset)
        # Draw "shooter"
        self.weapon.draw(display_surf,offset)

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

    def on_collide(self,other_obj):
        if isinstance(other_obj,Unit) or isinstance(other_obj,Wall):
            n = collision_normal(self,other_obj)
            if n:
                self.dx -= n[0]
                self.dx = clip(self.dx,-self.maxSpeed,self.maxSpeed)
                self.dy -= n[1]
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
        return math.degrees(math.atan2(pygame.mouse.get_pos()[0]-WINDOW_WIDTH/2,pygame.mouse.get_pos()[1]-WINDOW_HEIGHT/2))

class DummyTank(Tank):
    image_template = pygame.image.load("images/enemy-tank.png")

    def __init__(self,location):
        super().__init__(location)
        self.turret_turn = True # True if turning right
        self.turn_cooldown = 50
    
    def update(self):
        super().update()
        # Shoot bullets randomly
        #if random.random() < 0.01:
        #    self.shoot()
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


class ForceField(Unit):
    image_template = pygame.image.load("images/forcefield.png")
    
    def __init__(self,location,duration):
        super().__init__(location=location,hp=1000000000)
        self.duration = 100

    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.die()

