import math
import numpy as np
import random

"""
Explanation of the self.switch: 
Before, I had an if statement that says if the level of hunger is less than 10, go to the eating state. 
While the agent is in the eating state, it gains 1 satisfaction every timestep.
However, they are suppost to keep eating until they reach 100, but only they hit 10, they go to another state. 
When they go to another state, it substracts one from satisfaction and goes back to the eating state, and it just goes back and from from the eating state and the other
So now, they just go to the eating state if the switch is True, and the switch only changes when it's back at hundred
"""

class Buffalo:
    dt = 0.1
    speed = 5
    def __init__(self, x, y, size_area):
        self.x = x
        self.y = y
        self.c = np.array([self.x, self.y])

        self.theta  = np.random.uniform(-np.pi, np.pi) 
        self.v = np.array([np.cos(self.theta), np.sin(self.theta)])

        self.state = "grouping"
        self.change_x = 0
        self.change_y = 0
        self.change_theta = 0

        self.grass_eating = None
        self.satisfaction = random.randint(80, 100)
        self.color = (0.4, 0.2, 0) # Brown (102, 51, 0)
        
        self.switch = False 

        self.size_area = size_area
        self.size = 50

    def check_state(self, predator):
        if math.dist(predator.c, self.c) < 100:
            self.state = "run_away_from_predator"
        elif self.switch:
            self.state = "eating"
        elif self.grass_eating or self.satisfaction < 40:
            self.state = "hungry"
        else:
            self.state = "grouping"

    def perform_action(self, grasses, predator):   
        self.check_state(predator)
        
        if self.state == "grouping":
            self.grounping()
        elif self.state == "hungry":
            self.find_food(grasses)
        elif self.state == "eating":
            self.eat()
        elif self.state == "run_away_from_predator":
            self.avoid_predator(predator)
        
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
            
        self.satisfaction -= 1
        
        if math.dist(self.c, self.grass_eating.c) < 1:
            self.switch = True
        
    def closest_grass(self, grasses):
        # Find closest grass to eat
        closest_grass = grasses[0]
        for grass in grasses[1:]:
            if math.dist(self.c, grass.c) < math.dist(self.c, closest_grass.c):
                closest_grass = grass

        return closest_grass

    def eat(self):
        if self.grass_eating:
            if self not in self.grass_eating.agents_feeding:
                self.grass_eating.agents_feeding.append(self)  
              
            self.satisfaction += 1
        
            # If the grass has been eaten buffalo should go look for another grass if it's still hungry
            if not self.grass_eating.switch and self.switch:
                self.state = "hungry"
                self.grass_eating.agents_feeding.remove(self)
                self.grass_eating = None

            if self.satisfaction == 100:
                self.grass_eating.agents_feeding.remove(self)
                self.grass_eating = None
        else:    
            self.switch = False

    def grounping(self):
        new_location = [random.randint(0, self.size_area//4), random.randint(0, self.size_area//4)]
        self.change_x = new_location[0] - self.x
        self.change_y = new_location[1] - self.y 
        
        self.satisfaction -= 1

    def avoid_predator(self, predator):
        # repulsion_factor = -1 * ((predator.c - self.c)/ np.linalg.norm(predator.c - self.c)**2)
        self.change_x = self.x - predator.x
        self.change_y = self.y - predator.y


class Predator(Buffalo):
    def __init__(self, x, y, size_area, leader=None):
        super().__init__(x, y, size_area)
        self.clock = 0
        self.state = "chase_buffalo"
        self.color = (1, 0.5, 0) # Orange
        self.size = 100

    def check_state(self):
        if self.clock > 20:
            self.state = "chase_buffalo"
        else:
            self.state = "wait"

    def perform_action(self, buffalos):
        # self.check_state()

        if self.state == "chase_buffalo":
            self.chase_buffalo(buffalos)
        else:
            self.clock += 1

    def chase_buffalo(self, buffalos):
        attraction_factor = 0

        for buffalo in buffalos[1:]:
            if math.dist(buffalo.c, self.c) < 500:
                attraction_factor += (buffalo.c - self.c)
        
        # # No buffalos are near, need to move forward
        # if all(attraction_factor) == 0:
        #     self.change_x = self.x + self.speed*self.clock
        #     self.change_y = self.y + self.speed*self.clock
        # else:
        if not math.isnan(attraction_factor):
            Ua = attraction_factor / np.linalg.norm(attraction_factor)       
            w = 0.5 * (np.arctan2(Ua[1], Ua[0]) - self.theta)

            self.change_x = (self.speed * self.v)
            self.theta = self.theta + (self.dt * w)
            self.v = np.array([np.cos(self.theta), np.sin(self.theta)])
 
        self.clock += 1

        # Time is up, change states
        if self.clock == 150:
            self.clock = 0
            self.c = [0,0]


        


