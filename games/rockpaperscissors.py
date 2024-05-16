import pygame
import random
from other.common import Globals, update_score


class RockPaperScissors:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the screen
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Rock Paper Scissors")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        # Fonts
        self.font = pygame.font.SysFont(None, 48)
        self.result_font = pygame.font.SysFont(None, 64)

        # Game variables
        self.choices = ["Rock", "Paper", "Scissors"]
        self.player_choice = None
        self.computer_choice = None
        self.result = None
        self.player_score = 0
        self.computer_score = 0

    # Function to display text on screen
    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    # Function to display choices
    def draw_choices(self):
        self.draw_text("Choose your move:", self.font, self.BLACK, self.WIDTH // 2, self.HEIGHT // 4 - 40)
        self.draw_text("Rock", self.font, self.BLACK, self.WIDTH // 4, self.HEIGHT // 2)
        self.draw_text("Paper", self.font, self.BLACK, self.WIDTH // 2, self.HEIGHT // 2)
        self.draw_text("Scissors", self.font, self.BLACK, 3 * self.WIDTH // 4, self.HEIGHT // 2)
        self.draw_text(f"Player: {self.player_score}", self.font, self.BLACK, self.WIDTH // 4, self.HEIGHT // 4 - 80)
        self.draw_text(f"Computer: {self.computer_score}", self.font, self.BLACK, 3 * self.WIDTH // 4, self.HEIGHT // 4 - 80)

    # Function to get player choice
    def get_player_choice(self, pos):
        if self.HEIGHT // 2 - 24 < pos[1] < self.HEIGHT // 2 + 24:
            if self.WIDTH // 4 - 24 < pos[0] < self.WIDTH // 4 + 24:
                return "Rock"
            elif self.WIDTH // 2 - 24 < pos[0] < self.WIDTH // 2 + 24:
                return "Paper"
            elif 3 * self.WIDTH // 4 - 24 < pos[0] < 3 * self.WIDTH // 4 + 24:
                return "Scissors"
        return None

    # Function to get computer choice
    def get_computer_choice(self):
        return random.choice(self.choices)

    # Function to determine the winner
    def determine_winner(self, player_choice, computer_choice):
        if player_choice == computer_choice:
            return "It's a tie!"
        elif (player_choice == "Rock" and computer_choice == "Scissors") or \
             (player_choice == "Paper" and computer_choice == "Rock") or \
             (player_choice == "Scissors" and computer_choice == "Paper"):
            self.player_score += 1
            return "You win!"
        else:
            self.computer_score += 1
            return "Computer wins!"

    # Main game loop
    def run(self):
        running = True
        while running:
            self.screen.fill(self.WHITE)
            self.draw_choices()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.player_choice = self.get_player_choice(pos)
                    if self.player_choice:
                        self.computer_choice = self.get_computer_choice()
                        self.result = self.determine_winner(self.player_choice, self.computer_choice)

            if self.result:
                self.draw_text(f"Player: {self.player_choice}", self.font, self.BLACK, self.WIDTH // 4, self.HEIGHT // 4)
                self.draw_text(f"Computer: {self.computer_choice}", self.font, self.BLACK, 3 * self.WIDTH // 4, self.HEIGHT // 4)
                self.draw_text(self.result, self.result_font, self.BLUE, self.WIDTH // 2, 3 * self.HEIGHT // 4)

            pygame.display.flip()

        score_to_add = (self.player_score-self.computer_score)
        update_score(Globals.username, (score_to_add * 15))
        print("here")
        pygame.quit()


if __name__ == "__main__":
    game = RockPaperScissors()
    game.run()
