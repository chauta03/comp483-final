import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import AES


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

    # Get validation number
    # def set_validation_num(self, cipher_num):
    #     recovered_num = self.private_key.decrypt(
    #         cipher_num,
    #         padding.OAEP(
    #             mgf=padding.MGF1(algorithm=hashes.SHA256()),
    #             algorithm=hashes.SHA256(),
    #             label=None  # rarely used. Just leave it 'None'
    #         ))
    #
    #     self.validation_num = recovered_num.decode('utf-8')

    def set_validation_num(self, en_validation_num, en_AES_key, en_AES_iv):
        AES_key = self.private_key.decrypt(
            en_AES_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None  # rarely used. Just leave it 'None'
            ))
        AES_key = AES_key

        AES_iv = self.private_key.decrypt(
            en_AES_iv,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None  # rarely used. Just leave it 'None'
            ))
        AES_iv = AES_iv

        AES_manager = AES.EncryptionManager(AES_key, AES_iv)
        AES_manager.update_decryptor(en_validation_num)
        self.validation_num = int(AES_manager.finalize_decryptor().decode('utf-8'))

        # print("After")
        # print(AES_key)
        # print(AES_iv)
        # print(self.validation_num)



    # Takes vote and public key to make encrypted vote containing ID, validation num, and vote
    def create_vote(self, vote, CTF_public_key):
        message = f"{self.my_ID},{self.validation_num},{vote}".encode('utf-8')
        ciphertext1 = CTF_public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None  # rarely used. Just leave it 'None'
            )
        )
        return ciphertext1
