#source venv/bin/activate
 
import pygame
from Horse import Horse

GREY = (128, 128, 128)

colors = [
    (255, 0, 0),    #Red
    (0, 0, 0),      #Black
    (255, 255, 255),#White
    (0, 255, 0),    #Green
    (60, 179, 113), #MediumSeaGreen
]

horses = []

for i in range(5):
    horses.append(Horse("Horse" + str(i), colors[i], 100 + (50*i)))

 
pygame.init()
 
size = (1000, 600)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Horse-E")
 
done = False
 
clock = pygame.time.Clock()
 
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    screen.fill(GREY)
    
    #Race start
    for horse in horses:
        horse.update()
        horse.draw(screen)
 
    pygame.display.flip()
 
    clock.tick(60)
 

pygame.quit()