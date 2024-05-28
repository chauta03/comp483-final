import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class CLA:
    def __init__(self):
        self.validation_number_set = set()

    def get_validation_numbers(self):
        return self.validation_number_set

    # def __del__(self):
    #     self.validation_number_set.remove(self.validation_number)

    def get_random_validation_number(self):
        while True:
            number = random.randint(0, 2 ** 32 - 1)

            if len(self.validation_number_set) >= 2 ** 32:
                raise Exception("No more validation numbers available")

            if number not in self.validation_number_set:
                self.validation_number_set.add(number)
                return number

    def encrypt_validation_num(self, voter_public_key):
        message = str(self.get_random_validation_number()).encode('utf-8')
        ciphertext1 = voter_public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None  # rarely used. Just leave it 'None'
            )
        )
        return ciphertext1