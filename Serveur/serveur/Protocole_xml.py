import xml.dom.minidom
import sys
from Serveur.serveur.Protocole import Protocole
from Serveur.serveur.ClientRequest import ClientRequest


class Protocole_xml(Protocole):  ## sous classe pour protocole xml
    """Interface du langage de communication XML"""

    def __init__(self, fileManager):
        super(Protocole_xml).__init__()
        self.fileManager = fileManager


    def generateStringFormat(self, balise, text=''):
        messageToSend = xml.dom.minidom.Document()

        newElement = messageToSend.createElement(balise)
        messageToSend.appendChild(newElement)

        if text:
            text_xml = messageToSend.createTextNode(text)
            newElement.appendChild(text_xml)

        return messageToSend

    def generate(self, balise, text=''):
        answer  = self.generateStringFormat(balise, text)
        return answer.toxml()

    def interpreter(self, data):
        xmlData = xml.dom.minidom.parseString(data)

        ##Tous les cas possibles qui peuvent être envoyés par le client connecté.

        if (xmlData.getElementsByTagName("questionListeDossiers")):
            answer = ClientRequest.LISTE_DOSSIERS

        elif (xmlData.getElementsByTagName("questionListeFichiers")):
            answer = ClientRequest.LISTE_FICHIERS

        elif (xmlData.getElementsByTagName("creerDossier")):
            answer = ClientRequest.CREER_DOSSIER

        elif (xmlData.getElementsByTagName("televerserFichier")):
            answer = ClientRequest.TELEVERSER_FICHIER

        elif (xmlData.getElementsByTagName("telechargerFichier")):
            answer = ClientRequest.TELECHARGER_FICHIER

        elif (xmlData.getElementsByTagName("supprimerFichier")):
            answer = ClientRequest.SUPPRIMER_FICHIER

        elif (xmlData.getElementsByTagName("supprimerDossier")):
            answer = ClientRequest.SUPPRIMER_DOSSIER

        elif (xmlData.getElementsByTagName("questionFichierRecent")):
            answer = ClientRequest.FICHIER_RECENT

        elif (xmlData.getElementsByTagName("questionFicherIdentique")):
            answer = ClientRequest.FICHIER_IDENTIQUE

        else:
            answer = ClientRequest.QUITTER

        return answer

    def generateFolderList(self, folderList):
        xmlParentNode = self.generateStringFormat("listeDossiers")

        for folder in folderList:
            xmlChild = self.generateStringFormat("dossier", str(folder))
            xmlParentNode.childNodes[0].appendChild(xmlChild.childNodes[0])

        return xmlParentNode.toxml()

    def generateFileList(self, fileList):
        xmlParentNode = self.generateStringFormat("listeFichiers")

        for file in fileList:
            xmlChild = self.generateStringFormat("dossier", str(file))
            xmlParentNode.childNodes[0].appendChild(xmlChild.childNodes[0])

        return xmlParentNode.toxml()

    def generateDownloadInfo(self, signature, content, date):
        xmlParentNode = self.generateStringFormat("fichier")
        xmlSignature = self.generateStringFormat("signature", signature)
        xmlContent = self.generateStringFormat("contenu", content)
        xmlDate = self.generateStringFormat("date", date)

        xmlParentNode.childNodes[0].appendChild(xmlSignature.childNodes[0])
        xmlParentNode.childNodes[0].appendChild(xmlContent.childNodes[0])
        xmlParentNode.childNodes[0].appendChild(xmlDate.childNodes[0])

        return xmlParentNode.toxml()

    def generateFolderNotExists(self):
        answer = self.generate("erreurDossierInexistant")
        return answer

    def generateFolderExists(self):
        answer = self.generate("erreurDossierExiste")
        return answer

    def generateFileNotExists(self):
        answer = self.generate("erreurFichierInexistant")
        return answer

    def generateFileExists(self):
        answer = self.generate("erreurFichierExiste")
        return answer

    def generateOKMessage(self):
        answer = self.generate("ok")
        return answer

    def generatePositiveAnswer(self):
        answer = self.generate("oui")
        return answer

    def generateNegativeAnswer(self):
        answer = self.generate("non")
        return answer

    def generateReadFolderError(self):
        answer = self.generate("erreurDossierLecture")
        return answer

    def generateReadFileError(self):
        answer = self.generate("erreurFichierLecture")
        return answer

    def generateSignatureError(self):
        answer = self.generate("erreurSignature")
        return answer

    def generateQuitMessage(self):
        answer = self.generate("bye")
        return answer

    def obtainValue(self, xmlData, tag):
            for node in xmlData.getElementsByTagName(tag):
                answer = node.firstChild.data
                return answer

    def obtainDataFromRequest(self, xmlData, balise, sub_balise, seperator=''):

        ## Si cette fonction retourne rien, cela veux dire que le fichier racine existe, il est vide, parcontre.
        data = ''
        for node in xmlData.getElementsByTagName(balise):
            if node is not None:
                for node2 in node.getElementsByTagName(sub_balise):
                    data += node2.firstChild.data + seperator
        return data