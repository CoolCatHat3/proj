import socket
from threading import Thread
from all_windows.main_window import create_main_window
from other.common import *
from time import sleep

received_info = None


def recv_reg(info):
    global received_info
    # num, username, first_name, last_name, password = info
    received_info = info
    print(f"received {info}")


def recv_login(info):
    msg = buildMsg(info)
    print("1111", msg)
    send_q.put(msg)
    print("4141")


def client_recv_from_server(my_socket):
    while True:
        data = my_socket.recv(1024)
        data = data.decode('ascii')
        print("Server : " + data)
        recv_q.put(data)


def client_send_to_server(my_socket):
    while True:
        if not send_q.empty():
            msg = send_q.get()
            msg = msg.encode('utf-8')
            my_socket.send(msg)
            print("333", msg)
        sleep(0.02)  # sleep 20 ms - let the cpu breath


# won't start the game until the server confirms the login!
def main():
    print("starting...")
    print("client start")
    my_socket = socket.socket()
    my_socket.connect(("127.0.0.1", 18820))

    a = Thread(target=client_recv_from_server, args=(my_socket,))
    a.start()

    a = Thread(target=client_send_to_server, args=(my_socket,))
    a.start()

    print("client connect to server")

    print("activating registration window")
    create_main_window()


if __name__ == "__main__":
    main()
