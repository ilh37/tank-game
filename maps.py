import baseobjects, utils

# Map class to handle all ingame objects
class Map():
    def __init__(self,bounds,player):
        self.objects = []
        self.bounds = bounds
        self.player_tank = player
        self.objects.append(player)

    def spawn(self,obj):
        self.objects.append(obj)
    
    def spawns(self,objs):
        self.objects.extend(objs)

    def clear_dead(self):
        self.objects = list(filter(lambda x: not x.is_dead, self.objects))

    def update(self):
        for obj in self.objects:
            obj.update()
