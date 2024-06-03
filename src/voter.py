import os
import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import AES


# Class that controls all functions for a voter
class Voter:

    # Initializes voter with ID along with RSA encryption
    def __init__(self):
        self.my_ID = random.randint(0, 2 ** 32 - 1)
        self.validation_num = None
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()


    # Getter function for RSA public key
    def get_public_key(self):
        return self.public_key


    # Updates used validation number by decrypting validation number using RSA encrypted AES keys
    def set_validation_num(self, en_validation_num, en_AES_key, en_AES_iv):

        # Decrypts AES key and IV with RSA
        AES_key = self.private_key.decrypt(
            en_AES_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None  # rarely used. Just leave it 'None'
            ))
        AES_iv = self.private_key.decrypt(
            en_AES_iv,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None  # rarely used. Just leave it 'None'
            ))

        # Decrypts and updates validation number with AES
        AES_manager = AES.EncryptionManager(AES_key, AES_iv)
        temp_message = AES_manager.update_decryptor(en_validation_num)
        temp_message += AES_manager.finalize_decryptor()
        self.validation_num = int(temp_message.decode('utf-8'))


    # Given a public RSA key, encrypts CLA AES key with RSA public key and returns RSA encrypted AES key along with AES encrypted validation number
    def get_encrypted_vote(self, vote, CTF_public_key):

        # Creates random AES key and IV
        AES_key = os.urandom(32)
        AES_iv = os.urandom(16)

        # Creates and encrypts message to send with AES
        message = f"{self.my_ID},{self.validation_num},{vote}".encode('utf-8')
        AES_manager = AES.EncryptionManager(AES_key, AES_iv)
        en_vote = AES_manager.update_encryptor(message)
        en_vote += AES_manager.finalize_encryptor()

        # Encrypts AES key and IV with RSA
        en_AES_key = CTF_public_key.encrypt(
            AES_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None  # rarely used. Just leave it 'None'
            )
        )
        en_AES_iv = CTF_public_key.encrypt(
            AES_iv,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None  # rarely used. Just leave it 'None'
            )
        )

        # Returns encrypted vote and AES information
        return en_vote, en_AES_key, en_AES_iv
