import pygame
from baseobjects import *

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
