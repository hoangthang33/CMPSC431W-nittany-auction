from flask import Flask, render_template, request, redirect
import sqlite3
import hashlib

app = Flask(__name__)

# ---------- HASH FUNCTION ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- HOME ----------
@app.route('/')
def index():
    return render_template('index.html')

# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])

        conn = sqlite3.connect('auction.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()

        if user:
            # check roles
            cursor.execute("SELECT * FROM Bidders WHERE email=?", (email,))
            if cursor.fetchone():
                return "Welcome Bidder"

            cursor.execute("SELECT * FROM Sellers WHERE email=?", (email,))
            if cursor.fetchone():
                return "Welcome Seller"

            cursor.execute("SELECT * FROM Helpdesk WHERE email=?", (email,))
            if cursor.fetchone():
                return "Welcome HelpDesk"

        return "Login Failed"

    return render_template('login.html')

# ---------- SIGNUP ----------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])
        name = request.form['name']
        phone = request.form['phone']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']

        conn = sqlite3.connect('auction.db')
        cursor = conn.cursor()

        try:
            # insert address first
            cursor.execute("""
                INSERT INTO Address (street, city, state, zipcode)
                VALUES (?, ?, ?, ?)
            """, (street, city, state, zipcode))

            address_id = cursor.lastrowid

            # insert user
            cursor.execute("""
                INSERT INTO Users VALUES (?, ?, ?, ?)
            """, (email, password, name, phone))

            # default role = bidder
            cursor.execute("""
                INSERT INTO Bidders VALUES (?, ?)
            """, (email, address_id))

            conn.commit()

        except:
            return "Error creating account"

        return redirect('/login')

    return render_template('signup.html')


if __name__ == "__main__":
    app.run(debug=True)

