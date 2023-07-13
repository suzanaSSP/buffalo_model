import math
import numpy as np

class Buffalo:
    dt = 0.1
    radius = 3
    speed = 1
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.c = np.array([self.x, self.y])
        self.v = np.array([self.speed * math.cos(math.pi/2), self.speed*math.sin(math.pi/2)])

        self.state = "hungry"
        self.change_x = 0
        self.change_y = 0

        self.grass_eating = None
        self.satisfaction = 100
        self.color = (102, 51, 0)

        self.repulsion_agents = []
        self.orientation_agents = []
        self.attractive_agents = []

    def perform_action(self, grasses, leader):
        if self.state == "wandering_around":
            self.follow_the_leader(leader)
        elif self.state == "hungry":
            self.find_food(grasses)
        else:
            self.eat()
        
    def move(self):
        self.satisfaction -= 1

        new_x = self.x + (self.change_x * self.dt)
        new_y = self.y + (self.change_y * self.dt)

        self.x = new_x
        self.y = new_y
        self.c = np.array([self.x, self.y])

        if self.grass_eating and math.dist(self.grass_eating.c, self.c) < 2:
            self.state = "eating"

        self.change_x = 0
        self.change_y = 0

    def find_food(self, grasses):
        # list of potential grasses buffalo can eat
        attractive_grasses = []   
        for grass in grasses:
            if not grass.full_capacity:
                if math.dist(self.c, grass.c) <= self.radius:
                    self.state = self.eat
                    grass.num_agents_feeding += 1
                    break
                else:
                    attractive_grasses.append(grass)
        if not attractive_grasses:
            return None
        else:
            # Chose the closet grass with less buffalos to eat 
            self.grass_eating = self.closest_grass(attractive_grasses)
            self.change_x = self.grass_eating.x - self.x
            self.change_y = self.grass_eating.y - self.y
            self.move()

    def closest_grass(self, grasses):
        # Find closest grass to eat
        closest_grass = grasses[0]
        for grass in grasses[1:]:
            if math.dist(self.c, grass.c) < math.dist(self.c, closest_grass.c):
                closest_grass = grass

        return closest_grass

    def eat(self):
        if self.satisfaction > 100:
            self.state = "wandering_around"
            self.satisfaction = 0

    def follow_the_leader(self, leader):
        if self.satisfaction == 0:
            self.state = "hungry"
        self.move()

    def find_repulsion(self):
        repulsion_factor = 0
        for buffalo in self.repulsion_agents:
            repulsion_factor += (buffalo.c - self.c)/np.linalg.norm(buffalo.c, self.c)**2
        
        return -1 * repulsion_factor
    
    def orientation_factor(self):
        orientation_factor = 0
        for buffalo in self.orientation_agents:
            orientation_factor += buffalo.v
            
        

class Buffalo_Leader(Buffalo):

    screen_width = 600
    screen_height = 600
    def __init__(self, x, y):
        super().__init__(x, y)

    def move_somewhere(self):
        self.change_x = self.screen_width - self.x
        self.change_y = self.screen_height - self.y

        self.move()

    def perform_action(self, grasses):
        if self.state == "wandering_around":
            self.move_somewhere()
        elif self.state == "hungry":
            self.find_food(grasses)
        else:
            self.eat()



