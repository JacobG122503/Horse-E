#source venv/bin/activate
 
import pygame
from Horse import Horse
 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)

horses = [
    Horse("Red", RED, 100),
    Horse("Green", GREEN, 150),
    Horse("Black", BLACK, 200),
]
 
pygame.init()
 
size = (1000, 600)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
done = False
 
clock = pygame.time.Clock()
 
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    screen.fill(GREY)
    
    for horse in horses:
        horse.update()
        horse.draw(screen)
 
    pygame.display.flip()
 
    clock.tick(60)
 

pygame.quit()