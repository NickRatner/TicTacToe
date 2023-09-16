import socket
from _thread import *
import sys

server = "192.168.2.100"  #this is a local ip address
port = 5555 #a port that is typically open

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))  #binds the ip address stored in "server" to the given port
except socket.error as e:
    print("Something went wrong!")
    print(e)

s.listen(2)  #opens up the port so clients can connect to it. Argument is 2 because I only want 2 people to connect at a time for my tictactoe game
print("Waiting for connection, Server started")

def threaded_client(connection, connectedClients): #this is a threaded function, it will run as a seperate thread

    connection.send(str.encode("Connected"))  #sends a confirmation to the connecting object that everything worked
    reply = ""
    while True:
        try: #attempt to recieve data from whoever is connected
            data = connection.recv(2048) #recieve 2048 bits of information from the connection
            reply = data.decode("utf-8") #data is encoded, so we have to decode it first in the utf-8 format

            if not data:  #if no data is recieved (ex. if client disconnected)
                print("Disconnected")
                break
            else:
                print(f"Received: {reply}")
                print(f"Sending: {reply}")

            connection.sendall(str.encode(reply + str(connectedClients)))

        except:
            break

    print("Lost Connection")
    connection.close()

connectedClients = 0 #tracks the number of connected clients and sends it to each client, so it can figure out of it is "x" or "o"
while True: #this loop while continuously look for connections
    connection, addr = s.accept()  #this while store the connection and the address in the respective variables when a connection occurs
    print(f"Connected to: {addr}")

    connectedClients += 1
    start_new_thread(threaded_client, (connection, connectedClients))  #runs "threaded_client()" as a new thread