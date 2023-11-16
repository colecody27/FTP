# Client code 
import socket
import os

# ************************************************
# Downloads file from server
# @param filename - Name of file to be retreived from server
# ************************************************
def get(filename):
    # Print this is the right function
    print("I chose get")
    print("Receiving file from server...")

    # Create data channel 
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to port 0
    dataSocket.bind(('',0))

    # Retreive the ephemeral port number
    print ("I chose ephemeral port: ", dataSocket.getsockname()[1])

    # Connect to server 
    dataSocket.connect(serverName, serverPort)

    # Validate filename
    dirContents = os.listdir()

    i = 0
    if(filename in dirContents):
        while filename in dirContents:
            i += 1
        filename = str(i) + filename 

    # Open file in append mode
    file = open(filename, "a")

    # Get the data from the server and decode it
    while True:
        # Receive data
        data = dataSocket.recv(40).decode()

        # If there is no data then close file 
        if not data:
            file.close()
            break
        else:
            file.write(data)

    # Success output
    print("SUCCESS")
    print(filename + " has been downloaded successfully")
    print("Number of bytes downloaded: " + file.__sizeof__)

    # Close data channel 
    file.close()
    dataSocket.close()

# ************************************************
# Uploads file to server
# @param filename - Name of file to be retreived from server
# ************************************************
def put(filename):
    # Print this is the right function
    print("I chose put")

    # Create data channel 
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to port 0
    dataSocket.bind(('',0))

    # Retreive the ephemeral port number
    print ("I chose ephemeral port: ", dataSocket.getsockname()[1])

    # Connect to server 
    dataSocket.connect(serverName, serverPort)

    # Verify file is in directory
    dirContents = os.listdir()
    while filename not in dirContents:
        filename = input(filename + " was not found. Please re-enter filename.")

    file = open(filename, "r")
    
    # Upload file to server 
    print("Uploading file to server...")
    try:
        dataSocket.sendAll(file).encode()
    except IOError:
        print("Unable to upload contents to server")
        file.close()
        dataSocket.close()

    print("SUCCESS")
    print(filename + " has been uploaded successfully")
    print("Number of bytes uploaded: " + file.__sizeof__)

    file.close()
    dataSocket.close()

# ************************************************
# List files found on server
# ************************************************
def list():
    # Print this is the right function
    print("I chose list")
    print("Outputting files found on server...")

    # Create data channel 
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to port 0
    dataSocket.bind(('',0))

    # Retreive the ephemeral port number
    print ("I chose ephemeral port: ", dataSocket.getsockname()[1])

    # Connect to server 
    dataSocket.connect(serverName, serverPort)

    # Create temp file to store server contents
    try: # Create new file
        file = open("servercontents.txt", "x") 
    except IOError: # Overwrite contents of file
        file = open("servercontents.txt", "w")

    # Set file to append mode    
    open(file, "a")

    # Get the data from the server and decode it
    while True:
        # Receive data
        data = dataSocket.recv(40).decode()

        # If there is no data then close file 
        if not data:
            break
        else:
            file.write(data)        
    
    #Output contents of file
    lines = file.readlines()
    for line in lines:
        print(line)

    # Success output
    print("SUCCESS")
    print("Contents of server have been output successfully")
    print("Number of bytes downloaded: " + file.__sizeof__)

    # Close data channel 
    dataSocket.close()
    file.close()

# Name and port number of the server to which want to connect
serverName = "localhost"
serverPort = 12000

# Create a socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Connect to the server
clientSocket.connect((serverName, serverPort))

# Continiously accept user commands
while True:
    #Prompt user for command 
    print("ftp> get <file name> (Downloads file <file name> from the server)")
    print("ftp> put <file name> (Uploads file <file name> to the server)")
    print("ftp> ls (Lists files on the server)")
    print("ftp> quit (Disconnects from the server and exits)")
    [command, filename] = input("ftp> ").split(" ")

    match command:
        case "get":
            get(filename)
        case "put":
            put(filename)
        case "ls":
            list()
        case "quit":
            clientSocket.close()
            break    