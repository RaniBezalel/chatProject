import socket, threading

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080
currentClients = []

def serverInit():
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((SERVER_IP, SERVER_PORT))
        serverSocket.listen(0)
        print("Server is up and running")
        
    except socket.error as e:
        print(f"Socket error: {e}")

    while True:
        clientSocket, _ = serverSocket.accept()
        currentClients.append(clientSocket)

        try:
            newThread = threading.Thread(target=manageClient, args=(clientSocket, ))
            newThread.start()

        except threading.ThreadError as e:
            print(f"Thread error: {e}")


def sendMessageToAllClients(response):
        for client in currentClients:
            try:
                client.send(response.encode("utf-8"))
            except:
                 currentClients.remove(client)

def manageClient(clientSocket):
        clientUsername = (clientSocket.recv(1024)).decode("utf-8")
        welcomeMessage = f"{clientUsername} has joined the chatroom"
        sendMessageToAllClients(welcomeMessage)

        while True:
            message = (clientSocket.recv(1024).decode("utf-8")).strip()
            response = f"({clientUsername}):{message}"

            if (message.lower() == "exit"):
                sendMessageToAllClients(f"{clientUsername} has now left the chatroom")
                currentClients.remove(clientSocket)
                clientSocket.close()
                break
            
            sendMessageToAllClients(response)

if __name__ == '__main__':
     serverInit()