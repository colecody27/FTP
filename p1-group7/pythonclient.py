# Client code 
import socket

# Name and port number of the server to which want to connect
#ip = socket.gethostbyname()
serverName = 'ecs.fullerton.edu'
serverPort = 12000

# Create a socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Connect to the server
clientSocket.connect((serverName, serverPort))

# A string we want to send to the server
data = "Hello World This is a very long string."

bytesSent = 0

# Keep sending bytes until all bytes are sent
while bytesSent != len(data) :
    # Send that string !
    bytesSent += clientSocket.send(data[bytesSent :])

# Close the socket
clientSocket.close()