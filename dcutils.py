import base64, os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encryption:
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


