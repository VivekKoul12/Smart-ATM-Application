import json
from datetime import datetime


class FileManager:
    @staticmethod
    def read_data(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return {}

    @staticmethod
    def write_data(file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file)


class User:
    def __init__(self, bank, username, password, phone_number):
        self.bank = bank
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        self.bank.users[self.username]["balance"] = self.balance
        self.bank.save_data()
        return amount

    def withdraw(self, amount):
        if amount <= self.balance and self.balance - amount > 50000:
            self.balance -= amount
            self.bank.users[self.username]["balance"] = self.balance
            self.bank.save_data()
            return amount
        else:
            print("Minimum balace present cannot withdraw")
            return 0

    def check_balance(self):
        return self.balance


class Bank:
    def __init__(self):
        self.users_file = "users.json"
        self.admin_file = "admin.json"
        self.users = FileManager.read_data(self.users_file)
        self.admin = FileManager.read_data(self.admin_file)
        self.login_attempts = {}
        self.admin_credentials = {"admin": "admin", "password": "password"}

    def delete_user_account(self, username):
        if username in self.users:
            del self.users[username]
            self.save_data()
            print(f"User '{username}' account deleted successfully.")
        else:
            print(f"User '{username}' not found.")

    def get_total_balance(self):
        total_balance = sum(user["balance"] for user in self.users.values())
        return total_balance

    def save_data(self):
        FileManager.write_data(self.users_file, self.users)
        FileManager.write_data(self.admin_file, self.admin)

    def login(self, username, password, role):
        if role == "user" and username in self.users:
            if self.login_attempts.get(username, 0) >= 3:
                print(
                    f"Account for user {username} is locked. Contact admin for support.")
                return False
            elif self.users[username]["password"] == password:
                self.login_attempts.pop(username, None)
                return True
            else:
                print("Incorrect password. Please try again(Note:Only 3 attempts).")
                self.login_attempts[username] = self.login_attempts.get(
                    username, 0) + 1
                if self.login_attempts[username] == 3:
                    print(
                        f"Too many unsuccessful login attempts for user {username}. Contact admin")
                return False
        elif role == "admin" and username == self.admin_credentials["admin"] and password == self.admin_credentials["password"]:
            return True
        else:
            return False

    def register_user(self, username, password, phone_number):
        if username not in self.users:
            self.users[username] = {"password": password,
                                    "phone_number": phone_number, "balance": 5000}
            self.save_data()
            return True
        else:
            print("Username already exists. Please choose another.")
            return False

    def reset_password(self, username, phone_number, new_password):
        if username in self.users and self.users[username]["phone_number"] == phone_number:
            self.users[username]["password"] = new_password
            self.login_attempts.pop(username, None)
            self.save_data()
            return True
        else:
            print("Invalid username or phone number. Password reset failed.")
            return False

    def change_password(self, username, current_password, new_password):
        if username in self.users and self.users[username]["password"] == current_password:
            self.users[username]["password"] = new_password
            self.login_attempts.pop(username, None)
            self.save_data()
            return True
        else:
            print("Invalid username or current password. Password change failed.")
            return False
  #Extra creativity
    def collect_feedback(self, username=None):
        print("Thank you for using the Smart ATM System!")
        feedback = input("Do you have any feedback? (yes/no): ").lower()

        if feedback == "yes":
            user_rating = int(input("Rate your experience (out of 5): "))
            user_comments = input("Enter your feedback: ")

            feedback_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "username": username if username else "unknown",
                "rating": user_rating,
                "comments": user_comments
            }

            with open("feedback.json", "a") as feedback_file:
                json.dump(feedback_data, feedback_file)
                feedback_file.write("\n")
                print("\t\t", "~" * 96)
            print("\t\t|", "\t\t\t\t*** THANKYOU FOR VISITING ***", "\t\t\t\t\t|")
            print("\t\t|\t", "\t\t\t\t\t\t\t\t\t\t\t|")
            print("\t\t", "~" * 96)
            print("\n\n\n\n")
            

def main():
    bank = Bank()

    while True:
        print("\t\t", "~" * 96)
        print("\t\t|", "\t\t\t\t*** WELCOME TO THE SMART ATM SYSTEM ***","\t\t\t|")
        print("\t\t|\t","\t\t\t\t\t\t\t\t\t\t\t|")
        print("\t\t", "~" * 96)
        

        print("1. User Login")
        print("2. Admin Login")
        print("3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            print("\t\t", "*" * 32)
            print("\t\t|", "\t--- User Section ---", "\t|")
            print("\t\t", "*" * 32)
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if bank.login(username, password, "user"):
                user_data = bank.users[username]
                user = User(
                    bank, username, user_data["password"], user_data["phone_number"])
                user.balance = user_data["balance"]
                while True:
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Change Password")
                    print("5. Logout")
                    user_choice = int(input("Enter your choice: "))
                    if user_choice == 1:
                        amount = int(
                            input("Enter the amount to deposit: $"))
                        if (amount <= 100000):
                            total_deposit = user.deposit(amount)
                            print(
                                f"Deposited ${total_deposit} successfully.")
                        else:
                            print("Amount should be less that 1L")
                    elif user_choice == 2:
                        amount = int(
                            input("Enter the amount to withdraw: $"))
                        if (amount <= 50000):
                            total_withdraw = user.withdraw(amount)
                            if total_withdraw == 0:
                                print("Insufficient balance.")
                            else:
                                print(
                                    f"Withdrew ${total_withdraw} successfully.")
                        else:
                            print("Amount should be less than 50k")
                    elif user_choice == 3:
                        balance = user.check_balance()
                        print(f"Current Balance: ${balance}")
                    elif user_choice == 4:
                        current_password = input(
                            "Enter current password: ")
                        new_password = input("Enter new password: ")
                        if bank.change_password(username, current_password, new_password):
                            print("Password changed successfully.")
                        else:
                            print("Incorrect current password.")
                    elif user_choice == 5:
                        bank.collect_feedback(username)
                        bank.save_data()
                        break
        elif choice == 2:
            print("\t\t", "*" * 32)
            print("\t\t|", "\t--- Admin Section ---", "\t|")
            print("\t\t", "*" * 32)
            admin_username = input("Enter admin username: ")
            admin_password = input("Enter admin password: ")
            if bank.login(admin_username, admin_password, "admin"):
                while True:
                    print("1. Total Balance")
                    print("2. Cash Deposit")
                    print("3. Register New User")
                    print("4. Reset Password")
                    print("5. Delete user account")
                    print("6. Logout")
                    admin_choice = int(input("Enter your choice: "))
                    if admin_choice == 1:
                        total_balance = bank.get_total_balance()
                        if total_balance < 75000:
                            print("Notification: Balance is less than $75,000.")
                        print(f"Total Balance: ${total_balance}")
                    elif admin_choice == 2:
                        username = input(
                            "Enter the username to deposit cash: $")
                        if username in bank.users:
                            user = bank.users[username]
                            current_balance = user.get("balance", 0)
                            amount_to_deposit = int(
                                input("Enter the amount to deposit:$ "))
                            if amount_to_deposit <= 300000:
                                user["balance"] = current_balance + amount_to_deposit
                                bank.save_data()
                                print(
                                    f"Deposited ${amount_to_deposit} into {username}'s account.")
                            else:
                                print(
                                    "Deposit exceeds the maximum limit (3 lakhs).")
                        else:
                            print("User not found.")
                    elif admin_choice == 4:
                        username = input("Enter username: ")
                        phone_number = input(
                            "Enter 10-digit phone number: ")
                        new_password = input("Enter new password: ")
                        if bank.reset_password(username, phone_number, new_password):
                            print("Password reset successfully.")
                    elif admin_choice == 3:
                        new_user = input("Enter a new username: ")
                        new_password = input("Enter a new password: ")
                        phone_number = input("Enter 10-digit phone number: ")
                        if len(phone_number) == 10 and phone_number.isdigit():
                            if bank.register_user(new_user, new_password, phone_number):
                                print(
                                    f"User {new_user} registered successfully.")
                            else:
                                print(
                                    "Username already exists. Please choose another.")
                        else:
                            print(
                                "Invalid phone number. Please enter a 10-digit number.")
                    elif admin_choice == 5:
                        username_to_delete = input(
                            "Enter username to delete: ")
                        bank.delete_user_account(username_to_delete)
                    elif admin_choice == 6:
                        bank.collect_feedback()
                        bank.save_data()
                        break
            else:
                print("Wrong id or password.")
        elif choice == 3:
            print("\t\t", "~" * 96)
            print("\t\t|", "\t\t\t\t*** THANKYOU FOR VISITING ***", "\t\t\t\t\t|")
            print("\t\t|\t", "\t\t\t\t\t\t\t\t\t\t\t|")
            print("\t\t", "~" * 96)
            bank.save_data()
            break

if __name__ == "__main__":
    main()
