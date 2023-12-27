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
    
    connectionUsername = ""
    while connectionUsername == "":
        connectionUsername = input("Enter your name: ").strip()

    clientSocket.send(connectionUsername.encode("utf-8"))
    print(f"Hi {connectionUsername}, if you wish to leave write exit")
    print("-------------------------------------")

    operatingClient = True

    while operatingClient:
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
       
if __name__ == '__main__':
     runClient()