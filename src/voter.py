import CLA
import CTF
import random


class Voter:

    def setup_voter(self):
        self.CTF_public_key = CTF.get_public_key()
        self.validation_num = CLA.random_validation_number()

        self.my_ID = random.randint(0, 2 ** 32 - 1)

    def create_vote(self):
