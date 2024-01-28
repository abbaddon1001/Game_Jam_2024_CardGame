import pygame

## Displaying battle window

pygame.init()

clock = pygame.time.Clock()
fps   = 30

stage_counter = 0

## Game window
bottom_menu = 200
height = 512
width = 206 + bottom_menu
screen = pygame.display.set_mode((height, width))
pygame.display.set_caption('Comedy Dungeon')

## Loading background image
backgroundImage = pygame.image.load('Assets/Backgrounds/background.png').convert_alpha()
backgroundImage = pygame.transform.scale(backgroundImage, (650, 512))

## Menu image
panelImage = pygame.image.load('Assets/Backgrounds/bottom_menu.png').convert_alpha()
panelImage = pygame.transform.scale(panelImage, (520, 300))

# Initialize game state
game_state = "TITLE"

# Display title screen
title_font = pygame.font.Font('Assets/Fonts/Ancient Medium 500.ttf', 60)
title_text = title_font.render("COMEDY DUNGEON", True, (217, 177, 145))
title_text_rect = title_text.get_rect(center=(width/1.59, height/3))

click_font = pygame.font.Font('Assets/Fonts/Ancient Medium 500.ttf', 30)
click_text = click_font.render("Click to play", True, (217, 177, 145))
click_text_rect = click_text.get_rect(center=(width/5, height/1.5))

title_screen_background = pygame.image.load('Assets/Backgrounds/background.png').convert_alpha()
title_screen_background = pygame.transform.scale(title_screen_background, (650, 512))

# Display title screen
while game_state == "TITLE":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            game_state = "PLAY"

    screen.blit(title_screen_background, (0, 0))
    screen.blit(title_text, title_text_rect)
    screen.blit(click_text, click_text_rect)
    pygame.display.update()

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
    pygame.draw.rect(screen, (255, 57, 46), (x, y, filled_width, 20))

    # Render and blit the text "Laughter Meter" above the bar
    font = pygame.font.Font('Assets/Fonts/Ancient Medium 500.ttf', 36)
    text = font.render("Laughter Meter", True, (217, 177, 145))
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


## Card Class

class Card():
    def __init__(self, x,y, name, mechanic, laugh_damage):
        self.name = name
        self.mechanic = mechanic
        self.laugh_damage = laugh_damage
        card_img = pygame.image.load(f'Assets/Cards/{self.name}.jpg').convert_alpha()
        self.image = pygame.transform.scale(card_img, (card_img.get_width()/3.5, card_img.get_height()/3.5))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

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
        self.hp = hp
        self.alive = True
        self.boss_image = pygame.image.load(f'Assets/Sprites/{self.name}/boss.png').convert_alpha()
        self.laugh_image = pygame.image.load(f'Assets/Sprites/{self.name}/laugh.png').convert_alpha()
        self.defeat_image = pygame.image.load(f'Assets/Sprites/{self.name}/defeat.png').convert_alpha()
        self.current_image = self.boss_image
        self.image = pygame.transform.scale(self.current_image, (self.current_image.get_width()/2, self.current_image.get_height()/2))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.defeated_font = pygame.font.Font(None, 72)
        self.defeated_text = self.defeated_font.render("DEFEATED", True, (255, 0, 0))
        self.defeated_text_rect = self.defeated_text.get_rect(center=self.rect.center)


    def update_image(self):
        if self.laugh_meter >= self.max_laugh_meter:
            self.current_image = self.defeat_image
        elif self.laugh_meter > 0.5 * self.max_laugh_meter:
            self.current_image = self.laugh_image
        else:
            self.current_image = self.boss_image

        # Scale the current image and update the rect
        self.image = pygame.transform.scale(self.current_image, (self.current_image.get_width() // 2, self.current_image.get_height() // 2))
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self):
        screen.blit(self.image, self.rect)

        if self.laugh_meter >= self.max_laugh_meter:
            screen.blit(self.defeated_text, self.defeated_text_rect)

## Loading Boss fight
current_boss_name = 'pringles'
current_boss = Boss(height/2, width/2.5, current_boss_name, 100)

## Creating a player
player = Player()


## initializing and displaying 5 cards
x=64
for i in range(5):
    card = Card(x, height - bottom_menu + 25, 'Card Sleeve', 'Damage', 20)
    player.player_cards.append(card)
    x=x+64


# New game state for "BOSS DEFEATED" screen
defeated_state_font = pygame.font.Font('Assets/Fonts/Ancient Medium 500.ttf', 60)
defeated_state_text = defeated_state_font.render("BOSS DEFEATED", True, (217, 177, 145))
defeated_state_text_rect = defeated_state_text.get_rect(center=(width/1.59, height/3))

next_stage_font = pygame.font.Font('Assets/Fonts/Ancient Medium 500.ttf', 30)
next_stage_text = next_stage_font.render("Click to play next stage", True, (217, 177, 145))
next_stage_text_rect = next_stage_text.get_rect(center=(width/1.5, height/1.5))


game_over_font = pygame.font.Font('Assets/Fonts/Ancient Medium 500.ttf', 60)
game_over_text = game_over_font.render("GAME OVER", True, (217, 177, 145))
game_over_text_rect = game_over_text.get_rect(center=(width/1.59, height/3))



while True:

    clock.tick(fps)


    if game_state == "GAME_OVER":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(title_screen_background, (0, 0))
        screen.blit(game_over_text, game_over_text_rect)
        pygame.display.update()
        
    if game_state == "BOSS_DEFEATED":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                game_state = "PLAY"

        screen.blit(title_screen_background, (0, 0))
        screen.blit(defeated_state_text, defeated_state_text_rect)
        screen.blit(next_stage_text, next_stage_text_rect)
        pygame.display.update()

    if game_state == "PLAY":

        draw_background()
        draw_bottom()

        ## Draw entities
        
        current_boss.update_image()
        current_boss.draw()
        draw_laugh_meter(current_boss)


        if current_boss.laugh_meter >= current_boss.max_laugh_meter:
            # Switch to the new boss after defeating the current boss
            if stage_counter == 1:
                game_state = "GAME_OVER"

            else: 
                game_state = "BOSS_DEFEATED"
                stage_counter+=1
                print(stage_counter)
                current_boss_name = 'pepe'
                current_boss = Boss(height/2, width/2.5, current_boss_name, 200)


        for card in player.player_cards:
            card.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                for card in player.player_cards:
                    if card.rect.collidepoint(mouse_pos):

                        card.play(current_boss)

    pygame.display.update()
l