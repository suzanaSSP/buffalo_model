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
dt = 0.5
speed = 5

class Buffalo:
    
    def __init__(self, x, y, leader=None, predator=None):
        self.x = x
        self.y = y
        self.c = np.array([self.x, self.y])

        self.theta  = np.random.uniform(-np.pi, np.pi) 
        self.v = np.array([np.cos(self.theta), np.sin(self.theta)])

        self.state = None
        self.change_x = 0
        self.change_y = 0
        self.change_theta = 0

        self.grass_eating = None
        self.satisfaction = random.randint(80, 100)
        self.color = (0.4, 0.2, 0) # Brown (102, 51, 0)
        
        self.switch = False 
        self.leader =  self if leader is None else leader
        self.neighbors = []
        
        self.predator = None if predator is None else predator
       
    def attraction(self, Ua):
        w = 0.5 * (np.arctan2(Ua[1], Ua[0]) - self.theta)
        new_theta = self.theta + (w * dt)
        new_v = np.array([np.cos(new_theta), np.sin(new_theta)])
        new_c = self.c + (speed * self.v * dt)
        
        self.move(new_c, new_v, new_theta)
        
    def move(self, new_c, new_v, new_theta):
        self.c = new_c
        self.x = new_c[0]
        self.y = new_c[1]
        self.v = new_v
        self.theta = new_theta
        
        self.satisfaction -= 1
    
    def check_state(self, buffalos):
        neighbors = [other_agent for other_agent in buffalos if math.dist(other_agent.c, self.c) < 1000 and not self]
        
        for agent in neighbors:
            if isinstance(agent, Predator):
                self.state = "run_away_from_predator"        
                
        if self.switch:
            self.state = "eating"
        elif self.grass_eating or self.satisfaction < 40:
            self.state = "hungry"
        else:
            self.state = "grouping"

    def perform_action(self, grasses, buffalos, predator):   
        self.check_state(buffalos)
        
        if self.state == "grouping":
            self.grouping()
        elif self.state == "hungry":
            self.find_food(grasses)
        elif self.state == "eating":
            self.eat()
        elif self.state == "run_away_from_predator":
            self.avoid_predator(predator)
        
    # HUNGRY STATE
    def find_food(self, grasses):
        # list of potential grasses buffalo can eat
        good_grass = []   
        for grass in grasses:
            if not grass.full_capacity:
                good_grass.append(grass)
                
        if not good_grass:
            return None
        else:
            # Chose the closet grass with less buffalos to eat 
            self.grass_eating = self.closest_grass(good_grass)
            
        if math.dist(self.grass_eating.c, self.c) < 1:
            self.switch = True
            
        Ua = (self.grass_eating.c - self.c) / np.linalg.norm(self.grass_eating.c - self.c)
        self.attraction(Ua)
        
    def closest_grass(self, grasses):
        # Find closest grass to eat
        closest_grass = grasses[0]
        for grass in grasses[1:]:
            if math.dist(self.c, grass.c) < math.dist(self.c, closest_grass.c):
                closest_grass = grass

        return closest_grass

    # EATING STATE
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

    # GROUPING STATE
    def grouping(self):
        attraction_factor = 0
        for agent in self.neighbors:
            if isinstance(agent, BuffaloLeader):
                attraction_factor += ((agent.c - self.c) * 2) # more weight if it's a leader
            else:
                attraction_factor += (agent.c - self.c)
                
        if not self.neighbors:
            attraction_factor += ((self.leader.c - self.c) * 2)
            
        Ua = attraction_factor / np.linalg.norm(attraction_factor)
        self.attraction(Ua)
      
    # RUN_AWAY_FROM_PREDATOR STATE  
    def avoid_predator(self, predator):
        Ur = -1 * ((predator.c - self.c)/ np.linalg.norm(predator.c - self.c)**2)
        self.attraction(Ur)
        
class BuffaloLeader(Buffalo):
    def __init__(self, x, y, leader=None):
        super().__init__(x, y)
        self.color = (0.6, 0, 0) # Dark red
        self.clock = 0 
        
    def grouping(self):
        new_theta = np.random.uniform(-(np.pi)/4, np.pi/4)
        new_v = np.array([np.cos(new_theta), np.sin(new_theta)])
        new_c = self.c + (speed * new_v * dt)
        
        self.move(new_c, new_v, new_theta)
 
class Predator(Buffalo):
    def __init__(self, x, y, leader=None):
        super().__init__(x, y)
        self.color = (1, 0.5, 0) # Orange

    def perform_action(self, buffalos):
        # Only bufalos that are in the predators radius of hunt are added in this list
        self.neighbors = [buffalo for buffalo in buffalos if math.dist(buffalo.c, self.c) < 10 and not self]
        # If the list is not empty, you can hunt :)
        if self.neighbors:
            self.chase_buffalo(self.neighbors)
        else:
            self.random_walk(buffalos)

    # CHASE_BUFFALO STATE
    def chase_buffalo(self, buffalos):
        attraction_factor = 0

        for buffalo in self.neighbors:
            attraction_factor += (buffalo.c - self.c)
           
        Ua = attraction_factor / np.linalg.norm(attraction_factor)  
        self.attraction(Ua)
       
    # WAITING STATE     
    def random_walk(self, buffalos):
        # new_theta = np.random.uniform(-(np.pi)/4, np.pi/4)
        # new_v = np.array([np.cos(new_theta), np.sin(new_theta)])
        # new_c = self.c + (speed * new_v * dt)
        
        # self.move(new_c, new_v, new_theta)

        attraction_factor = 0
        for buffalo in buffalos:
            attraction_factor += (buffalo.c - self.c)
            
        Ua = attraction_factor / np.linalg.norm(attraction_factor)
        
        self.attraction(Ua)
        


