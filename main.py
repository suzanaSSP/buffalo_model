from world import Grass
import random
from agent import Buffalo, Buffalo_Leader
import matplotlib.pyplot as plt
import math

plotRealTime = True
width = 50
height = 50
Nt = 1000
num_grass = 2
num_buffalos = 20

fig, ax = plt.subplots()

leader = Buffalo_Leader(random.randint(0, width), random.randint(0, height))
buffalos = [Buffalo(random.randint(0, width), random.randint(0, height), leader) for _ in range(num_buffalos)]
grasses = [Grass(random.randint(0, width), random.randint(0, height), random.randint(0,10)) for _ in range(num_grass)]

buffalos.insert(0, leader)

for i in range(Nt):
    
    for grass in grasses:
        grass.decide_volume()
        grass.decide_capacity()
    
    for buffalo in buffalos:
        buffalo.perform_action(grasses)
        buffalo.move()
     
    x = [buffalo.x for buffalo in buffalos]
    y = [buffalo.y for buffalo in buffalos]   
    c = [buffalo.color for buffalo in buffalos]
    
    grass_x = [grass.x for grass in grasses]
    grass_y = [grass.y for grass in grasses]
    grass_c = [grass.color for grass in grasses]
    grass_s = [grass.size for grass in grasses]
       
    if plotRealTime or (i == Nt-1):
        plt.cla()
        plt.scatter(x, y, s=50, c=c)
        plt.scatter(grass_x, grass_y, s=grass_s, c=grass_c)
        ax.set(xlim=(0,width),ylim=(0,height))
        plt.pause(0.1)
    
    
    chosen_buffalo = buffalos[1]
    print(chosen_buffalo.state)
    print(chosen_buffalo.satisfaction)
    if chosen_buffalo.grass_eating:
        print(math.dist(chosen_buffalo.c, chosen_buffalo.grass_eating.c))

        
plt.show()
