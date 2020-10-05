#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 50001       # Port to listen on (non-privileged ports are > 1023)

class Server(BaseException):
    def __init__(self):
        pass
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            print("Listening...")

            #s.settimeout(None)
            s.listen()
            conn, addr = s.accept()
            with conn:
                conn.settimeout(1)
                print('Connected by', addr)
                while True:
                    try:

                        data = conn.recv(1024)
    #                       if not data:
    #                       exit()   break
                        print(data.decode())
                        conn.sendall(data)
                    except socket.timeout as exc:
                        print("Caught exception socket.error :", exc)
                        #exit(1);


if __name__=="__main__":
    server = Server()
    server.run()