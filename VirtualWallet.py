import os.path
import random
import sys 

FILE_NAME = "AllAccounts.csv"
ledger = {}

# line = 232323,0,0
def parseUserDetails(line):
    array = line.split(",")
    account_number = array[0]
    password = array[1]
    balance = int(array[2])
    user_details = {
        "account_number": account_number, 
        "password": password,
        "balance": balance
    }
    return user_details

#Reads accounts details from the drive
def readAccounts(FILE_NAME):
    if not os.path.isfile(FILE_NAME):
        return
    f = open(FILE_NAME, "r")
    lines_str = f.read()
    lines = lines_str.split("\n")
    for line in lines:
        user_details = parseUserDetails(line)
        account_number = user_details["account_number"]
        ledger[account_number] = user_details

#Adds an account, assigns a random account number while user inputs the password
def addAccount():
    user_details = {
        "account_number": str(random.randint(1, 10**6)), 
        "password": input("Choose a password please"),
        "balance": 0
    }
    account_number = user_details["account_number"]
    print('Your account number is', account_number)
    ledger[account_number] = user_details

#Shows balance of the account
def showBalance(user_details):
  print("Your balance is",user_details["balance"])

#Withdraws funds from the account
def withdraw(user_details):
  withdrawal_amount = int(input("How much do you want to withdraw"))
  user_details["balance"] = user_details["balance"] - withdrawal_amount
  print("Your balance is", user_details["balance"])

#Deposits funds to the account
def deposit(user_details):
  deposit_amount = int(input("How much do you want to deposit"))
  user_details["balance"] = user_details["balance"] + deposit_amount
  print("Your balance is", user_details["balance"])

#Prompts user for transaction
def promptForTransaction(user_details):
  user_transaction = input("Would you like to show balance, withdraw or deposit?")
  while user_transaction != "show balance" or user_transaction != "withdraw" or user_transaction != "deposit":
    if user_transaction == "show balance":
      showBalance(user_details)
      break
    elif user_transaction == "withdraw":
      withdraw(user_details)
      break
    elif user_transaction == "deposit":
      deposit(user_details)
      break
    else:
      print("Please try again")
      user_transaction = input("Would you like to show balance, withdraw or deposit?")
  promptForAction()

#Prompts user for account password
def promptForAccountPassword(user_details):
  user_password = input("What is your password")
  while user_password != user_details["password"]:
    print("Password is incorrect, please try again")
    user_password = input("What is your password")
  print("Password is correct")
  promptForTransaction(user_details)

#Prompts user for the account number
def accessAccount():
  user_account_number = input("What is your account number?")
  while user_account_number not in ledger.keys():
    print("Please try again")
    user_account_number = input("What is your account number?")
  user_details = ledger[user_account_number]
  promptForAccountPassword(user_details)

#Prompts user for a transaction type
def promptForAction():
  user_action = input("What would you like to do today? Create an account or access your account?")
  while True:
    if user_action == "create account":
      addAccount()
      break
    elif user_action == "access account":
      accessAccount()
      break
    else: 
      print("Please try again")
      user_action = input("What would you like to do today? Create an account or access your account?")

#Encodes user details into a string
def encodeUserDetails(user_details):
    line = str(user_details['account_number']) + "," + user_details['password'] + "," + str(user_details['balance']) 
    return line

#Adds the string of user details into a dictionary to be saved
def encodeLedger(ledger):
    lines = ""
    for key in ledger.keys():
        line = encodeUserDetails(ledger[key])
        lines += line + "\n"
    return lines[:-1]

#Writes data on the drive
def writeFile(ledger):
    file = open(FILE_NAME, "w")
    lines = encodeLedger(ledger)
    file.write(lines)
    file.close()

#Main function that calls read, prompt for action and write functions
def main():
    readAccounts(FILE_NAME)
    promptForAction()
    writeFile(ledger)
if __name__ == '__main__':
    main()
