from flask import Flask, request, redirect, url_for, session, flash, render_template_string
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "union_bank_secret_key"

DB_NAME = "union_bank.db"

# ---------------- DATABASE ----------------
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        aadhar TEXT NOT NULL,
        account_number TEXT UNIQUE NOT NULL,
        balance REAL DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

create_tables()

# ---------------- ACCOUNT NUMBER ----------------
def generate_account_number():
    conn = get_db_connection()
    while True:
        acc_no = str(random.randint(1000000000, 9999999999))
        account = conn.execute("SELECT * FROM accounts WHERE account_number=?", (acc_no,)).fetchone()
        if not account:
            conn.close()
            return acc_no

# ---------------- COMMON HTML TEMPLATE ----------------
BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #eef4ff;
        }

        .navbar {
            background: #0b3d91;
            color: white;
            padding: 18px;
            text-align: center;
            font-size: 26px;
            font-weight: bold;
        }

        .container {
            width: 420px;
            margin: 40px auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
        }

        .wide-container {
            width: 750px;
            margin: 40px auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
            text-align: center;
        }

        h2 {
            text-align: center;
            color: #0b3d91;
            margin-bottom: 20px;
        }

        label {
            font-weight: bold;
            display: block;
            margin-top: 12px;
            margin-bottom: 6px;
        }

        input {
            width: 100%;
            padding: 10px;
            border: 1px solid #bbb;
            border-radius: 6px;
            font-size: 14px;
            box-sizing: border-box;
        }

        button, .btn {
            width: 100%;
            padding: 12px;
            margin-top: 18px;
            border: none;
            border-radius: 8px;
            background: #2563eb;
            color: white;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            box-sizing: border-box;
        }

        button:hover, .btn:hover {
            opacity: 0.9;
        }

        .btn-green { background: #16a34a; }
        .btn-red { background: #dc2626; }
        .btn-orange { background: #f59e0b; }
        .btn-purple { background: #7c3aed; }
        .btn-gray { background: gray; }

        .flash {
            width: 420px;
            margin: 20px auto;
            padding: 12px;
            border-radius: 8px;
            font-weight: bold;
            text-align: center;
        }

        .flash.success {
            background: #dcfce7;
            color: #166534;
        }

        .flash.error {
            background: #fee2e2;
            color: #991b1b;
        }

        .result-success {
            margin-top: 20px;
            padding: 12px;
            background: #dcfce7;
            color: #166534;
            border-radius: 8px;
            font-weight: bold;
            line-height: 1.7;
        }

        .result-error {
            margin-top: 20px;
            padding: 12px;
            background: #fee2e2;
            color: #991b1b;
            border-radius: 8px;
            font-weight: bold;
            line-height: 1.7;
        }

        .details-box {
            margin-top: 20px;
            padding: 20px;
            background: #f8fafc;
            border-radius: 10px;
            border: 1px solid #ddd;
            line-height: 1.8;
            text-align: left;
        }

        .menu-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-top: 20px;
        }

        .menu-grid a {
            padding: 18px;
            text-align: center;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            text-decoration: none;
            display: block;
        }

        .welcome-text {
            font-size: 22px;
            color: #0b3d91;
            font-weight: bold;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="navbar">UNION BANK ACCOUNT MANAGEMENT SYSTEM</div>

    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="flash {{ category }}">{{ message }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    {{ content|safe }}
</body>
</html>
"""

def render_page(title, content):
    return render_template_string(BASE_HTML, title=title, content=content)

# ---------------- HOME / INDEX ----------------
@app.route("/")
def index():
    content = """
    <div class="container">
        <h2>Welcome to Union Bank</h2>
        <a href="/register" class="btn btn-green">Register</a>
        <a href="/login" class="btn">Login</a>
    </div>
    """
    return render_page("Union Bank", content)

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        if not username or not email or not password:
            flash("All fields are required", "error")
            return redirect(url_for("register"))

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )
            conn.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists", "error")
        finally:
            conn.close()

    content = """
    <div class="container">
        <h2>User Registration</h2>
        <form method="POST">
            <label>Username</label>
            <input type="text" name="username">

            <label>Email</label>
            <input type="email" name="email">

            <label>Password</label>
            <input type="password" name="password">

            <button type="submit" class="btn-green">Register</button>
            <a href="/" class="btn btn-gray">Back</a>
        </form>
    </div>
    """
    return render_page("Register", content)

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["username"] = username
            flash("Login successful", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "error")

    content = """
    <div class="container">
        <h2>User Login</h2>
        <form method="POST">
            <label>Username</label>
            <input type="text" name="username">

            <label>Password</label>
            <input type="password" name="password">

            <button type="submit">Login</button>
            <a href="/" class="btn btn-gray">Back</a>
        </form>
    </div>
    """
    return render_page("Login", content)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for("index"))

# ---------------- HOME PAGE ----------------
@app.route("/home")
def home():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    content = f"""
    <div class="wide-container">
        <div class="welcome-text">Welcome, {username}</div>
        <h2>Union Bank Dashboard</h2>

        <div class="menu-grid">
            <a href="/create_account" class="btn-green">Create Account</a>
            <a href="/deposit" style="background:#2563eb;">Deposit</a>
            <a href="/withdrawal" class="btn-red">Withdrawal</a>
            <a href="/balance" class="btn-orange">Current Balance</a>
            <a href="/details" class="btn-purple" style="grid-column: span 2;">Account Holder Details</a>
        </div>

        <a href="/logout" class="btn btn-gray" style="margin-top:25px;">Logout</a>
    </div>
    """
    return render_page("Home", content)

# ---------------- CREATE ACCOUNT ----------------
@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if "username" not in session:
        return redirect(url_for("login"))

    username_value = session["username"]
    result_html = ""

    if request.method == "POST":
        username = request.form["username"].strip()
        phone = request.form["phone"].strip()
        aadhar = request.form["aadhar"].strip()

        if not username or not phone or not aadhar:
            result_html = '<div class="result-error">All fields are required</div>'
        else:
            conn = get_db_connection()

            existing = conn.execute(
                "SELECT * FROM accounts WHERE username=?",
                (username,)
            ).fetchone()

            if existing:
                result_html = '<div class="result-error">This user already has an account</div>'
            else:
                acc_no = generate_account_number()
                conn.execute("""
                    INSERT INTO accounts (username, phone, aadhar, account_number, balance)
                    VALUES (?, ?, ?, ?, ?)
                """, (username, phone, aadhar, acc_no, 0))
                conn.commit()
                result_html = f'<div class="result-success">Account created successfully!<br>Generated Account Number: {acc_no}</div>'

            conn.close()

    content = f"""
    <div class="container">
        <h2>Create New Bank Account</h2>
        <form method="POST">
            <label>User Name</label>
            <input type="text" name="username" value="{username_value}">

            <label>Phone Number</label>
            <input type="text" name="phone">

            <label>Aadhar Number</label>
            <input type="text" name="aadhar">

            <button type="submit" class="btn-green">Create Account</button>
            <a href="/home" class="btn btn-gray">Back</a>
        </form>
        {result_html}
    </div>
    """
    return render_page("Create Account", content)

# ---------------- DEPOSIT ----------------
@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    if "username" not in session:
        return redirect(url_for("login"))

    result_html = ""

    if request.method == "POST":
        acc_no = request.form["account_number"].strip()
        amount = request.form["amount"].strip()

        if not acc_no or not amount:
            result_html = '<div class="result-error">All fields are required</div>'
        else:
            try:
                amount = float(amount)
                if amount <= 0:
                    result_html = '<div class="result-error">Amount must be greater than 0</div>'
                else:
                    conn = get_db_connection()
                    account = conn.execute(
                        "SELECT * FROM accounts WHERE account_number=?",
                        (acc_no,)
                    ).fetchone()

                    if not account:
                        result_html = '<div class="result-error">Account not found</div>'
                    else:
                        new_balance = account["balance"] + amount
                        conn.execute(
                            "UPDATE accounts SET balance=? WHERE account_number=?",
                            (new_balance, acc_no)
                        )
                        conn.commit()
                        result_html = f'<div class="result-success">₹{amount} deposited successfully.<br>New Balance: ₹{new_balance}</div>'
                    conn.close()
            except ValueError:
                result_html = '<div class="result-error">Enter valid amount</div>'

    content = f"""
    <div class="container">
        <h2>Deposit Money</h2>
        <form method="POST">
            <label>Account Number</label>
            <input type="text" name="account_number">

            <label>Deposit Amount</label>
            <input type="text" name="amount">

            <button type="submit">Deposit</button>
            <a href="/home" class="btn btn-gray">Back</a>
        </form>
        {result_html}
    </div>
    """
    return render_page("Deposit", content)

# ---------------- WITHDRAWAL ----------------
@app.route("/withdrawal", methods=["GET", "POST"])
def withdrawal():
    if "username" not in session:
        return redirect(url_for("login"))

    result_html = ""

    if request.method == "POST":
        acc_no = request.form["account_number"].strip()
        amount = request.form["amount"].strip()

        if not acc_no or not amount:
            result_html = '<div class="result-error">All fields are required</div>'
        else:
            try:
                amount = float(amount)
                if amount <= 0:
                    result_html = '<div class="result-error">Amount must be greater than 0</div>'
                else:
                    conn = get_db_connection()
                    account = conn.execute(
                        "SELECT * FROM accounts WHERE account_number=?",
                        (acc_no,)
                    ).fetchone()

                    if not account:
                        result_html = '<div class="result-error">Account not found</div>'
                    elif amount > account["balance"]:
                        result_html = '<div class="result-error">Insufficient balance</div>'
                    else:
                        new_balance = account["balance"] - amount
                        conn.execute(
                            "UPDATE accounts SET balance=? WHERE account_number=?",
                            (new_balance, acc_no)
                        )
                        conn.commit()
                        result_html = f'<div class="result-success">₹{amount} withdrawn successfully.<br>Remaining Balance: ₹{new_balance}</div>'
                    conn.close()
            except ValueError:
                result_html = '<div class="result-error">Enter valid amount</div>'

    content = f"""
    <div class="container">
        <h2>Withdraw Money</h2>
        <form method="POST">
            <label>Account Number</label>
            <input type="text" name="account_number">

            <label>Withdrawal Amount</label>
            <input type="text" name="amount">

            <button type="submit" class="btn-red">Withdraw</button>
            <a href="/home" class="btn btn-gray">Back</a>
        </form>
        {result_html}
    </div>
    """
    return render_page("Withdrawal", content)

# ---------------- CURRENT BALANCE ----------------
@app.route("/balance", methods=["GET", "POST"])
def balance():
    if "username" not in session:
        return redirect(url_for("login"))

    result_html = ""

    if request.method == "POST":
        acc_no = request.form["account_number"].strip()

        if not acc_no:
            result_html = '<div class="result-error">Please enter account number</div>'
        else:
            conn = get_db_connection()
            account = conn.execute(
                "SELECT username, balance FROM accounts WHERE account_number=?",
                (acc_no,)
            ).fetchone()
            conn.close()

            if account:
                result_html = f'''
                <div class="result-success">
                    Account Holder: {account["username"]}<br>
                    Current Balance: ₹{account["balance"]}
                </div>
                '''
            else:
                result_html = '<div class="result-error">Account not found</div>'

    content = f"""
    <div class="container">
        <h2>Current Balance</h2>
        <form method="POST">
            <label>Account Number</label>
            <input type="text" name="account_number">

            <button type="submit" class="btn-orange">Check Balance</button>
            <a href="/home" class="btn btn-gray">Back</a>
        </form>
        {result_html}
    </div>
    """
    return render_page("Current Balance", content)

# ---------------- ACCOUNT HOLDER DETAILS ----------------
@app.route("/details", methods=["GET", "POST"])
def details():
    if "username" not in session:
        return redirect(url_for("login"))

    result_html = ""

    if request.method == "POST":
        acc_no = request.form["account_number"].strip()

        if not acc_no:
            result_html = '<div class="result-error">Please enter account number</div>'
        else:
            conn = get_db_connection()
            account = conn.execute("""
                SELECT username, phone, aadhar, account_number, balance
                FROM accounts
                WHERE account_number=?
            """, (acc_no,)).fetchone()
            conn.close()

            if account:
                result_html = f"""
                <div class="details-box">
                    <strong>Account Holder Name:</strong> {account["username"]}<br>
                    <strong>Phone Number:</strong> {account["phone"]}<br>
                    <strong>Aadhar Number:</strong> {account["aadhar"]}<br>
                    <strong>Account Number:</strong> {account["account_number"]}<br>
                    <strong>Current Balance:</strong> ₹{account["balance"]}
                </div>
                """
            else:
                result_html = '<div class="result-error">Account not found</div>'

    content = f"""
    <div class="container">
        <h2>Account Holder Details</h2>
        <form method="POST">
            <label>Account Number</label>
            <input type="text" name="account_number">

            <button type="submit" class="btn-purple">Show Details</button>
            <a href="/home" class="btn btn-gray">Back</a>
        </form>
        {result_html}
    </div>
    """
    return render_page("Account Holder Details", content)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)