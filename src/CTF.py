from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class CTF:

    # Initializes CTF by creating RSA keys and makes candidate dictionary
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

        self.candidate_dict = {}

    # Getter function for RSA public key
    def get_public_key(self):
        return self.public_key

    # Updates used validation numbers set
    def update_validation_set(self, validation_number_set):
        self.used_validation_set = validation_number_set

    # Decrypts vote
    def decrypt_vote(self, cipher_vote):
        recovered_vote = self.private_key.decrypt(
            cipher_vote,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None  # rarely used. Just leave it 'None'
            ))

        return recovered_vote

    # Tallies an individual vote record
    def tally_vote(self, cipher_vote):

        # Gets decrypted vote information
        id, validation, candidate = self.decrypt_vote(cipher_vote).decode('utf-8').split(',')

        # Checks that vote is not from double voter
        if validation in self.used_validation_set:
            print("Vote already cast by given validation number")
            return

        # Records vote
        if candidate not in self.candidate_dict.keys():
            self.candidate_dict[candidate] = [id]
        else:
            self.candidate_dict[candidate].append(id)

    # Outputs election outcomes
    def get_election_results(self):
        print("***Election Results***")
        for candidate in self.candidate_dict.keys():
            print(f"{candidate}: {len(self.candidate_dict[candidate])}")
        print(f"\nRaw results{self.candidate_dict}")