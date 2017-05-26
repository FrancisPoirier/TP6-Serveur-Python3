import json
import sys
from Serveur.serveur.Protocole import Protocole
from Serveur.serveur.ClientRequest import ClientRequest


class Protocole_json(Protocole):  ## sous classe pour protocole json
    """Interface du langage de communication JSON"""

    def __init__(self, fileManager):
        super(Protocole_json, self).__init__()
        self.fileManager = fileManager


    def generateStringFormat(self, balise, text=''):
        jsonString = {balise: text}
        return jsonString

    def generate(self, balise, text=''):
        jsonString = self.generateStringFormat(balise, text)
        jsonData = json.dumps(jsonString)
        return jsonData

    def interpreter(self, data, key =''):
        jsonData = json.loads(data)

        for k in jsonData.keys():
            if key == k:

                if (key == "questionListeDossiers"):
                    answer = ClientRequest.LISTE_DOSSIERS

                elif (key == "questionListeFichiers"):
                    answer = ClientRequest.LISTE_FICHIERS

                elif (key == "creerDossier"):
                    answer = ClientRequest.CREER_DOSSIER

                elif (key == "televerserFichier"):
                    answer = ClientRequest.TELEVERSER_FICHIER

                elif (key == "telechargerFichier"):
                    answer = ClientRequest.TELECHARGER_FICHIER

                elif (key == "supprimerFichier"):
                    answer = ClientRequest.SUPPRIMER_FICHIER

                elif (key == "supprimerDossier"):
                    answer = ClientRequest.SUPPRIMER_DOSSIER

                elif (key == "questionFichierRecent"):
                    answer = ClientRequest.FICHIER_RECENT

                elif (key == "questionFicherIdentique"):
                    answer = ClientRequest.FICHIER_IDENTIQUE

                else:
                    answer = ClientRequest.QUITTER
                break
        else:
            print("La clé est invalide")
            sys.exit(1)

        return answer

    def generateFolderList(self, folderList):
        childKeyValue = []
        for folder in folderList:
            childKeyValue.append(folder)

        childKey = {'dossier' : childKeyValue}
        parentKey = {'listeDossiers' : childKey}
        return json.dumps(parentKey)

    def generateFileList(self, fileList):
        childKeyValue = []
        for file in fileList:
            childKeyValue.append(file)

        childKey = {'fichier': childKeyValue}
        parentKey = {'listeFichiers': childKey}
        return json.dumps(parentKey)

    def generateDownloadInfo(self, signature, content, date):
        keyValue = {"signature": signature, "content": content, "date": date}
        mainKey = {"fichier": keyValue}
        return json.dumps(mainKey)

    def generateFolderNotExists(self):
        answer = self.generate("reponse", "erreurDossierInexistant")
        return answer

    def generateFolderExists(self):
        answer = self.generate("reponse", "erreurDossierExiste")
        return answer

    def generateFileNotExists(self):
        answer = self.generate("reponse", "erreurFichierInexistant")
        return answer

    def generateFileExists(self):
        answer = self.generate("reponse", "erreurFichierExiste")
        return answer

    def generateOKMessage(self):
        answer = self.generate("reponse", "ok")
        return answer

    def generatePositiveAnswer(self):
        answer = self.generate("reponse", "oui")
        return answer

    def generateNegativeAnswer(self):
        answer = self.generate("reponse", "non")
        return answer

    def generateReadFolderError(self):
        answer = self.generate("reponse", "erreurDossierLecture")
        return answer

    def generateReadFileError(self):
        answer = self.generate("reponse", "erreurFichierLecture")
        return answer

    def generateSignatureError(self):
        answer = self.generate("reponse", "erreurSignature")
        return answer

    def generateQuitMessage(self):
        answer = self.generate("reponse", "bye")
        return answer

    def obtainValue(self, jsonData, key):
        data = jsonData.loads()
        return data[key]

    def obtainDataFromRequest(self, key, sub_key, seperator=''):

        ## Si cette fonction retourne rien, cela veux dire que le fichier racine existe, il est vide, parcontre.
        data = ''
        for aKey in key:
            if aKey is not None:
                for aSubKey in key[sub_key]:
                    data += aSubKey + seperator
        return data