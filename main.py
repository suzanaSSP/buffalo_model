import pygame
from world import Grass
import random
from agent import Buffalo, Buffalo_Leader

pygame.init()

plotRealTime = True
width = 600
height = 600
Nt = 500
num_grass = 5
num_buffalos = 0

random.seed(42)

buffalos = [Buffalo(random.randint(0, width), random.randint(0, height)) for _ in range(num_buffalos)]
grasses = [Grass(random.randint(0,width), random.randint(0, height), random.randint(0,10)) for _ in range(num_grass)]

screen = pygame.display.set_mode((width, height))
leader = Buffalo_Leader(random.randint(0, width), random.randint(0, height))
buffalos.append(leader)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for time in range(Nt):
        if plotRealTime or (time == Nt-1):
            for grass in grasses:
                grass.decide_volume()
                grass.decide_capacity()
                pygame.draw.circle(screen, grass.color, (grass.x, grass.y), 25)

            for buffalo in buffalos:
                if isinstance(buffalo, Buffalo_Leader):
                    buffalo.perform_action(grasses)
                else:
                    buffalo.perform_action(grasses, leader)

                pygame.draw.circle(screen, buffalo.color, (buffalo.x, buffalo.y), 10)

            pygame.display.update()

        screen.fill((255, 255, 255))

pygame.quit()
