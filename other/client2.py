import pickle
import sys
import socket
from threading import Thread
from main_window import *
from common import *
from time import sleep

received_info = None


def recv_reg(info):
    global received_info
    # num, username, first_name, last_name, password = info
    received_info = info
    print(f"received {info}")


def recv_login(info):
    #global received_info
    # num, username, password = info
    #received_info = info
    msg = buildMsg(info)
    print("1111", msg)
    send_q.put(msg)
    print("4141")
    #print(f"received {info}")


def client_recv_from_server(my_socket):
    while True:
        data = my_socket.recv(1024)
        data = data.decode('ascii')
        print("Server : " + data)
        recv_q.put(data)


def client_send_to_server(my_socket):
    while True:
        if send_q.empty() == False:
            msg = send_q.get()
            msg = msg.encode('utf-8')
            my_socket.send(msg)
            print("333", msg)
        sleep(0.02)  #sleep 20 ms - let the cpu breath


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
    login_confirmed = False
    print(not login_confirmed)
    while not login_confirmed:
        print(received_info)
        if received_info is not None:
            print("sending pickled information from registration")
            my_socket.send(pickle.loads(received_info))
            print("sent!!!!")



if __name__ == "__main__":
    main()
