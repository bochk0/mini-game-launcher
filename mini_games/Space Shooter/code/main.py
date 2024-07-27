import pygame
from random import randint,uniform
from os.path import join
import os

dir = 'D:\\code\\python vs code\\pyton Exercises\\PYTHON GAMES\\Space Shooter'
os.chdir(dir)
# import time

class player (pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        path_player = join('images','player.png')
        self.image = pygame.image.load(f'{path_player}').convert_alpha()
        self.rect = self.image.get_frect(center = (screen_width/2,screen_height/2))
        self.player_direction = pygame.math.Vector2()
        self.player_speed = 300

        #cooldown timing
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

        #mask 
        self.mask = pygame.mask.from_surface(self.image)

    def laser_cooldown(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
    
    def update(self,dt):
        self.player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) + int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.player_direction.y =   int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]) + int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.player_direction = self.player_direction.normalize() if self.player_direction else self.player_direction
        self.rect.center += self.player_direction * self.player_speed * dt
        if separate_key[pygame.K_SPACE] and self.can_shoot:
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser(laser_surf,self.rect.midtop,(all_sprites,laser_sprites))
            laser_sound.play()
        
class star(pygame.sprite.Sprite):
    def __init__ (self,groups,star_surf):
        super().__init__(groups)
        x = randint(0, screen_width)
        y = randint(0,screen_height)
        self.image = star_surf
        self.rect = self.image.get_frect(center = (x,y))

class laser(pygame.sprite.Sprite):
    def __init__ (self, surf,pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        
        # self.laser_direction = pygame.math.Vector2()
    def update(self,dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0 :
            self.kill()

class meteor(pygame.sprite.Sprite):
    def __init__(self,surf, pos,groups):
        super(). __init__ (groups)
        self.original_surf = surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = pos)
        self.meteor_creation_time = pygame.time.get_ticks()
        self.meteor_duration = 3500
        self.speed = randint(200,400)
        self.direction = pygame.math.Vector2(uniform(-0.5,0.5),1)
        self.rotation_speed = randint(30,60)
        self.rotation = 0

    def update(self,dt):
        self.rect.center += self.direction * self.speed * dt 
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf,self.rotation,1)
        self.rect = self.image.get_frect(center = self.rect.center)
        if pygame.time.get_ticks() - self.meteor_creation_time >= self.meteor_duration :
            # print("here")
            self.kill()

class animatedExplosion(pygame.sprite.Sprite):
    def __init__(self,frames,pos,groups):
        super().__init__(groups)
        self.frames = frames
        self.frames_index = 0
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_frect(center = pos)
    
    def update(self,dt):
        self.frames_index += 20 * dt
        if self.frames_index < len(self.frames):
            self.image = self.frames[int(self.frames_index)]
        else:
            self.kill()

def collision():
    global game_over
    collision_player = pygame.sprite.spritecollide(player,meteor_sprites,True, pygame.sprite.collide_mask)
    if collision_player:
        damage_sound.play()
        game_over = True
    for laser in laser_sprites:
        collision_lasers = pygame.sprite.spritecollide(laser,meteor_sprites,True)
        if collision_lasers:
            animatedExplosion(explosion_frames,laser.rect.midtop,all_sprites)
            explosion_sound.play()
            laser.kill()

def display_text(text1,color,pos,condition,rect = (0,0),move = (0,0) ,border_width = 0,radius = 0):
    text1_surf = font.render(text1, True, color)
    text1_rect = text1_surf.get_frect(midbottom = pos)
    gameWindow.blit(text1_surf, text1_rect)
    if condition == True:
        pygame.draw.rect(gameWindow,color,text1_rect.inflate(rect).move(move) ,border_width,radius)

def display_score(score):
    current_time = pygame.time.get_ticks() // 100
    display_text(str(current_time),(240,240,240),(screen_width / 2,screen_height - 50), True,(20,12),(0,-8),5, 10)

    display_text('highscore',(240,240,240),(screen_width - 110,screen_height - 80),False)
    display_text(str(highscore),(240,240,240),(screen_width -110,screen_height - 30), True,(20,12),(0,-8),5, 10)
    if game_over:
        display_text('Press SPACE to Play Again',(240,240,240),(screen_width/2, screen_height - 120),False)

def get_highscore(score):
    score = int(score)
    try:
        with open(join('code','highscore.txt'), 'r') as f:
            highscore = int(f.read())
    except:
        with open(join('code','highscore.txt'), 'w') as f:
            highscore = 0

    highscore = int(highscore)
    if score > highscore:
        highscore = score
    return highscore

