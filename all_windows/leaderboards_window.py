import tkinter as tk
from tkinter import ttk
import sqlite3

def open_leaderboards_window(parent_window):
    # Disable the main window
    parent_window.attributes('-disabled', True)

    def on_leaderboards_window_close():
        # Re-enable the main window when the register window is closed
        parent_window.attributes('-disabled', False)
        leaderboards_window.destroy()

    def fetch_leaderboard_data():
        # Connect to the database
        conn = sqlite3.connect('user_database.db')
        c = conn.cursor()

        # Fetch leaderboard data sorted by score in descending order
        c.execute("SELECT username, score FROM users ORDER BY score DESC")
        leaderboard_data = c.fetchall()

        # Close the connection
        conn.close()

        return leaderboard_data

    def populate_leaderboard_table():
        # Clear existing items in the treeview
        for item in leaderboard_treeview.get_children():
            leaderboard_treeview.delete(item)

        # Fetch leaderboard data from the database
        leaderboard_data = fetch_leaderboard_data()

        # Populate the leaderboard table with the fetched data
        for row in leaderboard_data:
            leaderboard_treeview.insert('', 'end', values=row)

    leaderboards_window = tk.Toplevel(parent_window)
    leaderboards_window.title("Leaderboards")
    leaderboards_window.geometry("700x550")
    leaderboards_window.protocol("WM_DELETE_WINDOW", on_leaderboards_window_close)

    # Create a treeview to display the leaderboard
    leaderboard_treeview = ttk.Treeview(leaderboards_window, columns=('Name', 'Score'), show='headings')
    leaderboard_treeview.heading('Name', text='Name')
    leaderboard_treeview.heading('Score', text='Score')
    leaderboard_treeview.pack(pady=20)

    # Populate the leaderboard table
    populate_leaderboard_table()

    leaderboards_window.mainloop()