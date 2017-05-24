import xml.dom.minidom
from Serveur.serveur.Protocole import Protocole


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
        pass