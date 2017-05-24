import sys
from Serveur.serveur.Connection import Connection
from Serveur.serveur.Serveur import Server
from Serveur.serveur.FileManager import FileManager
from Serveur.serveur.Protocole_xml import Protocole_xml
from Serveur.serveur.Protocole_json import Protocole_json


def main():

    #Vérification du bon nombre de paramètres
    if len(sys.argv) <= 2:
        print("Ce serveur nécessite le port et le format de message transmis, sois xml ou Json.")
        sys.exit(1)

    #Initialisations et assignations
    host = ''
    port = int(sys.argv[1])
    fileManager = FileManager()
    nb_clients = 1

    #Assignation et vérification des protocoles
    if (sys.argv[2] == "xml"):
        protocole = Protocole_xml(fileManager)

    elif(sys.argv[2] == "json"):
        protocole = Protocole_json(fileManager)

    else:
        print("Protocole invalide")
        sys.exit(1)

    #Début de la connexion
    connection = Connection(host, port)
    connection.startServerConnection()

    while True:
        print("Attente d'un client...")
        connection, addr = connection.serverSocket.accept()
        print("Connexion venant de ", addr)

        session = Server("Client " + str(nb_clients), connection, protocole)
        session.start()

        nb_clients += 1

if __name__ == '__main__':
    main()