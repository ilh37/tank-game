import pygame, baseobjects, utils

# Map class to handle all ingame objects
class Map():
    def __init__(self,bounds,player):
        self.objects = []
        self.bounds = bounds
        self.player_tank = player
        self.objects.append(player)
        self.camera_position=(800,450)

    def spawn(self,obj):
        self.objects.append(obj)
    
    def spawns(self,objs):
        self.objects.extend(objs)

    def clear_dead(self):
        self.objects = list(filter(lambda x: not x.is_dead, self.objects))

    def update(self):
        for obj in self.objects:
            obj.update()

    def draw(self, display_surf):
        display_surf.fill(utils.WHITE)

        player_loc = self.player_tank.location()
        for obj in self.objects:
            obj.draw(display_surf, (-player_loc[0]+self.camera_position[0],-player_loc[1]+self.camera_position[1]))
        pygame.display.update()
