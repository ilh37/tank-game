from baseobjects import *
from utils import *

class Wall(GameObject):
    def __init__(self, location, image):
        super().__init__(location)
        self.image = image
        #self.rect = self.image.get_rect()
        self.real_location = location
        #self.rect.center = (round(self.real_location[0]), round(self.real_location[1]))

