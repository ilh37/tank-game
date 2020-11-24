import pygame, math
from baseobjects import *
from wall import *

class Projectile(GameObject):
    def __init__(self, location, speed, angle, duration):
        super().__init__(location)
        self.angle = angle
        self.dx = speed * math.sin(math.radians(self.angle))
        self.dy = speed * math.cos(math.radians(self.angle))
        self.duration = duration
        self.life = 0
        
    def update(self):
        x = self.location()[0]
        y = self.location()[1]
        self.set_location(x+self.dx,y+self.dy)

        self.life += 1
        if self.life > self.duration:
            self.die()
    
    def speed(self):
        return math.sqrt(self.dx*self.dx + self.dy*self.dy) 
        

class Bullet(Projectile):
    image_template = pygame.image.load("images/minigun-bullet.png")
    
    def __init__(self, location, angle):
        super().__init__(location=location,speed=6.0,angle=angle,duration=150)
        
    def on_collide(self,other_obj):
        if isinstance(other_obj,Unit):
            other_obj.damage(10)
            self.die()
        elif isinstance(other_obj,Wall):
            n = collision_normal(self,other_obj)
            if n:
                self.dx -= n[0]
                self.dx = clip(self.dx,-self.speed(),self.speed())
                self.dy -= n[1]
                self.dy = clip(self.dy,-self.speed(),self.speed())
