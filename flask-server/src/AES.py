from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
# Code from practical-cryptography-in-python (git)


# Class to manage AES functions
class EncryptionManager:
    def __init__(self, key, iv):
        aesContext = Cipher(algorithms.AES(key),
                            modes.CBC(iv),
                            backend=default_backend())
        self.encryptor = aesContext.encryptor()
        self.decryptor = aesContext.decryptor()
        self.padder = padding.PKCS7(1792).padder()       # padder size limits max size of any message encrypted (set to 1792 to maximum message length given block size)
        self.unpadder = padding.PKCS7(1792).unpadder()   # padder size limits max size of any message encrypted (set to 1792 to maximum message length given block size)

    def update_encryptor(self, plaintext):
        return self.encryptor.update(self.padder.update(plaintext))

    def finalize_encryptor(self):
        return self.encryptor.update(self.padder.finalize()) + self.encryptor.finalize()

    def update_decryptor(self, ciphertext):
        return self.unpadder.update(self.decryptor.update(ciphertext))

    def finalize_decryptor(self):
        return self.unpadder.update(self.decryptor.finalize()) + self.unpadder.finalize()
