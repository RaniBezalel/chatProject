import socket, select, sys

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080

def runClient():
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((SERVER_IP, SERVER_PORT))

    except socket.error as e:
        print(f"Socket error: {e}")
        sys.exit()

    clientUsername = handleUserConnection()
    clientSocket.send(clientUsername.encode("utf-8"))

    operatingClient = True

    while operatingClient:
        # constently check for new input or new messages from other clients
        currentSockets, _, _ = select.select([clientSocket, sys.stdin], [], [])

        for sock in currentSockets:
            if sock == sys.stdin:
                message = sys.stdin.readline().strip()
                clientSocket.send(message.encode("utf-8"))

                if(message.lower() == "exit"):
                    clientSocket.close()
                    operatingClient = False
                    break
        else:
            serverResponse = (clientSocket.recv(1024)).decode("utf-8")
            print(serverResponse)

def handleUserConnection():
    connectionUsername = ""
    while connectionUsername == "":
        connectionUsername = input("Enter your name: ").strip()
    
    print(f"Hi {connectionUsername}, if you wish to leave write exit")
    print("-------------------------------------")

    return connectionUsername

if __name__ == '__main__':
     runClient()