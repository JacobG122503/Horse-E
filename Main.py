#source venv/bin/activate
 
import pygame
import random
from Horse import Horse
from Names import Name_List

GREY = (128, 128, 128)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
DIRT = (118,85,43)
GOLD = (255, 215, 0)

colorsR = []
for i in range(6):
    colorsR.append((random.randint(0,255), random.randint(0,255), random.randint(0,255)))

#Button class
class Button:
    def __init__(self, x, y, w, h, text, color, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.callback = callback

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        label = font.render(self.text, True, BLACK)
        screen.blit(label, (self.rect.x + 10, self.rect.y + 10))

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()

#Game Setup
pygame.init()  

SCREEN_X = 1000
SCREEN_Y = 600
size = (SCREEN_X, SCREEN_Y)
screen = pygame.display.set_mode(size)

statusMessage = None
horsesOff = 0

pygame.display.set_caption("Horse-E")
done = False
clock = pygame.time.Clock()

OG_Names = Name_List[:] 
Names = OG_Names[:]

#Generate horses
horses = []
finishOrder = []
for i in range(6):
    name = Names.pop(random.randint(0, len(Names) - 1))
    horses.append(Horse(name, colorsR[i], 150 + (50 * i)))

#Set up buttons for betting
buttons = []
font = pygame.font.SysFont(None, 36)
selected_bet = None

def reset_race():
    global horses, finishOrder, selected_bet, statusMessage, horsesOff, buttons, Names
    #Reset Variables
    Names = OG_Names[:]
    selected_bet = None
    statusMessage = None
    horsesOff = 0
    finishOrder = []
    horses = []
    buttons = []
    #Generate new horses
    for i in range(6):
        name = Names.pop(random.randint(0, len(Names) - 1))
        horses.append(Horse(name, colorsR[i], 150 + (50 * i)))
    #Display new bet buttons
    for i, horse in enumerate(horses):
        btn = Button((SCREEN_X - 250) / 2, 100 + i * 60, 230, 40, f"Bet on {horse.name}", horse.color, lambda name=horse.name: make_bet(name))
        buttons.append(btn)

def make_bet(horse_name):
    global selected_bet, statusMessage
    selected_bet = horse_name
    statusMessage = "You bet on: " + str(selected_bet)

for i, horse in enumerate(horses):
    btn = Button((SCREEN_X - 250) / 2, 100 + i * 60, 230, 40, f"Bet on {horse.name}", horse.color, lambda name=horse.name: make_bet(name))
    buttons.append(btn)

#Game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for btn in buttons:
                btn.check_click(pos)
            if horsesOff == 6:
                race_again_btn.check_click(pos)

 
    #Generate dirt background
    original_tile = pygame.image.load("Images/Dirt.png").convert()
    dirt_tile = pygame.transform.scale(original_tile, (25, 25))
    tile_width, tile_height = dirt_tile.get_size()
    for x in range(0, SCREEN_X, tile_width):
        for y in range(0, SCREEN_Y, tile_height):
            screen.blit(dirt_tile, (x, y))

    #Draw top and bottom bars
    pygame.draw.rect(screen, GREY, (0, 0, SCREEN_X, 50))                          
    pygame.draw.rect(screen, GREY, (0, SCREEN_Y - 50, SCREEN_X, 50))
    pygame.draw.line(screen, BLACK, (0, 50), (SCREEN_X, 50), 3)                          
    pygame.draw.line(screen, BLACK, (0, SCREEN_Y-50), (SCREEN_X, SCREEN_Y-50), 3)
    
    if selected_bet is None:
        #Bet Screen
        for btn in buttons:
            btn.draw(screen, font)
    elif horsesOff != 6:
        #Race logic
        
        #Horse lanes
        for i in range(7):
            pygame.draw.line(screen, GREY, (0, 140 + (50 * i)), (SCREEN_X, 140 + (50 * i)), 4)
            
        #Finish line
        FINISH_LINE_X = SCREEN_X - 100  
        pygame.draw.line(screen, WHITE, (FINISH_LINE_X, 50), (FINISH_LINE_X, SCREEN_Y - 50), 4)

        #Progress line
        pygame.draw.line(screen, WHITE, (200, 25), (SCREEN_X - 200, 25), 5)
                        
        #Race start
        #Sorted to draw the highest x last, so that the highest x will always be on top on the progress bar
        for horse in sorted(horses, key=lambda h: h.x):
            #Update race horse
            horse.update()
            horse.draw(screen, font)
            #Update progress line horse
            horse.drawProgLine(screen, min(200 + ((SCREEN_X - 400) * (horse.x / FINISH_LINE_X)), SCREEN_X - 200), 20)
            #This is so horses still run and game doesn't insta end
            if not horse.isOffScreen and horse.x >= SCREEN_X + 50:
                horsesOff += 1
                horse.isOffScreen = True
            #If crossed finish line
            #30 is horse width
            if (horse.x + 30 >= FINISH_LINE_X): 
                if horse.isFinished: continue
                finishOrder.append(horse) 
                horse.isFinished = True

    #Status text
    if selected_bet is not None:
        status_font = pygame.font.SysFont(None, 28)
        status_text = status_font.render(f"{statusMessage}", True, BLACK)
        screen.blit(status_text, (20, SCREEN_Y - 40))  
        
    #Ranking screen
    if horsesOff == 6:
        pygame.draw.rect(screen, GREY, (100, 100, SCREEN_X - 200, SCREEN_Y - 200))
        pygame.draw.rect(screen, BLACK, (100, 100, SCREEN_X - 200, SCREEN_Y - 200), 3)
        
        screen.blit(status_font.render("Race Results", True, BLACK), ((SCREEN_X - 120) / 2, 120))
        i = 1
        for horse in finishOrder:
            if i == 1:
                color = GOLD
            else:
                color = BLACK
            screen.blit(status_font.render(f"{i}. {horse.name}", True, color), ((SCREEN_X - 200) / 2, 150 + (30*i)))
            i += 1
        #Race again
        race_again_btn = Button((SCREEN_X - 200) // 2, 420, 200, 40, "Race Again", GOLD, reset_race)
        race_again_btn.draw(screen, font)

 
    pygame.display.flip()
    clock.tick(60)
 

pygame.quit()
