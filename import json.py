import json
import hashlib

class Account:
    def __init__(self, account_number, name, password, balance=0.0):
        self.account_number = account_number
        self.name = name
        self.password_hash = self.hash_password(password)
        self.balance = balance
        self.transactions = []
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        return self.hash_password(password) == self.password_hash
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposited: ${amount}")
            print("Deposit successful!")
        else:
            print("Invalid deposit amount.")
    
    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.transactions.append(f"Withdrawn: ${amount}")
            print("Withdrawal successful!")
        else:
            print("Insufficient funds or invalid amount.")
    
    def get_transaction_history(self):
        return self.transactions if self.transactions else ["No transactions yet."]

class Bank:
    def __init__(self, filename='bank_data.json'):
        self.filename = filename
        self.load_data()
    
    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                self.accounts = {acc: Account(**details) for acc, details in data.items()}
        except FileNotFoundError:
            self.accounts = {}
    
    def save_data(self):
        data = {acc: self.accounts[acc].__dict__ for acc in self.accounts}
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)
    
    def create_account(self, name, password):
        account_number = str(len(self.accounts) + 1).zfill(6)
        self.accounts[account_number] = Account(account_number, name, password)
        self.save_data()
        print(f"Account created successfully! Your account number is {account_number}")
    
    def authenticate(self, account_number, password):
        account = self.accounts.get(account_number)
        if account and account.verify_password(password):
            return account
        else:
            print("Invalid credentials.")
            return None

def main():
    bank = Bank()
    while True:
        print("\n1. Create Account\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter your name: ")
            password = input("Set your password: ")
            bank.create_account(name, password)
        
        elif choice == '2':
            account_number = input("Enter account number: ")
            password = input("Enter password: ")
            account = bank.authenticate(account_number, password)
            if account:
                while True:
                    print("\n1. View Balance\n2. Deposit\n3. Withdraw\n4. Transaction History\n5. Logout")
                    option = input("Enter your choice: ")
                    if option == '1':
                        print(f"Current Balance: ${account.balance}")
                    elif option == '2':
                        amount = float(input("Enter deposit amount: "))
                        account.deposit(amount)
                        bank.save_data()
                    elif option == '3':
                        amount = float(input("Enter withdrawal amount: "))
                        account.withdraw(amount)
                        bank.save_data()
                    elif option == '4':
                        print("Transaction History:")
                        for tx in account.get_transaction_history():
                            print(tx)
                    elif option == '5':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid option.")
        
        elif choice == '3':
            print("Exiting... Thank you!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
