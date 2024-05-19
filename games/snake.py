import pygame
import random
from other.common import Globals, update_score
from tkinter import messagebox

class SnakeGame:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the screen
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Snake Game")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        # Fonts
        self.font = pygame.font.SysFont(None, 48)

        # Game variables
        self.snake = [(self.WIDTH // 2, self.HEIGHT // 2)]
        self.direction = (0, 0)
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False

        # Clock
        self.clock = pygame.time.Clock()
        self.FPS = 10

    def generate_food(self):
        x = random.randint(0, (self.WIDTH - 20) // 20) * 20
        y = random.randint(0, (self.HEIGHT - 20) // 20) * 20
        return x, y

    def draw_snake(self):
        for segment in self.snake:
            pygame.draw.rect(self.screen, self.GREEN, (segment[0], segment[1], 20, 20))

    def draw_food(self):
        pygame.draw.rect(self.screen, self.RED, (self.food[0], self.food[1], 20, 20))

    def move_snake(self):
        head = (self.snake[0][0] + self.direction[0] * 20, self.snake[0][1] + self.direction[1] * 20)
        if head[0] < 0 or head[0] >= self.WIDTH or head[1] < 0 or head[1] >= self.HEIGHT:
            self.game_over = True
            return
        if head in self.snake[1:]:
            self.game_over = True
            return
        self.snake.insert(0, head)
        if self.snake[0] == self.food:
            self.food = self.generate_food()
            self.score += 1
        else:
            self.snake.pop()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction = (0, -1)
        elif keys[pygame.K_DOWN]:
            self.direction = (0, 1)
        elif keys[pygame.K_LEFT]:
            self.direction = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            self.direction = (1, 0)

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def run(self):
        running = True
        while running:
            self.screen.fill(self.BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_input()

            self.move_snake()
            if self.game_over:
                score_to_add = self.score * 15
                update_score(Globals.username, score_to_add)
                messagebox.showinfo(" ", "You earned " + str(score_to_add) + " points!! good job!")
                running = False

            self.draw_snake()
            self.draw_food()
            self.draw_text(f"Score: {self.score}", self.font, self.WHITE, self.WIDTH // 2, 30)

            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
