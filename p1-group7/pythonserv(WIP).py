# Server code
import socket
import os.path

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

    while True:
        print("ftp> get<file name> (Downloads file <file name> from the server)")
        print("ftp> put<file name> (Uploads file <file name> to the server)")
        print("ftp> ls (Lists files on the server)")
        print("ftp> quit (Disconnects from the server and exits)")
        userInput = input("ftp> ")

        if userInput == "get":
            print("I chose get")

            data = connectionSocket.recv(1024).decode()
            if not data:
                continue
            filename = 'output.txt'
            completeName = os.path.join(save_path, filename+".txt")
            fo = open(completeName, "w")
            while data:
                if not data:
                    break
                else:
                    fo.write(data)
                    data = connectionSocket.recv(1024).decode()
            print("Receiving file from client")
            print("Received successfully! New filename is: ", filename)

            fo.close()

        if userInput == "put":
            print("I chose put")

        if userInput == "ls":
            print("I chose ls")

        if userInput == "quit":
            #connectionSocket.close()
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