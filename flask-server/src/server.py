from flask import Flask, request, jsonify
import sqlite3
import random
import voter 
import CLA
import CTF
import json

app = Flask(__name__)

CLA_object = CLA.CLA()
CTF_object = CTF.CTF()

# Runs random voting simulation
candidates = ["John", "Noah", "Sophie", "Lexi"]
cipher_votes = []

# init db
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    c = conn.cursor()
    conn.execute('CREATE TABLE IF NOT EXISTS votes (id INTEGER PRIMARY KEY, candidate TEXT, votes INTEGER)')
    print("Table created successfully")
    conn.close()

init_sqlite_db()

@app.route('/add-vote', methods=['POST'])
def add_vote():
    msg = None
    try:
        post_data = request.get_json()
        candidate = post_data['candidate']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM votes WHERE candidate=?", (candidate,))
            row = cursor.fetchone()
            if row:
                cursor.execute("UPDATE votes SET votes = votes + 1 WHERE candidate=?", (candidate,))
            else:
                cursor.execute("INSERT INTO votes (candidate, votes) VALUES (?, 1)", (candidate,))
            conn.commit()
            msg = "Vote added successfully"
    except Exception as e:
        conn.rollback()
        msg = "Error occurred: " + str(e)
    finally:
        conn.close()
        return jsonify(msg=msg)

@app.route('/get-votes', methods=['GET'])
def get_votes():
    records = []

    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM votes")
            records = cursor.fetchall()
    except Exception as e:
        conn.rollback()
        print("Error occurred: " + str(e))
    finally:
        conn.close()
        return jsonify(records)
    

# Member API route
# @app.route('/vote')
# def startVote():
#     voter_object = voter.Voter()
#     en_validation_num, en_AES_key, en_AES_iv = CLA_object.get_encrypted_val_num(voter_object.get_public_key())
#     voter_object.set_validation_num(en_validation_num, en_AES_key, en_AES_iv)

#     # Have voter create encrypted vote to later tally
#     vote = random.choice(candidates)
#     en_vote, en_AES_key, en_AES_iv = voter_object.get_encrypted_vote(vote, CTF_object.get_public_key())
#     cipher_votes.append([en_vote, en_AES_key, en_AES_iv])

#     id = voter_object.get_id()
#     validation_num = voter_object.get_validation_num()
#     return {"info": [id, validation_num]}


if __name__ == '__main__':
    app.run(debug=True)
