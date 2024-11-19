import mysql.connector
from tkinter import *
from tkinter import messagebox

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="root",  # Replace with your MySQL password
    database="BankSystem"
)
cursor = conn.cursor()

# Global variable for logged-in user
logged_in_user = None

# Function to handle user login
def login():
    global logged_in_user
    username = entry_username.get()
    password = entry_password.get()

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        logged_in_user = username
        messagebox.showinfo("Login Successful", f"Welcome {username}")
        main_window.destroy()  # Close login window
        app_window()  # Open the dashboard window
    else:
        if not username or not password:
            messagebox.showerror("Error", "Fields cannot be empty.")
        else:
            # Register the new user
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            messagebox.showinfo("User Created", f"Account created for {username}")
            logged_in_user = username
            main_window.destroy()
            app_window()

# Function to handle amount credit
def credit_amount():
    try:
        amount = float(entry_amount.get())
        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than 0.")
            return

        cursor.execute("UPDATE users SET balance = balance + %s WHERE username=%s", (amount, logged_in_user))
        conn.commit()
        messagebox.showinfo("Success", f"₹{amount} credited to your account.")
        entry_amount.delete(0, END)
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered.")

# Function to handle amount debit
def debit_amount():
    try:
        amount = float(entry_amount.get())
        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than 0.")
            return

        cursor.execute("SELECT balance FROM users WHERE username=%s", (logged_in_user,))
        balance = cursor.fetchone()[0]

        if amount > balance:
            messagebox.showerror("Error", "Insufficient balance.")
        else:
            cursor.execute("UPDATE users SET balance = balance - %s WHERE username=%s", (amount, logged_in_user))
            conn.commit()
            messagebox.showinfo("Success", f"₹{amount} debited from your account.")
        entry_amount.delete(0, END)
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered.")

# Function to display user credentials
def display_credentials():
    cursor.execute("SELECT * FROM users WHERE username=%s", (logged_in_user,))
    user = cursor.fetchone()
    messagebox.showinfo(
        "User Details",
        f"Username: {user[1]}\nPassword: {user[2]}\nBalance: ₹{user[3]:.2f}"
    )

# Login window
def create_main_window():
    global main_window, entry_username, entry_password
    main_window = Tk()
    main_window.title("Bank Management System - Login")
    main_window.configure(bg="skyblue")
    
    Label(main_window, text="Username",font=("Arial", 12, "bold"), bg="skyblue").grid(row=0, column=0, padx=10, pady=10)
    entry_username = Entry(main_window)
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    Label(main_window, text="Password",font=("Arial", 12, "bold"), bg="skyblue").grid(row=1, column=0, padx=10, pady=10)
    entry_password = Entry(main_window, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    Button(main_window, text="Login/Register", command=login).grid(row=2, column=0, columnspan=2, pady=10)

    main_window.mainloop()

# Dashboard window
def app_window():
    global entry_amount
    app = Tk()
    app.title("Bank Management System - Dashboard")
    app.configure(bg="yellow")
    
    Label(app, text=f"Welcome, {logged_in_user}", font=("Arial", 16), bg="yellow").grid(row=0, column=0, columnspan=2, pady=10)

    Label(app, text="Enter Amount", font=("Arial", 12, "bold"), bg="yellow").grid(row=1, column=0, padx=10, pady=10)
    entry_amount = Entry(app)
    entry_amount.grid(row=1, column=1, padx=10, pady=10)

    Button(app, text="Credit Amount", command=credit_amount).grid(row=2, column=0, padx=10, pady=10)
    Button(app, text="Debit Amount", command=debit_amount).grid(row=2, column=1, padx=10, pady=10)
    Button(app, text="Display Credentials", command=display_credentials).grid(row=3, column=0, columnspan=2, pady=10)

    app.mainloop()

# Main function
if __name__ == "__main__":
    create_main_window()
