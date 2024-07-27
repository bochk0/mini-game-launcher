from settings import *
from sprites import *
from groups import AllSprites
from support import *
from random import choice, randint
from Timer import timer

class game():
    def __init__(self):
        #Initialization
        pygame.init()
        self.gamewindow = pygame.display.set_mode((screen_width , screen_height))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        
        self.exit_game = False
        self.game_over = False

        #groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.enemy_positions = []


        # loading assets
        self.load_assets()
        self.setup()
        self.game_music.play()
        self.bee_timer = timer(200, func = self.create_bee,repeat= True, autostart = True )


        #sprites
        # self.player = player(self.bee_frames, self.all_sprites,  choice(self.enemy_positions), self.collision_sprites)
        # self.bee = bee(self.player_frames,self.collision_sprites, choice(self.enemy_positions) , self.enemy_sprites)
    def create_bee(self):
        bee(frames = self.bee_frames,
            groups = (self.all_sprites, self.enemy_sprites) ,
            pos =  ((self.level_width + screen_width),(randint(0,self.level_height))),
            speed = randint(300, 500))

    def create_bullet(self, pos , direction):
        x = pos[0] + direction * 62 if direction == 1 else pos[0] + direction * 15 - self.bullet_frame.get_width()
        bullet(self.bullet_frame, (self.all_sprites, self.bullet_sprites) , (x, pos[1] + 12) , direction)
        x = pos[0] + direction * 50 if direction == 1 else pos[0] + direction * 5 - self.bullet_frame.get_width()
        self.shoot_sound.play()
        fire(self.fire_frame, self.all_sprites,(x , pos[1] + 12), self.player)

    def load_assets(self):
        #audio
        self.game_music = load_audio('audio', 'music',volume= 0.01)
        self.impact_sound = load_audio('audio', 'impact', format ='ogg')
        self.shoot_sound = load_audio('audio', 'shoot')
        #graphics
        self.bullet_frame = load_images('images','gun', 'bullet')
        self.fire_frame = load_images('images','gun', 'fire')
        self.player_frames = load_folder('images','player')
        self.worm_frames = load_folder('images','enemies','worm')
        self.bee_frames = load_folder('images','enemies','bee')

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        self.level_width = map.width * tilesize
        self.level_height = map.height * tilesize

        for x, y ,image in map.get_layer_by_name('Main').tiles():
            Sprite(image, (self.all_sprites , self.collision_sprites), (x * tilesize, y * tilesize))

        for x, y ,image in map.get_layer_by_name('Decoration').tiles():
            Sprite(image, (self.all_sprites ), (x * tilesize, y * tilesize))

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = player(self.player_frames, self.all_sprites,  (obj.x, obj.y), self.collision_sprites, self.create_bullet)
            if obj.name == 'Worm':
                self.worm = worm(self.worm_frames, (self.all_sprites, self.enemy_sprites ),  pygame.FRect(obj.x, obj.y , obj.width, obj.height) )
        # self.bee = bee(self.bee_frames,self.all_sprites ,  choice(self.enemy_positions) )

    def collisions(self):
        # bullet Enemy Collisions
        for bullet in self.bullet_sprites:
            sprite_collision = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
            if sprite_collision:
                bullet.kill()
                for sprite in sprite_collision:
                    self.impact_sound.play()
                    sprite.destroy()
        # Player And Enemy Collisions
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.exit_game = True

    def game_loop(self):
        while not self.exit_game:
            dt = self.clock.tick(framerate) / 1000
            if self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit_game = True

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit_game = True

            #update
            self.bee_timer.update()
            self.all_sprites.update(dt)
            self.collisions()
            #draw
            self.gamewindow.fill(Bg_color)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = game()
    game.game_loop()