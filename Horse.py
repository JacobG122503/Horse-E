import pygame
import random

class Horse:
    def __init__(self, name, color, y):
        self.isFinished = False
        self.isOffScreen = False
        self.name = name
        self.color = color
        self.x = 0
        self.y = y
        self.speed = random.uniform(.5, 1) 
        self.buffOrNerf = 0
        
        #Animation
        self.frame = 0
        self.animation_speed = 0.2 
        self.horseFrames = []
        
        #Tint them for their color
        for i in range(6):
            img = pygame.image.load(f"Images/frame{i+1}.png").convert_alpha()
            img = pygame.transform.scale(img, (125, 125))
            tint_surface = pygame.Surface(img.get_size()).convert_alpha()
            tint_surface.fill(self.color + (255,))
            img.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.horseFrames.append(img)
            
        #Decide if Blessed
        if random.uniform(0, 100) < 15:
            self.blessed = True
            self.name += "-b"
            self.speed = random.uniform(1,1.5)
            
    def update(self):
        #Horse may get tired or burst of energy
        if random.uniform(0,100) < 1:
            #Tired
            if random.uniform(0,100) < 50:
                self.buffOrNerf = -.25
                #self.name += "-t"
            else:
                self.buffOrNerf = .25
                #self.name += "-s"
        self.x += self.speed + random.uniform(0, 1) + self.buffOrNerf
        self.frame = (self.frame + self.animation_speed) % 6

    def draw(self, screen, font):
        currentFrame = self.horseFrames[int(self.frame)]
        imgX = self.x - (currentFrame.get_width() - 70)
        imgY = self.y - (currentFrame.get_height() - 30) / 2
        screen.blit(currentFrame, (imgX, imgY))

        label = font.render(self.name, True, (0, 0, 0))
        screen.blit(label, (self.x - label.get_width() - 35, self.y + 5))
        
    def drawProgLine(self, screen, x, y):
        currentFrame = self.horseFrames[int(self.frame)]
        smallFrame = pygame.transform.scale(currentFrame, (80, 80))
        imgX = x - (smallFrame.get_width() - 40)
        imgY = y - (smallFrame.get_height() + 10) / 2
        screen.blit(smallFrame, (imgX, imgY))
        #pygame.draw.rect(screen, self.color, (x, y, 10, 10))

