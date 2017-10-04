import base64, os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encryptor:
    def __init__(self, password=b"password", salt=b"testingasaltingg"):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
            )
        key = base64.urlsafe_b64encode(kdf.derive(password)) 
        self.fernet = Fernet(key)

    def encryptData(self, data):
        token = self.fernet.encrypt(data)
        return token

    def decryptData(self, data):
        token = self.fernet.decrypt(data)
        return token

class Encoder:
    """
     * Hides data inside of a list of pixels
     * @param   carrierData     list of pixels in RGB or RGBA format
     * @param   hiddenData      bits to hide inside the pixels
     * @return                  updated list of pixels with hidden data inside
    """
    def encode(self, carrierData, hiddenData):
        # Super hacky..
        # Image data comes in a tuple (which is immutable). To modify, I keep
        # track of the three values in the tuple and make a new tuple to
        # override the previous one LOL. This section also causes the most lag.
        i = 0
        for idx1, pixelList in enumerate(carrierData):
            tempPixelList = []
            for idx2, value in enumerate(pixelList):
                value = value & 0xFE
                if (i < len(hiddenData)):
                    value = value | hiddenData[i]
                i = i + 1
                tempPixelList.append(value)
            if (len(tempPixelList) == 4):
                pixelList = (tempPixelList[0], tempPixelList[1], tempPixelList[2], tempPixelList[3])
            else:
                pixelList = (tempPixelList[0], tempPixelList[1], tempPixelList[2])
            carrierData[idx1] = pixelList

        return carrierData

    """
     * Retrieves hidden data from a list of pixels
     * @param   carrierData     list of pixels in RGB or RGBA format
     * @return                  list of raw bits from carrier
    """
    def decode(self, carrierData):
        secretBits = []
        i = 0
        for pixelList in carrierData:
            for value in pixelList:
                secretBits.append(value & 0x1)
                i = i + 1

        return secretBits
