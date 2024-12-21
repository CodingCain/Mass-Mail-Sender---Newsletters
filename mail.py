import time
from getpass import getpass
import os
import sys
import smtplib
from email.mime.text import MIMEText


# Colors
GREEN = "\033[0;32m"
RED = "\033[0;31m"
CYAN = "\033[0;36m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"

# Text Formats
UNDERLINE = "\033[4m"
BOLD = "\033[1m"


show = ""

# Function to send email
def send_email(message, subject, sender_email, recipient_emails, sender_password):
    working_emails = []
    broken_emails = []

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
    
        for email in recipient_emails:
            try:
                # Set up the MIMEText email object
                msg = MIMEText(message)
                msg["Subject"] = subject
                msg["From"] = sender_email
                msg["To"] = email

                # Send the email
                server.sendmail(sender_email, email, msg.as_string())
                print(f"Email Sent To {GREEN}{email}{RESET}")
                working_emails.append(email)
            except Exception:
                print(f"Email Failed to send to {RED}{email}{RESET}")
                broken_emails.append(email)
    
    print(f"\n\n{GREEN}Message Sent To{RESET}")
    print("------------------")
    for email in working_emails:
        print(f"{CYAN}{email}{RESET}")
    print(f"\n\n{RED}Message Failed To Send To{RESET}")
    print("------------------")
    for email in broken_emails:
        print(f"{CYAN}{email}{RESET}")
    input(f"\n\n{BOLD}Press Enter to{RESET} {RED}Close Program{RESET}")


def get_email(): # Email server setup (Gmail SMTP)\
    correct_email = False
    while correct_email == False:
        sender_email = input("Sender Email: ").strip()
        while True:
            print(f"\n {CYAN}{sender_email}{RESET}", end="\n\n")
            is_email_valid = input(f"Is this Email correct? [{GREEN}Y{RESET}/{RED}n{RESET}]: ").strip().lower()
            if is_email_valid in ["yes", "y"]:
                clear_console()
                correct_email = True
                break
            elif is_email_valid in ["no", "n"]:
                clear_console()
                correct_email = False
                break
            else:
                print(f"{RED}invalid choice{RESET}. Try {GREEN}y{RESET} or {RED}n{RESET}")
                input(f"{BOLD}Press enter to continue{RESET}")
                clear_console()
    return sender_email

def get_password():
    global show
    correct_password = False
    while correct_password == False:
        sender_password = getpass(f"Sender Token Pass Key [{YELLOW}hidden{RESET}]: ").strip()
        show = input(f"To see password type '{YELLOW}show{RESET}' or press enter to continue: ")
        while True:
            if show in ["show", "'show'"]:
                print(f"\n {CYAN}{sender_password}{RESET}", end="\n\n")
            is_password_valid = input(f"Is this Password correct? [{GREEN}Y{RESET}/{RED}n{RESET}]: ").strip().lower()
            if is_password_valid in ["yes", "y"]:
                clear_console()
                correct_password = True
                break
            elif is_password_valid in ["no", "n"]:
                clear_console()
                correct_password = False
                break
            else:
                print(f"{RED}invalid choice{RESET}. Try {GREEN}y{RESET} or {RED}n{RESET}")
                input(f"{BOLD}Press enter to continue{RESET}")
                clear_console()
    return sender_password


def get_subject():
    correct_subject = False
    while correct_subject == False:
        subject = input("Subject: ")
        while True:
            print(f"\n {YELLOW}{subject}{RESET}", end="\n\n")
            is_subject_valid = input(f"Is this Subject correct? [{GREEN}Y{RESET}/{RED}n{RESET}]: ").strip().lower()
            if is_subject_valid in ["yes", "y"]:
                clear_console()
                correct_subject = True
                break
            elif is_subject_valid in ["no", "n"]:
                clear_console()
                correct_subject = False
                break
            else:
                print(f"{RED}invalid choice{RESET}. Try {GREEN}y{RESET} or {RED}n{RESET}")
                input(f"{BOLD}Press enter to continue{RESET}")
                clear_console()
    return subject




def get_recipient_emails():
    try:
        with open("recipients.txt", "r") as file:
            emails = [email.strip() for email in file]
            return emails
    except FileNotFoundError:
        clear_console()
        print("Missing 'recipients.txt' containing recipient emails formatted as")
        print("test1.mail@gmail.com")
        print("test2.mail@gmail.com")
        print("test3.mail@gmail.com")
        input(f"{BOLD}Press Enter to close{RESET}")
        sys.exit()



def get_body_text():
    try:
        with open("body.txt", "r") as file:
            body_text = file.read()
            return body_text
    except FileNotFoundError:
        clear_console()
        print(f"{RED}Missing{RESET} '{YELLOW}body.txt{RESET}' containing the message to send")
        input(f"{BOLD}Press Enter to close{RESET}")
        sys.exit()

def preview(body_text, subject, sender_email, recipient_email, sender_password):
    print(f"Email: {CYAN}{sender_email}{RESET}")
    if show in ["show", 'show']:
        print(f"Password: {CYAN}{sender_password}{RESET}")
    else:
        print(f"Password: {YELLOW}HIDDEN{RESET}")
    print(f"\nSubject: {YELLOW}{subject}{RESET}")
    print(f"\nBody Text: {body_text}")
    time.sleep(2)
    print(f"{UNDERLINE}-------------------------------------------------------------------------{RESET}")
    input(f"\n\n{BOLD}Press Enter to View Recipients{RESET}")
    clear_console()
    print(f"{GREEN}---- SEND TO ----{RESET}\n")
    for email in recipient_email:
        print(f"{CYAN}{email}{RESET}")
    time.sleep(2)
    input(f"\n\n{BOLD}Press Enter to Send All Emails{RESET}")
    clear_console()



# Main function
def main():
    sender_email = get_email()
    sender_password = get_password()
    recipient_emails = get_recipient_emails()
    subject = get_subject()
    body_text = get_body_text()
    preview(body_text, subject, sender_email, recipient_emails, sender_password)
    while True:
        confirm = input(f"Confirm Send All Emails: [{GREEN}Y{RESET}/{RED}n{RESET}]: ").strip().lower()
        if confirm in ["yes", "y"]:
            break
        elif confirm in ["no", "n"]:
            input("Press Enter to Exit")
            sys.exit()
        else:
            print(f"{RED}Invalid Selection{RESET}")
            input("Press Enter to continue")
            clear_console()
    send_email(body_text, subject, sender_email, recipient_emails, sender_password)


def clear_console():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

if __name__ == "__main__":
    main()
