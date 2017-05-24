import threading
from Serveur.serveur.RequestManager import RequestManager

class Server(threading.Thread):

    def __init__(self, threadName, connection, protocol):
        threading.Thread.__init__(self, name = threadName)
        self.connection = connection
        self.protocol = protocol
        self.requestManager = RequestManager(self)

    def run(self):
        while True: ##Pas certain si on doit faire plusieurs requêtes, jai envoyé un MIO au prof.
            clientRequest = self.connection.receive()
            interpretedClientRequest = self.protocol.interpreter(clientRequest)
            self.requestManaging(interpretedClientRequest)

    def requestManaging(self, clientRequest):
        self.requestManager.requestManaging(clientRequest)

    def bonjour(self):
        pass