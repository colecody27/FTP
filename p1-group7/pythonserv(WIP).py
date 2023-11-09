# Server code
import socket
import os.path

# Set the destination for writing output files
save_path = "D:\Fullerton\Senior Semester 1\CPSC_471\Programming_Assignment"

 # The port on which to listen
serverPort = 12000

 # Create a TCP's socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

 # Bind the socket to the port
serverSocket.bind(('', serverPort))

 # Start listening for incoming connections
serverSocket.listen(1) 
print ("The server is ready to receive")

 # Forever accept incoming connections
while True :
    # Accept a connection ; get client's socket
    connectionSocket, addr = serverSocket.accept()
    print("Connection to server is established")

    # Print the FTP protocol options as a loop and wait for user input
    while True:
        print("ftp> get<file name> (Downloads file <file name> from the server)")
        print("ftp> put<file name> (Uploads file <file name> to the server)")
        print("ftp> ls (Lists files on the server)")
        print("ftp> quit (Disconnects from the server and exits)")
        userInput = input("ftp> ")

        # If User wants to get a file from the server
        if userInput == "get":
            # Print this is the right function
            print("I chose get")

            # Get the data from the client and decode it
            data = connectionSocket.recv(1024).decode()
            # If there is no data then continue
            if not data:
                continue
            # Name the output file as output.txt
            filename = 'output.txt'
            # Create the output.txt file at desired destination on computer
            completeName = os.path.join(save_path, filename)
            # Open file
            fo = open(completeName, "w")
            while data:
                if not data:
                    break
                else:
                    fo.write(data)
                    # Write to the file the data gathered from the client side
                    data = connectionSocket.recv(1024).decode()
            print("Receiving file from client")
            print("Received successfully! New filename is: ", filename)

            # Close the file
            fo.close()

        if userInput == "put":
            print("I chose put")

        if userInput == "ls":
            print("I chose ls")

        if userInput == "quit":
            connectionSocket.close()
            break

    # The temporary buffer
    tmpBuff = "" 
    data = ""
    while len(data) != 40 :
        # Receive whatever the newly connected client has to send
        tmpBuff = connectionSocket.recv(40).decode()

        # The other side unexpectedly closed it’s socket
        if not tmpBuff :
            break

        # Save the data
        data += tmpBuff
        print (data)

    # Close the socket
    connectionSocket.close()