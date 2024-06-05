import os
import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import AES

def set_validation_num(private_key, en_validation_num, en_AES_key, en_AES_iv):

        # Decrypts AES key and IV with RSA
        AES_key = private_key.decrypt(
            en_AES_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None  # rarely used. Just leave it 'None'
            ))
        AES_iv = private_key.decrypt(
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
        
        validation_num = int(temp_message.decode('utf-8'))
        return validation_num

# Given a public RSA key, encrypts CLA AES key with RSA public key and returns RSA encrypted AES key along with AES encrypted validation number
def get_encrypted_vote(my_ID, validation_num, vote, CTF_public_key):

    # Creates random AES key and IV
    AES_key = os.urandom(32)
    AES_iv = os.urandom(16)

    # Creates and encrypts message to send with AES
    message = f"{my_ID},{validation_num},{vote}".encode('utf-8')
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