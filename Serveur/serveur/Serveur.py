import threading
import os
import shutil
from Serveur.serveur.RequestManager import RequestManager

class Server(threading.Thread):

    def __init__(self, threadName, connection, protocol, fileManager):
        threading.Thread.__init__(self, name = threadName)
        self.connection = connection
        self.protocol = protocol
        self.fileManager = fileManager
        self.requestManager = RequestManager(self)

    def run(self):
        while True:
            clientRequest = self.connection.receive()
            interpretedClientRequest = self.protocol.interpreter(clientRequest)

            ## L'interpreteur des protocoles renvoi un objet ClientRequest qui indique au RequestManager quoi faire.
            self.requestManaging(interpretedClientRequest, clientRequest)

    def sendToClient(self, answer):
        self.connection.send(answer)

    def requestManaging(self, clientRequest, informationForTreatment):
        self.requestManager.requestManaging(clientRequest, informationForTreatment)

    def hello(self):
        answer = self.protocol.generate("bonjourClient")
        self.sendToClient(answer)

    def serverName(self):
        answer = self.protocol.generate("nomServeur", "TP6 Dropbox")
        self.sendToClient(answer)

    def folderList(self, folderToList):
        #process client answer
        targetedFolder = self.protocol.obtainValue(folderToList, "questionListeDossiers")

        if self.fileManager.pathExists(targetedFolder):
            folderList = self.fileManager.getFolderList(targetedFolder)
            answer = self.protocol.generateFolderList(folderList)
        else:
            answer = self.protocol.generateFolderNotExists()

        self.sendToClient(answer)

    def fileList(self, folderToList):
        # process client answer
        targetedFolder = self.protocol.obtainValue(folderToList, "questionListeFichiers")

        if self.fileManager.pathExists(targetedFolder):
            fileList = self.fileManager.getFileList(targetedFolder)
            answer = self.protocol.generateFolderList(fileList)
        else:
            answer = self.protocol.generateFolderNotExists()

        self.sendToClient(answer)

    def createFolder(self, folderToCreate):
        #process client answer
        targetedFolder = self.protocol.obtainValue(folderToCreate, "creerDossier")

        #Get the path of the parent folders
        path = self.fileManager.getFilePath(targetedFolder)

        #Check if the folder already exists
        if self.fileManager.pathExists(targetedFolder):
            answer = self.protocol.generateFolderExists()

        #Check if the root of the folderToCreate is existing. It's the valid case
        elif self.fileManager.pathExists(path):
            os.mkdir("./" + str(targetedFolder))
            answer = self.protocol.generateOKMessage()

        else:
            answer = self.protocol.generateFolderNotExists()

        self.sendToClient(answer)

    def deleteFolder(self, folderToDelete):
        #process client answer
        targetedFolder = self.protocol.obtainValue(folderToDelete, "supprimerDossier")

        # Check if the folder exists
        if self.fileManager.pathExists(targetedFolder):
            try:
                shutil.rmtree(targetedFolder) ###rmtree doesnt work on readed folders according to doc
                answer = self.protocol.generateOKMessage()
            except:
                answer = self.protocol.generateReadedFolderError()
        else:
            answer = self.protocol.generateFolderNotExists()

        self.sendToClient(answer)

    def deleteFile(self, fileToDelete):
        # process client answer
        targetedFile = self.protocol.obtainValue(fileToDelete, "supprimerFichier")

        path = self.fileManager.getFilePath(targetedFile)

        # Check if the folder exists
        if self.fileManager.pathExists(path):
            # Check if the file exists
            if self.fileManager.pathExists(targetedFile):
                try:
                    os.remove(targetedFile)
                    answer = self.protocol.generateOKMessage()
                except:
                    answer = self.protocol.generateReadedFileError()
            else:
                answer = self.protocol.generateFileNotExists()
        else:
            answer = self.protocol.generateFolderNotExists()

        self.sendToClient(answer)
        
    def identicalFile(self):
        pass

    def recentFile(self):
        pass

    def download(self):
        pass

    def upload(self):
        pass

    def quit(self):
        pass