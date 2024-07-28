from typing import Any
from settings import *
from math import atan2,degrees
class sprite(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class collisionSprites(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class gun(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        #player Connection
        self.player_direction = pygame.Vector2(1,0)
        self.player = player
        self.distance = 140

        # sprite
        super().__init__(groups)
        self.gun_surf = pygame.image.load(join('images','gun','gun.png')).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)
    
    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(screen_width / 2 , screen_height / 2)
        self.player_direction = (mouse_pos - player_pos).normalize()
    
    def get_rotation(self):
        angle = degrees(atan2(self.player_direction.x,self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf , angle , 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf,abs(angle),1)
            self.image = pygame.transform.flip(self.image,False,True)

    def update(self, _):
        self.get_direction()
        self.get_rotation()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance

class bullet(pygame.sprite.Sprite):
    def __init__(self,surf,direction,pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.spawn_time = pygame.time.get_ticks()
        self.bullet_lifetime = 1000

        self.direction = direction 
        self.speed = 1200

    def update(self,dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.spawn_time >= self.bullet_lifetime:
            self.kill()

class enemy(pygame.sprite.Sprite):
    def __init__(self, groups, pos, player, frames,collisionSprites):
        super().__init__(groups)
        self.player = player
        #image
        self.frames, self.frame_index = frames , 0
        self.image = self.frames[self.frame_index]
        self.animation_speed = 6
        #rect
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-10,-40)
        self.collision_Sprites = collisionSprites
        self.direction = pygame.math.Vector2()
        self.speed = 400
        #death
        self.death_time = 0
        self.death_duration = 400


    def animate(self,dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)] 

    def move(self,dt):
        # get direction
        self. player_pos = pygame.Vector2(self.player.rect.center)
        self. enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (self.player_pos - self.enemy_pos).normalize()
        
        # Upgrade
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('Vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self,direction):
         for sprite in self.collision_Sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:self.hitbox_rect.right = sprite.rect.left 
                    if self.direction.x < 0:self.hitbox_rect.left = sprite.rect.right
                if direction == 'Vertical':
                    if self.direction.y > 0:self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0:  self.hitbox_rect.top = sprite.rect.bottom

    def destroy(self):
        #death Timer
        self.death_time = pygame.time.get_ticks()
        # Update Image
        surf = pygame.mask.from_surface(self.frames[0]).to_surface()
        surf.set_colorkey('black')
        self.image = surf

    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()

    def update(self,dt):
        if self.death_time == 0 :
            self.animate(dt)
            self.move(dt)
        else:
            self.death_timer()

