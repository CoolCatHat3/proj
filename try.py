# game_selection_window.py

import customtkinter
from rockpaperscissors import RockPaperScissors
from snake import SnakeGame
from simonsays import SimonSays
import tkinter as tk


def open_game_selection_window(parent_window):
    # Disable the main window
    parent_window.attributes('-disabled', True)

    def run_rps():
        app = RockPaperScissors()
        app.run()

    def run_snake():
        s = SnakeGame()
        s.run()

    def run_simon():
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

    button = customtkinter.CTkButton(master=game_frame, text="Rock paper scissors", command=run_rps)
    button.pack(pady=8, padx=8)
    button = customtkinter.CTkButton(master=game_frame, text="Snake", command=run_snake)
    button.pack(pady=8, padx=8)
    button = customtkinter.CTkButton(master=game_frame, text="Simon says", command=run_simon)
    button.pack(pady=8, padx=8)

    game_selection_window.mainloop()

