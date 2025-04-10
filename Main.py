#source venv/bin/activate
 
import pygame
import random
from Horse import Horse
from Names import Names

GREY = (128, 128, 128)
BLACK = (0, 0, 0)

colors = [
    (255, 0, 0),      #Red
    (255, 165, 0),    #Orange
    (255, 255, 0),    #Yellow
    (0, 255, 0),      #Green
    (0, 0, 255),      #Blue
    (128, 0, 128),    #Purple
]

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

#Generate horses
horses = []
for i in range(6):
    name = Names.pop(random.randint(0, len(Names) - 1))
    horses.append(Horse(name, colors[i], 150 + (50 * i)))

#Game Setup
pygame.init()  

SCREEN_X = 1000
SCREEN_Y = 600
size = (SCREEN_X, SCREEN_Y)
screen = pygame.display.set_mode(size)

statusMessage = None
raceOver = False

pygame.display.set_caption("Horse-E")
done = False
clock = pygame.time.Clock()

#Set up buttons for betting
buttons = []
font = pygame.font.SysFont(None, 36)
selected_bet = None

def make_bet(horse_name):
    global selected_bet, statusMessage
    selected_bet = horse_name
    statusMessage = "You bet on: " + str(selected_bet)

for i, horse in enumerate(horses):
    btn = Button((SCREEN_X - 200) / 2, 100 + i * 60, 220, 40, f"Bet on {horse.name}", horse.color, lambda name=horse.name: make_bet(name))
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
 
    screen.fill(GREY)
    
    #Finish Line
    FINISH_LINE_X = SCREEN_X - 100  
    pygame.draw.line(screen, (255, 255, 255), (FINISH_LINE_X, 50), (FINISH_LINE_X, SCREEN_Y - 50), 4)
    
    if selected_bet is None:
        #Bet Screen
        for btn in buttons:
            btn.draw(screen, font)
    else:
        #Race
        for horse in horses:
            horse.update()
            horse.draw(screen, font)
            #If crossed finish line
            #30 is horse width
            if (horse.x + 30 >= FINISH_LINE_X) and not raceOver:  
                raceOver = True
                statusMessage = f"{horse.name} has won the race!"
 
    #Draw top and bottom bars
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_X, 50))                          
    pygame.draw.rect(screen, BLACK, (0, SCREEN_Y - 50, SCREEN_X, 50))

    #Status text
    if selected_bet is not None:
        status_font = pygame.font.SysFont(None, 28)
        status_text = status_font.render(f"{statusMessage}", True, (255, 255, 255))
        screen.blit(status_text, (20, SCREEN_Y - 40))  
 
    pygame.display.flip()
    clock.tick(60)
 

pygame.quit()