from random import choice
from time import sleep
from turtle import *
from freegames import *
from other.common import Globals, update_score
from tkinter import messagebox

pattern = []
guesses = []
tiles = {
    vector(0, 0): ('red', 'dark red'),
    vector(0, -200): ('blue', 'dark blue'),
    vector(-200, 0): ('green', 'dark green'),
    vector(-200, -200): ('yellow', 'khaki'),
}


class SimonSays:
    def __init__(self):
        setup(420, 420, 370, 0)
        hideturtle()
        tracer(False)
        self.grid()
        self.score = 0  # Initialize score counter
        self.score_display = Turtle(visible=False)
        self.score_display.penup()
        self.score_display.goto(0, 200)  # Position the score display
        self.msg_display = Turtle(visible=False)
        self.msg_display.penup()
        self.msg_display.goto(100, 0)  # Position the score display
        onscreenclick(self.start)
        done()

    def grid(self):
        """Draw grid of tiles."""
        square(0, 0, 200, 'dark red')
        square(0, -200, 200, 'dark blue')
        square(-200, 0, 200, 'dark green')
        square(-200, -200, 200, 'khaki')
        update()

    def flash(self, tile):
        """Flash tile in grid."""
        glow, dark = tiles[tile]
        square(tile.x, tile.y, 200, glow)
        update()
        sleep(0.5)
        square(tile.x, tile.y, 200, dark)
        update()
        sleep(0.5)

    def grow(self):
        """Grow pattern and flash tiles."""
        tile = choice(list(tiles))
        pattern.append(tile)

        for tile in pattern:
            self.flash(tile)

        print('Pattern length:', len(pattern))
        guesses.clear()

    def tap(self, x, y):
        """Respond to screen tap."""
        onscreenclick(None)
        x = floor(x, 200)
        y = floor(y, 200)
        tile = vector(x, y)
        index = len(guesses)

        if tile != pattern[index]:
            score_to_add = self.score * 15
            update_score(Globals.username, score_to_add)
            messagebox.showinfo(" ", "You earned " + str(score_to_add) + " points!! \n close this window please")
            self.msg_display.write("Game is over! close this window...".format(self.score), align="center",
                                   font=("Arial", 16, "normal"))  # Game over msg display
            return

        guesses.append(tile)
        self.flash(tile)

        if len(guesses) == len(pattern):
            self.score += 1  # Increment score when player completes a round
            self.score_display.clear()  # Clear previous score
            self.score_display.write("Score: {}".format(self.score), align="center",
                                     font=("Arial", 16, "normal"))  # Update score display on screen
            print("Score:", self.score)
            self.grow()

        onscreenclick(self.tap)

    def start(self, x, y):
        """Start game."""
        self.grow()
        onscreenclick(self.tap)


if __name__ == "__main__":
    game = SimonSays()
