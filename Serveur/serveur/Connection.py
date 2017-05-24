import socket

class Connection:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.serverSocket = socket.socket()

    def startServerConnection(self):
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(5)

    def send(self, text):  ## envoyer information au client
        self.serverSocket.send(bytes(str(text), "UTF-8"))

    def receive(self):  ## recoi une réponse du client
        data = self.serverSocket.recv(2048).decode("UTF-8")
        return data

    def close(self):
        self.serverSocket.close()