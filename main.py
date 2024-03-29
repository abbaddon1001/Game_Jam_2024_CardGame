import pygame

## Displaying battle window

pygame.init()

clock = pygame.time.Clock()
fps   = 30

## Game window
bottom_menu = 200
height = 512
width = 206 + bottom_menu
screen = pygame.display.set_mode((height, width))
pygame.display.set_caption('Comedy Dungeon')

## Loading background image
backgroundImage = pygame.image.load('Assets/Backgrounds/sky_background.jpg').convert_alpha()

## Menu image
panelImage = pygame.image.load('Assets/Backgrounds/blue_menu.png').convert_alpha()



## Function for drawing background
def draw_background():
    screen.blit(backgroundImage, (0,0))

## Function to draw bottom panel menu
def draw_bottom():
    screen.blit(panelImage, (0, height-bottom_menu-50))

def draw_laugh_meter(boss):
    # Calculate the position to center the rectangle
    x = boss.rect.centerx - 100  
    y = boss.rect.y - 20  

    # Draw the background of the laugh meter
    pygame.draw.rect(screen, (74, 25, 25), (x, y, 200, 20))

    # Calculate the width of the filled portion based on the laugh meter value
    filled_width = (boss.laugh_meter / boss.max_laugh_meter) * 200 

    # Draw the filled portion of the laugh meter
    pygame.draw.rect(screen, (255, 0, 0), (x, y, filled_width, 20))

    # Render and blit the text "Laughter Meter" above the bar
    font = pygame.font.Font(None, 36)
    text = font.render("Laughter Meter", True, (255, 255, 255))
    text_rect = text.get_rect(center=(boss.rect.centerx, y - 20))  
    screen.blit(text, text_rect)




##Player class
class Player():
    def __init__(self, draw_card=False, shuffle_deck=False, select_card=False, win=False):
        self.player_cards = []
        self.draw_card = False
        self.shuffle_deck = False
        self.select_card = False
        self.win = False

## Deck class
class Deck():
    def __init__(x,y,self, cardList):
        self.cardList = cardList
        length = cardList.length
        deck_image = pygame.image.load('Assets/Cards/Deck.jpg')
        self.image = pygame.transform.scale(deck_image,(deck_image.get_width() / 3.5, deck_image.get_height() / 3.5))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)




## Card Class

class Card():
    def __init__(self, x,y, front_card, mechanic, laugh_damage):
        self.flipped_state = False
        self.mechanic = mechanic
        self.laugh_damage = laugh_damage
        back_card_img = pygame.image.load(f'Assets/Cards/Card Sleeve.png').convert_alpha()
        self.front_card = pygame.image.load(f'Assets/Memes/{front_card}.jpg')
        self.image = pygame.transform.scale(back_card_img, (back_card_img.get_width()/3.5, back_card_img.get_height()/3.5))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def on_click(self):
        self.image = pygame.transform.scale(self.front_card, (self.front_card.get_width()/3.5, self.front_card.get_height()/3.5))
        self.flipped_state = True
    def draw(self):
        screen.blit(self.image,self.rect)

    def play(self, boss):
        # Increment the laugh meter of the boss
        boss.laugh_meter += self.laugh_damage
        boss.laugh_meter = min(boss.laugh_meter, boss.max_laugh_meter)

##Boss Class
class Boss():
    def __init__(self, x,y, name, hp):
        self.name = name
        self.laugh = False
        self.max_laugh_meter = hp 
        self.laugh_meter = 0
        self.hp    = hp
        self.alive = True
        self.boss_image = pygame.image.load(f'Assets/Sprites/{self.name}/boss.png').convert_alpha()
        self.laugh_image = pygame.image.load(f'Assets/Sprites/{self.name}/laugh.png').convert_alpha()
        self.defeat_image = pygame.image.load(f'Assets/Sprites/{self.name}/defeat.png').convert_alpha()
        self.current_image = self.boss_image
        self.image = pygame.transform.scale(self.current_image, (self.current_image.get_width()/2, self.current_image.get_height()/2))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update_image(self):
        if self.laugh_meter > 0.5 * self.max_laugh_meter:
            self.current_image = self.laugh_image
        elif self.laugh_meter >= self.max_laugh_meter:
            self.current_image = self.defeat_image
        else:
            self.current_image = self.boss_image

    def draw(self):
        screen.blit(self.image, self.rect)

## Loading example Boss fight
Pringles = Boss(height/2, width/2.5, 'pringles', 200)



## card list
# cardList = []
# for i in range(1,11):
#     x = 64
#     card = Card(x, height-bottom_menu+25, str(i), 'Damage', 10)
#     cardList.append(card)
#     x += 64

## Creating a player
player = Player()

## initializing card deck

x=64

for i in range(1,6):
    card = Card(x, height - bottom_menu + 25, str(i), 'Damage', 20)
    player.player_cards.append(card)
    x=x+64


while True:

    clock.tick(fps)

    draw_background()
    draw_bottom()


    ## Draw entities
    
    Pringles.update_image()
    Pringles.draw()
    draw_laugh_meter(Pringles)
    

    for card in player.player_cards:
        card.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            for card in player.player_cards:
                if card.rect.collidepoint(mouse_pos) and card.flipped_state!=True:
                    card.on_click()

                if card.rect.collidepoint(mouse_pos) and card.flipped_state==True:
                    card.play(Pringles)
                    # Additional logic can be added here, such as removing the card from the player's hand

    pygame.display.update()
