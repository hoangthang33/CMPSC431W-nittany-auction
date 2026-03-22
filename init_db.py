import sqlite3

conn = sqlite3.connect('auction.db')
cursor = conn.cursor()

# ---------------- USERS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    email TEXT PRIMARY KEY,
    password TEXT,
)
""")

# ---------------- ADDRESS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Address (
    address_id INTEGER PRIMARY KEY AUTOINCREMENT,
    street TEXT,
    city TEXT,
    state TEXT,
    zipcode TEXT
)
""")

# ---------------- BIDDERS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Bidders (
    email TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    age INTEGER,
    address_id INTEGER,
    major TEXT,
    FOREIGN KEY(email) REFERENCES Users(email),
    FOREIGN KEY(address_id) REFERENCES Address(address_id)
)
""")

# ---------------- SELLERS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Sellers (
    email TEXT PRIMARY KEY,
    bank_routing_number TEXT,
    bank_account_number TEXT,
    balance REAL,
    FOREIGN KEY(email) REFERENCES Users(email)
)
""")

# ---------------- HELPDESK ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Helpdesk (
    email TEXT PRIMARY KEY,
    position TEXT,
    FOREIGN KEY(email) REFERENCES Users(email)
)
""")

# ---------------- CREDIT CARDS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Credit_Cards (
    credit_card_num TEXT PRIMARY KEY,
    card_type TEXT,
    expire_month INTEGER,
    expire_year INTEGER,
    security_code TEXT,
    owner_email TEXT,
    FOREIGN KEY(owner_email) REFERENCES Users(email)
)
""")

# ---------------- ZIPCODE INFO ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Zipcode_Info (
    zipcode TEXT PRIMARY KEY,
    city TEXT,
    state TEXT
)
""")

# ---------------- CATEGORIES ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Categories (
    parent_category TEXT,
    category_name TEXT PRIMARY KEY
)
""")

# ---------------- AUCTION LISTINGS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Auction_Listings (
    seller_email TEXT,
    listing_id INTEGER,
    category TEXT,
    auction_title TEXT,
    product_name TEXT,
    product_description TEXT,
    quantity INTEGER,
    reserve_price REAL,
    max_bids INTEGER,
    status INTEGER,
    PRIMARY KEY (seller_email, listing_id),
    FOREIGN KEY(seller_email) REFERENCES Sellers(email)
)
""")

# ---------------- BIDS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Bids (
    bid_id INTEGER PRIMARY KEY,
    seller_email TEXT,
    listing_id INTEGER,
    bidder_email TEXT,
    bid_price REAL,
    FOREIGN KEY(bidder_email) REFERENCES Bidders(email)
)
""")

# ---------------- TRANSACTIONS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Transactions (
    transaction_id INTEGER PRIMARY KEY,
    seller_email TEXT,
    listing_id INTEGER,
    buyer_email TEXT,
    date TEXT,
    payment REAL
)
""")

# ---------------- RATING ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Rating (
    bidder_email TEXT,
    seller_email TEXT,
    date TEXT,
    rating INTEGER,
    rating_desc TEXT
)
""")

# ---------------- REQUESTS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Requests (
    request_id INTEGER PRIMARY KEY,
    sender_email TEXT,
    helpdesk_staff_email TEXT,
    request_type TEXT,
    request_desc TEXT,
    request_status INTEGER
)
""")

conn.commit()
conn.close()