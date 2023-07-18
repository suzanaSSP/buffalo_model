import numpy as np

class Grass():
    def __init__(self, x, y, volume):
        self.x = x
        self.y = y
        self.c = np.array([self.x, self.y])
        
        self.volume = volume
        self.color = (0,0.5,0)

        self.size = 100
        self.grass_amount = 50
        self.agents_feeding = []
        self.full_capacity = False
        
        self.switch = True # True = yes you can eat the grass. False = no there's no grass

    def perform_action(self):
        # Action grass should do every timestep
        self.decide_volume()
        self.decide_capacity()
        self.eat_and_grow()
            
            
    def decide_volume(self):
        if self.volume == 0:
            self.color = (1, 1, 1)
        elif 0 < self.volume <= 3:
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
                
    def eat_and_grow(self):
        for buffalo in self.agents_feeding:
            self.grass_amount -= 1
            
        if not self.agents_feeding and self.switch:
            self.grass_amount += 0.5
            if not self.switch:
                self.volume += 1
            
        if self.grass_amount < 0.5:
            self.volume = 0 
            self.full_capacity = True # No Buffalos can eat it
            self.switch = False
            
        if self.volume > 4 and not self.switch:
            self.grass_amount = 50
            self.switch = True
            
            

