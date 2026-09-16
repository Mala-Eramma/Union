import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

DB_NAME = "union_bank.db"


# ---------------- DATABASE ----------------
def get_db():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_db()
    cur = conn.cursor()

    # users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # accounts table
    cur.execute("""
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


# ---------------- APP ----------------
class UnionBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Union Bank Account Management System")
        self.root.geometry("950x650")
        self.root.configure(bg="#dbeafe")

        self.current_user = None

        self.main_frame = tk.Frame(self.root, bg="#dbeafe")
        self.main_frame.pack(fill="both", expand=True)

        create_tables()
        self.show_welcome()

    # ---------- COMMON ----------
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def page_title(self, text):
        tk.Label(
            self.main_frame,
            text=text,
            font=("Arial", 22, "bold"),
            bg="#dbeafe",
            fg="#0f172a"
        ).pack(pady=20)

    def make_entry(self, label_text, show=None, default_value="", readonly=False):
        tk.Label(
            self.main_frame,
            text=label_text,
            font=("Arial", 12, "bold"),
            bg="#dbeafe",
            fg="#1e293b"
        ).pack(pady=(8, 2))

        entry = tk.Entry(self.main_frame, font=("Arial", 12), width=35, show=show)
        entry.pack(pady=5)

        if default_value:
            entry.insert(0, default_value)

        if readonly:
            entry.config(state="readonly")
            return entry

    def make_button(self, text, command, bg="#2563eb", width=24):
        tk.Button(
            self.main_frame,
            text=text,
            command=command,
            bg=bg,
            fg="white",
            font=("Arial", 12, "bold"),
            width=width,
            relief="flat",
            pady=8
        ).pack(pady=8)

    def show_message_on_page(self, text, ok=True):
        color = "#166534" if ok else "#991b1b"
        bg = "#dcfce7" if ok else "#fee2e2"

        box = tk.Label(
            self.main_frame,
            text=text,
            font=("Arial", 12, "bold"),
            bg=bg,
            fg=color,
            justify="left",
            wraplength=700,
            padx=15,
            pady=15
        )
        box.pack(pady=15)

    def generate_account_number(self):
        conn = get_db()
        cur = conn.cursor()

        while True:
            acc_no = str(random.randint(1000000000, 9999999999))
            cur.execute("SELECT 1 FROM accounts WHERE account_number=?", (acc_no,))
            if cur.fetchone() is None:
                conn.close()
                return acc_no

    def logout(self):
        self.current_user = None
        self.show_welcome()

    # ---------- WELCOME ----------
    def show_welcome(self):
        self.clear_frame()
        self.page_title("UNION BANK ACCOUNT MANAGEMENT SYSTEM")

        card = tk.Frame(self.main_frame, bg="white", bd=2, relief="groove", padx=40, pady=40)
        card.pack(pady=60)

        tk.Label(
            card,
            text="Welcome to Union Bank",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#1d4ed8"
        ).pack(pady=20)

        tk.Button(
            card,
            text="Register",
            command=self.show_register,
            bg="#16a34a",
            fg="white",
            font=("Arial", 12, "bold"),
            width=25,
            pady=8
        ).pack(pady=10)

        tk.Button(
            card,
            text="Login",
            command=self.show_login,
            bg="#2563eb",
            fg="white",
            font=("Arial", 12, "bold"),
            width=25,
            pady=8
        ).pack(pady=10)

    # ---------- REGISTER ----------
    def show_register(self):
        self.clear_frame()
        self.page_title("User Registration")

        username_entry = self.make_entry("User Name")
        email_entry = self.make_entry("Email")
        password_entry = self.make_entry("Password", show="*")

        def register_user():
            username = username_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get().strip()

            if not username or not email or not password:
                messagebox.showerror("Error", "All fields are required")
                return

            conn = get_db()
            cur = conn.cursor()
            try:
                cur.execute(
                    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, password)
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Registration successful. Please login.")
                self.show_login()
            except sqlite3.IntegrityError:
                conn.close()
                messagebox.showerror("Error", "Username already registered")

        self.make_button("Register", register_user, "#16a34a")
        self.make_button("Back", self.show_welcome, "gray")

    # ---------- LOGIN ----------
    def show_login(self):
        self.clear_frame()
        self.page_title("User Login")

        username_entry = self.make_entry("User Name")
        password_entry = self.make_entry("Password", show="*")

        def login_user():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if not username or not password:
                messagebox.showerror("Error", "All fields are required")
                return

            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, password)
            )
            user = cur.fetchone()
            conn.close()

            if user:
                self.current_user = username
                self.show_home()
            else:
                messagebox.showerror("Error", "Invalid username or password")

        self.make_button("Login", login_user, "#2563eb")
        self.make_button("Back", self.show_welcome, "gray")

    # ---------- HOME ----------
    def show_home(self):
        self.clear_frame()
        self.page_title(f"Welcome, {self.current_user}")

        btn_frame = tk.Frame(self.main_frame, bg="#dbeafe")
        btn_frame.pack(pady=20)

        btn_style = {
            "font": ("Arial", 12, "bold"),
            "fg": "white",
            "width": 20,
            "height": 2,
            "relief": "flat"
        }

        tk.Button(btn_frame, text="Create Account", command=self.show_create_account, bg="#16a34a", **btn_style).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Deposit", command=self.show_deposit, bg="#2563eb", **btn_style).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(btn_frame, text="Withdrawal", command=self.show_withdrawal, bg="#dc2626", **btn_style).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Current Balance", command=self.show_balance, bg="#f59e0b", **btn_style).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(btn_frame, text="Account Holder Details", command=self.show_details, bg="#7c3aed", **btn_style).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        bottom = tk.Frame(self.main_frame, bg="#dbeafe")
        bottom.pack(pady=20)

        tk.Button(
            bottom, text="Back", command=self.show_welcome,
            bg="gray", fg="white", font=("Arial", 12, "bold"), width=18
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            bottom, text="Logout", command=self.logout,
            bg="#dc2626", fg="white", font=("Arial", 12, "bold"), width=18
        ).grid(row=0, column=1, padx=10)

    # ---------- CREATE ACCOUNT ----------
    def show_create_account(self):
        self.clear_frame()
        self.page_title("Create New Bank Account")

        self.make_entry("User Name", default_value=self.current_user, readonly=True)
        phone_entry = self.make_entry("Phone Number")
        aadhar_entry = self.make_entry("Aadhar Number")

        def create_account():
            phone = phone_entry.get().strip()
            aadhar = aadhar_entry.get().strip()

            if not phone or not aadhar:
                messagebox.showerror("Error", "All fields are required")
                return

            conn = get_db()
            cur = conn.cursor()

            # same logged-in user should not create account again
            cur.execute("SELECT * FROM accounts WHERE username=?", (self.current_user,))
            existing = cur.fetchone()

            if existing:
                conn.close()
                self.show_create_account()
                self.show_message_on_page(
                    f"Account already exists for user: {self.current_user}\n"
                    f"Account Number: {existing[4]}",
                    ok=False
                )
                return

            acc_no = self.generate_account_number()

            cur.execute("""
                INSERT INTO accounts (username, phone, aadhar, account_number, balance)
                VALUES (?, ?, ?, ?, ?)
            """, (self.current_user, phone, aadhar, acc_no, 0.0))

            conn.commit()
            conn.close()

            self.show_create_account()
            self.show_message_on_page(
                f"Account created successfully!\n"
                f"Account Holder: {self.current_user}\n"
                f"Generated Account Number: {acc_no}",
                ok=True
            )

        self.make_button("Create Account", create_account, "#16a34a")
        self.make_button("Back", self.show_home, "gray")
        self.make_button("Logout", self.logout, "#dc2626")

    # ---------- DEPOSIT ----------
    def show_deposit(self):
        self.clear_frame()
        self.page_title("Deposit Money")

        acc_entry = self.make_entry("Account Number")
        amount_entry = self.make_entry("Deposit Amount")

        def deposit_money():
            acc_no = acc_entry.get().strip()
            amount_text = amount_entry.get().strip()

            if not acc_no or not amount_text:
                messagebox.showerror("Error", "All fields are required")
                return

            try:
                amount = float(amount_text)
                if amount <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Enter valid deposit amount")
                return

            conn = get_db()
            cur = conn.cursor()

            cur.execute("SELECT balance FROM accounts WHERE account_number=?", (acc_no,))
            row = cur.fetchone()

            if not row:
                conn.close()
                self.show_deposit()
                self.show_message_on_page("Account not found", ok=False)
                return

            new_balance = row[0] + amount
            cur.execute("UPDATE accounts SET balance=? WHERE account_number=?", (new_balance, acc_no))
            conn.commit()
            conn.close()

            self.show_deposit()
            self.show_message_on_page(
                f"₹{amount} deposited successfully.\nNew Balance: ₹{new_balance}",
                ok=True
            )

        self.make_button("Deposit", deposit_money, "#2563eb")
        self.make_button("Back", self.show_home, "gray")
        self.make_button("Logout", self.logout, "#dc2626")

    # ---------- WITHDRAWAL ----------
    def show_withdrawal(self):
        self.clear_frame()
        self.page_title("Withdraw Money")

        acc_entry = self.make_entry("Account Number")
        amount_entry = self.make_entry("Withdrawal Amount")

        def withdraw_money():
            acc_no = acc_entry.get().strip()
            amount_text = amount_entry.get().strip()

            if not acc_no or not amount_text:
                messagebox.showerror("Error", "All fields are required")
                return

            try:
                amount = float(amount_text)
                if amount <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Enter valid withdrawal amount")
                return

            conn = get_db()
            cur = conn.cursor()

            cur.execute("SELECT balance FROM accounts WHERE account_number=?", (acc_no,))
            row = cur.fetchone()

            if not row:
                conn.close()
                self.show_withdrawal()
                self.show_message_on_page("Account not found", ok=False)
                return

            balance = row[0]
            if amount > balance:
                conn.close()
                self.show_withdrawal()
                self.show_message_on_page("Insufficient balance", ok=False)
                return

            new_balance = balance - amount
            cur.execute("UPDATE accounts SET balance=? WHERE account_number=?", (new_balance, acc_no))
            conn.commit()
            conn.close()

            self.show_withdrawal()
            self.show_message_on_page(
                f"₹{amount} withdrawn successfully.\nRemaining Balance: ₹{new_balance}",
                ok=True
            )

        self.make_button("Withdraw", withdraw_money, "#dc2626")
        self.make_button("Back", self.show_home, "gray")
        self.make_button("Logout", self.logout, "#dc2626")

    # ---------- CURRENT BALANCE ----------
    def show_balance(self):
        self.clear_frame()
        self.page_title("Current Balance")

        acc_entry = self.make_entry("Account Number")

        def check_balance():
            acc_no = acc_entry.get().strip()

            if not acc_no:
                messagebox.showerror("Error", "Enter account number")
                return

            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT username, balance FROM accounts WHERE account_number=?", (acc_no,))
            row = cur.fetchone()
            conn.close()

            self.show_balance()

            if row:
                self.show_message_on_page(
                    f"Account Holder: {row[0]}\nCurrent Balance: ₹{row[1]}",
                    ok=True
                )
            else:
                self.show_message_on_page("Account not found", ok=False)

        self.make_button("Check Balance", check_balance, "#f59e0b")
        self.make_button("Back", self.show_home, "gray")
        self.make_button("Logout", self.logout, "#dc2626")

    # ---------- ACCOUNT HOLDER DETAILS ----------
    def show_details(self):
        self.clear_frame()
        self.page_title("Account Holder Details")

        acc_entry = self.make_entry("Account Number")

        def fetch_details():
            acc_no = acc_entry.get().strip()

            if not acc_no:
                messagebox.showerror("Error", "Enter account number")
                return

            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                SELECT username, phone, aadhar, account_number, balance
                FROM accounts
                WHERE account_number=?
            """, (acc_no,))
            row = cur.fetchone()
            conn.close()

            self.show_details()

            if row:
                self.show_message_on_page(
                    f"Account Holder Name: {row[0]}\n"
                    f"Phone Number: {row[1]}\n"
                    f"Aadhar Number: {row[2]}\n"
                    f"Account Number: {row[3]}\n"
                    f"Current Balance: ₹{row[4]}",
                    ok=True
                )
            else:
                self.show_message_on_page("Account not found", ok=False)

        self.make_button("Show Details", fetch_details, "#7c3aed")
        self.make_button("Back", self.show_home, "gray")
        self.make_button("Logout", self.logout, "#dc2626")


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = UnionBankApp(root)
    root.mainloop()
