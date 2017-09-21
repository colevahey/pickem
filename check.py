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
            checker(uname)
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

def checker(user):

    weeknumber = 1

    try:
        userpicks = open('./picks/picks' + str(weeknumber) + '.json', 'r')
        userpicksdata = json.loads(userpicks.read())
    except FileNotFoundError:
        print("You have no picks for week " + str(weeknumber))

    for user in userpicksdata:
        for gameselection in userpicksdata[user]:
            for game in data["games"]:
                if gameselection["id"] == game["id"]:
                    print("For game " + game["awayTeam"]["displayName"] + " at " + game["homeTeam"]["displayName"] + " you chose " + gameselection["abbreviation"] + " with a spread of " + gameselection["spread"])

                    if game["winner"] != None:
                        winnerlose = ["home","away"]
                        winnerlose.remove(game["winner"])
                        print("The winner of the game was " + game[game["winner"]+"Team"]["displayName"] + " by a score of " + game["scores"][game["winner"]] + " to " + game["scores"][winnerlose[0]] + ".")
                    print()
                else:
                    pass


login()
