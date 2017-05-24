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

    def interpreter(self, data, key =''):
        jsonData = json.loads(data)

        #try:
            #jsonData[key]
        #except:
            #key = "reponse"

        #if ("fichier" in jsonData[key]):
            #answer = self.obtainDataFromFolders(jsonData[key], "fichier", " ")
        #elif ("dossier" in jsonData[key]):
            #answer = self.obtainDataFromFolders(jsonData[key], "dossier", "/")
        #else:
        answer = jsonData[key]

        return answer


    def obtainDataFromFolders(self, key, sub_key, seperator=''):

        ## Si cette fonction retourne rien, cela veux dire que le fichier racine existe, il est vide, parcontre.
        data = ''
        for aKey in key:
            if aKey is not None:
                for aSubKey in key[sub_key]:
                    data += aSubKey + seperator
        return data