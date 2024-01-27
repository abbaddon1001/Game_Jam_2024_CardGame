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


##Player class
class Player():
    def __init__(self, draw_card, shuffle_deck, select_card):
        self.draw_card = False
        self.shuffle_deck = False
        self.select_card = False
        self.win = False

##Boss Class
class Boss():
    def __init__(self, x,y, name, hp):
        self.name = name
        self.laugh = False
        self.hp    = hp
        self.alive = True
        boss_image = pygame.image.load(f'Assets/Sprites/{self.name}/boss.png').convert_alpha()
        self.image = pygame.transform.scale(boss_image, (boss_image.get_width()/5, boss_image.get_height()/5))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def draw(self):
        screen.blit(self.image, self.rect)

## Loading example Boss fight
Pringles = Boss(height/2, width/2.2, 'pringles', 200 )



while True:

    clock.tick(fps)

    draw_background()
    draw_bottom()

    ## Draw entities
    Pringles.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
