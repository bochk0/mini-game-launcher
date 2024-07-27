from settings import *

class player(pygame.sprite.Sprite):
    def __init__(self,groups,pos):
        super().__init__(groups)
        self.surf = pygame.Surface((50,40))
        # pygame.draw.rect(self.surf, 'blue', (50,40),10)
        self.rect = self.surf.get_frect(center = pos)
        # self.collision_sprites = collisionsprites

        self.direction = pygame.Vector2()
        self.speed = 200

    def get_input(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) or int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction = int(keys[pygame.K_UP]) - int(keys[pygame.K_DOWN]) or int(keys[pygame.K_w]) - int(keys[pygame.K_s])

    def move(self,dt):
        self.rect.center.x += self.direction * self.speed * dt
        self.rect.center.y += self.direction * self.speed * dt

    def update(self,dt):
        self.get_input()
        self.move(dt)