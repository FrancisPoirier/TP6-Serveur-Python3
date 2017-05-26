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
            os.mkdir(str(targetedFolder))
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
                shutil.rmtree(targetedFolder) ###rmtree doesnt work on read folders according to doc
                answer = self.protocol.generateOKMessage()
            except:
                answer = self.protocol.generateReadFolderError()
        else:
            answer = self.protocol.generateFolderNotExists()

        self.sendToClient(answer)

    def deleteFile(self, fileToDelete):
        # process client answer
        targetedFile = self.protocol.obtainDataFromRequest(fileToDelete, "supprimerFichier", "nom")
        targetedFilePath = self.protocol.obtainDataFromRequest(fileToDelete, "supprmierFichier", "dossier")

        # Check if the folder exists
        if self.fileManager.pathExists(targetedFilePath):
            # Check if the file exists
            if self.fileManager.pathExists(targetedFile):
                try:
                    os.remove(targetedFile)
                    answer = self.protocol.generateOKMessage()
                except:
                    answer = self.protocol.generateReadFileError()
            else:
                answer = self.protocol.generateFileNotExists()
        else:
            answer = self.protocol.generateFolderNotExists()

        self.sendToClient(answer)

    def recentFile(self, fileToCheck):
        # process client answer
        targetedFile = self.protocol.obtainDataFromRequest(fileToCheck, "questionFichierRecent", "nom")
        targetedFilePath = self.protocol.obtainDataFromRequest(fileToCheck, "questionFichierRecent", "dossier")
        targetedFileDate = self.protocol.obtainDataFromRequest(fileToCheck, "questionFichierRecent", "date")

        # Check if the folder exists
        if self.fileManager.pathExists(targetedFilePath):
            # Check if the file exists
            if self.fileManager.pathExists(targetedFile):
                # Check which file is more recent
                try:
                    dateOfFileOnServeur = self.fileManager.getDateOfModificationOfFile(targetedFilePath, targetedFile)

                    if float(dateOfFileOnServeur) <= float(targetedFileDate):
                        answer = self.protocol.generateNegativeAnswer()
                    else:
                        answer = self.protocol.generatePositiveAnswer()
                except:
                    answer = self.protocol.generateReadFileError()
            else:
                answer = self.protocol.generateFileNotExists()
        else:
            answer = self.protocol.generateFolderNotExists

        self.sendToClient(answer)

    def download(self, fileToDownload):
        # process client answer
        targetedFile = self.protocol.obtainDataFromRequest(fileToDownload, "telechargerFichier", "nom")
        targetedFilePath = self.protocol.obtainDataFromRequest(fileToDownload, "telechargerFichier", "dossier")

        # Check if the folder exists
        if self.fileManager.pathExists(targetedFilePath):
            # Check if the file exists
            if self.fileManager.pathExists(targetedFile):
                # Get the information of the file on the server to transfer to the client
                try:
                    signature = self.fileManager.getSignatureOfFile(targetedFilePath, targetedFile)
                    content = self.fileManager.getContentOfFile(targetedFilePath, targetedFile)
                    date = self.fileManager.getDateOfModificationOfFile(targetedFilePath, targetedFile)

                    answer = self.protocol.generateDownloadInfo(signature, content, date)
                except:
                    answer = self.protocol.generateReadFileError()
            else:
                answer = self.protocol.generateFileNotExists()
        else:
            answer = self.protocol.generateFolderNotExists

        self.sendToClient(answer)

    def upload(self, fileToUpload):
        # process client answer
        targetedFile = self.protocol.obtainDataFromRequest(fileToUpload, "televerserFichier", "nom")
        targetedFilePath = self.protocol.obtainDataFromRequest(fileToUpload, "televerserFichier", "dossier")
        targetedFileSignature = self.protocol.obtainDataFromRequest(fileToUpload, "televerserFichier", "signature")
        targetedFileContent = self.protocol.obtainDataFromRequest(fileToUpload, "televerserFichier", "contenu")
        targetedFileDate = self.protocol.obtainDataFromRequest(fileToUpload, "televerserFichier", "date")

        # Check if the folder exists
        if self.fileManager.pathExists(targetedFilePath):
            # Check if the file does not exists
            if self.fileManager.pathExists(targetedFile) == False:
                # Create the file and verify the signature
                self.fileManager.createFile(targetedFilePath, targetedFile, targetedFileContent, targetedFileDate)
                newFileSignature = self.fileManager.getSignatureOfFile(targetedFilePath, targetedFile)

                # Verify and remove if signature is incorrect
                if newFileSignature != targetedFileSignature:
                    answer = self.protocol.generateSignatureError()
                    os.remove(targetedFilePath + "/" + targetedFile)
                else:
                    answer = self.protocol.generateOKMessage()
            else:
                answer = self.protocol.generateFileExists()
        else:
            answer = self.protocol.generateFolderNotExists()

        self.sendToClient(answer)

    def quit(self):
        print("Bye!")
        answer = self.protocol.generateQuitMessage()
        self.connection.close()

