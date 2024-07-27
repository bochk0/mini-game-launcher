import random
import pygame


# Initializing Variables

class level_2:
    def __init__(self):
        pygame.init()
        self.screen_width = 700
        self.screen_height = 500
        # Colors
        self.Blue = (0,0,235)
        self.White = (255,255,255)
        self.Red = (255,0,0)
        self.Green = (0,250,0)
        self.Black = (0,0,0)

        #Snake 
    #Creating Display 
        self.clock = pygame.time.Clock()
        self.gameWindow = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game')
        
        #Background Images
        # bgimg = pygame.image.load('')
        # bgimg = pygame.image.transform.scale('',)

        #Score
        # Functions
        # Apperaring text on screen
    def screen_text(self, text,color,x,y,size):
        font = pygame.font.SysFont(None, size)
        screen_text = font.render(text, True, color)
        self.gameWindow.blit(screen_text, [x,y])
# Plotting Snake in game
    def plot_Snake(self,gameWindow, color, snake_list, Snake_size):
        for x in snake_list:
            pygame.draw.rect(gameWindow, color, [x[0], x[1], Snake_size, Snake_size])
        # Draw the snake's head in a different color
        x = snake_list[-1][0]
        y = snake_list[-1][1]
        pygame.draw.rect(gameWindow, self.Blue, [x, y, Snake_size, Snake_size])
    def welcome(self):
        exit_game = False
        while not exit_game:
            self.gameWindow.fill(self.White)
            self.screen_text('Welcome to the World of Snakes!', self.Black, 150, 180, 40)
            self.screen_text('Enter "SPACE" to play the Game', self.Black, 240, 210, 22)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.Game_loop()
            pygame.display.update()
            self.clock.tick(60)
        


    #Creating game loop 
    def Game_loop(self):
        # Game specific Variables
        exit_game = False
        game_over = False
        fps = 60    
        # scores
        score = 0
        try:
            with open("highscoreLevel2.txt", 'r') as f:
                highscore = int(f.read())
        except:
            with open("highscoreLevel2.txt", 'w') as f:
                highscore = 0
                # highscore = int(f.read())
        # snake 
        Snake_size = 13
        Snake_x = 32
        Snake_y = 60
        velocity_x = 0
        velocity_y = 0
        ingame_velocity = 2
        Snake_list = []
        snake_length = 1
        #Food
        food_x = random.randint(0, self.screen_width-50)
        food_y = random.randint(0, self.screen_height-50)
        food_size = 15

        #Bonus Food
        Bonus_food_x = random.randint(0, self.screen_width-50)
        Bonus_food_y = random.randint(0, self.screen_height-50)
        Bonus_food_size = 25

        while not exit_game:
            if game_over :
                with open("highscorelevel2.txt", 'w')as f :
                    f.write(str(highscore))
                self.gameWindow.fill(self.White)
                self.screen_text(('Game Over! Press ENTER to Restart the game'), self.Red, 150, 180, 30 )
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.Game_loop()
            else:
                for event in pygame.event.get():
                    # Enabling exit button
                    if event.type == pygame.QUIT:
                        exit_game = True
                    # Snake Movements
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            velocity_x =  ingame_velocity
                            velocity_y =  0
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            velocity_x =  - ingame_velocity
                            velocity_y =  0
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            velocity_x =  0
                            velocity_y =  - ingame_velocity
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            velocity_x =  0
                            velocity_y =  ingame_velocity
                # Eating Normal Food
                if abs(food_x - Snake_x) <= 15 and abs(food_y - Snake_y) <= 15:
                    food_x = random.randint(0, self.screen_width-50)
                    food_y = random.randint(0, self.screen_height-50)
                    score+=10
                    snake_length+=1

                # Eating Bonus Food
                if abs(Bonus_food_x - Snake_x) <= 15 and abs(Bonus_food_y - Snake_y) <= 15:
                    Bonus_food_x = random.randint(0, self.screen_width-50)
                    Bonus_food_y = random.randint(0, self.screen_height-50)
                    score+=50
                    ingame_velocity += 0.5
                    snake_length+=1

                Snake_x = Snake_x + velocity_x
                Snake_y = Snake_y + velocity_y 

                head = []
                head.append(Snake_x)
                head.append(Snake_y)
                Snake_list.append(head)

                if len(Snake_list)>snake_length:
                    del Snake_list[0]
                for x in Snake_list[:-1]:
                    if x == head:
                        game_over = True
                if Snake_x < 0 or Snake_x == self.screen_width or Snake_y < 0 or Snake_y == self.screen_height:
                    game_over = True

                highscore = int(highscore)
                if score > highscore:
                    highscore = score

                self.gameWindow.fill(self.Black)
                self.screen_text(('score: '+str(score)) +  ('  High Score: '+str(highscore)), self.White, 5, 5,20 )
                self.plot_Snake(self.gameWindow,self.White, Snake_list , Snake_size)
                pygame.draw.rect(self.gameWindow,self.Red, [food_x , food_y , food_size , food_size])
                if score % 100 == 0 and score != 0:
                    pygame.draw.rect(self.gameWindow,self.Green, [Bonus_food_x , Bonus_food_y , Bonus_food_size , Bonus_food_size])
            pygame.display.update()
            self.clock.tick(fps)
        pygame.quit()
        exit()

if __name__ == "__main__":
    game = level_2()
    game.welcome()
    
