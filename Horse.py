import pygame
import random

class Horse:
    isFinished = False
    
    def __init__(self, name, color, y):
        self.name = name
        self.color = color
        self.x = 0
        self.y = y
        self.speed = random.uniform(1, 5) 
        #Animation
        self.horseFrames = [pygame.transform.scale(pygame.image.load(f"HorseFrames/frame{i+1}.png"), (125, 125)) for i in range(6)]
        self.frame = 0
        self.animation_speed = 0.2 


    def update(self):
        self.x += self.speed + random.uniform(0, 1)
        self.frame = (self.frame + self.animation_speed) % 6

    def draw(self, screen, font):
        currentFrame = self.horseFrames[int(self.frame)]
        screen.blit(currentFrame, (self.x, self.y - (currentFrame.get_height() - 30) / 2))

        label = font.render(self.name, True, (0, 0, 0))
        screen.blit(label, (self.x - label.get_width() - 10, self.y + 5))
