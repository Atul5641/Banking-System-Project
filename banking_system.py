import random
import re
from datetime import datetime

global conn, my_cursor  # Declare the global variables

import mysql.connector

# Establishing the connection to the database
conn = mysql.connector.connect(host='localhost', username='root', password='Atul@5641', database='banking_system')
my_cursor = conn.cursor()
conn.commit()

print("Connection successfully created!\n")
print("#=======================================================================================================#\n")
print("#=======================================================================================================#\n")

# List to store user data
users = []

# Function to generate a random 10-digit unique account number
def generate_account_number():
    return random.randint(1000000000, 9999999999)

# Function to validate password (at least 8 characters, contains a number and special character)
def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"\d", password):  # Check for digits
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # Check for special characters
        return False
    return True

# Function to validate contact number (should be 10 digits)
def validate_contact(contact):
    if len(contact) == 10 and contact.isdigit():
        return True
    return False

# Function to validate email (basic validation)
def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

# Function to add a user to the system
def add_user():
    print("#=======================================================================================================#\n")
    print("Enter the following details to create a new account:")

    # Taking user input
    name = input("Name: ")
    dob = input("Date of Birth (YYYY-MM-DD): ")
    city = input("City: ")

    # Generate a random 10-digit account number
    account_number = generate_account_number()

    # Validate password
    password = input("Password (min 8 characters, including number and special character): ")
    while not validate_password(password):
        print("Password must be at least 8 characters, contain a number, and a special character.")
        password = input("Password: ")

    # Validate initial balance (minimum 500)
    balance = float(input("Initial Balance (min 2000): "))
    while balance < 2000:
        print("Initial balance must be at least 2000.")
        balance = float(input("Initial Balance: "))

    # Validate contact number
    contact = input("Contact Number (10 digits): ")
    while not validate_contact(contact):
        print("Contact number must be 10 digits.")
        contact = input("Contact Number: ")

    # Validate email
    email = input("Email: ")
    while not validate_email(email):
        print("Invalid email format.")
        email = input("Email: ")

    # Address input
    address = input("Address: ")

    try:
        # Insert into users table
        user_query = """
        INSERT INTO users (name, dob, city, contact, email, address, account_number, balance, active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        user_data = (name, dob, city, contact, email, address, account_number, balance, True)
        my_cursor.execute(user_query, user_data)

        # Insert into login table
        login_query = "INSERT INTO login (account_number, password) VALUES (%s, %s)"
        login_data = (account_number, password)
        my_cursor.execute(login_query, login_data)

        conn.commit()  # Save changes to the database
        

        
        # Add user data to the users list
        users.append({
            'name': name,
            'dob': dob,
            'city': city,
            'contact': contact,
            'email': email,
            'address': address,
            'account_number': account_number,
            'balance': balance,
            'password': password,
            'active': True,
            'transactions': [],
            'previous_passwords': [password]
        })

        print("#=======================================================================================================#\n")
        print("\nUser Created Successfully!\n")
        print("Account Number:", account_number)
        print("Name:", name)
    except Exception as e:
        print("\nError saving user data:", str(e))
        conn.rollback()  # Undo changes if there’s an error

# Function to show user details based on account number
def show_user():
    account_number = input("\nEnter Account Number to view details: ")
    found = False

    for user in users:
        if str(user['account_number']) == account_number:
            print("#=======================================================================================================#\n")
            print("\nUser Details:")
            print("Name:", user['name'])
            print("Date of Birth:", user['dob'])
            print("City:", user['city'])
            print("Account Number:", user['account_number'])
            print("Balance:", user['balance'])
            print("Contact:", user['contact'])
            print("Email:", user['email'])
            print("Address:", user['address'])
            found = True
            break

    if not found:
        print("No user found with that account number.")

# Function to login a user based on account number and password
def login():
    print("#=======================================================================================================#\n")
    account_number = input("\nEnter Account Number: ")
    password = input("Enter Password: ")

    # Check if the account exists and the password matches
    for user in users:
        if str(user['account_number']) == account_number and user['password'] == password:
            print("\nLogin Successful!")
            print("Welcome, " + user['name'])
            return user  # Return the logged-in user's details
    print("Invalid account number or password. Please try again.")
    return None

# Function to show balance
def show_balance(user):
    if not user['active']:
        print("\nAccount is deactivated. You cannot view balance while your account is inactive.")
    else:
        print(f"\nYour Current Balance: {user['balance']}")

# Function to show transaction history
def show_transactions(user):
    if not user['active']:
        print("\nAccount is deactivated. You cannot view transaction history while your account is inactive.")
    else:
        if user['transactions']:
            print("\nTransaction History:\n")
            for transaction in user['transactions']:
                print(transaction)
        else:
            print("\nNo transactions yet.\n")

# Function to credit amount (deposit)def credit_amount(user):
def credit_amount(user):
    global conn, my_cursor  # Declare the global variables

    if not user['active']:
        print("\nAccount is deactivated. You cannot perform transactions while your account is inactive.")
        return

    amount = float(input("Enter amount to deposit: "))
    if amount > 0:
        user['balance'] += amount
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            my_cursor.execute(
                "INSERT INTO transactions (account_number, transaction_type, amount, timestamp, description) VALUES (%s, %s, %s, %s, %s)",
                (user['account_number'], 'credit', amount, timestamp, 'Deposit')
            )
            conn.commit()
            print(f"\n{amount} credited to your account.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    else:
        print("Amount must be positive.")

        print("Amount must be positive.")


        # Save transaction to the database
        try:
            my_cursor.execute(
                "INSERT INTO transactions (account_number, transaction_type, amount, timestamp, description) VALUES (%s, %s, %s, %s, %s)",
                (user['account_number'], 'credit', amount, timestamp, 'Deposit')
            )
            conn.commit()
            print(f"\n{amount} credited to your account.\n")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        else:
         print("Amount must be positive.")


# Function to debit amount (withdraw)
def debit_amount(user):
    global conn, my_cursor  # Declare global variables for db and cursor

    if not user['active']:
        print("\nAccount is deactivated. You cannot perform transactions while your account is inactive.\n")
        return

    # Get the amount to withdraw
    amount = float(input("Enter amount to withdraw: "))
    
    # Check if the amount is valid (greater than zero and less than or equal to the balance)
    if amount > 0 and amount <= user['balance']:
        user['balance'] -= amount  # Deduct the amount from the user's balance
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current timestamp

        # Insert the transaction into the transaction table in the database
        try:
            my_cursor.execute(
                "INSERT INTO transactions (account_number, transaction_type, amount, timestamp, description) VALUES (%s, %s, %s, %s, %s)",
                (user['account_number'], 'debit', amount, timestamp, 'Withdrawal')
            )
            conn.commit()  # Commit the transaction to the database

            # Update the user's transaction history (if you are maintaining it in a list)
            user['transactions'].append(f"{timestamp} - Debited: {amount}")

            print(f"\n{amount} debited from your account.\n")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    else:
        print("Invalid amount or insufficient balance.")


# Function to transfer amount to another account
def transfer_amount(user):
    global conn, my_cursor  # Declare global variables for db and cursor

    if not user['active']:
        print("\nAccount is deactivated. You cannot perform transactions while your account is inactive.\n")
        return

    # Ensure the recipient account number is valid (10 digits)
    transfer_to = input("Enter the recipient's 10-digit account number: ")
    while len(transfer_to) != 10 or not transfer_to.isdigit():
        print("The account number must be exactly 10 digits.")
        transfer_to = input("Enter the recipient's 10-digit account number: ")

    # Validate transfer amount
    amount = float(input("Enter amount to transfer: "))

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    if amount > user['balance']:
        print("Insufficient balance.")
        return

    # Find the recipient user
    recipient = None
    for u in users:
        if str(u['account_number']) == transfer_to:
            recipient = u
            break

    if recipient:
        # Deduct from sender's balance and add to recipient's balance
        user['balance'] -= amount
        recipient['balance'] += amount

        # Get the current timestamp for the transaction
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save the transaction to the database for the sender
        try:
            my_cursor.execute(
                "INSERT INTO transactions (account_number, transaction_type, amount, timestamp, description) VALUES (%s, %s, %s, %s, %s)",
                (user['account_number'], 'debit', amount, timestamp, f'Transferred to Account {transfer_to}')
            )
            conn.commit()  # Commit the transaction for the sender

            # Save the transaction for the recipient
            my_cursor.execute(
                "INSERT INTO transactions (account_number, transaction_type, amount, timestamp, description) VALUES (%s, %s, %s, %s, %s)",
                (recipient['account_number'], 'credit', amount, timestamp, f'Received from Account {user["account_number"]}')
            )
            conn.commit()  # Commit the transaction for the recipient

            # Update both sender and recipient transaction history
            user['transactions'].append(f"{timestamp} - Transferred: {amount} to Account {transfer_to}")
            recipient['transactions'].append(f"{timestamp} - Received: {amount} from Account {user['account_number']}")

            print(f"\n{amount} successfully transferred to account {transfer_to}.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    else:
        print("Recipient account not found.\n")


# Function to change password
def change_password(user):
    if not user['active']:
        print("\nAccount is deactivated. You cannot change the password while your account is inactive.\n")
    else:
        # Check if the new password is one of the last three passwords
        new_password = input("Enter new password (min 8 characters, including number and special character): ")
        
        # Ensure the password is not one of the last three passwords
        while not validate_password(new_password) or new_password in user['previous_passwords']:
            if new_password in user['previous_passwords']:
                print("You cannot reuse any of your last three passwords. Please choose a new password.")
            else:
                print("Password must be at least 8 characters, contain a number, and a special character.")
            new_password = input("New Password: ")
        
        # Add the new password to the list of previous passwords
        if len(user['previous_passwords']) >= 3:
            user['previous_passwords'].pop(0)  # Remove the oldest password if there are 3 previous ones
        user['previous_passwords'].append(user['password'])  # Store the current password in the history
        user['password'] = new_password  # Update the password

        print("Password has been successfully changed.")
        print("#=======================================================================================================#\n")


# Function to update profile details
def update_profile(user):
    if not user['active']:
        print("\nAccount is deactivated. You cannot update the profile while your account is inactive.")
    else:
        print("#=======================================================================================================#\n")
        print("\nUpdate your profile details:")
        print("1. Update Name")
        print("2. Update Contact Number")
        print("3. Update Email")
        print("4. Update Address")
        print("5. Go Back")

        choice = input("\nEnter the number of the detail you want to update: ")

        if choice == '1':
            user['name'] = input(f"Enter new Name (Current: {user['name']}): ") or user['name']
            print(f"Name updated to {user['name']}.")

        elif choice == '2':
            new_contact = input(f"Enter new Contact Number (Current: {user['contact']}): ") or user['contact']
            while not validate_contact(new_contact):
                print("Contact number must be 10 digits.")
                new_contact = input("Enter new Contact Number: ")
            user['contact'] = new_contact
            print(f"Contact Number updated to {user['contact']}.")

        elif choice == '3':
            new_email = input(f"Enter new Email (Current: {user['email']}): ") or user['email']
            while not validate_email(new_email):
                print("Invalid email format.")
                new_email = input("Enter new Email: ")
            user['email'] = new_email
            print(f"Email updated to {user['email']}.")

        elif choice == '4':
            user['address'] = input(f"Enter new Address (Current: {user['address']}): ") or user['address']
            print(f"Address updated to {user['address']}.")

        elif choice == '5':
            print("Going back to the previous menu.")

        else:
            print("Invalid choice! Please try again.")

# Function to activate or deactivate account
def activate_deativate_account_status(user):
    if user['active']:
        action = input(f"Your account is currently active. Do you want to deactivate your account? (y/n): ")
        if action.lower() == 'y':
            user['active'] = False
            print("Your account has been deactivated.")
        else:
            print("No changes made.")
    else:
        action = input(f"Your account is currently deactivated. Do you want to activate your account? (y/n): ")
        if action.lower() == 'y':
            user['active'] = True
            print("Your account has been activated.")
        else:
            print("No changes made.")

# Main loop to interact with the user
def main():
  
    global conn, my_cursor  # Ensure globals are accessible here too
    
    print("Welcome to the Banking System\n")
    print("#=======================================================================================================#\n")

    logged_in_user = None  # To keep track of the logged-in user

    while True:
        if logged_in_user:
            print("#=======================================================================================================#\n")
            print("\nLogged in as:", logged_in_user['name'])
            print("1. Show Balance")
            print("2. Show Transactions")
            print("3. Credit Amount")
            print("4. Debit Amount")
            print("5. Transfer Amount")
            print("6. Change Password")
            print("7. Update Profile")
            print("8. Activate/Deactivate Account")
            print("9. Log Out")
            print("10. Exit")

            choice = input("\nEnter your choice: ")

            if choice == '1':
                show_balance(logged_in_user)

            elif choice == '2':
                show_transactions(logged_in_user)

            elif choice == '3':
                credit_amount(logged_in_user)

            elif choice == '4':
                debit_amount(logged_in_user)

            elif choice == '5':
                transfer_amount(logged_in_user)

            elif choice == '6':
                change_password(logged_in_user)

            elif choice == '7':
                update_profile(logged_in_user)

            elif choice == '8':
                activate_deativate_account_status(logged_in_user)

            elif choice == '9':
                print("Logging out...")
                logged_in_user = None

            elif choice == '10':
                print("Exiting the system. Goodbye!\n")
                print("#=======================================================================================================#\n")
                break

            else:
                print("Invalid choice. Please try again.")
        else:
            print("#=======================================================================================================#\n")
            print("\n1. Add New User")
            print("2. Log In")
            print("3. Show User")
            print("4. Exit")

            choice = input("\nEnter your choice: ")

            if choice == '1':
                add_user()

            elif choice == '2':
                logged_in_user = login()

            elif choice == '3':
                show_user()

            elif choice == '4':
                print("Exiting the system. Goodbye!\n")
                print("#=======================================================================================================#\n")

                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
