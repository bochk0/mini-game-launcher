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

def repair(self):
        # If we have sufficient money and the castle is not at full health
        if self.money >= 1500 and self.health < self.max_Health:
            self.health = self.health + 500
            if self.health > 999:
                self.health = self.max_Health
            self.money = self.money - 1500

    def armour(self):
        if self.money >= 1000:
            self.max_Health = self.max_Health + 250
            self.money = self.money - 1000


class Enemy(pygame.sprite.Sprite):
    # Constructor
    def __init__(self, speed, health, animation_list, x, y,):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.health = health
        self.animation_list = animation_list
        self.alive = True
        self.action = 0 # walk: 0, attack: 1, death: 2
        self.frame_index = 0

        # The variable that records when we last switched costume
        self.update_time = 0

        # Select starting costume
        # 2D list - animation_list = [ [walk], [attack], [death] ]
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, 30, 50)
        self.rect.center = (x, y)

        self.death_cooldown_counter = 0
        self.last_attack = 0


    # Object/clone methods
    def update(self, surface, target, bullet_group):
        if self.alive:
            # Check for collision with bullet clones
            if pygame.sprite.spritecollide(self, bullet_group, True):
                self.health = self.health - 25

            # Move enemy - to shift hitbox to the right on each frame
            if self.action == 0:
                self.rect.x = self.rect.x + self.speed

            # To attack and deal damage to the castle
            if self.action == 1:
                # Check If enough time has passed since the last attack
                if pygame.time.get_ticks() - self.last_attack > 1000:
                    target.health = target.health - 25

                    if target.health <= 0:
                        print("DIED")
                        target.health = 0

                    # Update the time stamp (self.last_attack)
                    # Set self.last_attack to present time stamp
                    self.last_attack = pygame.time.get_ticks()

            # Check if enemy has reached the castle
            if self.rect.right > target.rect.left:
                #print("I've reached the Castle")
                self.update_action(1)

            # check if enemy's health has dropped to 0
            if self.health <= 0:
                target.money = target.money + 100
                target.exp = target.exp + 1
                self.update_action(2)
                self.alive = False




        self.update_animation()

        # Draw the enemy clone and its hitbox
        #pygame.draw.rect(surface, (0, 255, 0), self.rect, 5)
        surface.blit(self.image, (self.rect.x - 80, self.rect.y - 20))


    def update_animation(self):

        # Define animation cooldown
        ANIMATION_COOLDOWN = 30

        DEATH_COOLDOWN = random.randint(350, 700)
        self.death_cooldown_counter = self.death_cooldown_counter + 1

        # Update costume as per the frame index (costume number)
        self.image = self.animation_list[self.action][self.frame_index]

        # Check if enough time has passed since we last changed costume
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index = self.frame_index + 1
            self.update_time = pygame.time.get_ticks()

        # If the animation has run out then reset it
        if self.frame_index >= 9:
            if self.action == 2:
                self.frame_index = 9

                # Check if enough time has passed before we delete a dead body
                if self.death_cooldown_counter >= DEATH_COOLDOWN:
                    self.kill()
            else:
                self.frame_index = 0


    def update_action(self, new_action):
        # Check if the new action is different than the current action
        if new_action != self.action:
            self.action = new_action

            # reset frame_index to 0 whenever it switches action
            self.frame_index = 0

            # Update time stamp
            self.update_time = pygame.time.get_ticks()


# Create a bullet group(list)
bullet_group = pygame.sprite.Group()

# Create a castle clone
castle1 = Castle(image100, image60, image30,  900, 800, 1.2)
# 750, 780, 1

# Create an enemy group (list)
enemy_group = pygame.sprite.Group()

# Load Button images
repair_img = pygame.image.load("PygameAssets/utility/download-removebg-preview (6).png")
armour_img = pygame.image.load("PygameAssets/utility/download-removebg-preview (7).png")

# Create two button clones


repair_button = Button(0, 0, repair_img, 0.2)
armour_button = Button(250, 0, armour_img, 0.2)

# MAIN GAME LOOP

run = True
while run:

    # clock.tick(60)

    # Paint the bg
    screen.blit(bg, (0, 0))

    if repair_button.draw(screen) == True:
        print("repair button is pressed")
        castle1.repair()

    if armour_button.draw(screen) == True:
        print("armour button is pressed")
        castle1.armour()

    # Paint the castle clones
    castle1.Draw()
    castle1.shoot()


    # Draw bullet clones
    bullet_group.update()
    bullet_group.draw(screen)

    # Set up HUD -> Heads Up Display                                    x   y
    draw_text("Money: $" + str(castle1.money), Font_HUD, (0, 255, 30), 900, 580)
    draw_text("Exp: " + str(castle1.exp), Font_HUD, (255, 205, 0), 900, 540)
    draw_text("Wave: " + str(Wave), Font_HUD, (255, 0, 0), 900, 500)
    draw_text(str(castle1.health) + '/' + str(castle1.max_Health), Font_HUD, (0,255, 0), 10, 50)


    if castle1.health > 0:

        # Health bar bg
        health_rect_max = pygame.Rect(850, 780, (castle1.max_Health / 4), 35)
        pygame.draw.rect(screen, (0, 0, 0), health_rect_max)

        # Figure out the color
        if castle1.health > 600:
            color = (0, 255, 0)
        elif 300 <= castle1.health <= 600:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)

        # Green overlay
        health_rect = pygame.Rect(850, 780, castle1.health / 4, 35)
        pygame.draw.rect(screen, color, health_rect)

        draw_text("Health: " + str(castle1.health), Font_HUD, (0, 170, 20), 850, 780)
    else:
        draw_text("YOU LOST!", Font_HUD, (255, 0, 0) , 850, 780)

    # Create if the target difficulty has been reached
    # Create an enemy clone in the main game loop
    if Wave_difficulty < Target_difficulty:

        # Check if enough time has lapsed since we last cloned an enemy
        if pygame.time.get_ticks() - last_enemy > ENEMY_TIMER:
            ARandomKnight = random.randint(0, 2)
            ARandomSpeed = random.randint(1, random.randint(3, 5))
            enemy = Enemy(ARandomSpeed, 100, master_enemy_animation[ARandomKnight], 50, SCREEN_HEIGHT - 50)

            # Update last_enemy (put a stamp when we create an enemy clone)
            last_enemy = pygame.time.get_ticks()

            enemy_group.add(enemy)

            # Increase wave difficulty by enemy health
            Wave_difficulty += 100

    # Check if all the enemies of a wave have been spawned
    if Wave_difficulty >= Target_difficulty:
        # Check how many enemy clones are still alive
        Enemies_alive = 0
        for e in enemy_group:
            if e.alive == True:
                Enemies_alive += 1
        # Proceed to the next wave if there is no more enemies alive from the previous wave
        if Enemies_alive == 0 and Next_wave == False:
            Next_wave = True
            Level_reset_time = pygame.time.get_ticks()  # Register current time stamp as soon as the wave has been completed

    # Move on to the next wave
    if Next_wave == True:
        draw_text('Wave ' + str(Wave) + ' Completed', Font_HUD, (0, 170, 0), 450, 500)
        # Check if sufficient time has passed since we cleared the wave.
        if pygame.time.get_ticks() - Level_reset_time > 5000:
            Next_wave = False
            Wave = Wave + 1

            # Reset enemy spawning parameters
            Last_enemy = pygame.time.get_ticks()
            Wave_difficulty = 0
            Target_difficulty *= Difficulty_multiplier
            enemy_group.empty()


    enemy_group.update(screen, castle1, bullet_group)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # Update display window ( Refresh the Main Game Screen )
    pygame.display.update()

pygame.quit()
