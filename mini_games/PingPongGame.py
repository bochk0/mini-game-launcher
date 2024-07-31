

import pygame
import sys


pygame.init()


WIDTH, HEIGHT = 800, 600
BALL_SPEED = [5, 5]
PADDLE_SPEED = 10


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")


player_paddle = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 20, 100, 10)
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)


clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_paddle.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT]:
        player_paddle.x += PADDLE_SPEED

    
    ball.x += BALL_SPEED[0]
    ball.y += BALL_SPEED[1]

    
    if ball.left <= 0 or ball.right >= WIDTH:
        BALL_SPEED[0] = -BALL_SPEED[0]
    if ball.top <= 0 or ball.colliderect(player_paddle):
        BALL_SPEED[1] = -BALL_SPEED[1]

    
    screen.fill(BLACK)

    
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    
    pygame.display.flip()

    
    clock.tick(60)
