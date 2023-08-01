from world import Grass
import random
from agent import Buffalo, Buffalo_Leader
import matplotlib.pyplot as plt
import math

plotRealTime = True
L = 1000
min_value = 250
max_value = 750
Nt = 1000
num_grass = 5
num_buffalos = 20

def main():
    fig, ax = plt.subplots()

    leader = Buffalo_Leader(random.randint(min_value, max_value), random.randint(min_value, max_value), L)
    buffalos = [Buffalo(random.randint(min_value, max_value), random.randint(min_value, max_value), L,  leader) for _ in range(num_buffalos)]
    grasses = [Grass(random.randint(L//4, L), random.randint(L//4, L), random.randint(0,10)) for _ in range(num_grass)]

    buffalos.insert(0, leader)

    for i in range(Nt):
        
        for grass in grasses:
            grass.perform_action()
        
        for buffalo in buffalos:
            buffalo.perform_action(grasses)
            buffalo.update()
        
        x = [buffalo.x for buffalo in buffalos]
        y = [buffalo.y for buffalo in buffalos]   
        c = [buffalo.color for buffalo in buffalos]
        
        grass_x = [grass.x for grass in grasses]
        grass_y = [grass.y for grass in grasses]
        grass_c = [grass.color for grass in grasses]
        grass_s = [grass.size for grass in grasses]
        
        if plotRealTime or (i == Nt-1):
            plt.cla()
            plt.scatter(grass_x, grass_y, s=grass_s, c=grass_c)
            plt.scatter(x, y, s=50, c=c)
            ax.set(xlim=(0,L),ylim=(0,L))
            plt.pause(0.1)
        
        
        chosen_grass = grasses[0]
        chosen_buffalo = buffalos[0]
        print(chosen_buffalo.state)

            
    plt.show()

if __name__ == "__main__":
    main()