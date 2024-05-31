import random
import voter
import CLA
import CTF


def main():

    # Creates and initializes central institutions
    CLA_object = CLA.CLA()
    CTF_object = CTF.CTF()

    # # Initialize a voter with a validation number and ID
    # voter_object = voter.Voter(CLA_object.random_validation_number())

    # # Makes vote
    # cipher_vote = voter_object.create_vote("John", CTF_public_key)

    # Initializes a set of voters with a validation number and ID, and has them vote

    # Voter asks for shared key and sends public RSA key
    # CLA encrypts AES key with voter public key and sends back to voter along with AES encrypted number

    candidates = ["John", "Noah", "Sophie", "Lexi"]
    cipher_votes = []
    for _ in range(50):
        # voter_object = voter.Voter()
        # voter_object.set_validation_num(CLA_object.encrypt_validation_num(voter_object.get_public_key()))
        # cipher_votes.append(voter_object.create_vote(random.choice(candidates), CTF_public_key))

        # Create Voter and have voter get verification number
        voter_object = voter.Voter()
        en_validation_num, en_AES_key, en_AES_iv = CLA_object.get_encrypted_val_num(voter_object.get_public_key())
        voter_object.set_validation_num(en_validation_num, en_AES_key, en_AES_iv)

        # Have voter send vote to CTF to tally
        vote = random.choice(candidates)
        en_vote, en_AES_key, en_AES_iv = voter_object.get_encrypted_vote(vote, CTF_object.get_public_key())
        CTF_object.tally_vote(en_vote, en_AES_key, en_AES_iv)

    # CLA sends CTF its list of used validation numbers (digitally unsecure, would happen physically in real world)
    CTF_object.update_validation_set(CLA_object.get_validation_numbers())


    # Tallies votes with CTF
    # CTF_object.tally_vote(cipher_vote)
    # for cipher_vote in cipher_votes:
    #     CTF_object.tally_vote(cipher_vote)

    # Outputs election results
    CTF_object.get_election_results()

if __name__ == "__main__":
    main()