import CLA
import CTF
import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class Voter:

    def setup_voter(self):
        self.CTF_public_key = CTF.get_public_key()
        self.validation_num = CLA.random_validation_number()

        self.my_ID = random.randint(0, 2 ** 32 - 1)

    def create_vote(self):
        vote = "John"
        message = f"{self.my_ID},{self.validation_num},{vote}"

        ciphertext1 = self.CTF_public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None  # rarely used. Just leave it 'None'
            )
        )

        return ciphertext1
