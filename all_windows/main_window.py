from tkinter import messagebox
import customtkinter
from all_windows.login_window import open_login_window
from other.common import Globals, buildMsg, send_q, recv_q
from all_windows.register_window import open_register_window
from all_windows.game_selection_window import open_game_selection_window
from all_windows.leaderboards_window import open_leaderboards_window
from time import sleep

def create_main_window():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green")

    main_window = customtkinter.CTk()
    main_window.geometry("1000x750")

    label = customtkinter.CTkLabel(master=main_window, text="Arcade - home page", text_color="white")
    label.pack(pady=25, padx=10)

    auth_frame = customtkinter.CTkFrame(master=main_window)
    auth_frame.pack(pady=20, padx=30, fill="both", expand=True)

    def enable_game_button(name):
        register_button.configure(state='disabled')
        login_button.configure(state='disabled')
        logout_button.configure(state='normal')
        game_button.configure(state='normal')
        main_window.title("Main Menu " + name)

    def disable_game_button():
        register_button.configure(state='normal')
        login_button.configure(state='normal')
        logout_button.configure(state='disabled')
        game_button.configure(state='disabled')
        main_window.title("Main Menu")

    def logout():
        # Server communication
        msgDst = "server"
        username = Globals.username
        msgSrc = username
        msgType = "logout"
        msgData = ["stam"]
        msgSend = buildMsg(msgDst, msgSrc, msgType, msgData)
        send_q.put(msgSend)

        regFlag = False
        while not regFlag:
            if not recv_q.empty():
                msgRecv = recv_q.get()
                print("777197", msgRecv)
                parts = msgRecv.split(",")
                if parts[0] == "False":
                    print("9999", "we logout successful")
                    Globals.username = ""  # release the name of the user of this client
                    disable_game_button()
                    messagebox.showinfo("Logout Successful", "You are now logout!")
                    regFlag = True
                else:
                    messagebox.showerror("Logout Failed", "???")
                    regFlag = True  # do not wait here since it will stuck tkinter
            sleep(0.02)  # sleep 20 ms - let the cpu breath

    register_button = customtkinter.CTkButton(master=auth_frame, text="Register",
                                              command=lambda: open_register_window(main_window, enable_game_button))
    register_button.pack(pady=12, padx=10)

    login_button = customtkinter.CTkButton(master=auth_frame, text="Login", command=lambda: open_login_window(main_window, enable_game_button))
    login_button.pack(pady=12, padx=10)

    logout_button = customtkinter.CTkButton(master=auth_frame, text="Logout", command=logout, state='disabled')
    logout_button.pack(pady=12, padx=10)

    game_button = customtkinter.CTkButton(master=auth_frame, text="Game selection",  hover_color="green", state='disabled',
                           command=lambda: open_game_selection_window(main_window))
    game_button.pack(pady=12, padx=10)

    leaderboards_button = customtkinter.CTkButton(master=auth_frame, text="leaderboards",
                                command=lambda: open_leaderboards_window(main_window))
    leaderboards_button.pack(pady=12, padx=10)

    main_window.mainloop()


if __name__ == "__main__":
    create_main_window()
