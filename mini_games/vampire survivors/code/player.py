from settings import *
class player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collisionSprites):
        super().__init__(groups)
        #imports
        self.playerS = pygame.image.load(join('images','player','down','0.png')).convert_alpha()
        self.load_images()
        self.state,self.frame_index = 'down', 0
        self.image = self.playerS
        self.collisionSprites = collisionSprites
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60,-100)
        self.player_direction = pygame.math.Vector2()
        self.player_speed = 400
    
    def input(self):
        keys = pygame.key.get_pressed()
        self.player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) + int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.player_direction.y =   int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]) + int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.player_direction = self.player_direction.normalize() if self.player_direction else self.player_direction
        
    def move(self,dt):
        self.hitbox_rect.x += self.player_direction.x * self.player_speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.player_direction.y * self.player_speed * dt
        self.collision('Vertical')
        self.rect.center = self.hitbox_rect.center
    
    def load_images(self):
        self.frames = {'left': [] ,'right': [] ,'up': [],'down': []}
        for state in self.frames.keys():
            for folder_path, sub_folder, file_names in (walk(join('images','player', state))):
                if file_names:
                    for file in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                        full_path = (join(f'{folder_path}', f'{file}'))
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def collision(self,directions):
        for sprite in self.collisionSprites:
                # print(sprite.rect)
            if sprite.rect.colliderect(self.hitbox_rect):
                if directions == 'horizontal':
                    if self.player_direction.x > 0:self.hitbox_rect.right = sprite.rect.left 
                    if self.player_direction.x < 0:self.hitbox_rect.left = sprite.rect.right
                if directions == 'Vertical':
                    if self.player_direction.y > 0:self.hitbox_rect.bottom = sprite.rect.top
                    if self.player_direction.y < 0:  self.hitbox_rect.top = sprite.rect.bottom

    def animate(self,dt):
        # set state
        if self.player_direction == [0,0] : self.frame_index = 0
        if self.player_direction.x != 0:
            self.state = 'right' if self.player_direction.x > 0 else 'left' 
        if self.player_direction.y != 0:
            self.state = 'down' if self.player_direction.y > 0 else 'up' 

        # animate 
        self.frame_index += 5 *dt
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])] 

    def update(self,dt):
        self.input()
        self.move(dt)
        self.animate(dt)