# import modules
import sys
import re
from datetime import datetime
import random

# global variables
balance = 0
accounts = {}
points = 0
receiver_saved = {}
gift_cards = {}
activity_log = []
charge_comment = []
transfer_comment = []
pay_comment = []

def validate_input(**kwargs): # **kwargs: Variable keyword arguments (asterisk)
    """
    A function to validate user input.

    Parameters:
    **kwargs: Variable keyword arguments. Recognizes the following keys:
        - prompt (str): The input prompt to be shown to the user. The default is an empty string.
        - input_type (str): Specifies the type of the input. Can be 'int' or 'str'. The default is 'str'.
        - valid_range (list): Specifies the valid range for the input. If the input is not within this range, it is considered invalid. The default is None.
        - regex (str): Specifies the regular expression that the input should match. If the input does not match this regular expression, it is considered invalid. The default is None.

    Returns:
    input_value (int or str): The valid input received from the user.
    if user inputs 'q', return_to_main_menu() is called.
    """
    while True:
        try:
            prompt = kwargs.get('prompt', '')
            input_type = kwargs.get('input_type', 'str')
            valid_range = kwargs.get('valid_range', None)
            regex = kwargs.get('regex', None)

            input_value = input(prompt)
            if input_value.lower() == 'q': # check if user wants to quit
                return_to_main_menu()
                continue
            if input_type == 'int': # check if input is an integer
                input_value = int(input_value)
                if input_value <= 0:  # check if input is a positive integer
                    print("Invalid input. You must enter a value larger than 0.")
                    continue
            elif input_type == 'str': # check if input is a string
                input_value = str(input_value)
            if valid_range and input_value not in valid_range: # check if input is within the valid range
                print("Invalid input. Please enter a valid option.")
                continue
            if regex and not re.match(regex, input_value): # check if input matches the regular expression
                print("Invalid input. Please enter a valid value.")
                continue
            return input_value
        except ValueError:
            print("Invalid input. Please enter a valid value.")

def main_menu():
    """
    Displays the main menu of the Naver Pay and handles user input.

    This function continuously displays the main menu until the user chooses to exit.
    The menu includes options to check balance, top up balance, transfer money, make a payment,
    register a gift card, view activities, and exit the system.

    The user's choice is validated using the `validate_input` function, which ensures the input is an integer
    within the valid range of 1 to 8. Depending on the user's choice, the corresponding function is called.

    Raises:
    ValueError: If the input from `validate_input` is not a valid integer or not within the range of 1 to 8.
    """
    while True:
        print("\nNaver Pay")
        print("1. Check My Pay")
        print("2. Top Up")
        print("3. Transfer Money")
        print("4. Make Payment")
        print("5. Register Gift Card")
        print("6. View Activities")
        print("7. Convert Points to Balance")
        print("8. Exit Naver Pay")
        print("==If you want to quit, please press 'q' anytime in any process==")
        choice = validate_input(prompt="Please select a menu >> ", input_type='int', valid_range=range(1, 9))

        if choice == 1:
            check_balance()
        elif choice == 2:
            top_up()
        elif choice == 3:
            transfer_money()
        elif choice == 4:
            make_payment()
        elif choice == 5:
            register_giftcard()
        elif choice == 6:
            view_activities()
        elif choice == 7:
            convert_points_to_balance()
        elif choice == 8:
            exit_options()

def print_accounts():
    """
    Prints a list of accounts.
    """
    for name, details in accounts.items():
        print(f"{name}: {details['bank']} - {details['number']}")

def view_comment(comment_list: list, action: str):
    """
    Prints the user's comment history based on the action type.

    Parameters:
    comment_list (list): A list of dictionaries where each dictionary represents a comment.
    Each dictionary contains the date, amount, balance, and comment string.

    action (str): The type of action. It can be "charge", "transfer", or "pay".

    Returns:
    None: This function doesn't return anything; it only prints the comment history.
    """
    print("\nMy Comment History")
    if not comment_list:
        print("No comments recorded yet.")
        return
    if action == "charge":
        print("|Date|Money Charged|Balance|Comments|")
    elif action == "transfer":
        print("|Date|Money Sent|Balance|Comments|")
    elif action == "pay":
        print("|Date|Money Payed|Balance|Comments|")
    print("|---|---|---|---|")
    for log in comment_list:
        print(f"|{log['date']}|{log['amount']} ₩|{log['balance']} ₩|{log['comment']}|")


def log_transaction(amount: int, comment_str: str, comment_list: list, balance: int):
    """
    Logs a transaction by appending a dictionary to the comment list.

    Parameters:
    amount (int): The amount of money involved in the transaction.
    comment_str (str): A string that describes the transaction.
    comment_list (list): A list of dictionaries where each dictionary represents a comment.
    Each dictionary contains the date, amount, balance, and comment string.
    balance (float): The current balance after the transaction.

    Returns:
    None: This function doesn't return anything; it only modifies the comment_list.
    """
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    comment_list.append({'date': current_time, 'amount': amount, 'balance': balance, 'comment': comment_str})


def log_activity(action: str):
    """
    Logs an activity by appending a dictionary to the activity_log list.

    Parameters:
    action (str): A string that describes the activity.

    """
    current_time = datetime.now().strftime('%Y-%m-%d')
    activity_log.append({'date': current_time, 'action': action, 'balance': f"{balance}₩", 'points': f"{points}p"})


def view_activities():
    """
    Prints the user's activity history.
    """
    print("\nMy Activity History")
    if not activity_log:
        print("No activities recorded yet.")
        return
    print("|Date|Action|Balance|Points|")
    print("|---|---|---|---|")
    for log in activity_log:
        print(f"|{log['date']}|{log['action']}|{log['balance']}|{log['points']}|")

def exit_options():
    """
    Prints a goodbye message and exits the program.
    """
    print("Exiting the program.\nThank you for using Naver Pay.")
    sys.exit()

def return_to_main_menu():
    """
    Prints a message and returns to the main menu.
    """
    print("Ending the current task and returning to the main menu.")
    main_menu()

def check_balance():
    """
    Prints the user's Naver Pay information and logs the activity.
    """
    print("\nMy Pay Information")
    print(f"Name: Team2")
    print(f"Balance: {balance}₩")
    if accounts:
        print("Registered Accounts:")
        for name, details in accounts.items():
            print(f"{name}: {details['bank']} - {details['number']}")
    else:
        print("Registered Accounts: None")

    print(f"Points: {points}p")
    log_activity("Checked Pay Information")

    if balance == 0 or not accounts:
        print("\n1. Would you like to charge your balance?")
        print("2. Would you like to register an account?")
        print("3. Back to main menu")
        choice = validate_input(prompt="Choice >> ", input_type='str', valid_range=['1', '2', '3'])
        if choice == '1':
            top_up(skip_prompt=True)
        elif choice == '2':
            register_account()
        elif choice == '3':
            return

def register_account():
    """
    Registers a new bank account.
    """
    while True:
        print("\nRegister Account")
        bank = validate_input(prompt="Enter the name of the bank (only alphabets, max 5 characters) >> ", input_type='str', regex='^[A-Za-z]{1,5}$')
        number = validate_input(prompt="Enter the account number (only digits, max 14 characters) >> ", input_type='str', regex='^\d{1,14}$')
        if number in [account['number'] for account in accounts.values()]:
            print("This account is already registered. Please enter a different account number.")
            continue
        initial_balance = 100000
        name = str(len(accounts) + 1)
        accounts[name] = {'bank': bank, 'number': number, 'balance': initial_balance}
        print(f"Account registered: {name} - {bank} {number}, Initial balance: {initial_balance}₩")
        break

def top_up(charge_amount: int = None, skip_prompt: bool = False):
    """
    Charges the balance of the user's account.

    Parameters:
    charge_amount (int, optional): The amount to charge. If not provided, the user will be prompted to enter it.
    skip_prompt (bool, optional): If True, skips the initial prompt and goes straight to charging. Default is False.
    """
    global balance

    if not skip_prompt: # if skip_prompt is False, show the prompt
        sub_menu = validate_input(prompt="1) Acitivity\n2) Charge\nq) quit\nchoice >>", input_type='int', valid_range=[1, 2])
        if sub_menu == 1:
            view_comment(charge_comment, "charge")
            return
        elif sub_menu == 2:
            pass

    if not accounts: # if there are no registered accounts, prompt the user to register an account, and then go back to the main menu
        print("\nNo registered accounts. Please register an account first.")
        register_account()
        return

    charge_choice = validate_input(prompt="1) select account\n2) register new account\nq) quit\nchoice >>  ", input_type='int', valid_range=[1, 2])

    if charge_choice == 2: # if the user chooses to register a new account, call the register_account function
        register_account()
        selected_account = list(accounts.values())[-1]
    elif charge_choice == 1: # if the user chooses to select an existing account
        print("\nList of registered accounts\n")
        print_accounts()
        account_option = validate_input(prompt="\nSelect an account to charge >> ", input_type='int', valid_range=range(1, len(accounts) + 1)) # validate the account number
        selected_account = accounts[str(account_option)]

    if charge_amount is None: # if charge_amount is not provided, prompt the user to enter the amount
        amount = validate_input(prompt="Enter the amount to charge >> ", input_type='int')
    else: # if charge_amount is provided, use that amount
        amount = charge_amount

    def update_balance(): # higher order function
        global balance
        balance += amount

    if selected_account['balance'] < amount:
        print("Insufficient account balance.")
        print("Returning to the main screen")
        return

    selected_account['balance'] -= amount
    update_balance()  # update balance
    print(f"Charge completed. Account balance: {selected_account['balance']}₩, My Pay balance: {balance}₩")
    log_activity(f"Account charge: {amount}₩")
    comment_str = validate_input(prompt="Would you like to add a comment related to the charge? (Enter comment/Enter if none) >> ", input_type='str')
    log_transaction(amount, comment_str, charge_comment, balance)


def transfer_money():
    """
    Transfers money from the user's account to another account.
    """
    global balance

    sub_menu = validate_input(prompt="1) Acitivity\n2) Transfer\nq) quit\nchoice >>", input_type='int', valid_range=[1, 2])
    if sub_menu == 1:
        view_comment(transfer_comment, "transfer")
        return
    elif sub_menu == 2:
        pass

    print("\nTransfer Money")

    if not accounts: # if there are no registered accounts, prompt the user to register an account, and then go back to the main menu
        print("No registered accounts. Please register an account first.")
        register_account()
        return

    amount = validate_input(prompt="Enter the amount to transfer >> ", input_type='int')

    min_charge = lambda x: (x - balance + 999) // 1000 * 1000 # lambda function to calculate the minimum charge amount

    if balance < amount: # if the balance is less than the transfer amount, charge the balance
        print("Insufficient balance. The minimum charge amount is {}.".format(min_charge(amount)))
        print("Proceeding automatic charge. Please select the charge method.")
        top_up(min_charge(amount), skip_prompt=True) #skip the prompt and charge the balance
        print("\nAutomatic charge completed!\n")

    receiver_name = validate_input(prompt="Enter the receiver's name >> ", input_type='str')
    receiver_bank = validate_input(prompt="Enter the receiver's bank name (only alphabets, max 5 characters) >> ", input_type='str', regex='^[A-Za-z]{1,5}$') # validate the bank name(ex) NH, KB, IBK..)
    receiver_account = validate_input(prompt="Enter the receiver's account number (only digits, max 14 digits) >> ", input_type='str', regex='^\d{1,14}$') # validate the account number(no dash)

    save_info = validate_input(prompt="Would you like to save this information? (Y/N) >> ", input_type='str', valid_range=['Y', 'N', 'y', 'n'])

    if save_info.lower() == 'y': # if the user wants to save the receiver's information
        nickname = validate_input(prompt="Enter a nickname to save >> ", input_type='str')
        receiver_saved[nickname] = {'name': receiver_name, 'bank': receiver_bank, 'number': receiver_account}
        print(f"Saved: '{nickname}' - ({receiver_name}, {receiver_bank}, {receiver_account})")

    confirm = validate_input(prompt=f"Are you sure you want to transfer {amount} to {receiver_name}? (Y/N) >> ", input_type='str', valid_range=['Y', 'N', 'y', 'n'])

    if confirm.lower() == 'y':
        balance -= amount
        print(f"Transfer completed. Remaining balance: {balance}")
        log_activity(f"Transfer: {amount}")
        comment_str = validate_input(prompt="Would you like to add a comment related to the transfer? (Enter comment/Press enter if none) >> ", input_type='str')
        log_transaction(amount, comment_str, transfer_comment, balance)
    else: # if the user cancels the transfer
        print("Transfer cancelled.") # print a message that the transfer is cancelled and go main menu


def make_payment():
    """
    Makes a payment and earns points based on the payment amount.
    """
    global balance

    sub_menu = validate_input(prompt="1) Activity\n2) Make payment\nq) quit >> ", input_type='int', valid_range=[1, 2])
    if sub_menu == 1:
        view_comment(pay_comment, "pay")
        return
    elif sub_menu == 2:
        pass

    print("\nPay")
    global balance
    global points
    earned_points = 0

    def earn_points(amount: int): # higher order function
        """
        Calculates the points earned based on the payment amount.

        Parameters:
        amount (int): The payment amount.
        """
        nonlocal earned_points # nonlocal keyword is used to modify the value of a variable defined in the outer function
        earned_points = int(amount * 0.05) # calculate the points earned
        print(f"Payment amount: {amount}, Points to be earned: {earned_points}p")

    payment_amount = validate_input(prompt="Enter the amount to pay >> ", input_type='int') 
    earn_points(payment_amount) # call the earn_points function to calculate the points earned

    min_charge = lambda x: (x - balance + 999) // 1000 * 1000 # lambda function to calculate the minimum charge amount

    if balance < payment_amount: # if the balance is less than the payment amount, charge the balance
        print("Insufficient balance. The minimum charge amount is {}.".format(min_charge(payment_amount)))
        print("Proceeding with automatic charge. Please select the charge method.")
        top_up(min_charge(payment_amount), skip_prompt=True)
        print("\nAutomatic charge completed!\n")

    confirm_payment = validate_input(prompt=f"Do you want to pay {payment_amount}? (Y/N) >> ", input_type='str', valid_range=['Y', 'N', 'y', 'n'])
    if confirm_payment.lower() == 'y': # if the user confirms the payment
        balance -= payment_amount # deduct the payment amount from the balance
        points += earned_points # add the earned points to the total points
        print("Payment completed.")
        print(f"Payment amount: {payment_amount}, Earned points: {earned_points}p")
        print(f"Remaining balance: {balance}, Total points: {points}p")
        log_activity(f"Payment: {payment_amount}")
        comment_str = validate_input(prompt="Would you like to add a comment related to the payment? (Enter comment/Press enter if none) >> ", input_type='str')
        log_transaction(payment_amount, comment_str, pay_comment, balance)
        award_additional_points()
    else:
        print("Payment cancelled.")

def award_additional_points():
    """
    Awards additional points on a random chance.
    """
    global points
    chance = random.randint(1, 100) # generate a random number between 1 and 100
    additional_points = 0
    if chance <= 90:
        additional_points = 100
    elif chance <= 99:
        additional_points = 2000
    else:
        additional_points = 5000

    points += additional_points # add the additional points to the total points
    print(f"Congratulations! You've earned an additional {additional_points} points. Current points: {points}p")



def register_giftcard():
    """
    Registers a new gift card.
    """
    print("\nRegister Gift Card")
    card_number = validate_input(prompt="Enter the gift card number (only digits, 8 characters) >> ", input_type='str', regex='^[0-9]{8}$')
    card_balance = validate_input(prompt="Enter the balance on the gift card >> ", input_type='int')

    if card_number in gift_cards:
        print("This gift card is already registered.")
        return

    gift_cards[card_number] = card_balance
    print(f"Registered gift card - Number: {card_number}, Balance: {card_balance}₩")
    log_activity("Registered Gift Card")



def convert_points_to_balance():
    """
    Converts a specified amount of points to balance.
    """
    global balance, points

    if points <= 0:
        print("You have no points to convert.")
        return
    print(f"You have {points} points.")

    amount_to_convert = validate_input(prompt="Enter the amount of points you want to convert >> ", input_type='int')

    if amount_to_convert > points:
        print("You don't have enough points to convert that amount.")
        return

    choice = validate_input(prompt="Do you want to convert points to balance? (Y/N) >> ", input_type='str', valid_range=['Y', 'N', 'y', 'n'])

    if choice.lower() == 'y':
        balance += amount_to_convert
        points -= amount_to_convert
        print(f"Converted {amount_to_convert} points to {amount_to_convert}₩. Current balance: {balance}₩, points: {points}p")
        log_activity("Converted Points to Balance")
    else:
        print("Conversion cancelled.")


################################################################################
main_menu()