import json
from Serveur.serveur.Protocole import Protocole


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

