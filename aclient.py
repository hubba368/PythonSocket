import select
import sys
import socket
import string
import threading

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("127.0.0.1",4001))

running = 1

while running:
    
    try:
        s.send("Hello\r\n".encode())

        adminGreet = s.recv(80).decode()
        if adminGreet == "Admin-Greetings\r\n":
            print('Connect to:',"127.0.0.1,4001")
            s.send("Who\r\n".encode())
            adminWho = s.recv(80).decode()
            print(adminWho)
    #If the server is closed whilst still connected        
    except ConnectionResetError:
        print("Connection closed forcibly")
        running = 0
        s.close()
           

