import pygame
import random

#Import keyboard constants to be used later
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


#Window size constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Define a player object by extending pygame.sprite.Sprite
#The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/jet.jpeg").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)       
        self.rect = self.surf.get_rect()
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        #Keep the player on screen at all times
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
                )
            )
        self.speed = random.randint(5, 20)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

clock = pygame.time.Clock()
#Initialize pygame
pygame.init()


#Creating the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Create a custom event for adding new enemies
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

#Instantiate player (its a rectangle for now)
player = Player()

#Create groups to hold enemy or all sprites
# Enemies is used for collision detection and position updates
# All is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
#Variable to keep the main loop running
running = True

#Main Loop
while running:
    
   
    #Get all events in the queue
    for event in pygame.event.get():
        #Keypress event
        if event.type == KEYDOWN:
            #If escape is hit, close the game
            if event.key == K_ESCAPE:
                running = False
        #If the window is closed, close the game
        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
    
    #Get all keys pressed and update position
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    
    #Update enemy position
    enemies.update()
    #Fill the screen with black
    screen.fill((0, 0, 0))
    
    #Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    #Check for collisions
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False
    #Flip everything to the display
    pygame.display.flip()

    #Ensure it has a decent framerate of 60
    clock.tick(60)



pygame.quit()