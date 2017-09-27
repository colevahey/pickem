import json
from time import sleep
import hashlib
import adduser

users = open('users.json', 'r')
userdata = json.loads(users.read())

def login():
    uname = input("Username?\n>> ")
    password = input("Password?\n>> \033[8m")
    print("\033[0m")

    hash_object = hashlib.sha224(password.encode())
    hashpassword = hash_object.hexdigest()

    try:
        if userdata[uname]["password"] == hashpassword:
            print("Welcome back " + uname)
            print("Your current record is " + str(userdata[uname]["wins"]) + "-" + str(userdata[uname]["losses"]))
            print()
            sleep(3)
            return uname
        else:
            print("That password is incorrect")
            input("Try again? [Press enter to continue]")
            print()
            return login()
    except KeyError:
        print("That user does not exist")
        create = input("Try again [Press enter] or create new user [Press c enter]?\n>> ")
        if create.lower() == "c":
            print()
            print("NEW USER:\n")
            return adduser.main()
        else:
            print()
            return login()

if __name__ == '__main__':
    login()