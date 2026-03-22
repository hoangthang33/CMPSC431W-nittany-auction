import pandas as pd
import sqlite3
import hashlib

# ---------- HASH FUNCTION ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- CONNECT DB ----------
conn = sqlite3.connect("auction.db")
cursor = conn.cursor()

# =========================
# 1. LOAD USERS
# =========================
users_df = pd.read_csv("Users.csv")

for _, row in users_df.iterrows():
    email = row['email']
    password = hash_password(row['password'])

    try:
        cursor.execute("""
            INSERT INTO Users (email, password, name, phone)
            VALUES (?, ?, ?, ?)
        """, (email, password, "", ""))
    except:
        pass  # skip duplicates

print("Users loaded")

# =========================
# 2. LOAD BIDDERS
# =========================
bidders_df = pd.read_csv("Bidders.csv")

for _, row in bidders_df.iterrows():
    try:
        cursor.execute("""
            INSERT INTO Bidders (email, first_name, last_name, age, address_id, major)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row['email'],
            row['first_name'],
            row['last_name'],
            row['age'],
            row['home_address_id'],
            row['major']
        ))
    except:
        pass

print("Bidders loaded")

# =========================
# 3. LOAD SELLERS
# =========================
sellers_df = pd.read_csv("Sellers.csv")

for _, row in sellers_df.iterrows():
    try:
        cursor.execute("""
            INSERT INTO Sellers (email, bank_routing_number, bank_account_number, balance)
            VALUES (?, ?, ?, ?)
        """, (
            row['email'],
            row['bank_routing_number'],
            row['bank_account_number'],
            row['balance']
        ))
    except:
        pass

print("Sellers loaded")

# =========================
# 4. LOAD HELPDESK
# =========================
helpdesk_df = pd.read_csv("Helpdesk.csv")

for _, row in helpdesk_df.iterrows():
    try:
        cursor.execute("""
            INSERT INTO Helpdesk (email, position)
            VALUES (?, ?)
        """, (
            row['email'],
            row['position']
        ))
    except:
        pass

print("Helpdesk loaded")

# =========================
# SAVE + CLOSE
# =========================
conn.commit()
conn.close()

print("All data loaded successfully!")