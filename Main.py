#source venv/bin/activate
 
import pygame
from Horse import Horse

# simple button class
class Button:
    def __init__(self, x, y, w, h, text, color, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.callback = callback

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        label = font.render(self.text, True, (255, 255, 255))
        screen.blit(label, (self.rect.x + 10, self.rect.y + 10))

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()

GREY = (128, 128, 128)
BLACK = (0, 0, 0)

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

#Game Setup
pygame.init()  

SCREEN_X = 1000
SCREEN_Y = 600
size = (SCREEN_X, SCREEN_Y)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Horse-E")
done = False
clock = pygame.time.Clock()

#Set up buttons for betting
buttons = []
font = pygame.font.SysFont(None, 36)
selected_bet = None

def make_bet(horse_name):
    global selected_bet
    selected_bet = horse_name
    print("You bet on:", selected_bet)

for i, horse in enumerate(horses):
    btn = Button((SCREEN_X - 200) / 2, 100 + i * 60, 200, 40, f"Bet on {horse.name}", BLACK, lambda name=horse.name: make_bet(name))
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
    
    if selected_bet is None:
        #Bet Screen
        for btn in buttons:
            btn.draw(screen, font)
    else:
        #Race
        for horse in horses:
            horse.update()
            horse.draw(screen)

 
    pygame.display.flip()
 
    clock.tick(60)
 

pygame.quit()