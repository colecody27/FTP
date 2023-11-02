# Client code 
from socket import ∗

# Name and port number of the server to which want to connect
serverName = ecs.fullerton.edu
serverPort = 12000

# Create a socket
clientSocket = socket(AF INET, SOCKSTREAM) 
# Connect to the server
clientSocket.connect((serverName, serverPort))
# A string we want to send to the server
data = ”Hello World This is a very long string.”

# byte sSent = 0

# Keep sending bytes until all bytes are sent
while bytes Sent != len(data) :
# Send that string !
bytes Sent += clientSocket.send(data[ bytes Sent : ])
# Close the socket
clientSocket.close()