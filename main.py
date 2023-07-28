from world import Grass
import random
from agent import Buffalo, Predator
import matplotlib.pyplot as plt
import math

plotRealTime = True
L = 1000
min_value = 250
max_value = 750
Nt = 1000
num_grass = 5
num_buffalos = 2

def main():
    fig, ax = plt.subplots()

    # leader = Buffalo_Leader(random.randint(min_value, max_value), random.randint(min_value, max_value), L)
    predator = Predator(0, 0, L)
    buffalos = [Buffalo(random.randint(min_value, max_value), random.randint(min_value, max_value), L) for _ in range(num_buffalos)]
    grasses = [Grass(random.randint(L//4, L), random.randint(L//4, L), random.randint(0,10)) for _ in range(num_grass)]

    buffalos.insert(0, predator)

    for i in range(Nt):
        
        for grass in grasses:
            grass.perform_action()
        
        for buffalo in buffalos:
            if isinstance(buffalo, Predator):
                buffalo.perform_action(buffalos)
            else:
                buffalo.perform_action(grasses, predator)
            buffalo.move()
        
        x = [buffalo.x for buffalo in buffalos]
        y = [buffalo.y for buffalo in buffalos]   
        c = [buffalo.color for buffalo in buffalos]
        s = [buffalo.size for buffalo in buffalos]
        
        grass_x = [grass.x for grass in grasses]
        grass_y = [grass.y for grass in grasses]
        grass_c = [grass.color for grass in grasses]
        grass_s = [grass.size for grass in grasses]
        
        if plotRealTime or (i == Nt-1):
            plt.cla()
            plt.scatter(grass_x, grass_y, s=grass_s, c=grass_c)
            plt.scatter(x, y, s=s, c=c)
            ax.set(xlim=(0,L),ylim=(0,L))
            plt.pause(0.1)
            
    plt.show()

if __name__ == "__main__":
    main()