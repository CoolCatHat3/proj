# game_selection_window.py
from customtkinter import CTkFont
from tkinter import messagebox
import customtkinter
from games.rockpaperscissors import RockPaperScissors
from games.snake import SnakeGame
from games.simonsays import SimonSays


def open_game_selection_window(parent_window):
    # Disable the main window
    parent_window.attributes('-disabled', True)

    def run_rps():
        messagebox.showinfo("Rock paper scissors instructions: ", "   Choose Gesture: Select Rock, Paper, or Scissors."
                                                                  "Computer Chooses: The computer randomly selects "
                                                                  "Rock, Paper, or Scissors. "
                                                                  "Determine Winner:"
                                                                  "-Rock beats Scissors."
                                                                  "-Scissors beats Paper."
                                                                  "-Paper beats Rock."
                                                                  "Tie: If both you and the computer choose the same "
                                                                  "gesture, it’s a tie. "
                                                                  "Repeat: Play multiple rounds to see who wins more.")
        app = RockPaperScissors()
        app.run()

    def run_snake():
        messagebox.showinfo("Snake instructions: ", "Start the Game: move the snake to begin."
                                                    "Control the Snake: Use arrow keys to move the snake up, down, "
                                                    "left, or right. "
                                                    "Eat Food: Guide the snake to eat the food items that appear on "
                                                    "the screen. "
                                                    "Grow Longer: Each time the snake eats food, it grows longer."
                                                    "Avoid Crashing: Don't let the snake crash into the walls or its "
                                                    "own body. "
                                                    "Aim for High Score: Keep eating and growing to achieve the "
                                                    "highest score possible.")
        s = SnakeGame()
        s.run()

    def run_simon():
        messagebox.showinfo("🚨🚨Simon instructions:🚨🚨", "Turn On: click on the game window to start the game."
                                                           "Watch and Listen: The game will light up one of the four "
                                                           "colored buttons and play a corresponding tone. "
                                                           "Repeat the Sequence: Press the lit buttons in the same "
                                                           "order. "
                                                           "Progress: After each correct sequence, the game will add "
                                                           "one more step to the sequence. "
                                                           "Continue: Repeat the new, longer sequence."
                                                           "Game Over: If you press the wrong button, the game will "
                                                           "end. "
                                                           "Aim for High Score: Try to remember and replicate the "
                                                           "longest sequence possible to achieve the highest score")
        ss = SimonSays()
        ss.start()

    def on_game_selection_window_close():
        # Re-enable the main window when the register window is closed
        parent_window.attributes('-disabled', False)
        game_selection_window.destroy()

    game_selection_window = customtkinter.CTk()
    game_selection_window.geometry("800x550")
    game_selection_window.protocol("WM_DELETE_WINDOW", on_game_selection_window_close)

    label = customtkinter.CTkLabel(master=game_selection_window, text="Select your game... good luck and have fun!",
                                   text_color="white")
    label.pack(pady=25, padx=10)

    game_frame = customtkinter.CTkFrame(master=game_selection_window)
    game_frame.pack(pady=20, padx=30, fill="both", expand=True)

    button1 = customtkinter.CTkButton(master=game_frame, text="Rock paper scissors", command=run_rps,
                                      hover_color="blue", border_color="black", border_width=3)
    button1.pack(pady=8, padx=8)
    button2 = customtkinter.CTkButton(master=game_frame, text="Snake", command=run_snake, hover_color="yellow",
                                      border_color="black", border_width=3)
    button2.pack(pady=8, padx=8)
    button3 = customtkinter.CTkButton(master=game_frame, text="Simon", command=run_simon, hover_color="black",
                                      border_color="black", border_width=3)
    button3.pack(pady=8, padx=8)

    game_selection_window.mainloop()
