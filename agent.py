import math
import numpy as np
import random

dt = 0.5

class Buffalo:
    
    def __init__(self, x, y, leader=None, predator=None):
        self.x = x
        self.y = y
        self.c = np.array([self.x, self.y])

        self.theta  = np.random.uniform(-np.pi, np.pi) 
        self.v = np.array([np.cos(self.theta), np.sin(self.theta)])
        self.speed = 7 if self.state == "run_away_from_predator" else 5

        self.state = "grouping"
        self.grass_eating = None
        self.satisfaction = random.randint(150, 200)
        self.color = (0.4, 0.2, 0) # Brown (102, 51, 0)
        self.neighbors = None
        self.switch = False 
        self.leader =  self if leader is None else leader
        self.predator = None if predator is None else predator

        self.new_theta = 0
        self.new_v = None
        self.new_c = None
       
    def movement(self, U):
        w = 0.5 * (np.arctan2(U[1], U[0]) - self.theta)
        self.new_theta = self.theta + (w * dt)
        self.new_v = np.array([np.cos(self.new_theta), np.sin(self.new_theta)])
        self.new_c = self.c + (self.speed * self.v * dt)
    
        
    def update(self):
        self.c = self.new_c
        self.x = self.new_c[0]
        self.y = self.new_c[1]
        self.v = self.new_v
        self.theta = self.new_theta
        
        self.satisfaction -= 1
    
    def check_state(self, buffalos):
        self.neighbors = [other_buffalo for other_buffalo in buffalos if math.dist(other_buffalo.c, self.c) <= 200 and other_buffalo is not self]
        
        if self.predator in self.neighbors:
            self.state = "run_away_from_predator"              
        elif self.switch:
            self.state = "eating"
        elif self.grass_eating or self.satisfaction < 40:
            self.state = "hungry"
        else:
            self.state = "grouping"

    def perform_action(self, grasses, buffalos):   
        self.check_state(buffalos)
        
        if self.state == "grouping":
            self.grouping()
        elif self.state == "hungry":
            self.find_food(grasses)
        elif self.state == "eating":
            self.eat()
        elif self.state == "run_away_from_predator":
            self.avoid_predator()
        
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
        self.movement(Ua)
        
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
        self.movement(Ua)
      
    # RUN_AWAY_FROM_PREDATOR STATE  
    def avoid_predator(self):
        Ur = (-1 * ((self.predator.c - self.c)/ np.linalg.norm(self.predator.c - self.c)**2)) * 5

        self.movement(Ur)
        
class BuffaloLeader(Buffalo):
    def __init__(self, x, y, leader=None):
        super().__init__(x, y)
        self.color = (0.6, 0, 0) # Dark red
        self.neighbor_dist = None
        
    def grouping(self):
        self.new_theta = np.random.uniform(-(np.pi)/4, np.pi/4)
        self.new_v = np.array([np.cos(self.new_theta), np.sin(self.new_theta)])
        self.new_c = self.c + (self.speed * self.new_v * dt)
        
 
class Predator(Buffalo):
    def __init__(self, x, y, leader=None, predator=None):
        super().__init__(x, y, leader=None, predator=None)
        self.color = (1, 0.5, 0) # Orange
        self.speed = 5

    def perform_action(self, buffalos):
        # Only bufalos that are in the predators radius of hunt are added in this list
        self.neighbors = [other_buffalo for other_buffalo in buffalos if math.dist(other_buffalo.c, self.c) < 500 and other_buffalo is not self]
        self.neighbor_dist = [math.dist(agent.c, self.c) for agent in self.neighbors]
        # If the list is not empty, you can hunt :)
        if self.neighbors:
            self.state = "chase_buffalo"
            self.chase_buffalo(buffalos)
        else:
            self.state = "random_walk"
            self.random_walk()
        

    # WAITING STATE
    
    # CHASE_BUFFALO STATE
    def chase_buffalo(self, buffalos):
        attraction_factor = 0

        for buffalo in self.neighbors:
            if math.dist(buffalo.c, self.c) < 50:
                self.satisfaction = 200
                # buffalo.color = (0.5, 0.5, 0.5)
                buffalos.remove(buffalo)
            else:
                attraction_factor += (buffalo.c - self.c)

        Ua = attraction_factor / np.linalg.norm(attraction_factor)
        self.movement(Ua)
        
    # EXPLORING STATE
    def random_walk(self):
        self.new_theta = np.random.uniform(-(np.pi)/4, np.pi/2)
        self.new_v = np.array([np.cos(self.new_theta), np.sin(self.new_theta)])
        self.new_c = self.c + (self.speed * self.new_v * dt)
        

        
        


