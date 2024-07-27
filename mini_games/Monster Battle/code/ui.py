from settings import *

class UI:
    def __init__(self, monster, player_monsters, simple_surfs, get_input):
        pygame.font.init()
        self.surf = pygame.display.get_surface()
        self.simple_surfs = simple_surfs
        self.font = pygame.font.Font(None, 32)
        self.left = WINDOW_WIDTH/2 - 100 
        self.top = WINDOW_HEIGHT/2 + 50
        self.monster = monster
        #control
        self.get_input = get_input
        self.rows, self.cols = 2,2
        self.state = 'general'
        self.general_index = {'col':0, 'row':0}
        self.attack_index = {'col':0, 'row':0}
        self.general_options = ['Attack', 'Heal', 'Switch', 'Escape']
        self.switch_index = 0
        self.visible_monsters = 4
        self.player_monsters = player_monsters
        
        self.avaliable_monsters = [monster for monster in self.player_monsters if monster != self.monster and monster.health > 0] 
        
    def input(self):
        keys = pygame.key.get_just_pressed()
        if self.state == 'general':
            self.general_index['row'] = (self.general_index['row'] + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % self.rows
            self.general_index['col'] = (self.general_index['col'] + int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])) % self.cols
            if keys[pygame.K_SPACE]:
                self.state = (self.general_options[self.general_index['col'] + 2 * self.general_index['row']])
        elif self.state == 'Attack':
            self.attack_index['row'] = (self.attack_index['row'] + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % self.rows
            self.attack_index['col'] = (self.attack_index['col'] + int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])) % self.cols
            if keys[pygame.K_SPACE]:
                attack = (self.monster.ability[self.attack_index['col'] + 2 * self.attack_index['row']])
                self.get_input(self.state, attack)
                self.state = 'general'
        elif self.state == "Switch":
            if self.avaliable_monsters:
                self.switch_index = (self.switch_index + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % len(self.avaliable_monsters)
                if keys[pygame.K_SPACE]:
                    switch = self.avaliable_monsters[self.switch_index]
                    self.get_input(self.state, self.avaliable_monsters[self.switch_index])
                    self.state = 'general'
        elif self.state == "Heal":
            self.get_input('Heal')
            self.state = 'general'
        elif self.state == "Escape":
            self.get_input('Escape')
        

        if keys[pygame.K_ESCAPE]:
            self.state = 'general'
            self.general_index = {'col':0, 'row':0}
            self.attack_index = {'col':0, 'row':0}
            self.switch_index = 0
   
    def quad_options(self, index , options):
        #bg
        rect = pygame.FRect(self.left, self.top, 400, 200)
        pygame.draw.rect(self.surf, COLORS['white'], rect , 0 , 12 )
        #options
        for col in range(self.cols):
            for row in range(self.rows):
                x = self.left + rect.width / (self.cols * 2) + (rect.width / self.cols) * col
                y = self.top + rect.height / (self.rows * 2) + (rect.height / self.rows) * row
                i = col + 2 * row
                color = COLORS['darkgray'] if col == index['col'] and row == index['row'] else COLORS['black']
                font_surf = self.font.render(options[i], True, color)
                font_rect = font_surf.get_frect(center = (x,y)) 
                self.surf.blit(font_surf, font_rect)

    def switch(self):
        #bg
        rect = pygame.FRect(self.left, self.top - 150, 300, 400)
        pygame.draw.rect(self.surf, COLORS['white'], rect , 0 , 12 )
        #Menu
        y_offset = 0 if self.switch_index < self.visible_monsters else -(self.switch_index  - self.visible_monsters + 1 ) * rect.height / self.visible_monsters 
        for i in range(len(self.avaliable_monsters)):
            x = rect.centerx + 20
            y = rect.top + rect.height / (self.visible_monsters * 2) + ( rect.height / self.visible_monsters * i) + y_offset
            name = self.avaliable_monsters[i].name
            simple_surf = self.simple_surfs[name]
            simple_rect = simple_surf.get_frect(center = (x - 100 ,y))
            color = COLORS['darkgray'] if i == self.switch_index  else COLORS['black']
            text_surf = self.font.render(name, True, color)
            text_rect = text_surf.get_frect(center = (x,y))
            if rect.collidepoint(text_rect.center):
                self.surf.blit(text_surf, text_rect)
                self.surf.blit(simple_surf, simple_rect)

    def stats(self):
        #bg
        rect = pygame.FRect(self.left - 200 , self.top - 65, 250, 60)
        pygame.draw.rect(self.surf, COLORS['white'], rect, 0, 12 )
        #name
        self.font2 = pygame.font.Font(None, 25)
        name_surf = self.font2.render(self.monster.name, True, COLORS['black'])
        name_rect = name_surf.get_frect(topleft = rect.topleft + pygame.Vector2(rect.width * 0.35,12))
        self.surf.blit(name_surf,name_rect)
        #Health Bar
        health_rect = pygame.FRect(rect.left + 13, rect.top + 37, rect.width*0.9, 12)
        pygame.draw.rect(self.surf,COLORS['gray'],health_rect,0,3)
        self.draw_bar(health_rect, self.monster.health , self.monster.max_health)

    def draw_bar(self,rect, value, max_value):
        ratio = rect.width / max_value
        progress_rect = pygame.FRect(rect.topleft ,(value * ratio ,rect.height) )
        if rect.collidepoint(progress_rect.center):
            pygame.draw.rect(self.surf, COLORS['red'], progress_rect, 0, 3)

    def draw(self):
        match self.state:
            case 'general': self.quad_options(self.general_index, self.general_options)
            case 'Attack': self.quad_options(self.attack_index, self.monster.ability)
            case 'Switch': self.switch()
        if self.state != 'Switch': self.stats()

    def update(self):
        self.input()
        self.avaliable_monsters = [monster for monster in self.player_monsters if monster != self.monster and monster.health > 0]



class OpponentUI:
    def __init__(self, opponent_monster):
        self.surf = pygame.display.get_surface()
        self.Opponent_monster = opponent_monster
        self.left = WINDOW_WIDTH/2 + 300
        self.top =  WINDOW_HEIGHT/2 - 50

    def stats(self):
        #bg
        rect = pygame.FRect(0,0, 250,70).move_to(midleft = (600, self.Opponent_monster.rect.centery))
        pygame.draw.rect(self.surf, COLORS['white'], rect, 0, 12 )
        #name
        self.font2 = pygame.font.Font(None, 25)
        name_surf = self.font2.render(self.Opponent_monster.name, True, COLORS['black'])
        name_rect = name_surf.get_frect(topleft = rect.topleft + pygame.Vector2(rect.width * 0.35,12))
        self.surf.blit(name_surf,name_rect)
        #Health Bar
        health_rect = pygame.FRect(rect.left + 13, rect.top + 37, rect.width*0.9, 12)
        pygame.draw.rect(self.surf,COLORS['gray'],health_rect,0,3)
        self.draw_bar(health_rect, self.Opponent_monster.health , self.Opponent_monster.max_health)

    def draw_bar(self,rect, value, max_value):
        ratio = rect.width / max_value
        progress_rect = pygame.FRect(rect.topleft ,(value * ratio ,rect.height) )
        if rect.collidepoint(progress_rect.center):
            pygame.draw.rect(self.surf, COLORS['red'], progress_rect, 0, 3)

    def draw(self):
        self.stats()
