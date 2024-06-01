import random
import voter
import CLA
import CTF

# Main function that runs voting simulation
def main():

    # Creates and initializes central institutions
    CLA_object = CLA.CLA()
    CTF_object = CTF.CTF()

    # Runs random voting simulation
    candidates = ["John", "Noah", "Sophie", "Lexi"]
    cipher_votes = []
    for _ in range(40):

        # Create voter and have voter get verification number
        voter_object = voter.Voter()
        en_validation_num, en_AES_key, en_AES_iv = CLA_object.get_encrypted_val_num(voter_object.get_public_key())
        voter_object.set_validation_num(en_validation_num, en_AES_key, en_AES_iv)

        # Have voter create encrypted vote to later tally
        vote = random.choice(candidates)
        en_vote, en_AES_key, en_AES_iv = voter_object.get_encrypted_vote(vote, CTF_object.get_public_key())
        cipher_votes.append([en_vote, en_AES_key, en_AES_iv])


    # CLA sends CTF its list of used validation numbers
    en_validation_set, en_AES_key, en_AES_iv = CLA_object.get_validation_numbers(CTF_object.get_public_key())
    CTF_object.update_validation_set(en_validation_set, en_AES_key, en_AES_iv)


    # Tallies votes with CTF
    for en_vote, en_AES_key, en_AES_iv in cipher_votes:
        CTF_object.tally_vote(en_vote, en_AES_key, en_AES_iv)

    # Outputs election results
    CTF_object.get_election_results()

if __name__ == "__main__":
    main()