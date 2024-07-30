# Import libraries
import pygame
import math
import random

# Initialize pygame
pygame.init()

# Define some game variables
Wave = 1
Wave_difficulty = 0
Target_difficulty = 1000
Difficulty_multiplier = 1.1
Game_over = False
Next_wave= False
Enemies_alive = 0

ENEMY_TIMER = random.randint(1000, 2000)

# get_ticks() -> returns the current time stamp registered in pygame
last_enemy = pygame.time.get_ticks()

# Declare game screen dimension
SCREEN_WIDTH = 1200  # X
SCREEN_HEIGHT = 1000  # Y

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PROTECT NO ONE CASTLE DEFENSE GAME")

# Create a clock object
clock = pygame.time.Clock()
FPS = 60

# Load all images
bg = pygame.transform.scale(pygame.image.load("PygameAssets/bg/BG.JPEG"), (SCREEN_WIDTH, SCREEN_HEIGHT))
image100 = pygame.image.load("PygameAssets/castle/images-removebg-preview.png")
image60 = pygame.image.load("PygameAssets/castle/pixil-frame-0-removebg-preview.png")
image30 = pygame.image.load("PygameAssets/castle/pixil-frame-0__1_-removebg-preview.png")

bullet_image = pygame.image.load("PygameAssets/weapon/download-removebg-preview (5).png")
b_w = bullet_image.get_width()
b_h = bullet_image.get_height()
bullet_image = pygame.transform.scale(bullet_image, (int(b_w * 0.2), int(b_h * 0.2)))

# Define some game fonts
Font_HUD = pygame.font.SysFont("No One", 60)  # HUD = Heads Up Display

# Define a function to display text on the screen
def draw_text(text, font, colour, x, y):
    # To render some text using pygame's font component
    label = font.render(text, True, colour)
    screen.blit(label, (x, y))


# Play BG music
pygame.mixer.music.load('PygameAssets/spotifydown.com - Ghost.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.03)


# Music

# Parameters to load enemy images
# Enemy_Types = ['1_KNIGHT', '2_KNIGHT', '3_KNIGHT'] (For in-case use)
# Creating animation_type list
# animation_types = ['attack', 'death', 'walk'] (For in-case use)

# Nested for loops used to load all enemy images
master_enemy_animation = []  # A 3D list [ [ [], [], [] ], [ [], [], [] ], [ [], [], [] ] ]
Enemy_Types = ['1_KNIGHT', '2_KNIGHT', '3_KNIGHT']
animation_types = ['walk', 'attack', 'death']

for eachEnemyType in Enemy_Types:
    animation_list = []

    for EachAnimationType in animation_types:
        temp_list = []  # It is used to keep all 10 images of an animation
        for EachImage in range(0, 10, 1):
            img = pygame.image.load(f'PygameAssets/enemies/{eachEnemyType}/{EachAnimationType}/{EachImage}.png')
            e_w = img.get_width()
            e_h = img.get_height()
            img = pygame.transform.scale(img, (int(e_w * 0.1), int(e_h * 0.1)))
            temp_list.append(img)
            # By the end of this for loop, 10 images will be loaded and stored into the 'temp_list' list
        # By the end of this 'for loop', it would have loaded all 3 animation sequences opf an enemy type
        animation_list.append(temp_list)
    master_enemy_animation.append(animation_list)

"""
temp_list = [0, 1, 2, ..., 9.png]
animation_list = [ [0, 1, 2, ..., 9.png], [0, 1, 2, ..., 9.png], [0, 1, 2, ..., 9.png] ]   
"""


# Object-Oriented Programming (OOP)


# Bullet Class - This class inherits properties for Pygame sprite class
class Bullet(pygame.sprite.Sprite):
    # Constructor
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle)
        self.speed = 15
        self.gravity_induced_speed = 0
        self.vel_x = 0  # Initial x-velocity of a projectile clone
        self.vel_y = 0  # Initial y-velocity of a projectile clone


    def update(self):
        # The driver code that moves a projectile on each frame
        self.vel_x = self.speed * math.cos(self.angle)
        self.vel_y = -(self.speed * math.sin(self.angle))
        self.rect.x = self.rect.x + self.vel_x
        self.rect.y = self.rect.y + (self.vel_y + self.gravity_induced_speed)
        self.gravity_induced_speed += 0.4




# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Constructor
class CrossHair1(pygame.sprite.Sprite):
    def __init__(self, scale):
        image = pygame.image.load('PygameAssets/utility/No BG CrossHair.png')
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    def draw(self):
        mx, my = pygame.mouse.get_pos()
        self.rect.center = (mx, my)
        screen.blit(self.image, self.rect)
        self.CrossHair1.draw()


class Button():
    # Define Constructor
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    # Draw the button clones on the screen
    def draw(self, screen):

        action = False

        # Get Mouse Position
        pos = pygame.mouse.get_pos()

        # Check mouse hover and click conditions
        if self.rect.collidepoint(pos):
            # If the left mouse button ia pressed and the button is not already being pressed
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        # To reset the button when it left the mouse button is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        screen.blit(self.image, (self.rect.x , self.rect.y))


        # Return the status of a button
        return action



class Castle():
    # Constructor | Used to create a castle object/clone
    # The constructor kicks-in as soon as we crate a castle clone
    def __init__(self, image100, image60, image30, x, y, scale):
        # HEALTH OF THE CASTLE ( MAX_HEALTH )
        self.wave = 1
        self.health = 1000
        self.max_Health = self.health
        width = image100.get_width()
        height = image100.get_height()
        self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
        self.image60 = pygame.transform.scale(image60, (int(width * scale), int(height * scale)))
        self.image30 = pygame.transform.scale(image30, (int(width * scale), int(height * scale)))

        # Hit box for collision detection
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.fired = False
        self.money = 0
        self.exp = 0

    #   Object Method ( a certain action a castle clone can perform )
    def Draw(self):
        # Check which costume to be loaded on self.health
        if self.health > 600:
            self.image = self.image100
        elif 300 <= self.health <= 600:
            self.image = self.image60
        else:
            self.image = self.image30
        screen.blit(self.image, self.rect)

    def shoot(self):
        # Identify mouse position
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.topleft[0]
        y_dist = -(pos[1] - self.rect.topleft[1])
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        # random.randint(5,10)

        pygame.draw.line(screen, (255, 0, 0), (self.rect.center[0], self.rect.center[1]), pos, width=random.randint(5, 7))

        # Get mouse-click event
        if pygame.mouse.get_pressed()[0] and self.fired == False:
            self.fired = True
            bullet = Bullet(bullet_image, self.rect.center[0], self.rect.center[1], self.angle)
            bullet_group.add(bullet)

        # Reset mouse-click event when LMB (Left mouse button) is released
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False

