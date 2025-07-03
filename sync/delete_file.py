from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os
import hashlib

app = Flask(__name__)
DATABASE = 'banking.db'
SECRET_KEY = "super-secret-bank-key-123"
ENCRYPTION_KEY = "1234567890abcdef"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/init', methods=['GET'])
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        password TEXT,
                        pan TEXT,
                        balance REAL
                    )''')
    conn.commit()
    return "DB Initialized"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    pan = data.get("pan")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users (username, password, pan, balance) VALUES ('{username}', '{password}', '{pan}', 0)")
    conn.commit()

    print(f"[REGISTER] User created: {username} with PAN {pan}")
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    user = cursor.fetchone()

    if user:
        token = hashlib.md5((username + SECRET_KEY).encode()).hexdigest()
        print(f"[LOGIN] User {username} logged in with token {token}")
        return jsonify({'message': 'Login successful', 'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/balance', methods=['GET'])
def get_balance():
    username = request.args.get("username")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT balance FROM users WHERE username = '{username}'")
    row = cursor.fetchone()
    if row:
        return jsonify({'balance': row['balance']})
    return jsonify({'message': 'User not found'}), 404

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.get_json()
    username = data.get("username")
    amount = data.get("amount")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET balance = balance + {amount} WHERE username = '{username}'")
    conn.commit()
    print(f"[DEPOSIT] {amount} deposited to {username}")
    return jsonify({'message': f'{amount} deposited successfully'})

@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()
    username = data.get("username")
    amount = data.get("amount")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT balance FROM users WHERE username = '{username}'")
    row = cursor.fetchone()

    if row and row['balance'] >= amount:
        cursor.execute(f"UPDATE users SET balance = balance - {amount} WHERE username = '{username}'")
        conn.commit()
        print(f"[WITHDRAW] {amount} withdrawn by {username}")
        return jsonify({'message': f'{amount} withdrawn successfully'})
    return jsonify({'message': 'Insufficient funds'}), 400

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.get_json()
    sender = data.get("from")
    receiver = data.get("to")
    amount = data.get("amount")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(f"SELECT balance FROM users WHERE username = '{sender}'")
    row = cursor.fetchone()

    if row and row['balance'] >= amount:
        cursor.execute(f"UPDATE users SET balance = balance - {amount} WHERE username = '{sender}'")
        cursor.execute(f"UPDATE users SET balance = balance + {amount} WHERE username = '{receiver}'")
        conn.commit()
        print(f"[TRANSFER] {amount} transferred from {sender} to {receiver}")
        return jsonify({'message': 'Transfer successful'})
    return jsonify({'message': 'Transfer failed'}), 400

@app.route('/show', methods=['GET'])
def show_profile():
    username = request.args.get("username")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    row = cursor.fetchone()

    if row:
        html = f"""
        <h2>Account Details for {row['username']}</h2>
        <p>PAN: {row['pan']}</p>
        <p>Balance: ₹{row['balance']}</p>
        """
        return render_template_string(html)
    return "User not found", 404

@app.route('/admin/logs', methods=['GET'])
def view_logs():
    log_path = 'server.log'
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            return f"<pre>{f.read()}</pre>"
    return "No logs found"

@app.route('/store_card', methods=['POST'])
def store_card():
    data = request.get_json()
    username = data.get("username")
    pan = data.get("pan")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET pan = '{pan}' WHERE username = '{username}'")
    conn.commit()

    print(f"[PAN] Stored PAN {pan} for user {username}")
    return jsonify({'message': 'PAN stored'})

@app.route('/encrypt', methods=['POST'])
def fake_encrypt():
    data = request.get_json()
    text = data.get("data")
    result = ''.join(chr((ord(c) + 3) % 256) for c in text)
    return jsonify({'encrypted': result})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
