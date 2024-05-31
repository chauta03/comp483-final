import random
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import AES

class CLA:
    def __init__(self):
        self.validation_number_set = set()

    def get_validation_numbers(self):
        return self.validation_number_set

    # def __del__(self):
    #     self.validation_number_set.remove(self.validation_number)

    # Given a public RSA key, encrypts CLA AES key with RSA public key and returns RSA encrypted AES key along with AES encrypted validation number
    def get_encrypted_val_num(self, voter_public_key):
        AES_key = os.urandom(32)
        AES_iv = os.urandom(16)
        validation_num = self.get_random_validation_number()
        AES_manager = AES.EncryptionManager(AES_key, AES_iv)
        AES_manager.update_encryptor(str(validation_num).encode('utf-8'))
        en_validation_num = AES_manager.finalize_encryptor()
        # en_validation_num = voter_public_key.encrypt(
        #     str(self.get_random_validation_number()).encode('utf-8'),
        #     padding.OAEP(
        #         mgf=padding.MGF1(algorithm=hashes.SHA256()),
        #         algorithm=hashes.SHA256(),
        #         label=None  # rarely used. Just leave it 'None'
        #     )
        # )

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
        # print("Before")
        # print(AES_key)
        # print(AES_iv)
        # print(validation_num)
        return en_validation_num, en_AES_key, en_AES_iv


    def get_random_validation_number(self):
        while True:
            number = random.randint(0, 2 ** 32 - 1)

            if len(self.validation_number_set) >= 2 ** 32:
                raise Exception("No more validation numbers available")

            if number not in self.validation_number_set:
                self.validation_number_set.add(number)
                return number

    # def encrypt_validation_num(self, voter_public_key):
    #     message = str(self.get_random_validation_number()).encode('utf-8')
    #     ciphertext1 = voter_public_key.encrypt(
    #         message,
    #         padding.OAEP(
    #             mgf=padding.MGF1(algorithm=hashes.SHA256()),
    #             algorithm=hashes.SHA256(),
    #             label=None  # rarely used. Just leave it 'None'
    #         )
    #     )
    #     return ciphertext1