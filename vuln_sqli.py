# vuln_sqli.py
# Vulnerability: SQL Injection (OWASP A03 Injection)

import sqlite3

def init_db(conn):
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cur.execute("DELETE FROM users")
    cur.execute("INSERT INTO users (username, password) VALUES ('alice', 'alice123')")
    cur.execute("INSERT INTO users (username, password) VALUES ('bob', 'bob123')")
    conn.commit()

def login(conn, username, password):
    cur = conn.cursor()

    # ❌ Vulnerable: string concatenation into SQL query
    query = "SELECT id, username FROM users WHERE username = '" + username + "' AND password = '" + password + "';"
    print("[DEBUG] Running query:", query)

    cur.execute(query)
    return cur.fetchone()

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    init_db(conn)

    u = input("username: ")
    p = input("password: ")
    result = login(conn, u, p)

    if result:
        print("✅ Logged in as:", result[1])
    else:
        print("❌ Invalid credentials")
