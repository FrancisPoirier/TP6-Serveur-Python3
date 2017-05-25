import sys
from Serveur.serveur.ClientRequest import ClientRequest
from Serveur.serveur.Serveur import Server

class RequestManager: #Chef d'orchestre qui indique au serveur quoi faire.

    def __init__(self, server):
        self.server = server

    def requestManaging(self, clientRequest, informationForTreatment):
        #Vérification du type de donnée de la variable en paramètre, elle devrait faire partie de l'enum ClientRequest

        if (isinstance(clientRequest, ClientRequest) == False):
            print("The type of client request is incorrect")
            sys.exit(1)

        if (clientRequest == ClientRequest.BONJOUR_SERVEUR):
            self.server.hello()
        elif (clientRequest == ClientRequest.NOM_SERVEUR):
            self.server.serverName()
        elif (clientRequest == ClientRequest.LISTE_DOSSIERS):
            self.server.folderList(informationForTreatment)
        elif (clientRequest == ClientRequest.LISTE_FICHIERS):
            self.server.fileList(informationForTreatment)
        elif (clientRequest == ClientRequest.CREER_DOSSIER):
            self.server.createFolder(informationForTreatment)
        elif (clientRequest == ClientRequest.FICHIER_IDENTIQUE):
            self.server.identicalFile(informationForTreatment)
        elif (clientRequest == ClientRequest.FICHIER_RECENT):
            self.server.recentFile(informationForTreatment)
        elif (clientRequest == ClientRequest.SUPPRIMER_DOSSIER):
            self.server.deleteFolder(informationForTreatment)
        elif (clientRequest == ClientRequest.SUPPRIMER_FICHIER):
            self.server.deleteFile(informationForTreatment)
        elif (clientRequest == ClientRequest.TELECHARGER_FICHIER):
            self.server.download(informationForTreatment)
        elif (clientRequest == ClientRequest.TELEVERSER_FICHIER):
            self.server.upload(informationForTreatment)
        elif (clientRequest == ClientRequest.QUITTER):
            self.server.quit()