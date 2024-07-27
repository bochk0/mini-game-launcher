from settings import * 
from random import choice, uniform

class paddle(pygame.sprite.Sprite):

    def __init__(self,groups,pos):
        super().__init__(groups)
        #surf
        self.surf = pygame.Surface((SIZE.get('paddle')), pygame.SRCALPHA)
        self.image = self.surf
        pygame.draw.rect(self.image, COLORS['paddle'], pygame.FRect((0,0) ,  SIZE['paddle']), 0 , 6)
        self.rect = self.image.get_frect(center = pos)
        self.old_rect = self.rect.copy()
        #shadow surf
        self.shadow_surf = self.image.copy()
        self.shadow_image = self.shadow_surf
        pygame.draw.rect(self.shadow_image, COLORS['paddle shadow'], pygame.FRect((0,0) ,  SIZE['paddle']), 0 , 6)
        # self.shadow_rect = self.shadow_image.get_frect(center = pos)

        # self.shadow_rect.centerx = self.rect.centerx - 100

        self.direction = 0

    def move(self,dt):
        self.rect.centery += self.direction * self.speed * dt
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = screen_height if self.rect.bottom > screen_height else self.rect.bottom

    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.move(dt)
        self.get_direction()

class ball(pygame.sprite.Sprite):
    def __init__(self , groups , paddle_sprites , pos, update_score):
        super().__init__(groups)
        self.paddle_sprites = paddle_sprites
        self.update_score = update_score
        self.current_time = pygame.time.get_ticks()
        self.ball_duration = 1000


        self.surf = pygame.Surface((SIZE.get('ball')), pygame.SRCALPHA)
        self.image = self.surf
        pygame.draw.circle(self.image , COLORS.get('ball') , (SIZE["ball"][0]/2 , SIZE["ball"][1]/2) , SIZE["ball"][0]/2)
        
        self.shadow_image = self.image.copy()
        pygame.draw.circle(self.shadow_image , COLORS.get('ball shadow') , (SIZE["ball"][0]/2 , SIZE["ball"][1]/2) , SIZE["ball"][0]/2)
        # self.shadow_rect = self.shadow_image.get_frect(center = (pos[0] + 10, pos[1]))
        
        self.rect = self.image.get_frect(center = pos)
        self.old_rect = self.rect.copy()
        #speeds
        self.direction = pygame.Vector2(choice((-1,1)), uniform(0.7,0.8)* choice((-1,1)))
        self.speed = SPEED.get('ball')
        self.modify_speed = 0

    def move(self,dt):
        self.rect.x += self.direction.x * self.speed * dt * self.modify_speed
        self.collisions('horizontal')
        self.rect.y += self.direction.y * self.speed * dt * self.modify_speed
        self.collisions('Vertical')

    def wall_collisions(self):
        if self.rect.x >= screen_width or self.rect.x <= 0:
            self.update_score('player' if self.rect.x < screen_width/2 else 'Opponent') 
            self.reset()

        if self.rect.top < 0:
            self.rect.top = 0
            self.direction.y *= -1
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.direction.y *= -1

    def collisions(self, direction):
        # print(self.old_rect)
        for sprite in self.paddle_sprites:
            collision = sprite.rect.colliderect(self.rect)
            # print(collision)
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction.x *= -1
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1
                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y *= -1

    def reset(self):
        self.current_time = pygame.time.get_ticks()
        self.rect.center = ( screen_width/2 , screen_height/2 )
        self.direction = pygame.Vector2(choice((-1,1)), uniform(0.7,0.8)* choice((-1,1)))
   
    def timer(self):
        if (pygame.time.get_ticks() - self.current_time ) >= self.ball_duration:
            self.modify_speed = 1
        else:
            self.modify_speed = 0

    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.timer()
        self.move(dt)
        self.wall_collisions()

class Opponent(paddle):
    def __init__(self,groups,pos,ball):
        super().__init__(groups, pos,)
        self.speed = SPEED['opponent'] 
        self.rect.center = POS['opponent']
        self.ball = ball

    def get_direction(self):
        # pass
        self.direction = 1 if self.ball.rect.centery > self.rect.centery else -1
 
class player(paddle):
    def __init__(self,groups,pos):
        super().__init__(groups,pos)
        self.speed = SPEED['player']

    def get_direction(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]) or int(keys[pygame.K_s]) - int(keys[pygame.K_w]) 
    


