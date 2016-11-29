#Server Code
import socket
import select
import sys
import random
import re
import threading

TCP_IP = '127.0.0.1'
TCP_PORT = 4000
TCP_PORT2 = 4001
#Checks if client socket is created properly   
try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP,TCP_PORT))
        s.listen(5)
except socket.error:
           print("Failed to create socket")

    #Checks if admin socket is created properly
try:
        ads = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ads.bind((TCP_IP,TCP_PORT2))
        ads.listen(5)
except socket.error:
        print("Failed to create socket")

    
addrs = []
connList = []

connList.append(s)
connList.append(ads)

def Within(value, goal):
    #goal = ans
    #value = guess
    n1 = value + 3
    n2 = value - 3
    
    if goal > n2 and goal < n1:
           
        return 1
    else:
        return 0

#Player Client
def Player(conn):
    
    hello = conn.recv(80).decode() 
    if hello == "Hello\r\n":   
        conn.send("Greetings\r\n".encode())
     
    game = conn.recv(80).decode()
    if game == "Game\r\n":
        conn.send("Ready\r\n".encode())
     
    while game == "Game\r\n":
        ans = random.randint(1,30)
        #checks if the server is still running
        try:
            xx = conn.recv(80).decode()
        except ConnectionResetError:
            print("Client closed connection forcibly")
            conn.close()
            connList.remove(conn)
            break
        
        guess = int(xx)
                       
        if guess == ans:
            conn.send("Correct\r\n".encode())
            print("User has won. Ending game....\n")
            conn.close()
            connList.remove(conn)
            break

        elif Within(guess, ans):
            conn.send("Close\r\n".encode())

        elif guess > ans or guess < ans:
            conn.send("Far\r\n".encode())

def Admin(A_conn):

    admin_hello = A_conn.recv(80).decode()
    if admin_hello == "Hello\r\n":
        #print(admin_hello)
        A_conn.send("Admin-Greetings\r\n".encode())
    
    admin_who = A_conn.recv(80).decode()
    if admin_who == "Who\r\n":
        #print(admin_who)
        clientList = '\r\n'.join("%s, %s" % tup for tup in addrs)
        #print (clientList)
        A_conn.send(str(clientList).encode())
       # addrs.remove(A_addr)
    

#While the user is connected to the server...
running = 1

while running:
    
    try:
        r, w, e = select.select(connList,[],[])
    except ValueError:
        s.close()

    for i in r:
        #new connection - Client
        if i == s:
            (conn,addr) = s.accept()
            connList.append(conn)
            addrs.append(addr)
            print('Connection address from:',addr)                
            t = threading.Thread(target = Player, args = (conn,))               
            t.start()

        #new connection - Admin    
        elif i == ads:
            (A_conn,A_addr) = ads.accept()
            connList.append(A_conn)
           # addrs.append(A_addr)
            print('Admin connection from:',A_addr)
            A_t = threading.Thread(target = Admin, args = (A_conn,)) 
            A_t.start()
