import hashlib
import json

def main():
    uname = input("New Username?\n>> ")
    password = input("New Password?\n>> \033[8m")
    print("\033[0m")

    users = open('users.json', 'r')
    userdata = json.loads(users.read())

    hash_object = hashlib.sha224(password.encode())
    hashpassword = hash_object.hexdigest()

    try:
        userdata[uname]
        print("User " + uname + " already exists.")
        updatepword = input("Update password (Y/N)? ")
        if updatepword.upper() == "Y":
            pass
        else:
            print("Aborted")
            exit()
    except KeyError:
        pass

    userdata[uname] = {"password": hashpassword, "wins": 0, "losses":0}

    userdatafile = open('users.json', 'w')

    userdatafile.write(
        json.dumps(userdata)
    )

    print("User " + uname + " successfully added")

if __name__ == '__main__':
    main()
