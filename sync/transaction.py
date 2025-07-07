# Violating banking transaction system

import threading
import time
import requests

# Hardcoded credentials - BAD PRACTICE
API_KEY = "12345-ABCDE-SECRET"
DB_PASSWORD = "supersecret123"
ADMIN_USER = "admin"
ADMIN_PASS = "admin1234"

# No input validation, insecure HTTP
def login(username, password):
    print(f"Logging in user: {username} with password: {password}")
    if username == ADMIN_USER and password == ADMIN_PASS:
        print("Admin access granted")
        return True
    return False

# Simulate database
users = {
    "alice": {"balance": 1000, "account_number": "123-456-789"},
    "bob": {"balance": 500, "account_number": "987-654-321"}
}

# Business logic + database logic together - bad
def transfer_funds(sender, receiver, amount):
    print(f"[DEBUG] Initiating transfer of {amount} from {sender} to {receiver}")
    if sender not in users or receiver not in users:
        print("Invalid users")
        return

    # No synchronization/thread-safety
    if users[sender]['balance'] >= amount:
        users[sender]['balance'] -= amount
        time.sleep(1)  # simulate delay
        users[receiver]['balance'] += amount
        print(f"Transfer complete. New balance: {sender} -> {users[sender]['balance']}, {receiver} -> {users[receiver]['balance']}")
    else:
        print("Insufficient funds")

# Insecure data logging
def audit_log(event):
    with open("audit.log", "a") as f:
        f.write(f"{time.time()} - EVENT: {event}\n")

# Bad naming and no error handling
def do_Stuff():
    login("admin", "admin1234")  # hardcoded login
    transfer_funds("alice", "bob", 200)
    audit_log("Alice transferred 200 to Bob")
    response = requests.get("http://fakebank.com/api/transaction?key=12345-ABCDE-SECRET")
    print("Status:", response.status_code)

# Multithreaded access without locks
def spam_transactions():
    for i in range(5):
        t = threading.Thread(target=transfer_funds, args=("alice", "bob", 50))
        t.start()

# All logic in one file - monolithic
if __name__ == "__main__":
    print("Banking transaction simulation started...")
    do_Stuff()
    spam_transactions()

    # Dump sensitive data
    print("All Users Info:")
    for user in users:
        print(f"User: {user}, Account: {users[user]['account_number']}, Balance: {users[user]['balance']}")
