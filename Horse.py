import pygame
import random

class Horse:
    def __init__(self, name, color, y):
        self.name = name
        self.color = color
        self.x = 0
        self.y = y
        self.speed = random.uniform(1, 3)

    def update(self):
        self.x += self.speed + random.uniform(0, 1)

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 30, 30))

        label = font.render(self.name, True, (0, 0, 0))
        screen.blit(label, (self.x - label.get_width() - 10, self.y + 5))
