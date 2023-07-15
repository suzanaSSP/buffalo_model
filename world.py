import numpy as np

class Grass():
    def __init__(self, x, y, volume):
        self.x = x
        self.y = y
        self.c = np.array([self.x, self.y])
        self.volume = volume
        self.color = (0,0.5,0)
        self.agents_feeding = []
        self.full_capacity = False
        self.size = volume

    def decide_volume(self):
        if self.volume <= 3:
            self.size = 100
            self.color = (0.7, 0.8, 0.7) # Celadon
        elif 3 < self.volume <= 7:
            self.size = 200
            self.color = (0.3, 0.78, 0.47) # Esmerald Green
        else:
            self.size = 300
            self.color = (0.14, 0.54, 0.14) # Forest Green

    def decide_capacity(self):
        if self.volume <= 3:
            if len(self.agents_feeding) > 6:
                self.full_capacity = True
        
        if 3 < self.volume <= 7:
            if len(self.agents_feeding) > 14:
                self.full_capacity = True

        if self.volume > 7:
            if len(self.agents_feeding) > 20:
                self.full_capacity = True

