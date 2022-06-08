import re
#pip install passlib
#pip install bcrypt
from passlib.hash import bcrypt

#seeing if github updates

def username_select():
    while True:
        condition = 0
        username = input('Please enter a username or type exit to return to menu:\n')  #cant create username if already exists  FIX ME
        
        lowered = username.lower()
        if lowered == "exit":
            return

        with open('hashes.txt', 'r') as hashfile:
            for line in hashfile:
                stored_user = str(line.split(" ")[0]) #split method
                if stored_user.lower() == lowered:
                    print("That username already exists, please select a different one\n")
                    condition = 2
            if condition == 2:
                continue
        
        replaced = lowered.maketrans("012345689", "oizeasbbg")
        translated = lowered.translate(replaced)
        lst = []
        for i in lowered:
            lst.append(i)

        accepted = re.findall('\w', lowered)  #makes array of all accepted characters in provided username
        if(accepted == lst):
            with open('blacklist.txt', 'r') as file:
                for line in file:
                    stripped = line.rstrip('\n')
                    if stripped.lower() in lowered:
                        print("Username may not contain any profanity\n")
                        condition = 1
                        break
                    if stripped.lower() in translated:
                        print("Username may not contain any profanity or profanity with substituted letters\n")
                        condition = 1
                        break                  
        else:
            print("username can only contain characters a-z, A-Z, 0-9 and _\n")
            condition = 1
        if condition == 0:
            print("username accepted\n")
            return username
        

def password_select():
    while True:
        condition = 0
        password = input("Please Enter a Password:\n")
        length = len(password)
        if length < 8:
            print("\nPasswords must be between 8-64 characters\n")
            condition = 1
        elif length > 64:
            print ("\nPasswords must be between 8-64 characters\n")
            condition = 1
        else:
            with open('passwords.txt', 'r') as pfile:
                for line in pfile:
                    stripped = line.rstrip('\n')
                    if stripped == password:
                        print("Your password is on a list of most common passwords and is not secure enough\n")
                        condition = 1
                        break
        if condition == 0:
            print("password accepted\n")
            return password


def hash_and_store(username, password):
    
    hashed_password = hasher.hash(password+pepper)

    f = open("hashes.txt", "a")
    text = (str(username+ " "+ hashed_password+"\n"))
    f.write(text)
    f.close()

def login():  
    count = 0
    username = input('Please enter your username or type exit to return to menu:\n')
    
    lowered = username.lower()
    if lowered == "exit":
        return
        
    with open('hashes.txt', 'r') as hashfile:
        for line in hashfile:
            stored_user = str(line.split(" ")[0]) #split method
            if stored_user.lower() == lowered:
                stored_password = str(line.split(" ")[1])
                stored_password = stored_password.rstrip('\n')
                while True:
                    password = input("Welcome "+ username+ ". Please input your password or type exit to return to menu\n")
                    lowered = password.lower()
                    if lowered == "exit":
                        return
                    if hasher.verify(password+pepper, stored_password) == True:
                        print("\n#####\nLogin Successful\n#####\n\n")
                        return
                    else:
                        print("Incorrect password\n")
                        count += 1
                        if count == 10:
                            print("\n#####\nToo many incorrect attempts, you will be returned to the menu\n#####\n\n")
                            return
        
    print("Username does not exist\n")
                  
                        
def main():
    while True:
        selection = input("Do you wish to:\n1: Sign up\n2: Log in\n3: Exit\n")
        if selection == '1':
            username = username_select()
            if username == None:
                continue
            password = password_select()
            hash_and_store(username, password)
        elif selection == '2':
            login()
        elif selection == '3' or selection.lower() == 'exit':
            break
        else:
            continue

pepper = "r3pp3Pdn4t415"  #salt and pepper backwards with numbers to be random as possible
hasher = bcrypt.using(rounds=13)  # Make the have have more itterations
main()


