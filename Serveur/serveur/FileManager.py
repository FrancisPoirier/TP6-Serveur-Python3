import base64
import binascii
import os
import sys
import hashlib

class FileManager:

    def getFilePath(self, file):
        split = file.rsplit("/", 1)
        filepath = split[0]
        return filepath

    def getFileName(self, file):
        ## Retourne seulement le nom du fichier d'un chemin donné complet.
        ## Retourne text.txt si l'entrée est : "C:/D3/D1/text.txt"

        split = file.rsplit("/", 1)
        fileName = split[1]
        return fileName

    def createFile(self, filePath, fileName, content, lastTimeModified):
        completeFileName = filePath + "/" + fileName

        encodedcontent = content.encode()
        processedContent = base64.decodebytes(encodedcontent)
        newContent = processedContent.decode()

        file = open(completeFileName, 'w')
        file.write(newContent)
        file.close()

        date = os.stat(completeFileName).st_atime
        date_m = float(lastTimeModified)
        os.utime(completeFileName, (date, date_m))

    def getDateOfModificationOfFile(self, filePath, fileName):
        completeFileName = filePath + "/" + fileName

        try:
            # Voici comment lire le contenu d'un fichier

            fileStat = os.stat(completeFileName)

        except:
            print("Impossible de lire le fichier " + completeFileName)
            sys.exit(1)

        # Génération de la date de modification du fichier
        lastTimeModifiedDate = str(fileStat.st_mtime)
        return lastTimeModifiedDate

    def getSignatureOfFile(self, filePath, fileName):
        completeFileName = filePath + "/" + fileName

        try:
            # Voici comment lire le contenu d'un fichier
            file = open(completeFileName)
            fileContent = file.read()
            file.close()

        except:
            print("Impossible de lire le fichier " + completeFileName)
            sys.exit(1)

        # Encoder le fichier binaire en format UTF-8.
        utf8Content = fileContent.encode(encoding='UTF-8')

        # Génération de la signature du fichier
        md5Signature = hashlib.md5()
        md5Signature.update(utf8Content)

        signature = md5Signature.hexdigest()
        return signature

    def getContentOfFile(self, filePath, fileName):
        completeFileName = filePath + "/" + fileName

        try:
            # Voici comment lire le contenu d'un fichier
            file = open(completeFileName)
            fileContent = file.read()
            file.close()

        except:
            print("Impossible de lire le fichier " + completeFileName)
            sys.exit(1)

        # Encoder le fichier binaire en format UTF-8.
        utf8Content = fileContent.encode(encoding='UTF-8')

        # Voici comment encoder le contenu du fichier
        encodedContent = binascii.b2a_base64(utf8Content)

        # Aller chercher les codes ASCII de l'encodage
        asciiContent = encodedContent.decode(encoding='ascii')

        # Aller chercher les codes ASCII de l'encodage
        asciiContent = encodedContent.decode(encoding='ascii')
        return asciiContent