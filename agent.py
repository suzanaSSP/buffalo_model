import math
import numpy as np
import random

dt = 0.5

class Buffalo:
    
    def __init__(self, x, y, leader=None, predator=None):
        self.x = x
        self.y = y
        self.c = np.array([self.x, self.y])

        self.state = None

        self.theta  = np.random.uniform(-np.pi, np.pi) 
        self.v = np.array([np.cos(self.theta), np.sin(self.theta)])
        self.speed = 10 if self.state == 'run_away_from_predator' else 5 

        self.grass_eating = None
        self.satisfaction = 200
        self.color = (0.4, 0.2, 0) # Brown (102, 51, 0)
        self.switch = False 
        
        self.neighbors = None
        self.leader =  self if leader is None else leader
        self.predator = None if predator is None else predator

        self.new_theta = 0
        self.new_v = np.array([0,0])
        self.new_c = np.array([0,0])
       
    def new_position(self, U):
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
        
        if self.state != "eating":
            self.satisfaction -= 1
    
    def check_state(self, buffalos):
        self.neighbors = [other_buffalo for other_buffalo in buffalos if math.dist(other_buffalo.c, self.c) <= 200 and other_buffalo is not self]
        self.neighbors_speed = [neighbor.speed for neighbor in self.neighbors]
        
        if self.predator in self.neighbors or 10 in self.neighbors_speed:
            if len(self.neighbors) > 10 and math.dist(self.c, self.predator.c) < 100:
                self.state == "attack_predator"
            else:
                self.state = "run_away_from_predator"             
        elif self.switch:
            self.state = "eating"
        elif self.satisfaction < 100:
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
        else:
            self.attack_predator(buffalos)
        
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
        self.new_position(Ua)
        
    def closest_grass(self, grasses):
        # Find closest grass to eat
        closest_grass = grasses[0]
        for grass in grasses[1:]:
            if math.dist(self.c, grass.c) < math.dist(self.c, closest_grass.c):
                closest_grass = grass

        return closest_grass

    # EATING STATE
    def eat(self):
        self.satisfaction += 1
        if self.grass_eating:
            if self not in self.grass_eating.agents_feeding:
                self.grass_eating.agents_feeding.append(self)  
              
        
            # If the grass has been eaten buffalo should go look for another grass if it's still hungry
            if not self.grass_eating.switch and self.switch:
                self.state = "hungry"
                self.grass_eating.agents_feeding.remove(self)
                self.grass_eating = None

            if self.satisfaction == 200:
                self.grass_eating.agents_feeding.remove(self)
                self.grass_eating = None
        else:    
            self.switch = False

    # GROUPING STATE
    def grouping(self):
        attraction_factor = 0
        repulsion_factor = 0
        orientation_factor = np.array([0,0], dtype='float64')
        
        for agent in self.neighbors:
            if agent.state != "eating":
                orientation_factor += agent.v
                repulsion_factor += (agent.c-self.c)/(np.linalg.norm(agent.c - self.c)**2)
                if isinstance(agent, BuffaloLeader):
                    attraction_factor += ((agent.c - self.c) * 2) # more weight if it's a leader
                else:
                    attraction_factor += (agent.c - self.c)
                        
        if attraction_factor == 0 and repulsion_factor == 0 and (orientation_factor == np.array([0, 0])).all():
            attraction_factor += ((self.leader.c - self.c) * 2)
            repulsion_factor += (self.leader.c-self.c)/(np.linalg.norm(self.leader.c - self.c)**2)
            orientation_factor += self.leader.v
           
        Uo = (self.v + orientation_factor)/np.linalg.norm(self.v + orientation_factor)     
        Ur = -1 * repulsion_factor
        Ua = attraction_factor / np.linalg.norm(attraction_factor)
        U = Ua + Ur + Uo
        self.new_position(U)
      
    # RUN_AWAY_FROM_PREDATOR STATE  
    def avoid_predator(self):
        if self.neighbors:
            orientation_factor = np.array([0,0], dtype='float64')
            attraction_factor = 0
            for agent in self.neighbors:
                attraction_factor += (agent.c - self.c)
                orientation_factor += agent.v
        Uo = (self.v + orientation_factor)/np.linalg.norm(self.v + orientation_factor)
        Ua = attraction_factor / np.linalg.norm(attraction_factor)
        Ur = -1 * ((self.predator.c - self.c)/ np.linalg.norm(self.predator.c - self.c))
        
        U = Ua + Ur + Uo
        self.new_position(U)

    # ATTACK_PREDATOR STATE
    def attack_predator(self, buffalos):
        buffalos.remove(self.predator)

        
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
        self.speed = 6
        self.buffalos_eaten = 0
        self.satisfaction = 400

    # def find_prev_state(self):
    #     self.states.append(self.state)
    #     if len(self.states) == 3:
    #         del self.states[0]

    #     if len(self.states) == 2:
    #         self.prev_state = self.states[0]
    #         self.state = self.states[1]


    def check_states(self, buffalos):
        # Only bufalos that are in the predators radius of hunt are added in this list
        self.neighbors = [other_buffalo for other_buffalo in buffalos if math.dist(other_buffalo.c, self.c) < 500 and other_buffalo is not self]
        
        if self.satisfaction <= 300:
            self.state = "chase_buffalos"
        elif self.satisfaction > 300 and self.state != "hide":
            self.state = "find_hiding_place"
        elif self.state == "find_hiding_place" and not self.neighbors: # Found good place to hide with no buffalos nearby
            self.state = "hide"
            
    
    def perform_action(self, buffalos):
        self.check_states(buffalos)

        if self.state == "find_hiding_place":
            self.find_location()
        elif self.state == "chase_buffalos":
            self.chase_buffalo(buffalos)
    
    # HIDE STATE

    # FIND HIDING PLACE STATE
    def find_location(self):
        repulsion_factor = np.array([0,0], dtype='float64')
        for neighbor in self.neighbors:
            repulsion_factor += (neighbor.c - self.c)/np.linalg.norm(neighbor.c - self.c)**2

        Ur = -1 * repulsion_factor
        self.new_position(Ur)
    
    # CHASE_BUFFALO STATE
    def chase_buffalo(self, buffalos):
        if not self.neighbors:
            self.go_closer_to_buffalos(buffalos)
        else:
            attraction_factor = 0

            for buffalo in self.neighbors:
                if math.dist(buffalo.c, self.c) < 50:
                    buffalos.remove(buffalo)
                    self.buffalos_eaten += 1
                else:
                    attraction_factor += (buffalo.c - self.c)

            self.satisfaction = self.buffalos_eaten * 100

            Ua = attraction_factor / np.linalg.norm(attraction_factor)
            self.new_position(Ua)
            
    def go_closer_to_buffalos(self, buffalos):
        attraction_factor = 0
        for buffalo in buffalos:
            attraction_factor += (buffalo.c - self.c)

        Ua = attraction_factor / np.linalg.norm(attraction_factor)
        self.new_position(Ua)

    # EXPLORING STATE
    def random_walk(self):
        self.clock += 1
        self.new_theta = np.random.uniform(-(np.pi)/4, np.pi/2)
        self.new_v = np.array([np.cos(self.new_theta), np.sin(self.new_theta)])
        self.new_c = self.c + (self.speed * self.new_v * dt)
        

        
        


