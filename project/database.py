import sqlite3

def get_connection():
    return sqlite3.connect("bank.db")

def find_user_by_credentials(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    conn.close()
    return user

def get_account_balance(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE user_id=?", (user_id,))
    balance = cur.fetchone()
    conn.close()
    return balance[0] if balance else None

def update_balances_and_log_transfer(from_user_id, to_user_id, amount):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE accounts SET balance = balance - ? WHERE user_id=?", (amount, from_user_id))
        cur.execute("UPDATE accounts SET balance = balance + ? WHERE user_id=?", (amount, to_user_id))
        cur.execute("INSERT INTO transfers (from_user, to_user, amount) VALUES (?, ?, ?)",
                    (from_user_id, to_user_id, amount))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return False
    finally:
        conn.close()
