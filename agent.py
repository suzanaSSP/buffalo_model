import math
import numpy as np

class Buffalo:
    dt = 0.1
    radius = 3
    speed = 1
    def __init__(self, x, y, leader=None):
        self.x = x
        self.y = y
        self.c = np.array([self.x, self.y])
        self.v = np.array([self.speed * math.cos(math.pi/2), self.speed*math.sin(math.pi/2)])

        self.state = "follow_the_leader"
        self.change_x = 0
        self.change_y = 0

        self.grass_eating = None
        self.satisfaction = 100
        self.hunger = False if self.satisfaction > 10 else True
        self.color = (0.4, 0.2, 0) # Brown (102, 51, 0)

        self.repulsion_agents = []
        self.orientation_agents = []
        self.attractive_agents = []
        
        self.leader = self if leader is None else leader
            
    def perform_action(self, grasses):   
        if self.state == "follow_the_leader":
            self.follow_the_leader()
        elif self.state == "hungry":
            self.find_food(grasses)
        else:
            self.eat()
        
    def move(self):
        new_x = self.x + (self.change_x * self.dt)
        new_y = self.y + (self.change_y * self.dt)

        self.x = new_x
        self.y = new_y
        self.c = np.array([self.x, self.y])
        
        self.change_x = 0
        self.change_y = 0

    def find_food(self, grasses):
        # list of potential grasses buffalo can eat
        attractive_grasses = []   
        for grass in grasses:
            if not grass.full_capacity:
                attractive_grasses.append(grass)
                
        if not attractive_grasses:
            return None
        else:
            # Chose the closet grass with less buffalos to eat 
            self.grass_eating = self.closest_grass(attractive_grasses)
            self.change_x = self.grass_eating.x - self.x
            self.change_y = self.grass_eating.y - self.y
            
        if math.dist(self.c, self.grass_eating.c) <= self.radius:
                self.state = "eating"
        self.satisfaction -= 1
        
    def closest_grass(self, grasses):
        # Find closest grass to eat
        closest_grass = grasses[0]
        for grass in grasses[1:]:
            if math.dist(self.c, grass.c) < math.dist(self.c, closest_grass.c):
                closest_grass = grass

        return closest_grass

    def eat(self):
        if self.grass_eating and self not in self.grass_eating.agents_feeding:
            self.grass_eating.agents_feeding.append(self)  
              
        self.satisfaction += 1
        if self.satisfaction >= 100:
            self.grass_eating.agents_feeding.remove(self)
            self.grass_eating = None
            self.state = "follow_the_leader"

    def follow_the_leader(self):
        if self.hunger:
            self.state = "hungry"
            
        self.change_x = self.leader.x - self.x
        self.change_y = self.leader.y - self.y
        
        self.satisfaction -= 1



class Buffalo_Leader(Buffalo):

    screen_width = 600
    screen_height = 600
    
    def __init__(self, x, y, leader=None):
        super().__init__(x, y)

    def check_grass(self, grasses):
        grass_list = grasses
        for grass in grass_list:
            if math.dist(self.c, grass.c) <= self.radius:
                grass_list.remove(grass)
                
        chosen_grass = grass_list[0]
        self.change_x = chosen_grass.x - self.x
        self.change_y = chosen_grass.y - self.y
        
        self.satisfaction -= 1
        
    def check_state(self):
        if self.hunger:
            self.state = "hungry"
        elif self.grass_eating:
            self.state = "eating"
        else:
            self.state = "follow_the_leader"
            
        
    def perform_action(self, grasses):
        self.check_state()
        
        if self.state == "follow_the_leader":
            self.check_grass(grasses)
        elif self.state == "hungry":
            self.find_food(grasses)
        else:
            self.eat()



