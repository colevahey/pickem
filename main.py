import urllib.request
import json
from time import sleep
import hashlib
import adduser

rawhtml = urllib.request.urlopen("https://cfb-scoreboard-api.herokuapp.com/v1/date/20170923")

data = json.loads(rawhtml.read().decode("utf-8"))

def login():
    uname = input("Username?\n>> ")
    password = input("Password?\n>> \033[8m")
    print("\033[0m")

    users = open('users.json', 'r')
    userdata = json.loads(users.read())

    hash_object = hashlib.md5(password.encode())
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

def main():
    #For each game in the database for that week
    for game in data["games"]:

        #If the game has a spread
        if game["odds"]["spread"] != "N/A":

            #Print the teams playing in the game
            print(game["awayTeam"]["displayName"] + " at " + game["homeTeam"]["displayName"])

            #Print the spread of the game
            print(game["odds"]["spread"])
            print()
            sleep(1)

def selections(user):

    userselections = {}

    for game in data["games"]:
        if game["odds"]["spread"] != "N/A":
            print("\n" + game["awayTeam"]["displayName"] + " at " + game["homeTeam"]["displayName"])
            print(game["odds"]["spread"])
            selection = input("Who do you select? (A/H)\n>> ").title()
            if selection == "A":
                print("You selected " + game["awayTeam"]["displayName"])
                userselections.update({game["id"]:game["awayTeam"]["displayName"]})
            elif selection == "H":
                print("You selected " + game["homeTeam"]["displayName"])
                userselections.update({game["id"]:game["homeTeam"]["displayName"]})
            else:
                print("That pick is invalid. You have to start over now.")
                input("Press enter to continue")

    print(userselections)

login()
