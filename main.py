import urllib.request
import json
from time import sleep
import hashlib

def login():
    uname = input("Username?\n>> ")
    password = input("Password?\n>> \033[8m")
    print("\033[0m")

    users = open('users.json', 'r')
    userdata = json.loads(users.read())

    hash_object = hashlib.md5(password.encode())
    hashpassword = hash_object.hexdigest()

    try:
        if userdata[uname] == hashpassword:
            print("Welcome, " + uname)
            main()
        else:
            print("That password is incorrect")
            input("Try again? [Press enter to continue]")
            print()
            login()
    except KeyError:
        print("That user does not exist")
        create = input("Try again [Press enter] or create new user [Press c enter]?\n>> ")
        if create.lower() == "c":
            print("DO THE CREATE THING")
        else:
            print()
            login()

def main():
    rawhtml = urllib.request.urlopen("https://cfb-scoreboard-api.herokuapp.com/v1/date/20170923")

    data = json.loads(rawhtml.read().decode("utf-8"))

    #For each game in the database for that week
    for game in data["games"]:

        #If the game has a spread
        if game["odds"]["spread"] != "N/A":

            #Print the teams playing in the game
            print(game["homeTeam"]["displayName"] + " vs. " + game["awayTeam"]["displayName"])

            #Print the spread of the game
            print(game["odds"]["spread"])
            print()

login()
