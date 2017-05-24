
import threading

class Server(threading.Thread):

    def __init__(self, threadName, connection):
        threading.Thread.__init__(self, name = threadName)
        self.connection = connection

    def run(self):
        pass