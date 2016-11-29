import select
import sys
import socket
import string
import threading

win = False
score = 0


#This method checks the signal sent from server after user has inputted their guess.
def CheckAnswer(answer):
    guess = answer           
    
    if guess == "Far\r\n":
        print("Your guess is too far.")        
        print("Your Score is: " + str(score))
        
    elif guess == "Close\r\n":
        print("Your guess is close!")        
        print("Your Score is: " + str(score))
        
    elif guess == "Correct\r\n":
        print("You guessed correctly!")
        print("Your Score is: " + str(score))
        file = open("Scoreboard.txt","wt")
        file.write("Score was " + str(score))
        file.close()
        print("Game Over.")
        s.close()

#Client Server Code

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("127.0.0.1",4000))

print('Connect to:',"127.0.0.1,4000")

try:
    s.send("Hello\r\n".encode())
    greet = s.recv(80).decode()
    if greet == "Greetings\r\n":
        s.send("Game\r\n".encode())
    ready = s.recv(80).decode()
    if ready == "Ready\r\n":
        while win is not True:

            answer = (str(input("What is your guess:  ")))
            
            s.send(answer.encode())
            goal = s.recv(80).decode()
        
            CheckAnswer(goal)
        
            score += 1
        
            if goal == "Correct":
                print("Score saved.")
                print("Game Over.")
                s.rec(1024)
                s.close()
                break
    
 #Try except for when the server is closed before game completion   
except ConnectionResetError:
    print("Couldn't connect to Server. Closing Game.")
    s.close()
    
    


           
if ready == "Ready\r\n":
    while win is not True:

        answer = (str(input("What is your guess:  ")))
        
        s.send(answer.encode())
        goal = s.recv(80).decode()
    
        CheckAnswer(goal)
    
        score += 1
    
        if goal == "Correct":
            print("Score saved.")
            print("Game Over.")
            s.rec(1024)
            s.close()
            break
    
    
        





    
        

