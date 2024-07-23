import random

import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class SnakeGame:
    def __init__(self, width=400, height=400):
        self.width = width
        self.height = height
        self.block_size = 10
        self.speed = 15

        self.game_over = False
        self.score = 0

        pygame.init()

        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')

        self.clock = pygame.time.Clock()

        self.snake = [(self.width / 2, self.height / 2)]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.spawn_food()

    def spawn_food(self):
        self.food = (random.randrange(0, self.width // self.block_size) * self.block_size,
                     random.randrange(0, self.height // self.block_size) * self.block_size)

    def draw_snake(self):
        for segment in self.snake:
            pygame.draw.rect(self.display, GREEN, (segment[0], segment[1], self.block_size, self.block_size))

    def draw_food(self):
        pygame.draw.rect(self.display, RED, (self.food[0], self.food[1], self.block_size, self.block_size))

    def move_snake(self):
        head = self.snake[0]
        if self.direction == "UP":
            new_head = (head[0], head[1] - self.block_size)
        elif self.direction == "DOWN":
            new_head = (head[0], head[1] + self.block_size)
        elif self.direction == "LEFT":
            new_head = (head[0] - self.block_size, head[1])
        elif self.direction == "RIGHT":
            new_head = (head[0] + self.block_size, head[1])

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()

    def check_collision(self):
        head = self.snake[0]
        if (head[0] < 0 or head[0] >= self.width or
                head[1] < 0 or head[1] >= self.height or
                head in self.snake[1:]):
            self.game_over = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != "DOWN":
                    self.direction = "UP"
                elif event.key == pygame.K_DOWN and self.direction != "UP":
                    self.direction = "DOWN"
                elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                    self.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                    self.direction = "RIGHT"

    def start_game(self):
        while not self.game_over:
            self.display.fill(BLACK)
            self.handle_events()
            self.move_snake()
            self.check_collision()
            self.draw_snake()
            self.draw_food()
            pygame.display.update()
            self.clock.tick(self.speed)

        pygame.quit()
