
import tkinter as tk
from tkinter import messagebox
import sqlite3
import random
import os

# =========================
# DATABASE SETUP
# =========================
DB_NAME = "union_bank.db"

conn = sqlite3.connect(DB_NAME)
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


# =========================
# MAIN APPLICATION
# =========================
class UnionBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Union Bank Account Management System")
        self.root.geometry("1000x650")
        self.root.config(bg="#eef4ff")
        self.root.resizable(False, False)

        self.current_user = None
        self.show_welcome_page()

    # -------------------------
    # COMMON STYLES
    # -------------------------
    def page_title(self, text):
        tk.Label(
            self.root,
            text=text,
            font=("Arial", 24, "bold"),
            bg="#eef4ff",
            fg="#0b3d91"
        ).pack(pady=20)

    def create_entry(self, parent, width=30, show=None):
        return tk.Entry(parent, font=("Arial", 12), width=width, bd=2, relief="groove", show=show)

    def create_button(self, parent, text, bg, command, width=18):
        return tk.Button(
            parent,
            text=text,
            font=("Arial", 12, "bold"),
            bg=bg,
            fg="white",
            width=width,
            height=2,
            relief="flat",
            command=command,
            cursor="hand2"
        )

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_header(self):
        header = tk.Frame(self.root, bg="#0b3d91", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="UNION BANK ACCOUNT MANAGEMENT SYSTEM",
            font=("Arial", 22, "bold"),
            bg="#0b3d91",
            fg="white"
        ).pack(pady=15)

    # =========================
    # WELCOME PAGE
    # =========================
    def show_welcome_page(self):
        self.clear_window()
        self.create_header()

        main = tk.Frame(self.root, bg="#eef4ff")
        main.pack(expand=True)

        self.page_title("Welcome to Union Bank")

        box = tk.Frame(main, bg="white", bd=2, relief="ridge", padx=40, pady=40)
        box.pack(pady=20)

        tk.Label(box, text="Choose an option", font=("Arial", 16, "bold"), bg="white", fg="#333").pack(pady=15)

        self.create_button(box, "Register", "#16a34a", self.show_register_page, 20).pack(pady=10)
        self.create_button(box, "Login", "#2563eb", self.show_login_page, 20).pack(pady=10)

    # =========================
    # REGISTER PAGE
    # =========================
    def show_register_page(self):
        self.clear_window()
        self.create_header()
        self.page_title("User Registration")

        form = tk.Frame(self.root, bg="white", bd=2, relief="ridge", padx=40, pady=30)
        form.pack(pady=20)

        tk.Label(form, text="Username", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, sticky="w", pady=10)
        self.reg_username = self.create_entry(form)
        self.reg_username.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(form, text="Email", font=("Arial", 12, "bold"), bg="white").grid(row=1, column=0, sticky="w", pady=10)
        self.reg_email = self.create_entry(form)
        self.reg_email.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(form, text="Password", font=("Arial", 12, "bold"), bg="white").grid(row=2, column=0, sticky="w", pady=10)
        self.reg_password = self.create_entry(form, show="*")
        self.reg_password.grid(row=2, column=1, pady=10, padx=10)

        btn_frame = tk.Frame(form, bg="white")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        self.create_button(btn_frame, "Register", "#16a34a", self.register_user, 15).grid(row=0, column=0, padx=10)
        self.create_button(btn_frame, "Back", "gray", self.show_welcome_page, 15).grid(row=0, column=1, padx=10)

    def register_user(self):
        username = self.reg_username.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_password.get().strip()

        if not username or not email or not password:
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

    # =========================
    # LOGIN PAGE
    # =========================
    def show_login_page(self):
        self.clear_window()
        self.create_header()
        self.page_title("User Login")

        form = tk.Frame(self.root, bg="white", bd=2, relief="ridge", padx=40, pady=30)
        form.pack(pady=20)

        tk.Label(form, text="Username", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, sticky="w", pady=10)
        self.login_username = self.create_entry(form)
        self.login_username.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(form, text="Password", font=("Arial", 12, "bold"), bg="white").grid(row=1, column=0, sticky="w", pady=10)
        self.login_password = self.create_entry(form, show="*")
        self.login_password.grid(row=1, column=1, pady=10, padx=10)

        btn_frame = tk.Frame(form, bg="white")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

        self.create_button(btn_frame, "Login", "#2563eb", self.login_user, 15).grid(row=0, column=0, padx=10)
        self.create_button(btn_frame, "Back", "gray", self.show_welcome_page, 15).grid(row=0, column=1, padx=10)

    def login_user(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            self.current_user = username
            self.show_home_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    # =========================
    # HOME PAGE
    # =========================
    def show_home_page(self):
        self.clear_window()
        self.create_header()

        tk.Label(
            self.root,
            text=f"Welcome, {self.current_user}",
            font=("Arial", 20, "bold"),
            bg="#eef4ff",
            fg="#0b3d91"
        ).pack(pady=20)

        button_frame = tk.Frame(self.root, bg="#eef4ff")
        button_frame.pack(pady=20)

        self.create_button(button_frame, "Create Account", "#10b981", self.show_create_account_page, 20).grid(row=0, column=0, padx=15, pady=15)
        self.create_button(button_frame, "Deposit", "#2563eb", self.show_deposit_page, 20).grid(row=0, column=1, padx=15, pady=15)
        self.create_button(button_frame, "Withdrawal", "#ef4444", self.show_withdraw_page, 20).grid(row=1, column=0, padx=15, pady=15)
        self.create_button(button_frame, "Current Balance", "#f59e0b", self.show_balance_page, 20).grid(row=1, column=1, padx=15, pady=15)
        self.create_button(button_frame, "Account Holder Details", "#8b5cf6", self.show_account_details_page, 25).grid(row=2, column=0, columnspan=2, pady=15)

        self.create_button(self.root, "Logout", "gray", self.logout, 15).pack(pady=20)

    def logout(self):
        self.current_user = None
        self.show_welcome_page()

    # =========================
    # ACCOUNT NUMBER GENERATION
    # =========================
    def generate_account_number(self):
        while True:
            acc_no = str(random.randint(1000000000, 9999999999))
            cursor.execute("SELECT * FROM accounts WHERE account_number=?", (acc_no,))
            if cursor.fetchone() is None:
                return acc_no

    # =========================
    # CREATE ACCOUNT PAGE
    # =========================
    def show_create_account_page(self):
        self.clear_window()
        self.create_header()
        self.page_title("Create New Bank Account")

        form = tk.Frame(self.root, bg="white", bd=2, relief="ridge", padx=40, pady=30)
        form.pack(pady=20)

        tk.Label(form, text="User Name", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, sticky="w", pady=10)
        self.acc_username = self.create_entry(form)
        self.acc_username.insert(0, self.current_user)
        self.acc_username.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(form, text="Phone Number", font=("Arial", 12, "bold"), bg="white").grid(row=1, column=0, sticky="w", pady=10)
        self.acc_phone = self.create_entry(form)
        self.acc_phone.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(form, text="Aadhar Number", font=("Arial", 12, "bold"), bg="white").grid(row=2, column=0, sticky="w", pady=10)
        self.acc_aadhar = self.create_entry(form)
        self.acc_aadhar.grid(row=2, column=1, pady=10, padx=10)

        btn_frame = tk.Frame(form, bg="white")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        self.create_button(btn_frame, "Create Account", "#10b981", self.create_account, 16).grid(row=0, column=0, padx=10)
        self.create_button(btn_frame, "Back", "gray", self.show_home_page, 16).grid(row=0, column=1, padx=10)

        self.create_result_box()

    def create_account(self):
        username = self.acc_username.get().strip()
        phone = self.acc_phone.get().strip()
        aadhar = self.acc_aadhar.get().strip()

        if not username or not phone or not aadhar:
            self.result_label.config(text="All fields are required", fg="red")
            return

        cursor.execute("SELECT * FROM accounts WHERE username=?", (self.current_user,))
        existing = cursor.fetchone()

        if existing:
            self.result_label.config(text="This user already has a Union Bank account", fg="red")
            return

        account_number = self.generate_account_number()

        cursor.execute("""
            INSERT INTO accounts (username, phone, aadhar, account_number, balance)
            VALUES (?, ?, ?, ?, ?)
        """, (self.current_user, phone, aadhar, account_number, 0))
        conn.commit()

        self.result_label.config(
            text=f"Account created successfully!\nGenerated Account Number: {account_number}",
            fg="green"
        )

    # =========================
    # DEPOSIT PAGE
    # =========================
    def show_deposit_page(self):
        self.clear_window()
        self.create_header()
        self.page_title("Deposit Money")

        form = tk.Frame(self.root, bg="white", bd=2, relief="ridge", padx=40, pady=30)
        form.pack(pady=20)

        tk.Label(form, text="Account Number", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, sticky="w", pady=10)
        self.dep_acc = self.create_entry(form)
        self.dep_acc.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(form, text="Deposit Amount", font=("Arial", 12, "bold"), bg="white").grid(row=1, column=0, sticky="w", pady=10)
        self.dep_amt = self.create_entry(form)
        self.dep_amt.grid(row=1, column=1, pady=10, padx=10)

        btn_frame = tk.Frame(form, bg="white")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

        self.create_button(btn_frame, "Deposit", "#2563eb", self.deposit_money, 16).grid(row=0, column=0, padx=10)
        self.create_button(btn_frame, "Back", "gray", self.show_home_page, 16).grid(row=0, column=1, padx=10)

        self.create_result_box()

    def deposit_money(self):
        acc_no = self.dep_acc.get().strip()
        amount = self.dep_amt.get().strip()

        if not acc_no or not amount:
            self.result_label.config(text="Please enter all fields", fg="red")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                self.result_label.config(text="Deposit amount must be greater than 0", fg="red")
                return
        except ValueError:
            self.result_label.config(text="Enter valid amount", fg="red")
            return

        cursor.execute("SELECT balance FROM accounts WHERE account_number=?", (acc_no,))
        account = cursor.fetchone()

        if not account:
            self.result_label.config(text="Account not found", fg="red")
            return

        new_balance = account[0] + amount
        cursor.execute("UPDATE accounts SET balance=? WHERE account_number=?", (new_balance, acc_no))
        conn.commit()

        self.result_label.config(
            text=f"₹{amount} deposited successfully.\nNew Balance: ₹{new_balance}",
            fg="green"
        )

    # =========================
    # WITHDRAW PAGE
    # =========================
    def show_withdraw_page(self):
        self.clear_window()
        self.create_header()
        self.page_title("Withdraw Money")

        form = tk.Frame(self.root, bg="white", bd=2, relief="ridge", padx=40, pady=30)
        form.pack(pady=20)

        tk.Label(form, text="Account Number", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, sticky="w", pady=10)
        self.with_acc = self.create_entry(form)
        self.with_acc.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(form, text="Withdrawal Amount", font=("Arial", 12, "bold"), bg="white").grid(row=1, column=0, sticky="w", pady=10)
        self.with_amt = self.create_entry(form)
        self.with_amt.grid(row=1, column=1, pady=10, padx=10)

        btn_frame = tk.Frame(form, bg="white")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

        self.create_button(btn_frame, "Withdraw", "#ef4444", self.withdraw_money, 16).grid(row=0, column=0, padx=10)
        self.create_button(btn_frame, "Back", "gray", self.show_home_page, 16).grid(row=0, column=1, padx=10)

        self.create_result_box()

    def withdraw_money(self):
        acc_no = self.with_acc.get().strip()
        amount = self.with_amt.get().strip()

        if not acc_no or not amount:
            self.result_label.config(text="Please enter all fields", fg="red")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                self.result_label.config(text="Withdrawal amount must be greater than 0", fg="red")
                return
        except ValueError:
            self.result_label.config(text="Enter valid amount", fg="red")
            return

        cursor.execute("SELECT balance FROM accounts WHERE account_number=?", (acc_no,))
        account = cursor.fetchone()

        if not account:
            self.result_label.config(text="Account not found", fg="red")
            return

        current_balance = account[0]
        if amount > current_balance:
            self.result_label.config(text="Insufficient balance", fg="red")
            return

        new_balance = current_balance - amount
        cursor.execute("UPDATE accounts SET balance=? WHERE account_number=?", (new_balance, acc_no))
        conn.commit()

        self.result_label.config(
            text=f"₹{amount} withdrawn successfully.\nRemaining Balance: ₹{new_balance}",
            fg="green"
        )

    # =========================
    # BALANCE PAGE
    # =========================
    def show_balance_page(self):
        self.clear_window()
        self.create_header()
        self.page_title("Current Balance")

        form = tk.Frame(self.root, bg="white", bd=2, relief="ridge", padx=40, pady=30)
        form.pack(pady=20)

        tk.Label(form, text="Account Number", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, sticky="w", pady=10)
        self.bal_acc = self.create_entry(form)
        self.bal_acc.grid(row=0, column=1, pady=10, padx=10)

        btn_frame = tk.Frame(form, bg="white")
        btn_frame.grid(row=1, column=0, columnspan=2, pady=20)

        self.create_button(btn_frame, "Check Balance", "#f59e0b", self.check_balance, 16).grid(row=0, column=0, padx=10)
        self.create_button(btn_frame, "Back", "gray", self.show_home_page, 16).grid(row=0, column=1, padx=10)

        self.create_result_box()

    def check_balance(self):
        acc_no = self.bal_acc.get().strip()

        if not acc_no:
            self.result_label.config(text="Please enter account number", fg="red")
            return

        cursor.execute("SELECT username, balance FROM accounts WHERE account_number=?", (acc_no,))
        account = cursor.fetchone()

        if account:
            self.result_label.config(
                text=f"Account Holder: {account[0]}\nCurrent Balance: ₹{account[1]}",
                fg="#0b3d91"
            )
        else:
            self.result_label.config(text="Account not found", fg="red")

    # =========================
    # ACCOUNT HOLDER DETAILS PAGE
    # =========================
    def show_account_details_page(self):
        self.clear_window()
        self.create_header()
        self.page_title("Account Holder Details")

        form = tk.Frame(self.root, bg="white", bd=2, relief="ridge", padx=40, pady=30)
        form.pack(pady=20)

        tk.Label(form, text="Account Number", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, sticky="w", pady=10)
        self.det_acc = self.create_entry(form)
        self.det_acc.grid(row=0, column=1, pady=10, padx=10)

        btn_frame = tk.Frame(form, bg="white")
        btn_frame.grid(row=1, column=0, columnspan=2, pady=20)

        self.create_button(btn_frame, "Show Details", "#8b5cf6", self.show_details, 16).grid(row=0, column=0, padx=10)
        self.create_button(btn_frame, "Back", "gray", self.show_home_page, 16).grid(row=0, column=1, padx=10)

        # result frame instead of popup
        self.details_box = tk.Frame(self.root, bg="white", bd=2, relief="ridge", padx=20, pady=20)
        self.details_box.pack(pady=20)

        self.details_title = tk.Label(
            self.details_box,
            text="Account Details",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#0b3d91"
        )
        self.details_title.pack(pady=10)

        self.details_result = tk.Label(
            self.details_box,
            text="Enter account number and click 'Show Details'",
            font=("Arial", 13),
            bg="white",
            fg="#333",
            justify="left"
        )
        self.details_result.pack()

    def show_details(self):
        acc_no = self.det_acc.get().strip()

        if not acc_no:
            self.details_result.config(text="Please enter account number", fg="red")
            return

        cursor.execute("""
            SELECT username, phone, aadhar, account_number, balance
            FROM accounts
            WHERE account_number=?
        """, (acc_no,))
        account = cursor.fetchone()

        if account:
            details = (
                f"Account Holder Name : {account[0]}\n\n"
                f"Phone Number        : {account[1]}\n\n"
                f"Aadhar Number       : {account[2]}\n\n"
                f"Account Number      : {account[3]}\n\n"
                f"Current Balance     : ₹{account[4]}"
            )
            self.details_result.config(text=details, fg="#0b3d91")
        else:
            self.details_result.config(text="Account not found", fg="red")

    # =========================
    # COMMON RESULT BOX
    # =========================
    def create_result_box(self):
        result_frame = tk.Frame(self.root, bg="white", bd=2, relief="ridge", padx=20, pady=20)
        result_frame.pack(pady=20)

        tk.Label(
            result_frame,
            text="Result",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#0b3d91"
        ).pack(pady=10)

        self.result_label = tk.Label(
            result_frame,
            text="Result will be shown here",
            font=("Arial", 13),
            bg="white",
            fg="#333",
            justify="center"
        )
        self.result_label.pack()


# =========================
# RUN APP
# =========================
root = tk.Tk()
app = UnionBankApp(root)
root.mainloop()