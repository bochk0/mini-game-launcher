from settings import *
from support import *
from monster import *
from ui import *
from attack import attackAnimatedSprite
from timergame import timer
from random import choice


class Game:
    def __init__(self):
        #basics
        pygame.init()
        self.gamewindow = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Monster Battle')
        self.clock = pygame.time.Clock()

        self.game_over = False
        self.exit_game = False
        self.player_active = True

        #loading assets
        self.load_assets()

        #groups
        self.all_sprites = pygame.sprite.Group()
        # self.opponent_sprites = pygame.sprite.Group()

        #data
        player_monster_list = ['Sparchu', 'Jacana', 'Plumette', 'Atrox', 'Gulfin', 'Charmadillo']
        # player_monster_list = ['Sparchu']
        self.player_monsters = [Monster(name,self.back_images[name]) for name in player_monster_list]
        self.player = self.player_monsters[0]
        self.all_sprites.add(self.player)
        Opponent_monster_name = choice(list(MONSTER_DATA.keys()))
        self.Opponent_monster = Opponent(Opponent_monster_name,self.front_images[Opponent_monster_name],self.all_sprites)
        #UI
        self.opponent_ui = OpponentUI(self.Opponent_monster)
        self.ui = UI(self.player, self.player_monsters, self.simple_surfs, self.get_input)
        #timers
        self.timers = {'player_end': timer(1000, func = self.opponent_turn), 'opponent_end': timer(1000, func = self.player_turn)}

    def load_assets(self):
        self.front_images = load_folder('images', 'front')
        self.back_images = load_folder('images', 'back')
        self.bg_surfs = load_folder('images', 'other')
        self.simple_surfs = load_folder('images', 'simple')
        self.attack_frames = tile_importer(4, 'images','attacks' )
        self.audio  = audio_importer('audio')

    def get_input(self, state, data = None):
        if state == 'Attack':
            self.apply_action( self.Opponent_monster,data)
            self.player_active = False
            self.timers['player_end'].activate()
        elif state == 'Heal':
            self.player.health += 50
            attackAnimatedSprite(self.attack_frames['green'], self.player, self.all_sprites)
        elif state == 'Switch':
            self.player.kill()
            self.player = data
            self.all_sprites.add(self.player)
            self.ui.monster = self.player

        elif state == 'Escape':
            self.exit_game = True
        
    def apply_action(self, monster, data):
        if monster.health >= 0:
            Data = ABILITIES_DATA[data]
            multiplier = ELEMENT_DATA[Data['element']][monster.element]
            monster.health -= Data['damage'] * multiplier
            attackAnimatedSprite(self.attack_frames[Data['animation']], monster,self.all_sprites)
            self.audio[Data['animation']].play()
            # sound.set_volume(0.5)
            # sound.play()

    def player_turn(self):
        self.player_active = True
        if self.player.health <= 0:
            avaliable_monsters = [monster for monster in self.player_monsters if monster.health > 0]
            if avaliable_monsters:
                self.player.kill()
                self.player = avaliable_monsters[0]
                self.ui.monster= self.player
                self.all_sprites.add(self.player)
            else:
                self.exit_game = True

    def opponent_turn(self):
        if self.Opponent_monster.health <= 0:
            self.player_active = True
            self.Opponent_monster.kill()
            monster_name = choice(list(MONSTER_DATA.keys()))
            self.Opponent_monster = Opponent(monster_name, self.front_images[monster_name], self.all_sprites)
            self.opponent_ui.Opponent_monster = self.Opponent_monster
        else:
            attack = choice(self.Opponent_monster.ability)
            self.apply_action(self.player, attack)
            self.timers['opponent_end'].activate()

    def timers_update(self):
        for timer in self.timers.values():
            timer.update()

    def draw_monster_floor(self):
        for sprite in self.all_sprites:
            if isinstance(sprite, Creature):
                floor_rect = self.bg_surfs['floor'].get_frect(center = sprite.rect.midbottom + pygame.Vector2(0, 12))
                self.gamewindow.blit(self.bg_surfs['floor'], floor_rect)
   
    def game_loop(self):
        while not self.exit_game:
            dt = self.clock.tick() / 1000
            if self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit_game = True

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit_game = True
            # update
            self.timers_update()
            self.all_sprites.update(dt)
            if self.player_active:
                self.ui.update()
                        
            #drawing the game background
            self.gamewindow.blit(self.bg_surfs['bg'], (0,0))
            self.draw_monster_floor()
            self.all_sprites.draw(self.gamewindow)
            self.ui.draw()
            self.opponent_ui.draw()
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.game_loop()
