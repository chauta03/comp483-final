from flask import Flask
import random
import voter 
import CLA
import CTF

app = Flask(__name__)

CLA_object = CLA.CLA()
CTF_object = CTF.CTF()

# Runs random voting simulation
candidates = ["John", "Noah", "Sophie", "Lexi"]
cipher_votes = []


# Member API route
@app.route('/vote')
def startVote():
    voter_object = voter.Voter()
    en_validation_num, en_AES_key, en_AES_iv = CLA_object.get_encrypted_val_num(voter_object.get_public_key())
    voter_object.set_validation_num(en_validation_num, en_AES_key, en_AES_iv)

    # Have voter create encrypted vote to later tally
    vote = random.choice(candidates)
    en_vote, en_AES_key, en_AES_iv = voter_object.get_encrypted_vote(vote, CTF_object.get_public_key())
    cipher_votes.append([en_vote, en_AES_key, en_AES_iv])

    id = voter_object.get_id()
    validation_num = voter_object.get_validation_num()
    return {"info": [id, validation_num]}


if __name__ == '__main__':
    app.run(debug=True)
