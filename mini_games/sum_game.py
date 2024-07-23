import random

import pygame


class SumGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Sum Game")
        self.font = pygame.font.Font(None, 74)
        self.clock = pygame.time.Clock()
        self.running = True

    def start_game(self):
        num1, num2 = random.randint(0, 10), random.randint(0, 10)
        correct_answer = num1 + num2
        user_answer = ""
        input_active = False

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_RETURN:
                            if user_answer.isdigit() and int(user_answer) == correct_answer:
                                print("True!")
                            else:
                                print("False!")
                            user_answer = ""
                            num1, num2 = random.randint(0, 10), random.randint(0, 10)
                            correct_answer = num1 + num2
                        elif event.key == pygame.K_BACKSPACE:
                            user_answer = user_answer[:-1]
                        else:
                            user_answer += event.unicode
                    else:
                        input_active = True

            self.screen.fill((255, 255, 255))
            question_text = self.font.render(f"{num1} + {num2} = ?", True, (0, 0, 0))
            self.screen.blit(question_text, (200, 150))

            answer_text = self.font.render(user_answer, True, (0, 0, 0))
            self.screen.blit(answer_text, (200, 250))

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
