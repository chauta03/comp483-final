from collections import defaultdict
from flask import Flask, request, jsonify
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import random
import sqlite3
import CLA, voter, CTF
import helper

app = Flask(__name__)

CTF_object = CTF.CTF()


# init db
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS voters (id INTEGER PRIMARY KEY, identification INTEGER, validation INTEGER, candidate TEXT)')
    print("Table voters created successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS cipher_votes (id INTEGER PRIMARY KEY, en_vote BLOB, en_AES_key BLOB, en_AES_iv BLOB)')

    conn.close()

init_sqlite_db()

@app.route('/add-vote', methods=['POST'])
def add_vote():

    my_ID = random.randint(0, 2 ** 32 - 1)
    validation_num = None
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # get validation number set
    validation_num_set = helper.query_db('SELECT validation FROM voters')

    en_validation_num, en_AES_key, en_AES_iv = CLA.get_encrypted_val_num(public_key, validation_num_set)
    validation_num = voter.set_validation_num(private_key, en_validation_num, en_AES_key, en_AES_iv)

    post_data = request.get_json()
    candidate = post_data['candidate']
    try:
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO voters (candidate) VALUES (?)', (validation_num))
            conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error occurred in INSERT INTO voters: " + str(e))
    finally:
        conn.close()
    
    # Have voter create encrypted vote to later tally
    en_vote, en_AES_key, en_AES_iv = voter.get_encrypted_vote(my_ID, validation_num, candidate, CTF_object.get_public_key())

    try:
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO cipher_votes (en_vote, en_AES_key, en_AES_iv) VALUES (?, ?, ?)', (en_vote, en_AES_key, en_AES_iv))
            conn.commit()

    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
        return jsonify(my_ID)

@app.route('/get-votes')
def get_votes():
    raw_data = defaultdict(list)
    
    try:
        with sqlite3.connect('database.db') as conn:
            validation_num_set = helper.query_db('SELECT validation FROM voters')
            en_validation_set, en_AES_key, en_AES_iv = CLA.get_validation_numbers(CTF_object.get_public_key(), validation_num_set)
            CTF_object.update_validation_set(en_validation_set, en_AES_key, en_AES_iv)

            rows = helper.query_db('SELECT * FROM cipher_votes')
            for row in rows:
                en_vote, en_AES_key, en_AES_iv = row[1], row[2], row[3]
                id, validation, candidate = CTF_object.decrypt_vote(en_vote, en_AES_key, en_AES_iv).split(',')
                raw_data[candidate].append(id)

    except Exception as e:
        print("Error occurred in SELECT * FROM cipher_votes: " + str(e))
    finally:
        return jsonify(raw_data)

if __name__ == '__main__':
    app.run(debug=True)