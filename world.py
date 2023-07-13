import numpy as np

class Grass():
    def __init__(self, x, y, volume):
        self.x = x
        self.y = y
        self.c = np.array([self.x, self.y])
        self.volume = volume
        self.color = (0,128,0)
        self.num_agents_feeding = 0
        self.full_capacity = False

    def decide_volume(self):
        if self.volume <= 3:
            self.color = (175, 225, 175) # Celadon
        elif 3 < self.volume <= 7:
            self.color = (80, 200, 120) # Esmerald Green
        else:
            self.color = (34, 139, 34) # Forest Green

    def decide_capacity(self):
        if self.volume <= 3:
            if self.num_agents_feeding > 6:
                self.full_capacity = True
        
        if 3 < self.volume <= 7:
            if self.num_agents_feeding > 14:
                self.full_capacity = True

        if self.volume > 7:
            if self.num_agents_feeding > 20:
                self.full_capacity = True

