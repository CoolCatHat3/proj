import socket
from threading import Thread, Lock
import sqlite3

users = []
conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()

# Create a table named 'users' with columns 'username' (primary key), 'password', 'score', and 'login'
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    score INTEGER,
                    login TEXT
                )''')

conn.commit()
conn.close()


class User:

    def __init__(self, user, password, bornYear, email, gender, user_socket):
        self.user = user
        self.password = password
        self.bornYear = bornYear
        self.email = email
        self.gender = gender

        self.login = "True"
        self.user_socket = user_socket

    def __repr__(self):
        data = self.user + " " + self.password + " " + self.bornYear + " " + self.email + " " + self.gender + " " + self.login
        return data


class handle_client(Thread):
    clients = []  # class variable
    lock = Lock()

    @classmethod
    def broadcast(cls, to, msg):  # class method
        msg = msg + ","
        msg = msg.encode('utf-8')
        handle_client.lock.acquire()
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()

        # Execute a SELECT query to retrieve user data based on the username
        cursor.execute("SELECT * FROM users WHERE username=?", (to,))
        username = cursor.fetchone()

        # Execute a SELECT query to retrieve user data based on the username
        cursor.execute("SELECT login FROM users WHERE username=?", (to,))
        user_login = cursor.fetchone()
        for i in users:
            if users[i][0] == to:
                user = i
        conn.close()
        if user_login[0] == "True":
            if to == "All":  # send message to all
                username.user_socket.send(msg)
            elif to == username[0]:  # send message just to specific user
                user.user_socket.send(msg)
        handle_client.lock.release()

    def __init__(self, client_socket):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.login = "False"
        self.user = None
        handle_client.clients.append(client_socket)

    # login   - can be true/false - it true, the client login to server
    # srcName - who send the message - server of one of the clients
    # msgType - command type: login, register or logout.
    # msgData - data being transferred in the messages.
    def buildMsgToClient(self, msg_login, msg_type, srcName, msg_data):
        data = msg_login + "," + msg_type + "," + srcName + "," + msg_data
        return data

    def parse_client_message(self, client_message):
        parts = client_message.split(",")
        msgDst = parts[0]
        msgSrc = parts[1]
        message_type = parts[2]

        if message_type == "login":
            user = parts[3]
            password = parts[4]

            conn = sqlite3.connect('user_database.db')
            cursor = conn.cursor()

            # Execute a SELECT query to retrieve user data based on the username
            cursor.execute("SELECT * FROM users WHERE username=?", (user,))
            username = cursor.fetchone()

            conn.close()

            if username:
                # If the user exists, check if the provided password matches the stored password
                stored_password = username[1]  # Index 1 corresponds to the password column
                login_before = username[3]  # Check if someone already logged in to this account.
                if password == stored_password and login_before == "False":
                    print("user {} login succesfully".format(user))
                    self.login = "True"

                    # Connect to SQLite database
                    conn = sqlite3.connect('user_database.db')
                    cursor = conn.cursor()
                    # Define the update parameters
                    username_to_update = user
                    new_login = 'True'
                    # Execute the UPDATE statement
                    update_query = "UPDATE users SET login = ? WHERE username = ?"
                    cursor.execute(update_query, (new_login, username_to_update))
                    # Commit the changes to the database
                    conn.commit()
                    # Close the connection
                    conn.close()
                    val = User(user, password, 'bornYear', 'email', 'gender', self.client_socket)
                    users.append(val)
                    self.user = username
                    data = self.buildMsgToClient(self.login, "Login", "Server", "Succeed")
                    return data
                elif login_before == "True":
                    print(("user {} is already logged in to the server".format(user)))
                    data = self.buildMsgToClient(self.login, "Login", "Server", "Failed")
                else:
                    print("user {} login failed".format(user))
                    data = self.buildMsgToClient(self.login, "Login", "Server", "Failed")
            else:
                print("Username not found. Please register first.")
                print("user {} login failed".format(user))
                data = self.buildMsgToClient(self.login, "Login", "Server", "Failed")

        elif message_type == "logout":
            self.login = "False"
            # Connect to SQLite database
            conn = sqlite3.connect('user_database.db')
            cursor = conn.cursor()
            # Define the update parameters
            username_to_update = msgSrc
            new_login = "False"
            # Execute the UPDATE statement
            update_query = "UPDATE users SET login = ? WHERE username = ?"
            cursor.execute(update_query, (new_login, username_to_update,))

            # Commit the changes to the database
            conn.commit()
            cursor.execute("SELECT login FROM users WHERE username = ?", (username_to_update,))
            print(cursor.fetchone())
            # Close the connection
            conn.close()
            self.user = None
            data = self.buildMsgToClient(self.login, "Logout", "Server", "You succesfully logout")

        elif message_type == "register":
            user = parts[3]
            password = parts[4]
            bornYear = parts[5]
            email = parts[6]
            gender = parts[7]

            conn = sqlite3.connect('user_database.db')
            cursor = conn.cursor()

            # Execute a SELECT query to retrieve user data based on the username
            cursor.execute("SELECT * FROM users WHERE username=?", (user,))
            username = cursor.fetchone()

            conn.close()

            if username:
                # If the user exists, can't register...
                print("user {} already exist".format(user))
                data = self.buildMsgToClient(self.login, "Registration", "Server", "Failed - user already exist")
                return data

            val = User(user, password, bornYear, email, gender, self.client_socket)
            users.append(val)

            # Insert the new user data
            conn = sqlite3.connect('user_database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, score, login) VALUES (?, ?, ?, ?)",
                           (user, password, 0, "True"))

            conn.commit()
            conn.close()
            print("User registered successfully.")

            print("The client register user {} password {} email {}".format(user, password, email))
            self.login = "True"  # when someone register he also login
            self.user = user
            data = self.buildMsgToClient(self.login, "Registration", "Server", "Succeed")
        else:
            val = client_message[::-1]  # reverse the string
            msg_type = "Unknown"
            msg_data = val
            data = msg_type + "," + msg_data
        return data

    def run(self):
        stop = 1
        while stop == 1:
            try:
                client_info = self.client_socket.recv(1024)

            except:
                print("client {} close forcibly the socket".format(self.user))
                stop = 0  # stop the while. get out from thread
                # print("111",users)
                for i, o in enumerate(users):  # set the user to logout (do not remove him from users list!!!)
                    if o.user == self.user:
                        o.login = "False"  # del users[i]
                        print("222 state of user", o.user, o.login)
                        break

                continue
            # handle_client.broadcast(client_info)
            client_info_str = client_info.decode('utf-8')

            if client_info_str == "":
                self.client_socket.close()
                print("client close the socket")
            print("server got: " + client_info_str)
            data = self.parse_client_message(client_info_str)
            if data == "Send":
                continue  # we already send response to client from parse_client_message()
            data = data.encode('utf-8')  # convert the string to bytes
            self.client_socket.send(data)


class Server:
    def __init__(self, port):
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', port))

    def go(self):
        self.server_socket.listen(5)

        while 1:
            print("wait for client")
            (client_socket, client_address) = self.server_socket.accept()
            print("new client connect")

            stam = handle_client(client_socket)
            stam.start()


def main():
    print("server start")
    a = Server(8820)
    a.go()


if __name__ == "__main__":
    main()
