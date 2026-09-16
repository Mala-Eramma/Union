import tkinter as tk
from tkinter import messagebox
import sqlite3
import random
from datetime import datetime

# ==============================
# DATABASE SETUP
# ==============================

class BankDatabase:
    def __init__(self, db_name="union_bank.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Account table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_no TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                aadhar TEXT NOT NULL,
                balance REAL DEFAULT 0
            )
        """)

        # Transactions table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_no TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                date_time TEXT NOT NULL,
                FOREIGN KEY (account_no) REFERENCES accounts(account_no)
            )
        """)
        self.conn.commit()

    def generate_unique_account_no(self):
        while True:
            acc_no = str(random.randint(1000000000, 9999999999))  # 10-digit account number
            self.cursor.execute("SELECT account_no FROM accounts WHERE account_no=?", (acc_no,))
            if not self.cursor.fetchone():
                return acc_no

    def create_account(self, name, phone, aadhar):
        acc_no = self.generate_unique_account_no()
        self.cursor.execute("""
            INSERT INTO accounts (account_no, name, phone, aadhar, balance)
            VALUES (?, ?, ?, ?, 0)
        """, (acc_no, name, phone, aadhar))
        self.conn.commit()
        return acc_no

    def get_account(self, account_no):
        self.cursor.execute("SELECT * FROM accounts WHERE account_no=?", (account_no,))
        return self.cursor.fetchone()

    def deposit(self, account_no, amount):
        account = self.get_account(account_no)
        if not account:
            return "invalid"

        new_balance = account[4] + amount
        self.cursor.execute("UPDATE accounts SET balance=? WHERE account_no=?", (new_balance, account_no))

        self.cursor.execute("""
            INSERT INTO transactions (account_no, transaction_type, amount, date_time)
            VALUES (?, ?, ?, ?)
        """, (account_no, "Deposit", amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        self.conn.commit()
        return new_balance

    def withdraw(self, account_no, amount):
        account = self.get_account(account_no)
        if not account:
            return "invalid"

        current_balance = account[4]
        if amount > current_balance:
            return "insufficient"

        new_balance = current_balance - amount
        self.cursor.execute("UPDATE accounts SET balance=? WHERE account_no=?", (new_balance, account_no))

        self.cursor.execute("""
            INSERT INTO transactions (account_no, transaction_type, amount, date_time)
            VALUES (?, ?, ?, ?)
        """, (account_no, "Withdrawal", amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        self.conn.commit()
        return new_balance


# ==============================
# MAIN APPLICATION
# ==============================

class UnionBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Union Bank Account Management System")
        self.root.geometry("900x600")
        self.root.configure(bg="#f4f8fb")
        self.root.resizable(False, False)

        self.db = BankDatabase()

        self.primary_color = "#003366"     # Deep blue
        self.secondary_color = "#ff6600"   # Orange
        self.bg_color = "#f4f8fb"
        self.card_color = "#ffffff"
        self.text_color = "#1a1a1a"

        self.setup_home_page()

    # --------------------------
    # Utility methods
    # --------------------------
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_header(self, title):
        header = tk.Frame(self.root, bg=self.primary_color, height=80)
        header.pack(fill="x")

        title_label = tk.Label(
            header,
            text=title,
            font=("Segoe UI", 24, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        title_label.pack(pady=20)

    def create_back_button(self):
        back_btn = tk.Button(
            self.root,
            text="← Back",
            font=("Segoe UI", 11, "bold"),
            bg=self.secondary_color,
            fg="white",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            command=self.setup_home_page
        )
        back_btn.place(x=20, y=95)

    # --------------------------
    # Home Page
    # --------------------------
    def setup_home_page(self):
        self.clear_window()
        self.create_header("Union Bank Account Management")

        # Welcome section
        welcome_frame = tk.Frame(self.root, bg=self.bg_color)
        welcome_frame.pack(pady=30)

        tk.Label(
            welcome_frame,
            text="Welcome to Union Bank",
            font=("Segoe UI", 22, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        ).pack()

        tk.Label(
            welcome_frame,
            text="Manage accounts, deposit money, and withdraw funds securely",
            font=("Segoe UI", 12),
            bg=self.bg_color,
            fg="#555555"
        ).pack(pady=8)

        # Card section
        card_frame = tk.Frame(self.root, bg=self.bg_color)
        card_frame.pack(pady=40)

        self.create_option_card(card_frame, "Create Account", "Open a new bank account", self.open_create_account, 0)
        self.create_option_card(card_frame, "Deposit", "Add money to your account", self.open_deposit_page, 1)
        self.create_option_card(card_frame, "Withdrawal", "Withdraw money securely", self.open_withdraw_page, 2)

        # Footer
        footer = tk.Label(
            self.root,
            text="Union Bank • Secure Banking Management System",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg="#666666"
        )
        footer.pack(side="bottom", pady=20)

    def create_option_card(self, parent, title, subtitle, command, column):
        card = tk.Frame(parent, bg=self.card_color, width=220, height=220, highlightbackground="#d9d9d9", highlightthickness=1)
        card.grid(row=0, column=column, padx=20)
        card.pack_propagate(False)

        icon = "🏦" if title == "Create Account" else "💰" if title == "Deposit" else "💳"

        tk.Label(card, text=icon, font=("Segoe UI Emoji", 38), bg=self.card_color).pack(pady=(20, 10))
        tk.Label(card, text=title, font=("Segoe UI", 16, "bold"), bg=self.card_color, fg=self.primary_color).pack()
        tk.Label(card, text=subtitle, font=("Segoe UI", 10), bg=self.card_color, fg="#666666", wraplength=180).pack(pady=10)

        tk.Button(
            card,
            text="Open",
            font=("Segoe UI", 11, "bold"),
            bg=self.secondary_color,
            fg="white",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=command
        ).pack(pady=15)

    # --------------------------
    # Create Account Page
    # --------------------------
    def open_create_account(self):
        self.clear_window()
        self.create_header("Create New Account")
        self.create_back_button()

        form = tk.Frame(self.root, bg=self.card_color, padx=40, pady=30, highlightbackground="#d9d9d9", highlightthickness=1)
        form.pack(pady=60)

        tk.Label(form, text="Open a Union Bank Account", font=("Segoe UI", 18, "bold"), bg=self.card_color, fg=self.primary_color).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Label(form, text="User Name:", font=("Segoe UI", 12), bg=self.card_color).grid(row=1, column=0, sticky="w", pady=10)
        name_entry = tk.Entry(form, font=("Segoe UI", 12), width=28)
        name_entry.grid(row=1, column=1, pady=10)

        tk.Label(form, text="Phone Number:", font=("Segoe UI", 12), bg=self.card_color).grid(row=2, column=0, sticky="w", pady=10)
        phone_entry = tk.Entry(form, font=("Segoe UI", 12), width=28)
        phone_entry.grid(row=2, column=1, pady=10)

        tk.Label(form, text="Aadhar Number:", font=("Segoe UI", 12), bg=self.card_color).grid(row=3, column=0, sticky="w", pady=10)
        aadhar_entry = tk.Entry(form, font=("Segoe UI", 12), width=28)
        aadhar_entry.grid(row=3, column=1, pady=10)

        def submit_account():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            aadhar = aadhar_entry.get().strip()

            # Validation
            if not name or not phone or not aadhar:
                messagebox.showerror("Error", "All fields are required!")
                return

            if not phone.isdigit() or len(phone) != 10:
                messagebox.showerror("Error", "Phone number must be 10 digits!")
                return

            if not aadhar.isdigit() or len(aadhar) != 12:
                messagebox.showerror("Error", "Aadhar number must be 12 digits!")
                return

            try:
                acc_no = self.db.create_account(name, phone, aadhar)
                messagebox.showinfo(
                    "Account Created",
                    f"Account created successfully!\n\nAccount Number: {acc_no}\nInitial Balance: ₹0"
                )
                self.setup_home_page()
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to create account.\n{str(e)}")

        tk.Button(
            form,
            text="Create Account",
            font=("Segoe UI", 12, "bold"),
            bg=self.secondary_color,
            fg="white",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=submit_account
        ).grid(row=4, column=0, columnspan=2, pady=25)

    # --------------------------
    # Deposit Page
    # --------------------------
    def open_deposit_page(self):
        self.clear_window()
        self.create_header("Deposit Money")
        self.create_back_button()

        form = tk.Frame(self.root, bg=self.card_color, padx=40, pady=30, highlightbackground="#d9d9d9", highlightthickness=1)
        form.pack(pady=80)

        tk.Label(form, text="Deposit to Account", font=("Segoe UI", 18, "bold"), bg=self.card_color, fg=self.primary_color).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Label(form, text="Account Number:", font=("Segoe UI", 12), bg=self.card_color).grid(row=1, column=0, sticky="w", pady=10)
        acc_entry = tk.Entry(form, font=("Segoe UI", 12), width=28)
        acc_entry.grid(row=1, column=1, pady=10)

        tk.Label(form, text="Amount to Deposit:", font=("Segoe UI", 12), bg=self.card_color).grid(row=2, column=0, sticky="w", pady=10)
        amount_entry = tk.Entry(form, font=("Segoe UI", 12), width=28)
        amount_entry.grid(row=2, column=1, pady=10)

        def deposit_money():
            acc_no = acc_entry.get().strip()
            amount_text = amount_entry.get().strip()

            if not acc_no or not amount_text:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                amount = float(amount_text)
                if amount <= 0:
                    messagebox.showerror("Error", "Deposit amount must be greater than 0!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount!")
                return

            result = self.db.deposit(acc_no, amount)

            if result == "invalid":
                messagebox.showerror("Invalid User", "Account number not found!")
            else:
                messagebox.showinfo("Success", f"₹{amount:.2f} deposited successfully!\nNew Balance: ₹{result:.2f}")
                self.setup_home_page()

        tk.Button(
            form,
            text="Deposit",
            font=("Segoe UI", 12, "bold"),
            bg=self.secondary_color,
            fg="white",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=deposit_money
        ).grid(row=3, column=0, columnspan=2, pady=25)

    # --------------------------
    # Withdrawal Page
    # --------------------------
    def open_withdraw_page(self):
        self.clear_window()
        self.create_header("Withdraw Money")
        self.create_back_button()

        form = tk.Frame(self.root, bg=self.card_color, padx=40, pady=30, highlightbackground="#d9d9d9", highlightthickness=1)
        form.pack(pady=80)

        tk.Label(form, text="Withdraw from Account", font=("Segoe UI", 18, "bold"), bg=self.card_color, fg=self.primary_color).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Label(form, text="Account Number:", font=("Segoe UI", 12), bg=self.card_color).grid(row=1, column=0, sticky="w", pady=10)
        acc_entry = tk.Entry(form, font=("Segoe UI", 12), width=28)
        acc_entry.grid(row=1, column=1, pady=10)

        tk.Label(form, text="Amount to Withdraw:", font=("Segoe UI", 12), bg=self.card_color).grid(row=2, column=0, sticky="w", pady=10)
        amount_entry = tk.Entry(form, font=("Segoe UI", 12), width=28)
        amount_entry.grid(row=2, column=1, pady=10)

        def withdraw_money():
            acc_no = acc_entry.get().strip()
            amount_text = amount_entry.get().strip()

            if not acc_no or not amount_text:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                amount = float(amount_text)
                if amount <= 0:
                    messagebox.showerror("Error", "Withdrawal amount must be greater than 0!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount!")
                return

            result = self.db.withdraw(acc_no, amount)

            if result == "invalid":
                messagebox.showerror("Invalid User", "Account number not found!")
            elif result == "insufficient":
                messagebox.showerror("Insufficient Balance", "Insufficient Balance")
            else:
                messagebox.showinfo("Success", f"₹{amount:.2f} withdrawn successfully!\nRemaining Balance: ₹{result:.2f}")
                self.setup_home_page()

        tk.Button(
            form,
            text="Withdraw",
            font=("Segoe UI", 12, "bold"),
            bg=self.secondary_color,
            fg="white",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=withdraw_money
        ).grid(row=3, column=0, columnspan=2, pady=25)


# ==============================
# RUN APPLICATION
# ==============================

if __name__ == "__main__":
    root = tk.Tk()
    app = UnionBankApp(root)
    root.mainloop()