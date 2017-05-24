import threading

class Server(threading.Thread):

    def __init__(self, threadName, connection, protocol):
        threading.Thread.__init__(self, name = threadName)
        self.connection = connection
        self.protocol = protocol

    def run(self):
        pass