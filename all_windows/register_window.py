# register_window.py
from customtkinter import CTkFont
import customtkinter
from tkinter import messagebox
from time import sleep
from other.common import buildMsg, send_q, recv_q, Globals


def open_register_window(parent_window, enable_game_button_callback):
    # Disable the main window
    parent_window.attributes('-disabled', True)
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green")

    register_window = customtkinter.CTk()
    register_window.geometry("800x550")

    # Define custom fonts
    custom_font = CTkFont(family="Helvetica", size=14, weight="bold")

    def attempt_register():
        # Here, you'd collect the data and send it to the server
        # For now, just print it to the console or use a messagebox to simulate registration
        username = username_entry.get()
        password = password_entry.get()
        verifypassword = verifypassword_entry.get()
        email = email_entry.get()
        gender = gender_entry.get()
        print(username, password, email, gender)

        # Server communication
        msgDst = "server"
        msgSrc = username
        msgType = "register"
        msgData = [username, password, email, gender]
        msgSend = buildMsg(msgDst, msgSrc, msgType, msgData)
        send_q.put(msgSend)
        regFlag = False
        while not regFlag:
            if not recv_q.empty():
                msgRecv = recv_q.get()
                print("772477", msgRecv)
                parts = msgRecv.split(",")
                if parts[0] == "True" and verifypassword == password and email.__contains__("@gmail.com") and (
                        gender.startswith("m") or gender.startswith("f")):
                    if len(password) > 4:
                        print("9999", "we registered successfully")
                        Globals.username = username  # save the name of the user of this client
                        messagebox.showinfo("Registration Successful", "You are now registered!")

                        # Close the register window and re-enable the main window
                        on_register_window_close()
                        parent_window.attributes('-disabled', False)
                        enable_game_button_callback(username)  # Enable the game button on successful registration
                        regFlag = True
                    else:
                        messagebox.showerror("Registration Failed",
                                             "Your password is too weak, please try again!")
                        regFlag = True  # do not wait here since it will stuck tkinter
                elif verifypassword != password:
                    messagebox.showerror("Registration Failed", "You typed two diffrent passwords, please try again!")
                    regFlag = True  # do not wait here since it will stuck tkinter
                elif not email.__contains__("@gmail.com"):
                    messagebox.showerror("Registration Failed", "Email is not correct, please try again!")
                    regFlag = True  # do not wait here since it will stuck tkinter
                elif not gender.startswith("m") or not gender.startswith("f"):
                    messagebox.showerror("Registration Failed", "gender incorrect, please try again and type M or F!")
                    regFlag = True  # do not wait here since it will stuck tkinter
                else:
                    messagebox.showerror("Registration Failed", "Username already taken, please try again!")
                    regFlag = True  # do not wait here since it will stuck tkinter
            sleep(0.02)  # sleep 20 ms - let the cpu breath

    def on_register_window_close():
        # Re-enable the main window when the register window is closed
        parent_window.attributes('-disabled', False)
        register_window.destroy()

    register_window.protocol("WM_DELETE_WINDOW", on_register_window_close)  # Bind custom close function

    label = customtkinter.CTkLabel(master=register_window, text="Register window", text_color="white", font=custom_font)
    label.pack(pady=25, padx=10)

    register_frame = customtkinter.CTkFrame(master=register_window)
    register_frame.pack(pady=20, padx=30, fill="both", expand=True)

    username_entry = customtkinter.CTkEntry(master=register_frame, placeholder_text="Username")
    username_entry.pack(pady=12, padx=10)

    password_entry = customtkinter.CTkEntry(master=register_frame, placeholder_text="Password", show="*")
    password_entry.pack(pady=12, padx=10)

    verifypassword_entry = customtkinter.CTkEntry(master=register_frame, placeholder_text="Verify password", show="*")
    verifypassword_entry.pack(pady=12, padx=10)

    email_entry = customtkinter.CTkEntry(master=register_frame, placeholder_text="email")
    email_entry.pack(pady=12, padx=10)

    gender_entry = customtkinter.CTkEntry(master=register_frame, placeholder_text="M/F")
    gender_entry.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(master=register_frame, text="Register", font=custom_font, command=attempt_register)
    button.pack(pady=8, padx=8)

    register_window.mainloop()
