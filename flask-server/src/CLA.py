import random
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import AES

# Given a public RSA key, encrypts CLA AES key with RSA public key and returns RSA encrypted AES key along with AES encrypted validation number set
def get_validation_numbers(CTF_public_key, validation_number_set):

    # Creates random AES key and IV
    AES_key = os.urandom(32)
    AES_iv = os.urandom(16)

    # Creates and encrypts message to send with AES
    message = repr(validation_number_set).encode('utf-8')
    AES_manager = AES.EncryptionManager(AES_key, AES_iv)
    en_validation_set = AES_manager.update_encryptor(message)
    en_validation_set += AES_manager.finalize_encryptor()

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

    # Returns encrypted set and AES information
    return en_validation_set, en_AES_key, en_AES_iv

def get_encrypted_val_num(voter_public_key, validation_number_set):

    # Creates random AES key and IV
    AES_key = os.urandom(32)
    AES_iv = os.urandom(16)

    # Creates and encrypts message to send with AES
    validation_num = get_random_validation_number(validation_number_set)
    AES_manager = AES.EncryptionManager(AES_key, AES_iv)
    en_validation_num = AES_manager.update_encryptor(str(validation_num).encode('utf-8'))
    en_validation_num += AES_manager.finalize_encryptor()

    # Encrypts AES key and IV with RSA
    en_AES_key = voter_public_key.encrypt(
        AES_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None  # rarely used. Just leave it 'None'
        )
    )
    en_AES_iv = voter_public_key.encrypt(
        AES_iv,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None  # rarely used. Just leave it 'None'
        )
    )

    # Returns encrypted set and AES information
    return en_validation_num, en_AES_key, en_AES_iv

# Generates a random validation number
def get_random_validation_number(validation_number_set):
    while True:
        number = random.randint(0, 2 ** 32 - 1)

        if len(validation_number_set) >= 2 ** 32:
            raise Exception("No more validation numbers available")

        if number not in validation_number_set:
            return number