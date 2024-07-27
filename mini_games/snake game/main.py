import pygame
from level1 import level_1
from level2 import level_2
from level3 import level_3
pygame.font.init()

screen_width = 700
screen_height = 500
exit_game = False
white = (255,255,255)
black = (0,0,0)

def screen_text(text,color,x,y,size):
    font = pygame.font.SysFont(None, size)
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])


# creating Display 
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('SNAKE GAME')
while not exit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                game = level_1()
                game.Game_loop()
            if event.key == pygame.K_2:
                game = level_2()
                game.Game_loop()
            if event.key == pygame.K_3:
                game = level_3()
                game.Game_loop()
    gameWindow.fill(white)
    screen_text('Welcome to the World of Snakes!', black, 150, 180 , 40)
    screen_text('Press "1" for Level 1!', black, 250, 230 , 27)
    screen_text('Press "2" for Level 1!', black, 250, 260 , 27)
    screen_text('Press "3" for Level 1!', black, 250, 290 , 27)
    pygame.display.update()