#########################################
#TshewangTashi
#Electronics and communications engineering
#02230115
##########################################
#REFERENCES
#https://www.geeksforgeeks.org/python-programming-language/
############################################


import random
import os
import time

# Define Account class for Bank Account
class Account:
    # Initialize the account with properties like account number, password, type, and balance
    def __init__(self, account_Number, password, account_Type, balance=0):
        self.a = account_Number
        self.p = password
        self.at = account_Type
        self.b = balance

    # This is a method for depositing given amount to the account balance
    def deposit(self, amount):
        if amount > 0:
            self.b += amount # increase balance everytime when credited by amount credited
            print("Processing deposit...")
            time.sleep(2)  # Simulate loading time
            print(f"Your account {self.a} has been Credited with Nu.{amount}. Available balance is Nu.{self.b}")#This will display the amount deposited
        else:
            print("Error Input") # If input given is invalid, this will display error message

    # define method withdraw for withdrawing money 
    def withdraw(self, amount):
        if 0 < amount <= self.b:#Checks whether there is enough balance in the account
            self.b -= amount #deduct balance everytime when debited by amount withdrawn
            print("Processing withdrawal...")
            time.sleep(2)  # Simulate loading time
            print(f"Your account {self.a} has been Debited with Nu.{amount}. Available balance is Nu.{self.b}")#This will display the amount debited
        else:
            print("Insufficient Balance")#If balance is not enough, this message will be displayed
     
     # define method to check current available balance
    def check_balance(self):
        print("Checking balance...")
        time.sleep(1)  # Simulate loading time
        print(f"Your Available balance is {self.b}")

    # This block of code will save account details to a text file for future use
    def save_to_file(self):
        with open('accounts.txt', 'a') as file:
            file.write(f"{self.a},{self.p},{self.at},{self.b}\n")#It updates the file

# create class derived from Account class for Personal Account
class PersonalAccount(Account):
    # Personal account properties are constructed by inherting from Account class
    def __init__(self, a, p, b=0):
        super().__init__(a, p, 'Personal', b)

# It is another class derived from Account class for Business Account
class BusinessAccount(Account):
    # As same as personal account, business account properties are constructed by inherting from Account class
    def __init__(self, a, p, b=0):
        super().__init__(a, p, 'Business', b)

# This function is for generating a random account number and password
def generate_account_details():
    # Generate a random 5-digit account number and a default 4-digit password
    a = random.randint(10000, 99999)
    p = random.randint(1000, 9999)
    return a, p

# Function to open new account
def open_account(at):
    # Generate account number and password
    a, p = generate_account_details()
    # Option for a new personal or bussiness account 
    if at == 'Personal':
        account = PersonalAccount(a, p)
    elif at == 'Business':
        account = BusinessAccount(a, p)
    else:
        print("Invalid account type")#Message for invalid input
        return None

    account.save_to_file()     # Save the account details to file
    print(f"Account created. Account number: {a}, MPIN: {p}")
    return account

# Function to read txt file 
def load_accounts():
    #data from txt file will be extracted and storedd in the account variable declared below in the form of nested dictionary
    accounts = {}
    # Check if the accounts file exists
    if os.path.exists('accounts.txt'):
        with open('accounts.txt', 'r') as file: # Read each line and create account objects
            for line in file:
                a, p, at, b = line.strip().split(',')
                if at == 'Personal':
                    accounts[a] = PersonalAccount(a, p, float(b))
                elif at == 'Business':
                    accounts[a] = BusinessAccount(a, p, float(b))
    return accounts

# Function for logging in to an account
def login(a, p, accounts):
    account = accounts.get(a) 
    # Checks if the account number and password matches the one in the file
    if account and account.p == p:
        print("Logging in...")
        time.sleep(2)  # Simulate loading time
        print(f"Login successful for account number {a}")#If it matches, it successfuly logs in and this message will be displayed
        return account
    else:
        print("Invalid account number or MPIN")#Message to display for unsuccessful login
        return None

# Function for fund transfer
def send_money(sender, receiver_account_number, amount, accounts):
    # Check if the receiver account exists
    if receiver_account_number in accounts:
        # Check if the sender has sufficient balance
        if sender.b >= amount:
            print("Processing transaction...")
            time.sleep(3)  # Simulate loading time
            sender.withdraw(amount)
            receiver = accounts[receiver_account_number]
            receiver.deposit(amount)
            print(f"Transferred Nu.{amount} to account number {receiver_account_number}")#Message to display to whom the money was tranferred
        else:
            print("Insufficient funds")#If the balance is not suufficient, this error messahe will be displayed
    else:
        print("Receiver account does not exist")#This message is for non existing bank account

# This a main function for running the application
def main():
    # Load existing accounts from txt file
    accounts = load_accounts()

    while True:
        # Option for user to choose(main menu)
        print("\n1. Open Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")#Users will imput their choice here

        if choice == '1':#For option 1, new account will be opened
            at = input("Account type you wish to OPEN (Personal/Business): ")
            open_account(at)
        elif choice == '2':
            # For option 2 , it prompt login details and authenticate the user
            a = input("Enter account number: ")
            p = input("Enter MPIN: ")
            account = login(a, p, accounts)

            if account:#If login is successful, it goe in the main loop
                while True:
                    # Option for user to choose in their account
                    print("\n1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Send Money")
                    print("5. Delete Account")
                    print("6. Logout")
                    sub_choice = input("Enter your choice: ")

                    if sub_choice == '1':
                        # choice 1 checks and display account balance
                        account.check_balance()
                    elif sub_choice == '2':
                        # choice 2 prompt for deposit amount and add to balance
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                    elif sub_choice == '3':
                        # Prompt for withdrawal amount and deduct from balance
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                    elif sub_choice == '4':
                        # Prompt for receiver account and amount, then send money
                        receiver_account_number = input("Enter valid receiver account number: ")
                        amount = float(input("Enter amount to transfer: "))
                        send_money(account, receiver_account_number, amount, accounts)
                    elif sub_choice == '5':
                        # Deletes the logged-in account from records
                        accounts.pop(account.a)
                        print("Deleting account...")
                        time.sleep(2)  # Simulate loading time
                        print(f"Account {account.a} deleted")
                        break
                    elif sub_choice == '6':
                        # Logout and return to the main menu
                        print("Logging out...")
                        time.sleep(1)  # Simulate loading time
                        print("Logged out")
                        break
                    else:
                        print("Invalid choice")
        elif choice == '3':
            # Exit the application
            print("Exiting application...")
            time.sleep(1)  # Simulate loading time
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    #main function called for running the application
    main()
