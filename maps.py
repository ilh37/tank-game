import pygame, baseobjects, utils, units, wall

# Map class to handle all ingame objects
class Map():
    def __init__(self,bounds,player):
        self.objects = []
        self.bounds = bounds
        self.player_tank = player
        self.objects.append(player)
        self.camera_position=(800,450)

    def load_data(self):
        pass

    def is_lost(self):
        return False

    def is_won(self):
        return True
    
    def spawn(self,obj):
        self.objects.append(obj)
    
    def spawns(self,objs):
        self.objects.extend(objs)

    def clear_dead(self):
        self.objects = list(filter(lambda x: not x.is_dead, self.objects))

    def update(self):
        for obj in self.objects:
            obj.update()
            # Clamp objects to map
            obj.set_rect(obj.rect.clamp(pygame.Rect((0,0),self.bounds)))

        # Deal with collisions
        for obj1 in self.objects:
            for obj2 in self.objects:
                if obj1 != obj2 and utils.colliding(obj1,obj2):
                    obj1.on_collide(obj2)

    def draw(self, display_surf):
        display_surf.fill(utils.BLACK)

        player_loc = self.player_tank.location()
        pygame.draw.rect(display_surf, utils.WHITE, pygame.Rect(-player_loc[0]+self.camera_position[0], -player_loc[1]+self.camera_position[1], 1600, 900))
        for obj in self.objects:
            obj.draw(display_surf, (-player_loc[0]+self.camera_position[0],-player_loc[1]+self.camera_position[1]))
        pygame.display.update()

class Map1(Map):
    def load_data(self):
        self.enemy = units.DummyTank((600,300))
        self.spawn(units.Crate((700,500)))
        self.spawn(units.Crate((800,400)))
        w = wall.Wall((100,100), pygame.image.load("images/wall-test.png"))
        self.spawn(w)
        self.spawn(self.enemy)  

    def is_lost(self):
        return self.player_tank.is_dead

    def is_won(self):
        return self.enemy.is_dead
