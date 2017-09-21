import urllib.request
import json
from time import sleep
import hashlib
import adduser

rawhtml = urllib.request.urlopen("https://cfb-scoreboard-api.herokuapp.com/v1/date/20170923")

data = json.loads(rawhtml.read().decode("utf-8"))

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
            selections(uname)
        else:
            print("That password is incorrect")
            input("Try again? [Press enter to continue]")
            print()
            login()
    except KeyError:
        print("That user does not exist")
        create = input("Try again [Press enter] or create new user [Press c enter]?\n>> ")
        if create.lower() == "c":
            print()
            print("NEW USER:\n")
            adduser.main()
        else:
            print()
            login()

def selections(user):

    userselections = [] 

    for game in data["games"]:
        if game["odds"]["spread"] != "N/A":
            print("\n" + game["awayTeam"]["displayName"] + " at " + game["homeTeam"]["displayName"])
            print(game["odds"]["spread"])
            selection = input("Who do you select? (A/H)\n>> ").title()
            if selection == "A":
                print("You selected the " + game["awayTeam"]["displayName"])
                userselections.append({"id":game["id"],"pick":"away","spread":game["odds"]["spread"]})
            elif selection == "H":
                print("You selected " + game["homeTeam"]["displayName"])
                userselections.append({"id":game["id"],"pick":"home","spread":game["odds"]["spread"]})
            else:
                print("That pick is invalid. You have to start over now.")
                input("Press enter to continue")
                userselections = []
                break
                selections(user)


    try:
        userpicks = open('./picks/picks1.json', 'r')
        userpicksdata = json.loads(userpicks.read())
    except FileNotFoundError:
        userpicksdata = {}

    userpicksdata.update({user:userselections})

    userpicks = open('./picks/picks1.json', 'w')

    print(userselections)
    userpicks.write(json.dumps(userpicksdata))

login()
