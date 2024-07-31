import pygame
import sys
import random


pygame.init()


WIDTH, HEIGHT = 800, 600
FPS = 60


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")


player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 50, 50, 50)


enemies = []


bullets = []


clock = pygame.time.Clock()


numberofEnemies = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(player.centerx - 2, player.top, 4, 10)
                bullets.append(bullet)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 7.5
    if keys[pygame.K_RIGHT]:
        player.x += 7.5

    
    for bullet in bullets:
        bullet.y -= 10
        if bullet.y < 0:
            bullets.remove(bullet)

    
    if random.randint(0, 500) < 2:
        enemy = pygame.Rect(random.randint(0, WIDTH - 40), 0, 40, 40)
        enemies.append(enemy)
        numberofEnemies += 1
        if numberofEnemies > 6:
            enemies.remove(enemy)
            numberofEnemies = 0

    
    for enemy in enemies:
        enemy.y += 1  
        if enemy.y > HEIGHT:
            enemies.remove(enemy)

    if player.y > WIDTH:
        player.y = player.y


    
    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)

    
    screen.fill(BLACK)

    
    pygame.draw.rect(screen, GREEN, player)
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    
    pygame.display.flip()

    
    clock.tick(FPS)
