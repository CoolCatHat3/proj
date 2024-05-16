# login_window.py
from tkinter import messagebox
import customtkinter
from time import sleep
from other.common import buildMsg, send_q, recv_q, Globals


def open_login_window(parent_window, enable_game_button_callback):
    parent_window.attributes('-disabled', True)

    login_window = customtkinter.CTk()
    login_window.geometry("800x550")

    def attempt_login():
        # Here, you'd collect the data and send it to the server
        # For now, just print it to the console or use a messagebox to simulate registration
        username = username_entry.get()
        password = password_entry.get()
        print(username, password)

        # Server communication
        msgDst = "server"
        msgSrc = username
        msgType = "login"
        msgData = [username, password]
        msgSend = buildMsg(msgDst, msgSrc, msgType, msgData)
        send_q.put(msgSend)
        regFlag = False
        while not regFlag:
            if not recv_q.empty():
                msgRecv = recv_q.get()
                print("777127", msgRecv)
                parts = msgRecv.split(",")
                if parts[0] == "True":
                    print("9999", "we login successful")
                    Globals.username = username  # save the name of the user of this client
                    messagebox.showinfo("Login Successful", "You are now logined!")

                    # Close the login window and re-enable the main window
                    close_login_window()
                    parent_window.attributes('-disabled', False)
                    enable_game_button_callback(username)  # Enable the game button on successful registration
                    regFlag = True
                else:
                    messagebox.showerror("Login Failed", "Incorrect username or password.")
                    regFlag = True  # do not wait here since it will stuck tkinter
            sleep(0.02)  # sleep 20 ms - let the cpu breath

    def close_login_window():
        parent_window.attributes('-disabled', False)  # Re-enable the main window
        login_window.destroy()

    login_window.protocol("WM_DELETE_WINDOW", close_login_window)  # Bind custom close function

    label = customtkinter.CTkLabel(master=login_window, text="Login window", text_color="white")
    label.pack(pady=25, padx=10)

    login_frame = customtkinter.CTkFrame(master=login_window)
    login_frame.pack(pady=20, padx=30, fill="both", expand=True)

    username_entry = customtkinter.CTkEntry(master=login_frame, placeholder_text="Username")
    username_entry.pack(pady=12, padx=10)

    password_entry = customtkinter.CTkEntry(master=login_frame, placeholder_text="Password", show="*")
    password_entry.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(master=login_frame, text="Login", command=attempt_login)
    button.pack(pady=8, padx=8)

    login_window.mainloop()