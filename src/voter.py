import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class Voter:

    # Initializes voter with validation number and ID
    def __init__(self, validation_num):
        self.validation_num = validation_num
        self.my_ID = random.randint(0, 2 ** 32 - 1)

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
