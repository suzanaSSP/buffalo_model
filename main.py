from world import Grass
import random
from agent import Buffalo, Predator, BuffaloLeader
import matplotlib.pyplot as plt
import math

plotRealTime = True
L = 1000
min_value = 200
max_value = 700
Nt = 1000
num_grass = 30
num_buffalos = 30

predator = Predator(random.randint(min_value, max_value), random.randint(min_value, max_value))
buffalo_leader = BuffaloLeader(random.randint(min_value, max_value), random.randint(min_value, max_value))
buffalos = [Buffalo(random.randint(min_value, max_value), random.randint(min_value, max_value), buffalo_leader, predator) for _ in range(num_buffalos)]
grasses = [Grass(random.randint(0, L), random.randint(0, L), random.randint(0,10)) for _ in range(num_grass)]

buffalos.append(buffalo_leader)
buffalos.append(predator)


def perfom_agent_actions(buffalos, grasses):
    for grass in grasses:
            grass.perform_action()
        
    for buffalo in buffalos:

        if isinstance(buffalo, Predator):
            if buffalo.satisfaction < -50:
                buffalos.remove(buffalo)
            else:
                buffalo.perform_action(buffalos)
        else:
            if buffalo.satisfaction < -50 or math.dist(buffalo.c, predator.c) < 50:
                buffalos.remove(buffalo)
            else:
                buffalo.perform_action(grasses, buffalos)


def main_simulation(buffalos, grasses):
    fig, ax = plt.subplots()

    for i in range(Nt):

        # Define what state each agent is at and calculate next position
        perfom_agent_actions(buffalos, grasses)

        # Update values all at the same time
        for buffalo in buffalos:
            buffalo.update()
        
        x = [buffalo.x if buffalo.x <= L else buffalo.x - 100 for buffalo in buffalos]
        y = [buffalo.y if buffalo.y <= L else buffalo.y - 100 for buffalo in buffalos]   
        c = [buffalo.color for buffalo in buffalos]
        
        grass_x = [grass.x if grass.x <=L else grass.x - 100 for grass in grasses]
        grass_y = [grass.y if grass.y <=L else grass.y - 100 for grass in grasses]
        grass_c = [grass.color for grass in grasses]
        grass_s = [grass.size for grass in grasses]

        if plotRealTime or (i == Nt-1):
            plt.cla()
            # ax.add_artist(radius_circle)
            plt.scatter(grass_x, grass_y, s=grass_s, c=grass_c)
            plt.scatter(x, y, s=100, c=c)    
            ax.set(xlim=(0,L),ylim=(0,L))
            plt.pause(0.1)
            
            chosen_grass = grasses[9]
            print(chosen_grass.volume)
            if not chosen_grass.switch:
                print(chosen_grass.switch)
   
    plt.show()

if __name__ == '__main__':
    main_simulation(buffalos, grasses)
 