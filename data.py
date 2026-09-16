import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

# ---------------- DATABASE CONNECTION ----------------
conn = sqlite3.connect("union_bank.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Create accounts table
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


# ---------------- MAIN APPLICATION ----------------
class UnionBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Union Bank Account Management System")
        self.root.geometry("750x550")
        self.root.configure(bg="#dbeafe")

        self.current_user = None
        self.show_welcome_page()

    # Clear current window
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------------- WELCOME PAGE ----------------
    def show_welcome_page(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="UNION BANK ACCOUNT MANAGEMENT SYSTEM",
            font=("Arial", 18, "bold"),
            bg="#dbeafe",
            fg="darkblue"
        ).pack(pady=40)

        tk.Button(
            self.root,
            text="Register",
            font=("Arial", 14, "bold"),
            width=20,
            bg="#16a34a",
            fg="white",
            command=self.show_register_page
        ).pack(pady=15)

        tk.Button(
            self.root,
            text="Login",
            font=("Arial", 14, "bold"),
            width=20,
            bg="#2563eb",
            fg="white",
            command=self.show_login_page
        ).pack(pady=15)

    # ---------------- REGISTER PAGE ----------------
    def show_register_page(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="User Registration",
            font=("Arial", 18, "bold"),
            bg="#dbeafe",
            fg="darkblue"
        ).pack(pady=20)

        tk.Label(self.root, text="Username", font=("Arial", 12), bg="#dbeafe").pack()
        self.reg_username = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.reg_username.pack(pady=5)

        tk.Label(self.root, text="Email", font=("Arial", 12), bg="#dbeafe").pack()
        self.reg_email = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.reg_email.pack(pady=5)

        tk.Label(self.root, text="Password", font=("Arial", 12), bg="#dbeafe").pack()
        self.reg_password = tk.Entry(self.root, font=("Arial", 12), width=30, show="*")
        self.reg_password.pack(pady=5)

        tk.Button(
            self.root,
            text="Register",
            font=("Arial", 12, "bold"),
            bg="#16a34a",
            fg="white",
            width=15,
            command=self.register_user
        ).pack(pady=15)

        tk.Button(
            self.root,
            text="Back",
            font=("Arial", 12, "bold"),
            bg="gray",
            fg="white",
            width=15,
            command=self.show_welcome_page
        ).pack()

    def register_user(self):
        username = self.reg_username.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_password.get().strip()

        if username == "" or email == "" or password == "":
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )
            conn.commit()
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_login_page()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already registered")

    # ---------------- LOGIN PAGE ----------------
    def show_login_page(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="User Login",
            font=("Arial", 18, "bold"),
            bg="#dbeafe",
            fg="darkblue"
        ).pack(pady=20)

        tk.Label(self.root, text="Username", font=("Arial", 12), bg="#dbeafe").pack()
        self.login_username = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.login_username.pack(pady=5)

        tk.Label(self.root, text="Password", font=("Arial", 12), bg="#dbeafe").pack()
        self.login_password = tk.Entry(self.root, font=("Arial", 12), width=30, show="*")
        self.login_password.pack(pady=5)

        tk.Button(
            self.root,
            text="Login",
            font=("Arial", 12, "bold"),
            bg="#2563eb",
            fg="white",
            width=15,
            command=self.login_user
        ).pack(pady=15)

        tk.Button(
            self.root,
            text="Back",
            font=("Arial", 12, "bold"),
            bg="gray",
            fg="white",
            width=15,
            command=self.show_welcome_page
        ).pack()

    def login_user(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cursor.fetchone()

        if user:
            self.current_user = username
            messagebox.showinfo("Success", f"Welcome {username}")
            self.show_home_page()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    # ---------------- HOME PAGE ----------------
    def show_home_page(self):
        self.clear_window()

        tk.Label(
            self.root,
            text=f"Welcome, {self.current_user}",
            font=("Arial", 18, "bold"),
            bg="#dbeafe",
            fg="darkblue"
        ).pack(pady=20)

        button_frame = tk.Frame(self.root, bg="#dbeafe")
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Create Account",
            font=("Arial", 12, "bold"),
            bg="#10b981",
            fg="white",
            width=20,
            height=2,
            command=self.show_create_account_page
        ).grid(row=0, column=0, padx=10, pady=10)

        tk.Button(
            button_frame,
            text="Deposit",
            font=("Arial", 12, "bold"),
            bg="#2563eb",
            fg="white",
            width=20,
            height=2,
            command=self.show_deposit_page
        ).grid(row=0, column=1, padx=10, pady=10)

        tk.Button(
            button_frame,
            text="Withdrawal",
            font=("Arial", 12, "bold"),
            bg="#ef4444",
            fg="white",
            width=20,
            height=2,
            command=self.show_withdraw_page
        ).grid(row=1, column=0, padx=10, pady=10)

        tk.Button(
            button_frame,
            text="Current Balance",
            font=("Arial", 12, "bold"),
            bg="#f59e0b",
            fg="white",
            width=20,
            height=2,
            command=self.show_balance_page
        ).grid(row=1, column=1, padx=10, pady=10)

        tk.Button(
            button_frame,
            text="Account Holder Details",
            font=("Arial", 12, "bold"),
            bg="#8b5cf6",
            fg="white",
            width=25,
            height=2,
            command=self.show_account_details_page
        ).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        tk.Button(
            self.root,
            text="Logout",
            font=("Arial", 12, "bold"),
            bg="gray",
            fg="white",
            width=15,
            command=self.logout
        ).pack(pady=20)

    def logout(self):
        self.current_user = None
        self.show_welcome_page()

    # ---------------- ACCOUNT NUMBER GENERATION ----------------
    def generate_account_number(self):
        while True:
            acc_no = str(random.randint(1000000000, 9999999999))
            cursor.execute("SELECT * FROM accounts WHERE account_number=?", (acc_no,))
            if cursor.fetchone() is None:
                return acc_no

    # ---------------- CREATE ACCOUNT PAGE ----------------
    def show_create_account_page(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="Create New Bank Account",
            font=("Arial", 18, "bold"),
            bg="#dbeafe",
            fg="darkblue"
        ).pack(pady=20)

        tk.Label(self.root, text="User Name", font=("Arial", 12), bg="#dbeafe").pack()
        self.acc_username = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.acc_username.insert(0, self.current_user)
        self.acc_username.pack(pady=5)

        tk.Label(self.root, text="Phone Number", font=("Arial", 12), bg="#dbeafe").pack()
        self.acc_phone = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.acc_phone.pack(pady=5)

        tk.Label(self.root, text="Aadhar Number", font=("Arial", 12), bg="#dbeafe").pack()
        self.acc_aadhar = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.acc_aadhar.pack(pady=5)

        tk.Button(
            self.root,
            text="Create Account",
            font=("Arial", 12, "bold"),
            bg="#10b981",
            fg="white",
            width=18,
            command=self.create_account
        ).pack(pady=15)

        tk.Button(
            self.root,
            text="Back",
            font=("Arial", 12, "bold"),
            bg="gray",
            fg="white",
            width=18,
            command=self.show_home_page
        ).pack()

    def create_account(self):
        username = self.acc_username.get().strip()
        phone = self.acc_phone.get().strip()
        aadhar = self.acc_aadhar.get().strip()

        if username == "" or phone == "" or aadhar == "":
            messagebox.showerror("Error", "All fields are required")
            return

        # Check whether this logged-in user already has an account
        cursor.execute("SELECT * FROM accounts WHERE username=?", (self.current_user,))
        existing = cursor.fetchone()

        if existing:
            messagebox.showwarning("Warning", "This user already has an account")
            return

        account_number = self.generate_account_number()

        cursor.execute("""
            INSERT INTO accounts (username, phone, aadhar, account_number, balance)
            VALUES (?, ?, ?, ?, ?)
        """, (self.current_user, phone, aadhar, account_number, 0))

        conn.commit()
        messagebox.showinfo("Success", f"Account created successfully\nAccount Number: {account_number}")
        self.show_home_page()

    # ---------------- DEPOSIT PAGE ----------------
    def show_deposit_page(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="Deposit Money",
            font=("Arial", 18, "bold"),
            bg="#dbeafe",
            fg="darkblue"
        ).pack(pady=20)

        tk.Label(self.root, text="Enter Account Number", font=("Arial", 12), bg="#dbeafe").pack()
        self.dep_acc = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.dep_acc.pack(pady=5)

        tk.Label(self.root, text="Enter Deposit Amount", font=("Arial", 12), bg="#dbeafe").pack()
        self.dep_amt = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.dep_amt.pack(pady=5)

        tk.Button(
            self.root,
            text="Deposit",
            font=("Arial", 12, "bold"),
            bg="#2563eb",
            fg="white",
            width=18,
            command=self.deposit_money
        ).pack(pady=15)

        tk.Button(
            self.root,
            text="Back",
            font=("Arial", 12, "bold"),
            bg="gray",
            fg="white",
            width=18,
            command=self.show_home_page
        ).pack()

    def deposit_money(self):
        acc_no = self.dep_acc.get().strip()
        amount = self.dep_amt.get().strip()

        if acc_no == "" or amount == "":
            messagebox.showerror("Error", "Please enter all fields")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Enter valid amount")
            return

        cursor.execute("SELECT balance FROM accounts WHERE account_number=?", (acc_no,))
        account = cursor.fetchone()

        if account is None:
            messagebox.showerror("Error", "Account not found")
            return

        new_balance = account[0] + amount
        cursor.execute("UPDATE accounts SET balance=? WHERE account_number=?", (new_balance, acc_no))
        conn.commit()

        messagebox.showinfo("Success", f"Amount deposited successfully\nNew Balance: ₹{new_balance}")

    # ---------------- WITHDRAW PAGE ----------------
    def show_withdraw_page(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="Withdraw Money",
            font=("Arial", 18, "bold"),
            bg="#dbeafe",
            fg="darkblue"
        ).pack(pady=20)

        tk.Label(self.root, text="Enter Account Number", font=("Arial", 12), bg="#dbeafe").pack()
        self.with_acc = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.with_acc.pack(pady=5)

        tk.Label(self.root, text="Enter Withdrawal Amount", font=("Arial", 12), bg="#dbeafe").pack()
        self.with_amt = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.with_amt.pack(pady=5)

        tk.Button(
            self.root,
            text="Withdraw",
            font=("Arial", 12, "bold"),
            bg="#ef4444",
            fg="white",
            width=18,
            command=self.withdraw_money
        ).pack(pady=15)

        tk.Button(
            self.root,
            text="Back",
            font=("Arial", 12, "bold"),
            bg="gray",
            fg="white",
            width=18,
            command=self.show_home_page
        ).pack()

    def withdraw_money(self):
        acc_no = self.with_acc.get().strip()
        amount = self.with_amt.get().strip()

        if acc_no == "" or amount == "":
            messagebox.showerror("Error", "Please enter all fields")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Enter valid amount")
            return

        cursor.execute("SELECT balance FROM accounts WHERE account_number=?", (acc_no,))
        account = cursor.fetchone()

        if account is None:
            messagebox.showerror("Error", "Account not found")
            return

        current_balance = account[0]
        if amount > current_balance:
            messagebox.showerror("Error", "Insufficient balance")
            return

        new_balance = current_balance - amount
        cursor.execute("UPDATE accounts SET balance=? WHERE account_number=?", (new_balance, acc_no))
        conn.commit()

        messagebox.showinfo("Success", f"Amount withdrawn successfully\nRemaining Balance: ₹{new_balance}")

    # ---------------- BALANCE PAGE ----------------
    def show_balance_page(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="Current Balance",
            font=("Arial", 18, "bold"),
            bg="#dbeafe",
            fg="darkblue"
        ).pack(pady=20)

        tk.Label(self.root, text="Enter Account Number", font=("Arial", 12), bg="#dbeafe").pack()
        self.bal_acc = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.bal_acc.pack(pady=5)

        tk.Button(
            self.root,
            text="Check Balance",
            font=("Arial", 12, "bold"),
            bg="#f59e0b",
            fg="white",
            width=18,
            command=self.check_balance
        ).pack(pady=15)

        tk.Button(
            self.root,
            text="Back",
            font=("Arial", 12, "bold"),
            bg="gray",
            fg="white",
            width=18,
            command=self.show_home_page
        ).pack()

    def check_balance(self):
        acc_no = self.bal_acc.get().strip()

        if acc_no == "":
            messagebox.showerror("Error", "Please enter account number")
            return

        cursor.execute("SELECT balance FROM accounts WHERE account_number=?", (acc_no,))
        account = cursor.fetchone()

        if account:
            messagebox.showinfo("Current Balance", f"Available Balance: ₹{account[0]}")
        else:
            messagebox.showerror("Error", "Account not found")

    # ---------------- ACCOUNT HOLDER DETAILS PAGE ----------------
    def show_account_details_page(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="Account Holder Details",
            font=("Arial", 18, "bold"),
            bg="#dbeafe",
            fg="darkblue"
        ).pack(pady=20)

        tk.Label(self.root, text="Enter Account Number", font=("Arial", 12), bg="#dbeafe").pack()
        self.det_acc = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.det_acc.pack(pady=5)

        tk.Button(
            self.root,
            text="Show Details",
            font=("Arial", 12, "bold"),
            bg="#8b5cf6",
            fg="white",
            width=18,
            command=self.show_details
        ).pack(pady=15)

        tk.Button(
            self.root,
            text="Back",
            font=("Arial", 12, "bold"),
            bg="gray",
            fg="white",
            width=18,
            command=self.show_home_page
        ).pack()

    def show_details(self):
        acc_no = self.det_acc.get().strip()

        if acc_no == "":
            messagebox.showerror("Error", "Please enter account number")
            return

        cursor.execute("""
            SELECT username, phone, aadhar, account_number, balance
            FROM accounts
            WHERE account_number=?
        """, (acc_no,))
        account = cursor.fetchone()

        if account:
            details = (
                f"Account Holder Name: {account[0]}\n"
                f"Phone Number: {account[1]}\n"
                f"Aadhar Number: {account[2]}\n"
                f"Account Number: {account[3]}\n"
                f"Current Balance: ₹{account[4]}"
            )
            messagebox.showinfo("Account Holder Details", details)
        else:
            messagebox.showerror("Error", "Account not found")


# ---------------- RUN APPLICATION ----------------
root = tk.Tk()
app = UnionBankApp(root)
root.mainloop()