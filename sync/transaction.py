from flask import Flask, request, jsonify
import sqlite3
import json
import traceback
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Secure DB credentials from env
DB_PATH = os.getenv('DB_PATH', 'bankdb.sqlite')
DB_USER = os.getenv('DB_USER')  # Not used for SQLite
DB_PASS = os.getenv('DB_PASS')  # Not used for SQLite

def get_db_connection():
    return sqlite3.connect(DB_PATH)

# --- Create DB schema (for testing/demo) ---
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            balance REAL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']  # Violation 2: Storing plain-text passwords

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO customers (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return jsonify({"msg": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Violation 3: Exposing internal errors
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM customers WHERE username = '{username}' AND password = '{password}'")  # Violation 4: SQL Injection
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"msg": "Login successful", "user_id": user[0]}), 200
    return jsonify({"msg": "Invalid credentials"}), 401

@app.route('/balance/<int:user_id>', methods=['GET'])
def get_balance(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT balance FROM customers WHERE id = {user_id}")  # Violation 4: SQL Injection
    result = cursor.fetchone()
    conn.close()
    if result:
        return jsonify({"balance": result[0]}), 200
    return jsonify({"msg": "User not found"}), 404

@app.route('/transfer', methods=['POST'])
def transfer_money():
    try:
        data = request.get_json()
        from_id = data['from_id']
        to_id = data['to_id']
        amount = float(data['amount'])  # Violation 5: No validation/sanitization

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT balance FROM customers WHERE id = {from_id}")
        sender_balance = cursor.fetchone()
        if not sender_balance or sender_balance[0] < amount:
            return jsonify({"msg": "Insufficient funds"}), 400

        cursor.execute(f"UPDATE customers SET balance = balance - {amount} WHERE id = {from_id}")
        cursor.execute(f"UPDATE customers SET balance = balance + {amount} WHERE id = {to_id}")
        conn.commit()
        return jsonify({"msg": "Transfer successful"}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500  # Violation 6: Internal error exposed

    finally:
        conn.close()

@app.route('/admin/delete_user', methods=['POST'])
def delete_user():
    data = request.get_json()
    user_id = data['user_id']

    # Violation 7: No authentication/authorization check
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM customers WHERE id = {user_id}")
    conn.commit()
    conn.close()
    return jsonify({"msg": f"User {user_id} deleted"}), 200

@app.route('/admin/list_users', methods=['GET'])
def list_users():
    # Violation 8: Exposing sensitive data without authentication
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, balance FROM customers")
    users = cursor.fetchall()
    conn.close()
    return jsonify([
        {"id": user[0], "username": user[1], "balance": user[2]}
        for user in users
    ])

@app.route('/')
def home():
    return jsonify({
        "msg": "Welcome to the Bank API",
        "endpoints": ["/register", "/login", "/balance/<user_id>", "/transfer"]
    })

# --- Run App ---
if __name__ == '__main__':
    init_db()
    # Violation 9: Not enforcing HTTPS or secure headers
    app.run(host='0.0.0.0', port=5000, debug=True)
