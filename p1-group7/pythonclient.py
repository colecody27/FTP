# Client code 
import socket
import os
import sys

def main():
    # Store server's ephemeral port number
    global dataPort

    # Creation of the Control Channel - stays active for the entire duration of the connection and accepts commands (Different form Data Channel)
    global serverName
    serverName = sys.argv[1]

    # Gets the port number from user when running file
    serverPort = int(sys.argv[2])

    # Creation of TCP socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    clientSocket.connect((serverName, serverPort))
    print(f"Made connection to {serverName}:{serverPort}")

    while True:
        # Prompt user for command 
        print("ftp> get <file name> (Downloads file <file name> from the server)")
        print("ftp> put <file name> (Uploads file <file name> to the server)")
        print("ftp> ls (Lists files on the server)")
        print("ftp> quit (Disconnects from the server and exits)")

        # Validate user input
        userInput = input("ftp> ").split(" ")
        if (len(userInput) == 1):
            command = userInput[0]
        else:
            command, filename = userInput[0], userInput[1]

        match command:
            case "get":
                clientSocket.send(bytes("get", 'utf-8'))
                dataPort = int(clientSocket.recv(40).decode())
                get(filename)
            case "put":
                clientSocket.send(bytes("put", 'utf-8'))
                dataPort = int(clientSocket.recv(40).decode())
                put(filename)
            case "ls":
                clientSocket.send(bytes("ls", 'utf-8'))
                dataPort = int(clientSocket.recv(40).decode())
                list()
            case "quit":
                clientSocket.send(command.encode())
                clientSocket.close()
                print("Connection closed" )
                break
            case _:
                print("ftp> Command not found.")

# ************************************************
# Give unique names to files
# @param filename - Name of file to be retreived from server
# ************************************************
def get_unique_filename(filename):
        # Validate filename uniqueness in the local directory
        dirContents = os.listdir()

        # File doesn't exist, return original filename
        if filename not in dirContents:
            return filename  

        i = 1
        while True:
            # Create a new filename by appending a numeric suffix
            new_filename = f"{os.path.splitext(filename)[0]}_{i}{os.path.splitext(filename)[1]}"
            if new_filename not in dirContents:
                return new_filename  # Return unique filename
            i += 1

# ************************************************
# Downloads file from server
# @param filename - Name of file to be retreived from server
# ************************************************
def get(filename):
    # Print this is the right function
    print("I chose get")

    # Create data channel 
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server 
    dataSocket.connect((serverName, dataPort))

    # Send filename to server
    dataSocket.send(filename.encode())
    
    #generate a unqiue filename
    new_filename = get_unique_filename(filename)   

    # Open file in append mode
    file = open(new_filename, "a")

    # Get the data from the server and decode it
    print("Receiving file from server...")
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
    print("Number of bytes downloaded: " + str(os.stat(filename).st_size))

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

    # Connect to server 
    dataSocket.connect((serverName, dataPort))

    # Verify file is in directory
    dirContents = os.listdir()
    while filename not in dirContents:
        filename = input(filename + " was not found. Please re-enter filename.")

    # Send filename to server 
    dataSocket.send(filename.encode())

    file = open(filename, "r")
    
    # Upload file to server 
    print("Uploading file to server...")
    try:
        dataSocket.sendall(file.read().encode())
    except IOError:
        print("Unable to upload contents to server")
        file.close()
        dataSocket.close()

    print("SUCCESS")
    print(filename + " has been uploaded successfully")
    print("Number of bytes uploaded: " + str(os.stat(filename).st_size))

    file.close()
    dataSocket.close()

# ************************************************
# List files found on server
# ************************************************
def list():
    # Print this is the right function
    print("I chose list")
    print("Finding files on server...")
    print(serverName)
    # Create data channel 
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server 
    dataSocket.connect((serverName, dataPort))
    dirList = ""

    # Get the data from the server and decode it
    while True:
        # Receive data
        data = dataSocket.recv(40).decode()

        # If there is no data then close file 
        if not data:
            break
        else:
            dirList = dirList + data
    
    #Output contents of file
    for line in dirList.split("\n"):
        print(line)

    # Success output
    print("SUCCESS")
    print("Contents of server have been output successfully")
    print("Number of bytes downloaded: " + str(len(dirList.encode('utf-8')))) 

    # Close data channel 
    dataSocket.close()

if __name__ == "__main__":
    main()
