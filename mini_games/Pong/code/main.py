from settings import *
from sprites import * 
from groups import AllSprites 
import json
class game():
    def __init__(self):
        #Initialization
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.gamewindow = pygame.display.set_mode((screen_width,screen_height))
        pygame.display.set_caption('Pong')
        
        #groups
        self.all_sprites = AllSprites()
        self.paddle_sprites = pygame.sprite.Group()
        
        #Sprites
        self.player = player((self.all_sprites,self.paddle_sprites), POS.get('player'))
        self.ball = ball(self.all_sprites, self.paddle_sprites ,(screen_width/2,screen_height/2), self.update_score)
        self.opponent = Opponent((self.all_sprites, self.paddle_sprites), POS['opponent'], self.ball)

        self.exit_game = False
        self.game_over = False
        
        # SCORE
        try:
            with open(join('data', 'score.txt')) as score_file:
                self.score = json.load(score_file)
                print('in try')
        except:
            # print('in except')
            self.score = {'player': 0, 'Opponent': 0}

        # self.score = {'player': 0 , 'Opponent': 0 }
        self.font = pygame.font.Font(None, 160)

    def display_text(self,text1,color,pos,condition,rect = (0,0),move = (0,0) ,border_width = 0,radius = 0):
        text1_surf = self.font.render(text1, True, color)
        text1_rect = text1_surf.get_frect(midbottom = pos)
        self.gamewindow.blit(text1_surf, text1_rect)
        if condition == True:
            pygame.draw.rect(self.gamewindow,color,text1_rect.inflate(rect).move(move) ,border_width,radius)

    def update_score(self, side):
        self.score ['player' if side == 'player' else 'Opponent'] += 1

    def game_loop(self):
        while not self.exit_game:
            dt = self.clock.tick()/1000

            if self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit_game = True
                        

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        with open(join('data', 'score.txt'), 'w') as score_file:
                            json.dump(self.score, score_file)
                        self.exit_game = True

                self.gamewindow.fill(COLORS.get('bg'))
                self.display_text(str(self.score['player']) , COLORS['bg detail'] , (screen_width/2 + 100 , screen_height / 2 + 100 ) , False)
                self.display_text(str(self.score['Opponent']) , COLORS['bg detail'] , (screen_width/2 - 100 , screen_height / 2 + 100 ) , False)
                pygame.draw.line(self.gamewindow, COLORS['bg detail'], (screen_width/2, 0), (screen_width/2, screen_height), 10)
                self.all_sprites.draw()
                self.all_sprites.update(dt)
                pygame.display.update()
    pygame.quit()


game = game()
game.game_loop()