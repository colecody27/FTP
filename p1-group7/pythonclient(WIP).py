# Client code 
import socket

# Name and port number of the server to which want to connect
#ip = socket.gethostbyname()
serverName = "localhost"
serverPort = 12000

# Create a socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Connect to the server
clientSocket.connect((serverName, serverPort))

# While Loop to send a file to server
while True:
    print("Send file to server")
    # Getting the input file name
    filename = input ("input filename you want to send: ")
    # Open and read target file, if no file then break
    try:
        fi = open(filename, "r")
        data = fi.read()
        if not data:
            break
        # If there is data, encode it and send it
        while data:
            clientSocket.send(str(data).encode())
            data = fi.read()
        fi.close()
        break
    except IOError:
        print("You entered an invalid filename!\
              Please enter a valid name")

# A string we want to send to the server
data = "Hello World This is a very long string."

bytesSent = 0

# Keep sending bytes until all bytes are sent
while bytesSent != len(data):
    # Send that string !
    bytesSent += clientSocket.send(data[bytesSent :].encode())

# Close the socket
clientSocket.close()