from settings import *
from Timer import timer
from math import sin
from random import randint

class Sprite(pygame.sprite.Sprite):
    def __init__(self, surf, groups, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)

class bullet(Sprite):
    def __init__(self, surf, groups, pos, direction):
        super().__init__(surf, groups, pos)
        # adjust the image 
        self.image = pygame.transform.flip(self.image,  direction == -1, False )
        self.direction = direction
        self.speed = 850
        

    def update(self,dt):
        self.rect.x += self.direction * self.speed * dt

class fire(Sprite):
    def __init__(self, surf, groups, pos, player):
        super().__init__(surf, groups, pos)
        self.player = player 
        self.flip = player.flip
        self.timer = timer(100, autostart = True, func = self.kill)
        self.y_correction = pygame.Vector2(0,9)
        if self.player.flip:
            self.rect.midright = self.player.rect.midleft  + self.y_correction
            self.image = pygame.transform.flip(surf, True, False)
        else:
            self.rect.midleft  = self.player.rect.midright + self.y_correction
            
    
    def update(self,_):
        self.timer.update()
        if self.player.flip:
            self.rect.midright = self.player.rect.midleft  + self.y_correction
        else:
            self.rect.midleft  = self.player.rect.midright + self.y_correction
        
        if self.flip != self.player.flip:
            self.kill()

class AnimatedSprites(Sprite):
    def __init__(self,frames, groups, pos):
        self.frames, self.frame_index, self.animation_speed = frames, 0, 10
        super().__init__(self.frames[self.frame_index], groups, pos)

    def animate(self,dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

class Enemy(AnimatedSprites):
    def __init__(self, frames, groups, pos):
        super().__init__(frames, groups, pos)
        self.death_timer = timer(200, func = self.kill)
        self.check = False
    def destroy(self):
        self.death_timer.activate()
        self.animation_speed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey('black')
        self.check = True

    def update(self, dt):
        self.death_timer.update()
        if not self.check:
            self.move(dt)
            self.animate(dt)
        self.constraint()

        # self.death_timer.update()
        # if not self.death_timer:
        #     self.move(dt)
        #     self.animate(dt)
        # self.constraint()

class bee(Enemy):
    def __init__(self, frames, groups, pos, speed):
        super().__init__(frames, groups, pos)
        self.speed = speed
        self.amplitude = randint(400, 600)
        self.frequency = randint(300, 600)
        # self.enemy_sprites = enemysprites
    
    def move(self,dt):
        self.rect.x -= self.speed * dt
        self.rect.y += sin(pygame.time.get_ticks() / self.frequency) * self.amplitude * dt

    def constraint(self):
        if self.rect.x <= 0:
            self.kill()


class worm(Enemy):
    def __init__(self, frames, groups, rect):
        super().__init__(frames, groups, rect.topleft)
        self.speed = randint(160,200)
        self.frames = frames
        self.area = rect
        self.rect.bottomleft = rect.bottomleft + pygame.Vector2(0,-33)
        self.direction = 1
        # self.enemy_sprites = enemysprites

    def move(self,dt):
        self.rect.x += self.direction * self.speed * dt 
        

    def constraint(self):
        if not self.area.contains(self.rect):
            self.frames = [pygame.transform.flip(surf, True, False) for surf in self.frames]
            self.direction *= -1

class player(AnimatedSprites):
    def __init__(self,frames ,groups,pos,collisionsprites, create_bullet):
        super().__init__(frames,groups,pos)
        self.collision_sprites = collisionsprites
        self.create_bullet = create_bullet
        # self.hitbox_rect = self.rect.inflate(-20,-10)

        self.flip = True
        self.direction = pygame.Vector2()
        self.speed = 500
        self.gravity = 50
        self.on_floor = False

        #timer
        self.shoot_timer = timer(500)

    def get_input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) or int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = -20
        if pygame.mouse.get_pressed()[0] and not self.shoot_timer.active:
            self.create_bullet(self.rect.center, -1 if self.flip else 1)
            self.shoot_timer.activate()
        
    def move(self,dt):
        #horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collisions('horizontal')
        #vertical
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y 
        self.collisions('vertical')

    def collisions(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom 
                    self.direction.y = 0

    def check_floor(self):
        chk_rect = pygame.FRect((0,0), (self.rect.width,2)).move_to(midtop = self.rect.midbottom)
        levelrects = [sprite.rect for sprite in self.collision_sprites]
        self.on_floor = True if chk_rect.collidelist(levelrects) >= 0 else False
    
    def animate(self, dt):
        if self.direction.x:
            self.frame_index += self.animation_speed * dt
            self.flip = self.direction.x < 0
        else:
            self.frame_index = 0
        
        self.frame_index = 1 if not self.on_floor else self.frame_index
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        self.image = pygame.transform.flip(self.image, self.flip, False)

    def update(self,dt):
        self.shoot_timer.update()
        self.animate(dt)
        self.check_floor()
        self.get_input()
        self.move(dt)