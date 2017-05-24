import sys
from Serveur.serveur.ClientRequest import ClientRequest
from Serveur.serveur.Serveur import Server

class RequestManager: #Chef d'orchestre qui indique au serveur quoi faire.

    def __init__(self, server):
        self.server = server

    def requestManaging(self, clientRequest):
        #Vérification du type de donnée de la variable en paramètre, elle devrait faire partie de l'enum ClientRequest

        if (isinstance(clientRequest, ClientRequest) == False):
            print("The type of client request is incorrect")
            sys.exit(1)

        if (clientRequest == ClientRequest.BONJOUR_SERVEUR):
            self.server.bonjour()
        elif (clientRequest == ClientRequest.NOM_SERVEUR):
            pass
        elif (clientRequest == ClientRequest.LISTE_DOSSIERS):
            pass
        elif (clientRequest == ClientRequest.LISTE_FICHIERS):
            pass
        elif (clientRequest == ClientRequest.CREER_DOSSIER):
            pass
        elif (clientRequest == ClientRequest.FICHIER_IDENTIQUE):
            pass
        elif (clientRequest == ClientRequest.FICHIER_RECENT):
            pass
        elif (clientRequest == ClientRequest.SUPPRIMER_DOSSIER):
            pass
        elif (clientRequest == ClientRequest.SUPPRIMER_FICHIER):
            pass
        elif (clientRequest == ClientRequest.TELECHARGER_FICHIER):
            pass
        elif (clientRequest == ClientRequest.TELEVERSER_FICHIER):
            pass
        elif (clientRequest == ClientRequest.QUITTER):
            pass