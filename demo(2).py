import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector

class BankManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry("1920x1080")
        
        # Database Connection
        self.connection = self.create_db_connection()
        
        # Load bank logo
        self.bank_logo = Image.open("bank_logo.jpg").resize((100, 100), Image.Resampling.LANCZOS)
        self.bank_logo_photo = ImageTk.PhotoImage(self.bank_logo)
        self.bank_details_frame = None
        self.center_frame = None
        
        # Initialize the login page
        self.setup_login_page()
        
    def create_db_connection(self):
        try:
            return mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='root',
                database='bank_management_system'
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            return None
        
    def setup_bank_details(self):
        """Sets up the bank details frame at the top of the window."""
        if self.bank_details_frame:
            self.bank_details_frame.destroy()

        self.bank_details_frame = tk.Frame(self.root, bg='white', relief='raised', borderwidth=1)
        self.bank_details_frame.pack(side='top', fill='x')
        tk.Label(self.bank_details_frame, image=self.bank_logo_photo, bg='white').pack(side='left', padx=10)
        tk.Label(self.bank_details_frame, text="GLOBAL BANK", font=('Arial', 24, 'bold'), bg='white').pack(side='left', padx=10)
        tk.Label(self.bank_details_frame, text="123 Bank Street, Financial City, 000123", font=('Arial', 10), bg='white').pack(side='left', padx=10)
    
    def setup_background(self, image_path):
        """Sets the background image for the window."""
        bg_image = Image.open(image_path).resize((1920, 1080), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self.root, image=bg_photo)
        bg_label.image = bg_photo  # Keep a reference to prevent garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def clear_frame(self):
        """Clears all child widgets from the root."""
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def open_create_account_window(self):
        """Open a window for creating a new account."""
        create_window = tk.Toplevel(self.root)
        create_window.title("Create Account")
        create_window.geometry("3480x2160")

        tk.Label(create_window, text="Full Name").pack(pady=5)
        name_entry = tk.Entry(create_window)
        name_entry.pack(pady=5)

        tk.Label(create_window, text="Phone Number").pack(pady=5)
        phone_entry = tk.Entry(create_window)
        phone_entry.pack(pady=5)

        tk.Label(create_window, text="Email").pack(pady=5)
        email_entry = tk.Entry(create_window)
        email_entry.pack(pady=5)

        tk.Label(create_window, text="Aadhar Number").pack(pady=5)
        aadhar_entry = tk.Entry(create_window)
        aadhar_entry.pack(pady=5)

        tk.Label(create_window, text="Password").pack(pady=5)
        password_entry = tk.Entry(create_window, show='*')
        password_entry.pack(pady=5)

        tk.Button(create_window, text="Create Account",
                  command=lambda: self.create_account(
                      name_entry.get(), phone_entry.get(), email_entry.get(),
                      aadhar_entry.get(), password_entry.get(), create_window
                  )).pack(pady=10)
        
    def create_account(self, name, phone, email, aadhar, password, window):
        bank_name = "BANK"
        account_number = f"{bank_name}{random.randint(10000, 99999)}"
        if not all([name, phone, email, aadhar, password]):
            messagebox.showerror("Error", "All fields are required!")
            return
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO users (name, phone_number, email, aadhar_number, password, account_number) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (name, phone, email, aadhar, password, account_number))
            self.connection.commit()
            messagebox.showinfo("Success", f"Account created successfully! Your account number is {account_number}")
            window.destroy()  # Close the create account window
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

            
    def update_balance_label(self, account_number):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT balance FROM users WHERE account_number = %s", (account_number,))
        new_balance = cursor.fetchone()['balance']
        print(f"Updated Balance for Account {account_number}: ₹{new_balance}")  # Debug print
        self.balance_label.config(text=f"Balance: ₹{new_balance:.2f}")

    
    def setup_login_page(self):
        self.clear_frame()
        self.setup_background("login_background.jpg")
        self.setup_bank_details()

        login_frame = tk.Frame(self.root, bg='white', relief='groove', borderwidth=2)
        login_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=300)

        tk.Label(login_frame, text="Login", font=('Arial', 18, 'bold'), bg='white').pack(pady=10)
        tk.Label(login_frame, text="Account Number:", bg='white').pack(pady=5)
        account_entry = tk.Entry(login_frame)
        account_entry.pack(pady=5)
        tk.Label(login_frame, text="PIN:", bg='white').pack(pady=5)
        pin_entry = tk.Entry(login_frame, show='*')
        pin_entry.pack(pady=5)

        tk.Button(login_frame, text="Login", bg='lightgreen', fg='black',
                  command=lambda: self.login(account_entry.get(), pin_entry.get())).pack(pady=10)
        tk.Button(login_frame, text="Create Account", bg='darkred', fg='white', command=self.open_create_account_window).pack(pady=10)

    def login(self, account_number, pin):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE account_number = %s AND password = %s"
            cursor.execute(query, (account_number, pin))
            user = cursor.fetchone()

            if user:
                self.open_dashboard(user)
            else:
                messagebox.showerror("Login Failed", "Invalid Account Number or PIN")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def open_dashboard(self, user):
        self.clear_frame()
        self.setup_background("background.jpg")
        self.setup_bank_details()

        # Main container
        main_container = tk.Frame(self.root, relief='sunken', bg='beige')
        main_container.pack(fill='both', expand=True)

        # User Details Frame - Fixed positioning ABOVE scrollable content
        user_frame = tk.Frame(main_container, bg='white', relief='groove', borderwidth=2)
        user_frame.pack(pady=(5,10), padx=20, fill='x')

        tk.Label(user_frame, text=f"Name: {user['name']}", font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='w', padx=10)
        tk.Label(user_frame, text=f"Account Number: {user['account_number']}", font=('Arial', 12), bg='white').grid(row=0, column=1, sticky='w', padx=10)
        tk.Label(user_frame, text=f"Email: {user['email']}", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', padx=10)

        # Balance Label
        self.balance_label = tk.Label(user_frame, text=f"Balance: ₹{user['balance']}", font=('Arial', 12, 'bold'), fg='green', bg='white')
        self.balance_label.grid(row=1, column=1, sticky='w', padx=10)

        # View Details Button
        tk.Button(user_frame, text="View Details", font=('Arial', 12),bg='skyblue', fg='white', command=lambda: self.view_details(user['account_number'])).grid(row=2, column=0, pady=10)

        # Transaction History Button
        tk.Button(user_frame, text="Transaction History", font=('Arial', 12),bg='pink', fg='white', command=lambda: self.view_transaction_history(user['account_number'])).grid(row=2, column=1, pady=10)


        # Create a Canvas for Scrollable UI
        canvas = tk.Canvas(main_container, bg='white')
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True, pady=10)

        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas
        scrollable_frame = tk.Frame(canvas, bg='white')
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=self.root.winfo_screenwidth())

        # Frame configurations
        frame_style = {
            'bg': 'white', 
            'relief': 'groove', 
            'borderwidth': 2
        }

        # Credit/Debit Frame
        credit_debit_frame = tk.Frame(scrollable_frame, **frame_style)
        credit_debit_frame.pack(pady=10, padx=20, fill='x')
        
        # Add Title to Frame
        tk.Label(credit_debit_frame, text="Credit/Debit Transaction", font=('Arial', 14, 'bold'), bg='white', anchor='w').grid(row=0, column=0, columnspan=3, pady=10,padx=10, sticky="w")
        
        tk.Label(credit_debit_frame, text="Transaction Amount:", font=('Arial', 12), bg='white').grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")
        amount_entry = tk.Entry(credit_debit_frame, width=30)  # Increased width
        amount_entry.grid(row=2, column=1, padx=5, pady=5)

        credit_button = tk.Button(credit_debit_frame, text="Credit",bg='green', fg='white', command=lambda: self.credit_debit(user['account_number'], amount_entry.get(), 'credit'))
        credit_button.grid(row=3, column=0, pady=20)

        debit_button = tk.Button(credit_debit_frame, text="Debit", bg='red', fg='white', command=lambda: self.credit_debit(user['account_number'], amount_entry.get(), 'debit'))
        debit_button.grid(row=3, column=2, pady=20)

        credit_debit_frame.grid_columnconfigure(0, weight=1)
        credit_debit_frame.grid_columnconfigure(1, weight=1)
        credit_debit_frame.grid_columnconfigure(2, weight=1)

        # Transfer Frame
        transfer_frame = tk.Frame(scrollable_frame, **frame_style)
        transfer_frame.pack(pady=10, padx=20, fill='x')

        # Add Title to Frame
        tk.Label(transfer_frame, text="Money Transfer", font=('Arial', 14, 'bold'), bg='white', anchor='w').grid(row=0, column=0, columnspan=3, pady=10,padx=10, sticky="w")

        tk.Label(transfer_frame, text="Recipient Account:", font=('Arial', 12), bg='white').grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")
        recipient_entry = tk.Entry(transfer_frame, width=30)  # Increased width
        recipient_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(transfer_frame, text="Amount :", font=('Arial', 12), bg ='white').grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")
        transfer_amount_entry = tk.Entry(transfer_frame, width=30)  # Increased width
        transfer_amount_entry.grid(row=4, column=1, padx=5, pady=5)

        transfer_button = tk.Button(transfer_frame, text="Transfer", bg='lightgreen', fg='black', command=lambda: self.transfer_money(user['account_number'], recipient_entry.get(), transfer_amount_entry.get()))
        transfer_button.grid(row=5, column=1, pady=20)

        transfer_frame.grid_columnconfigure(0, weight=1)
        transfer_frame.grid_columnconfigure(1, weight=1)
        transfer_frame.grid_columnconfigure(2, weight=1)

        # Apply for Credit Card Frame
        apply_credit_card_frame = tk.Frame(scrollable_frame, **frame_style)
        apply_credit_card_frame.pack(pady=10, padx=20, fill='x')

        # Add Title to Frame
        tk.Label(apply_credit_card_frame, text="Apply for Credit Card", font=('Arial', 14, 'bold'), bg='white', anchor='w').grid(row=0, column=0, columnspan=3, pady=10,padx=10, sticky="w")

        tk.Label(apply_credit_card_frame, text="Income (₹):", font=('Arial', 12), bg='white').grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")
        income_entry = tk.Entry(apply_credit_card_frame, width=30)  # Increased width
        income_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(apply_credit_card_frame, text="Current Address:", font=('Arial', 12), bg='white').grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")
        address_entry = tk.Entry(apply_credit_card_frame, width=30)  # Increased width
        address_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(apply_credit_card_frame, text="Annual Expenses (₹):", font=('Arial', 12), bg='white').grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")
        expenses_entry = tk.Entry(apply_credit_card_frame, width=30)  # Increased width
        expenses_entry.grid(row=6, column=1, padx=5, pady=5)

        submit_card_button = tk.Button(apply_credit_card_frame, text="Apply", bg='yellow', fg='black', command=lambda: self.submit_card_application(user['account_number'], income_entry.get(), address_entry.get(), expenses_entry.get()))
        submit_card_button.grid(row=7, column=1, pady=20)

        # Change PIN Frame
        change_pin_frame = tk.Frame(scrollable_frame, **frame_style)
        change_pin_frame.pack(pady=10, padx=20, fill='x')

        # Add Title to Frame
        tk.Label(change_pin_frame, text="Change PIN", font=('Arial', 14, 'bold'), bg='white', anchor='w').grid(row=0, column=0, columnspan=3, pady=10,padx=10, sticky="w")

        tk.Label(change_pin_frame, text="Current PIN:", font=('Arial', 12), bg='white').grid(row=1, column=0, pady=10)
        current_pin_entry = tk.Entry(change_pin_frame, width=30, show="*")  # Increased width
        current_pin_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(change_pin_frame, text="New PIN:", font=('Arial', 12), bg='white').grid(row=2, column=0, pady=10)
        new_pin_entry = tk.Entry(change_pin_frame, width=30, show="*")  # Increased width
        new_pin_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(change_pin_frame, text="Confirm New PIN:", font=('Arial', 12), bg='white').grid(row=3, column=0, pady=10)
        confirm_pin_entry = tk.Entry(change_pin_frame, width=30, show="*")  # Increased width
        confirm_pin_entry.grid(row=3, column=1, padx=5, pady=5)

        change_pin_button = tk.Button(change_pin_frame, text="Change PIN", bg='orange', fg='black', command=lambda: self.change_pin(user['account_number'], current_pin_entry.get(), new_pin_entry.get(), confirm_pin_entry.get()))
        change_pin_button.grid(row=4, column=1, pady=20)

        # Logout Button
        logout_button = tk.Button(self.root, text="Logout", font=('Arial', 12), bg='red', fg='white', command=self.setup_login_page)
        logout_button.pack(side='bottom', pady=10)

        # Update scrollable region
        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def submit_card_application(self, account_number, income, address, expenses):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO credit_card_applications (account_number, income, address, expenses) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (account_number, income, address, expenses))
            self.connection.commit()

            messagebox.showinfo("Application Submitted", "Your credit card application has been submitted.")
            self.open_dashboard({'account_number': account_number})  # Return to dashboard
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
    
    def view_details(self, account_number):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE account_number = %s"
            cursor.execute(query, (account_number,))
            user = cursor.fetchone()

            if user:
                details = f"Name: {user['name']}\nAccount Number: {user['account_number']}\nEmail: {user['email']}\nBalance: ₹{user['balance']}\n"
                messagebox.showinfo("Account Details", details)
            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def credit_debit(self, account_number, amount, transaction_type):
        try:
            amount = float(amount)
            cursor = self.connection.cursor()
            if transaction_type == 'credit':
                query = "UPDATE users SET balance = balance + %s WHERE account_number = %s"
                cursor.execute(query, (amount, account_number))
            elif transaction_type == 'debit':
                query = "UPDATE users SET balance = balance - %s WHERE account_number = %s"
                cursor.execute(query, (amount, account_number))

            self.connection.commit()

            # Update balance in dashboard after transaction
            self.update_balance_label(account_number)
            messagebox.showinfo("Transaction Successful", f"{transaction_type.capitalize()} of ₹{amount} successful!")
            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")

    def transfer_money(self, sender_account, recipient_account, amount, recipient_entry=None, transfer_amount_entry=None):
        try:
            amount = float(amount)
            cursor = self.connection.cursor(dictionary=True)

            # Check if recipient account exists
            query = "SELECT * FROM users WHERE account_number = %s"
            cursor.execute(query, (recipient_account,))
            recipient = cursor.fetchone()

            if not recipient:
                messagebox.showerror("Recipient Error", "Recipient account does not exist.")
                return

            # Check if sender has sufficient balance
            query = "SELECT balance FROM users WHERE account_number = %s"
            cursor.execute(query, (sender_account,))
            sender_balance = cursor.fetchone()

            if sender_balance and sender_balance['balance'] >= amount:
                # Deduct from sender
                query = "UPDATE users SET balance = balance - %s WHERE account_number = %s"
                cursor.execute(query, (amount, sender_account))

                # Add to recipient
                query = "UPDATE users SET balance = balance + %s WHERE account_number = %s"
                cursor.execute(query, (amount, recipient_account))

                self.connection.commit()

                # Update the sender's balance in the dashboard
                self.update_balance_label(sender_account)

                # Clear the entry fields after the operation
                if recipient_entry:
                    recipient_entry.delete(0, tk.END)
                if transfer_amount_entry:
                    transfer_amount_entry.delete(0, tk.END)

                messagebox.showinfo("Transfer Successful", f"₹{amount} transferred to account {recipient_account}")
            else:
                messagebox.showerror("Insufficient Funds", "You have insufficient balance to make this transfer.")
            
            # Explicitly refresh the dashboard or balance label
            self.update_balance_label(sender_account)

            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid transfer details.")
    
    #try to display transaction history
    def view_transaction_history(self, account_number):
        """Fetch and display the complete transaction history for the logged-in user."""
        try:
            # Fetch all transactions for the logged-in user (as sender or recipient)
            cursor = self.connection.cursor(dictionary=True)
            query = """
            SELECT 
                transaction_id,
                sender_account,
                recipient_account,
                amount,
                transaction_type,
                transaction_date
            FROM transactions
            WHERE sender_account = %s OR recipient_account = %s
            ORDER BY transaction_date DESC
            """
            cursor.execute(query, (account_number, account_number))
            transactions = cursor.fetchall()
            cursor.close()

            # Create a new window for transaction history
            history_window = tk.Toplevel(self.root)
            history_window.title("Transaction History")
            history_window.geometry("800x500")

            # Title
            tk.Label(history_window, text="Transaction History", font=('Arial', 16, 'bold')).pack(pady=10)

            # Frame for list and scrollbar
            list_frame = tk.Frame(history_window)
            list_frame.pack(fill='both', expand=True, padx=10, pady=10)

            # Scrollbar for the Listbox
            scrollbar = tk.Scrollbar(list_frame, orient="vertical")
            scrollbar.pack(side="right", fill="y")

            # Listbox to display transactions
            transaction_list = tk.Listbox(
                list_frame, 
                yscrollcommand=scrollbar.set, 
                font=('Arial', 12), 
                width=100, 
                height=20
            )
            transaction_list.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=transaction_list.yview)

            # Populate the Listbox with transaction details
            if transactions:
                for transaction in transactions:
                    transaction_id = transaction['transaction_id']
                    sender = transaction['sender_account']
                    recipient = transaction['recipient_account']
                    amount = transaction['amount']
                    t_type = transaction['transaction_type'].capitalize()
                    date = transaction['transaction_date'].strftime("%Y-%m-%d %H:%M:%S")

                    # Determine the appropriate description for the transaction
                    if t_type == "Transfer":
                        if account_number == sender:
                            transaction_text = (
                                f"ID: {transaction_id} | {date} | {t_type}: Sent ₹{amount:.2f} to {recipient}"
                            )
                        else:
                            transaction_text = (
                                f"ID: {transaction_id} | {date} | {t_type}: Received ₹{amount:.2f} from {sender}"
                            )
                    elif t_type == "Credit":
                        transaction_text = f"ID: {transaction_id} | {date} | {t_type}: Credited ₹{amount:.2f}"
                    elif t_type == "Debit":
                        transaction_text = f"ID: {transaction_id} | {date} | {t_type}: Debited ₹{amount:.2f}"

                    # Add the transaction to the Listbox
                    transaction_list.insert(tk.END, transaction_text)
            else:
                transaction_list.insert(tk.END, "No transaction history available.")

            # Close Button
            tk.Button(history_window, text="Close", command=history_window.destroy).pack(pady=10)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
    
    def apply_for_card(self, account_number):
        self.clear_frame()
        apply_frame = tk.Frame(self.root, bg='white', relief='groove', borderwidth=2)
        apply_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=300)

        tk.Label(apply_frame, text="Apply for Credit Card", font=('Arial', 18, 'bold'), bg='white').pack(pady=10)
        tk.Label(apply_frame, text="Income (₹):", bg='white').pack(pady=5)
        income_entry = tk.Entry(apply_frame)
        income_entry.pack(pady=5)

        tk.Label(apply_frame, text="Current Address:", bg='white').pack(pady=5)
        address_entry = tk.Entry(apply_frame)
        address_entry.pack(pady=5)

        tk.Label(apply_frame, text="Annual Expenses (₹):", bg='white').pack(pady=5)
        expenses_entry = tk.Entry(apply_frame)
        expenses_entry.pack(pady=5)

        submit_button = tk.Button(apply_frame, text="Submit", command=lambda: self.submit_card_application(account_number, income_entry.get(), address_entry.get(), expenses_entry.get()))
        submit_button.pack(pady=10)

    def submit_card_application(self, account_number, income, address, expenses):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO credit_card_applications (account_number, income, address, expenses) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (account_number, income, address, expenses))
            self.connection.commit()

            messagebox.showinfo("Application Submitted", "Your credit card application has been submitted.")
            self.open_dashboard({'account_number': account_number})  # Return to dashboard
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def change_pin(self, account_number):
        self.clear_frame()
        change_pin_frame = tk.Frame(self.root, bg='white', relief='groove', borderwidth=2)
        change_pin_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=300)

        tk.Label(change_pin_frame, text="Change PIN", font=('Arial', 18, 'bold'), bg='white').pack(pady=10)
        tk.Label(change_pin_frame, text="Account Number:", bg='white').pack(pady=5)
        account_entry = tk.Entry(change_pin_frame)
        account_entry.pack(pady=5)

        tk.Label(change_pin_frame, text="Current PIN:", bg='white').pack(pady=5)
        current_pin_entry = tk.Entry(change_pin_frame, show='*')
        current_pin_entry.pack(pady=5)

        tk.Label(change_pin_frame, text="New PIN:", bg='white').pack(pady=5)
        new_pin_entry = tk.Entry(change_pin_frame, show='*')
        new_pin_entry.pack(pady=5)

        tk.Label(change_pin_frame, text="Confirm New PIN:", bg='white').pack(pady=5)
        confirm_pin_entry = tk.Entry(change_pin_frame, show='*')
        confirm_pin_entry.pack(pady=5)

        submit_button = tk.Button(change_pin_frame, text="Submit", command=lambda: self.submit_pin_change(account_entry.get(), current_pin_entry.get(), new_pin_entry.get(), confirm_pin_entry.get()))
        submit_button.pack(pady=10)

    def submit_pin_change(self, account_number, current_pin, new_pin, confirm_pin):
        if new_pin != confirm_pin:
            messagebox.showerror("PIN Mismatch", "New PIN and Confirm PIN do not match.")
            return

        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM users WHERE account_number = %s AND password = %s"
            cursor.execute(query, (account_number, current_pin))
            user = cursor.fetchone()

            if user:
                update_query = "UPDATE users SET password = %s WHERE account_number = %s"
                cursor.execute(update_query, (new_pin, account_number))
                self.connection.commit()

                messagebox.showinfo("PIN Changed", "Your PIN has been updated successfully.")
                self.setup_login_page()  # Go back to login page after successful change
            else:
                messagebox.showerror("Incorrect PIN", "Current PIN is incorrect.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))


def main():
    root = tk.Tk()
    app = BankManagementSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()