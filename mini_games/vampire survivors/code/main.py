from settings import *
from sprites import *gith
from player import *
from groups import AllSprite
from random import randint,choice
from pytmx.util_pygame import load_pygame

class Game:
    def __init__(self):
    # creating Display 
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self.gameWindow = pygame.display.set_mode((screen_width,screen_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(join('images','BOUNCY GUM.ttf'), 30)
        
        self.exit_game = False 
        self.game_over = False
        #groups
        self.all_sprites = AllSprite()
        self.collisionSprites = pygame.sprite.Group()
        self.bulletSprites = pygame.sprite.Group()
        self.enemySprites = pygame.sprite.Group()

        #audio
        self.shoot_sound = pygame.mixer.Sound(join('audio','shoot.wav'))
        self.shoot_sound.set_volume(0.4)
        self.game_sound = pygame.mixer.Sound(join('audio','music.wav'))
        self.game_sound.set_volume(0.01)
        self.impact_sound = pygame.mixer.Sound(join('audio','impact.ogg'))
        self.impact_sound.set_volume(0.5)
        self.game_sound.play()

        #enemy
        self.enemy_respawntime = 1000
        self.enemy_creationtime = 0
        self.enemy_positions = []
        #bullet 
        self.can_shoot = True
        self.cooldown_time = 200
        self.shoot_time = 0
        
        #setup
        self.load_images()
        self.setup()
        
    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images','gun','bullet.png')).convert_alpha()
        folders = list(walk(join('images', 'enemies')))[0][1]
        self.Enemyframes = {}
        for folder in folders:
            for folder_path, sub_folder, file_names in (walk(join('images','enemies', folder))):
                self.Enemyframes[folder] = []
                if file_names:
                    for file in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                        full_path = (join(f'{folder_path}', f'{file}'))
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.Enemyframes[folder].append(surf)

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            self.bullet = bullet( self.bullet_surf, self.gun.player_direction, pos , (self.all_sprites, self.bulletSprites))
            self.shoot_time = pygame.time.get_ticks()
            self.can_shoot = False
            self.shoot_sound.play()

    def cooldown_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if (current_time - self.shoot_time) >= self.cooldown_time:
                self.can_shoot = True

    def enemy_respawntimer(self):
        current_time = pygame.time.get_ticks()
        if (current_time - self.enemy_creationtime) >= self.enemy_respawntime:
            self.enemy = enemy((self.all_sprites,self.enemySprites),choice(self.enemy_positions),self.player,choice(list(self.Enemyframes.values())),self.collisionSprites)
            self.enemy_creationtime = pygame.time.get_ticks()
        
    def setup(self):
        map = load_pygame(join('data','maps','world.tmx'))
        for x,y, image in map.get_layer_by_name('Ground').tiles():
            sprite(image, (x*tilesize,y*tilesize) , self.all_sprites)
        
        for obj in map.get_layer_by_name('Objects'):
            collisionSprites(obj.image, (obj.x,obj.y), (self.all_sprites, self.collisionSprites))
        
        for obj in map.get_layer_by_name('Collisions'):
            collisionSprites(pygame.Surface((obj.width,obj.height)) , (obj.x,obj.y) ,self.collisionSprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == "Player":
                self.player = player((obj.x,obj.y), self.all_sprites, self.collisionSprites)
                self.gun = gun(self.player,self.all_sprites)
            else:
                self.enemy_positions.append((obj.x, obj.y))
    
    def collisions(self):
        if self.bulletSprites:
            for bullet in self.bulletSprites:
                collision = pygame.sprite.spritecollide(bullet, self.enemySprites, False,pygame.sprite.collide_mask)
                if collision:
                    for sprite in collision:
                        sprite.destroy()
                    self.impact_sound.play()
                    self.bullet.kill()
        elif self.gun:
            gun_collision = pygame.sprite.spritecollide(self.gun,self.enemySprites, False, pygame.sprite.collide_mask)
            if gun_collision:
                for sprite in gun_collision:
                    sprite.destroy()
                self.impact_sound.play()
                # print('Gun Kill')
                
    def player_collision(self):
        if self.enemySprites:
            player_collision = pygame.sprite.spritecollide(self.player, self.enemySprites,False , pygame.sprite.collide_mask)
            if player_collision:
                self.game_over = True

    def display_text(self,text1,color,pos,condition,rect = (0,0),move = (0,0) ,border_width = 0,radius = 0):
        text1_surf = self.font.render(text1, True, color)
        text1_rect = text1_surf.get_frect(center = pos)
        self.gameWindow.blit(text1_surf, text1_rect)
        if condition == True:
            pygame.draw.rect(self.gameWindow,color,text1_rect.inflate(rect).move(move) ,border_width,radius)

    #gameLoop
    def Game_loop(self):
        
        while not self.exit_game:
            dt = self.clock.tick()/1000

            if self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit_game = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            game = Game()
                            game.Game_loop()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit_game = True

            #    update
                keys = pygame.key.get_pressed()
                self.enemy_respawntimer()
                self.player_collision()
                self.collisions()
                self.cooldown_timer()
                self.input()
                self.all_sprites.update(dt)
    

                if self.game_over : self.display_text('Hit SPACE to replay the Game!','red',(screen_width/2,screen_height/2), True)
                self.all_sprites.draw(self.player.rect.center)
                pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.Game_loop()